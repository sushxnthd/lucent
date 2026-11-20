#!/usr/bin/env python3
"""E002-615: source-timestamp stress of published Silesian5 FC frame-index aliases.

Prospective freeze E002_615_FROZEN.md at d0b0a0c. No images, raw rows, source
member names, frame indices, or participant identifiers leave this process.
This is NOT a physical 30-fps shutter simulation or a velocity certificate.
"""
import bisect
import collections
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
import pathlib
import statistics
import sys
import zipfile

from e002_582_silesian5_fc import (SOURCE_SHA256, parse_text, eye_runs,
                                   retained_indices)
from e002_582_source_probe import retrieve

N_PHASE = 10
RATE_RATIO = Decimal(10) / Decimal(3)


def parse_timestamps(raw):
    """Two columns, frame-id then acquisition timestamp; fail closed."""
    try:
        lines = raw.decode("utf-8-sig").splitlines()
    except UnicodeDecodeError:
        lines = raw.decode("cp1250").splitlines()
    times = {}
    prev_id, prev_t = None, None
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) != 2:
            raise ValueError("TIMESTAMP_NOT_TWO_FIELDS")
        try:
            fid = int(fields[0])
            t = Decimal(fields[1])
        except (ValueError, InvalidOperation) as exc:
            raise ValueError("INVALID_TIMESTAMP_ROW") from exc
        if str(fid) != fields[0] or not t.is_finite():
            raise ValueError("NONCANONICAL_ID_OR_NONFINITE_TIME")
        if prev_id is not None and (fid <= prev_id or t <= prev_t):
            raise ValueError("NONMONOTONIC_TIMESTAMP")
        times[fid] = t
        prev_id, prev_t = fid, t
    if len(times) < 2:
        raise ValueError("INSUFFICIENT_TIMESTAMPS")
    return times


def paired_sources(data):
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise ValueError("SOURCE_ARCHIVE_HASH_CHANGED")
    output = []
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        entries = z.infolist()
        if len(entries) > 500 or sum(i.file_size for i in entries) > 120_000_000:
            raise ValueError("ZIP_SIZE_LIMIT")
        by_stem = collections.defaultdict(dict)
        for info in entries:
            if info.is_dir():
                continue
            path = pathlib.PurePosixPath(info.filename)
            if path.is_absolute() or ".." in path.parts or "\\" in info.filename or info.file_size > 30_000_000:
                raise ValueError("UNSAFE_ARCHIVE_MEMBER")
            if info.flag_bits & 1:
                raise ValueError("ENCRYPTED_MEMBER")
            if path.suffix.lower() not in (".tag", ".txt"):
                continue
            key = (str(path.parent).casefold(), path.stem.casefold())
            ext = path.suffix.lower()
            if ext in by_stem[key]:
                raise ValueError("DUPLICATE_MEMBER_STEM")
            by_stem[key][ext] = info
        tags = sorted(((key, members) for key, members in by_stem.items()
                       if ".tag" in members), key=lambda x: x[0])
        if len(tags) != 5:
            raise ValueError("EXPECTED_FIVE_TAG_MEMBERS")
        for key, members in tags:
            rows = parse_text(z.read(members[".tag"]))
            if ".txt" not in members:
                output.append((rows, None, "NO_UNAMBIGUOUS_TIMESTAMP_MEMBER"))
                continue
            try:
                ts = parse_timestamps(z.read(members[".txt"]))
                if any(fid not in ts for fid, *_ in rows):
                    raise ValueError("ANNOTATED_FRAME_WITHOUT_TIMESTAMP")
                output.append((rows, ts, "ELIGIBLE"))
            except ValueError as exc:
                output.append((rows, None, str(exc)))
    if sum(len(rows) for rows, _, _ in output) != 58884:
        raise ValueError("ANNOTATION_ROW_COUNT_CHANGED")
    return output


