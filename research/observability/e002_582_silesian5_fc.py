#!/usr/bin/env python3
"""E002-582: public human full-closure annotation index-omission experiment.

FROZEN protocol: E002_582_FROZEN.md, committed before archive retrieval.
This is not an exposure-integrating camera simulation or physiological certificate.
No source rows, filenames, face landmarks, or identifiers are printed or committed.
"""
import collections
import hashlib
import io
import json
import pathlib
import re
import statistics
import sys
import zipfile

from e002_582_source_probe import retrieve, MAX_MEMBER, MAX_TOTAL

TOKEN = re.compile(r"[,:;\t ]+")
FLAGS_FC = {"X", "C"}
FLAGS_NV = {"X", "N"}
EXPECTED_ROWS = 58884
EXPECTED_SEQUENCES = 5


def parse_text(raw):
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        content = raw.decode("cp1250")
    rows = []
    for lineno, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [x for x in TOKEN.split(line) if x]
        if not parts or not re.fullmatch(r"\d+", parts[0]):
            # Allow headings, never skip numeric rows.
            continue
        if len(parts) != 19:
            raise ValueError("NUMERIC_ROW_NOT_19_FIELDS")
        fid = int(parts[0])
        nf, lfc, lnv, rfc, rnv = parts[2:7]
        if nf not in FLAGS_NV or lnv not in FLAGS_NV or rnv not in FLAGS_NV:
            raise ValueError("UNKNOWN_NUISANCE_FLAG")
        if lfc not in FLAGS_FC or rfc not in FLAGS_FC:
            raise ValueError("UNKNOWN_CLOSURE_FLAG")
        # The published 12 geometric fields are finite numeric quantities.
        for item in parts[7:]:
            try:
                val = float(item)
            except ValueError as exc:
                raise ValueError("INVALID_GEOMETRY_FIELD") from exc
            if not (-1e8 < val < 1e8):
                raise ValueError("NONFINITE_OR_EXTREME_GEOMETRY")
        if rows and fid <= rows[-1][0]:
            raise ValueError("NONMONOTONIC_OR_DUPLICATE_FRAME_ID")
        rows.append((fid, nf, lfc, lnv, rfc, rnv))
    return rows


def source_structure(data):
    """Privacy-safe format diagnostics, no row values or source filenames."""
    summary = []
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            if not info.filename.lower().endswith(".tag"):
                continue
            raw = z.read(info)
            lines = raw.decode("utf-8-sig", errors="replace").splitlines()
            fields = collections.Counter()
            starts = collections.Counter()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                fields[len([x for x in TOKEN.split(line) if x])] += 1
                starts["digit" if line[0].isdigit() else "other"] += 1
            summary.append({"line_count": len(lines),
                            "field_count_histogram": dict(sorted(fields.items())),
                            "leading_character_class": dict(starts)})
    return {"experiment": "E002-582", "tier": "SOURCE_SHAPE_ONLY",
            "tag_members": len(summary), "tag_shape_summaries": summary}


def parse_archive(data):
    if not zipfile.is_zipfile(io.BytesIO(data)):
        raise ValueError("INVALID_ZIP")
    sequences = []
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos = z.infolist()
        if len(infos) > 500 or sum(x.file_size for x in infos) > MAX_TOTAL:
            raise ValueError("ZIP_SIZE_LIMIT")
        for info in infos:
            if info.is_dir():
                continue
            path = pathlib.PurePosixPath(info.filename)
            if path.is_absolute() or ".." in path.parts or "\\" in info.filename or info.file_size > MAX_MEMBER:
                raise ValueError("UNSAFE_MEMBER")
            if info.flag_bits & 1:
                raise ValueError("ENCRYPTED_MEMBER")
            raw = z.read(info)
            if len(raw) != info.file_size:
                raise ValueError("ZIP_MEMBER_INTEGRITY")
            if b"\x00" in raw[:1024]:
                continue
            rows = parse_text(raw)
            if rows:
                sequences.append(rows)
    if len(sequences) != EXPECTED_SEQUENCES:
        raise ValueError("EXPECTED_FIVE_ANNOTATION_SEQUENCES")
    if sum(len(s) for s in sequences) != EXPECTED_ROWS:
        raise ValueError("EXPECTED_58884_ANNOTATION_ROWS")
    return sequences


def retained_indices(first, last, phase):
    out = set()
    k = 0
    while True:
        idx = first + phase + (10 * k) // 3
        if idx > last:
            break
        out.add(idx)
        k += 1
    return out


def eye_runs(rows, eye):
    # eye=0 left; eye=1 right.
    fc_col = 2 if eye == 0 else 4
    nv_col = 3 if eye == 0 else 5
    positive = []
    i = 0
    while i < len(rows):
        if rows[i][fc_col] != "C":
            i += 1
            continue
        a = i
        while (i + 1 < len(rows) and rows[i+1][fc_col] == "C"
               and rows[i+1][0] == rows[i][0] + 1):
            i += 1
        b = i
        positive.append((a, b, nv_col))
        i += 1
    return positive