def quantile(sorted_values, p):
    if not sorted_values:
        raise ValueError("EMPTY_QUANTILE")
    x = (len(sorted_values) - 1) * p
    i = int(x)
    return sorted_values[i] if i + 1 == len(sorted_values) else (
        sorted_values[i] + (sorted_values[i+1] - sorted_values[i]) * (x - i))


def time_nearest_samples(ids, times, d, phase):
    """Monotonic virtual point selector; exact Decimal arithmetic, early ties."""
    t0, tend = times[0], times[-1]
    selected = set()
    k = 0
    while True:
        target = t0 + (Decimal(phase) + RATE_RATIO * k) * d
        if target > tend:
            break
        j = bisect.bisect_left(times, target)
        if j == len(times):
            idx = len(times)-1
        elif j == 0:
            idx = 0
        elif target-times[j-1] <= times[j]-target:
            idx = j-1
        else:
            idx = j
        selected.add(ids[idx])
        k += 1
    return selected


def eligible_runs(rows):
    result = []
    for eye in (0, 1):
        for a, b, nv_col in eye_runs(rows, eye):
            if a == 0 or b == len(rows)-1:
                continue
            seg = rows[a-1:b+2]
            if any(seg[i+1][0] != seg[i][0]+1 for i in range(len(seg)-1)):
                continue
            if any(r[1] == "N" or r[nv_col] == "N" for r in seg):
                continue
            result.append((rows[a][0], rows[b][0]))
    return result


def count_outside(deltas, median, scale):
    """Strict relative threshold with exact decimal comparisons (no float drift)."""
    return sum(abs(dt - median) * scale > median for dt in deltas)


def analyze_sequence(rows, ts):
    ids = [r[0] for r in rows]
    times = [ts[fid] for fid in ids]
    pairs = [(times[i]-times[i-1], ids[i]-ids[i-1])
             for i in range(1,len(ids))]
    consecutive = [dt for dt, gap in pairs if gap == 1]
    if len(consecutive) < 2:
        raise ValueError("INSUFFICIENT_CONSECUTIVE_TIMES")
    d = statistics.median(consecutive)
    if d <= 0:
        raise ValueError("NONPOSITIVE_MEDIAN_CADENCE")
    ratios = sorted(float(dt/d) for dt in consecutive)
    uniform = [times[0] + (fid-ids[0])*d for fid in ids]
    actual_sets = [time_nearest_samples(ids,times,d,p) for p in range(N_PHASE)]
    uniform_sets = [time_nearest_samples(ids,uniform,d,p) for p in range(N_PHASE)]
    index_sets = [retained_indices(ids[0],ids[-1],p) for p in range(N_PHASE)]
    runs = eligible_runs(rows)
    actual, uniform_n, index = [0]*N_PHASE,[0]*N_PHASE,[0]*N_PHASE
    changed_vs_uniform = changed_vs_index = 0
    for a,b in runs:
        for p in range(N_PHASE):
            va = not any(fid in actual_sets[p] for fid in range(a,b+1))
            vu = not any(fid in uniform_sets[p] for fid in range(a,b+1))
            vi = not any(fid in index_sets[p] for fid in range(a,b+1))
            actual[p] += va
            uniform_n[p] += vu
            index[p] += vi
            changed_vs_uniform += va != vu
            changed_vs_index += va != vi
    return {
        "frames":len(rows), "consecutive_time_pairs":len(consecutive),
        "nonconsecutive_index_pairs":len(pairs)-len(consecutive),
        "median_time_step_source_units":str(d),
        "dimensionless_dt_over_median_quantiles":{
            str(p):round(quantile(ratios,p),6) for p in (0,.01,.5,.99,1)},
        "outside_10_percent":count_outside(consecutive, d, 10),
        "outside_25_percent":count_outside(consecutive, d, 4),
        "eligible_fc_runs":len(runs),
        "omitted_event_phases_actual_timestamp_nearest":actual,
        "omitted_event_phases_uniform_timestamp_nearest":uniform_n,
        "omitted_event_phases_original_floor_index":index,
        "changed_event_phases_actual_vs_uniform_nearest":changed_vs_uniform,
        "changed_event_phases_actual_vs_original_index":changed_vs_index
    }


def analyze(data):
    paired = paired_sources(data)
    results = []
    for rows,ts,status in paired:
        if status != "ELIGIBLE":
            results.append({"status":"ABSTAIN_SOURCE_TIMING","reason":status,
                            "annotated_frames":len(rows)})
            continue
        try:
            results.append({"status":"SOURCE_TIMESTAMP_COMPUTED",
                            **analyze_sequence(rows,ts)})
        except ValueError as exc:
            results.append({"status":"ABSTAIN_SOURCE_TIMING","reason":str(exc),
                            "annotated_frames":len(rows)})
    return {
        "experiment":"E002-615", "protocol_sha":"d0b0a0c6f659a7a8a02416d0907902676bbfa02f",
        "source_archive_sha256":SOURCE_SHA256,
        "source":"https://www.blinkingmatters.com/research",
        "source_sequences":len(results), "sequence_aggregates":results,
        "evidence_tier":"PUBLISHED_HUMAN_FC_WITH_SOURCE_TIMESTAMP_VIRTUAL_POINT_STRESS_ONLY",
        "physical_30fps_exposure_verified":False, "physical_clock_verified":False,
        "independent_anatomical_raters":False, "velocity_ceiling_certified":False,
        "e002_371_empirically_validated":False,
        "product":"ABSTAIN_UNCALIBRATED", "release":"BLOCKED"
    }


def self_test():
    assert parse_timestamps(b"0 100\n1 110\n2 120\n") == {
        0:Decimal(100),1:Decimal(110),2:Decimal(120)}
    for bad in (b"0 100\n1 90\n",b"0 100\n0 110\n",
                b"0 100 2\n",b"0 NaN\n1 2\n",b"0 1\n2 2\n1 3\n"):
        try:parse_timestamps(bad)
        except ValueError:pass
        else:raise AssertionError("MALFORMED_TIMESTAMP_ACCEPTED")
    ids=list(range(40))
    ts=[Decimal(i)*10 for i in ids]
    d=Decimal(10)
    for p in range(10):
        assert time_nearest_samples(ids,ts,d,p)==time_nearest_samples(
            ids,[t*3+Decimal(71) for t in ts],d*3,p)
    # Boundary cases must not be misclassified by binary float rounding.
    assert count_outside([Decimal('0.009'), Decimal('0.010'), Decimal('0.011')], Decimal('0.010'), 10) == 0
    assert count_outside([Decimal('0.0089'), Decimal('0.0111')], Decimal('0.010'), 10) == 2
    assert count_outside([Decimal('0.0075'), Decimal('0.0125')], Decimal('0.010'), 4) == 0
    assert count_outside([Decimal('0.0074'), Decimal('0.0126')], Decimal('0.010'), 4) == 2
    # Timestamp perturbation is visible in cadence, not silently smoothed.
    rows=[(i,"X","C" if i==20 else "X","X","X","X") for i in ids]
    good=analyze_sequence(rows,dict(zip(ids,ts)))
    assert good["outside_10_percent"]==0 and good["eligible_fc_runs"]==1
    jitter=ts[:]
    jitter[20]+=Decimal(4)
    shifted=analyze_sequence(rows,dict(zip(ids,jitter)))
    assert shifted["outside_10_percent"]>=2
    # Deterministic tie favors earlier frame.
    assert time_nearest_samples([0,1,2],[Decimal(0),Decimal(10),Decimal(20)],
                                Decimal(5),1)=={0}
    print(json.dumps({"experiment":"E002-615","synthetic_self_test":"PASS",
                      "test_groups":6},sort_keys=True))


if __name__=="__main__":
    self_test()
    if "--source" in sys.argv:
        print(json.dumps(analyze(retrieve()),sort_keys=True))