def analyze_sequence(rows):
    first, last = rows[0][0], rows[-1][0]
    retained = [retained_indices(first, last, phase) for phase in range(10)]
    totals = collections.Counter()
    lengths = collections.Counter()
    missed_by_phase = [0] * 10
    for eye in (0, 1):
        for a, b, nv_col in eye_runs(rows, eye):
            totals["all_fc_runs"] += 1
            if a == 0 or b == len(rows) - 1:
                totals["boundary_abstain"] += 1
                continue
            segment = rows[a-1:b+2]
            if any(segment[i+1][0] != segment[i][0] + 1 for i in range(len(segment)-1)):
                totals["missing_index_abstain"] += 1
                continue
            if any(r[1] == "N" or r[nv_col] == "N" for r in segment):
                totals["nuisance_abstain"] += 1
                continue
            length = b-a+1
            lengths[str(length) if length <= 3 else "4+"] += 1
            totals["eligible_fc_runs"] += 1
            missed = [not any(idx in kept for idx in range(rows[a][0], rows[b][0]+1))
                      for kept in retained]
            for phase, missing in enumerate(missed):
                missed_by_phase[phase] += int(missing)
            nmiss = sum(missed)
            if nmiss:
                totals["runs_missed_any_phase"] += 1
            if nmiss == 10:
                totals["runs_missed_all_phases"] += 1
            if rows[a][0] >= first+10 and rows[b][0] <= last-10:
                expected = {1: 7, 2: 4, 3: 1}.get(length, 0)
                if nmiss != expected:
                    raise ValueError("EXACT_PHASE_PREDICTION_FALSIFIED")
                totals["interior_phase_law_checked"] += 1
    return totals, lengths, missed_by_phase


def analyze(sequences, archive_sha):
    totals, lengths = collections.Counter(), collections.Counter()
    phases = [0] * 10
    sequence_counts = []
    for rows in sequences:
        t, lens, miss = analyze_sequence(rows)
        totals.update(t)
        lengths.update(lens)
        phases = [a+b for a,b in zip(phases,miss)]
        sequence_counts.append({"rows": len(rows), "eligible_fc_runs": t["eligible_fc_runs"],
                                "runs_missed_any_phase": t["runs_missed_any_phase"]})
    return {"experiment": "E002-582", "evidence_tier": "INVESTIGATOR_HUMAN_FC_LABEL_INDEX_ALIAS_ONLY",
            "source_archive_sha256": archive_sha,
            "source": "https://www.blinkingmatters.com/research",
            "nominal_reference_fps": 100, "nominal_target_fps": 30,
            "physical_exposure_verified": False, "camera_clock_verified": False,
            "independent_anatomical_rater_pair": False, "velocity_ceiling_certified": False,
            "total_annotated_frames": sum(len(s) for s in sequences),
            "source_sequences": len(sequences),
            "fc_runs": dict(sorted(totals.items())),
            "eligible_run_lengths_native_frames": {k:lengths[k] for k in ("1","2","3","4+")},
            "phase_missed_fc_runs": phases, "per_sequence_aggregate": sorted(sequence_counts, key=lambda x: (x["rows"], x["eligible_fc_runs"], x["runs_missed_any_phase"])),
            "positive_index_alias_witness": totals["runs_missed_any_phase"] > 0,
            "human_shutter_gap_bound_validated": False,
            "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}


def self_test():
    def make(flags, missing=None, nuisance=None):
        rows=[]
        for i, fc in enumerate(flags):
            if i == missing:
                continue
            nf = "N" if i == nuisance else "X"
            rows.append((i,nf,fc,"X","X","X"))
        return rows
    # One-frame source-positive, 10 phase schedules, 7 misses.
    t, lens, p = analyze_sequence(make(["X"]*20+["C"]+["X"]*20))
    assert t["eligible_fc_runs"] == 1 and sum(p) == 7 and lens["1"] == 1
    for length, expected in [(2,4),(3,1),(4,0),(8,0)]:
        t, _, p = analyze_sequence(make(["X"]*20+["C"]*length+["X"]*20))
        assert t["eligible_fc_runs"] == 1 and sum(p) == expected
    t, _, _ = analyze_sequence(make(["X"]*20+["C"]+["X"]*20,nuisance=20))
    assert t["nuisance_abstain"] == 1 and t["eligible_fc_runs"] == 0
    t, _, _ = analyze_sequence(make(["X"]*20+["C"]+["X"]*20,missing=19))
    assert t["missing_index_abstain"] == 1
    t, _, _ = analyze_sequence(make(["X"]*20+["C"]+["X"]*20))
    assert t["runs_missed_all_phases"] == 0
    s1 = make(["X"]*20+["C"]+["X"]*20)
    s2 = make(["X"]*20+["C"]*2+["X"]*20)
    assert analyze([s1,s2], "0"*64) == analyze([s2,s1], "0"*64)
    good = "0:0:X:C:X:X:X:1:2:3:4:5:6:7:8:9:10:11:12\n"
    assert len(parse_text(good.encode())) == 1
    for bad in ("0:0:X:C:X:X:X:1:2\n", "0:0:X:Z:X:X:X:1:2:3:4:5:6:7:8:9:10:11:12\n"):
        try:
            parse_text(bad.encode())
        except ValueError:
            pass
        else:
            raise AssertionError("MALFORMED_SOURCE_ACCEPTED")
    print(json.dumps({"self_test": "PASS", "tested_phase_misses": {"1":7,"2":4,"3":1,"4+":0}},
                     sort_keys=True))


if __name__ == "__main__":
    self_test()
    if "--source" in sys.argv:
        raw = retrieve()
        print(json.dumps(source_structure(raw), sort_keys=True))
        print(json.dumps(analyze(parse_archive(raw), hashlib.sha256(raw).hexdigest()), sort_keys=True))
