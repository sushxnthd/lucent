#!/usr/bin/env python3
"""E002-578: execute E002-575 on one genuine LPW DEVELOPMENT video.

No anatomical labels, pixel-derived features, image exports, or held-out access.
No output of owner-only window indices or raw human imagery.
"""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

import e002_575_lpw_packet as packet
import e002_577_lpw_range_probe as source

EXP = "E002-578"
VIDEO = "LPW/1/1.avi"
VIDEO_SHA = "158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86"
NATIVE_FRAMES = 2000
WIDTH, HEIGHT = 640, 480
RATE = "95/1"
WINDOW = 19
N_WINDOWS = 10


class InstrumentError(Exception):
    pass


def development_ids():
    ordered = sorted((hashlib.sha256(
        ("E002-573-LPW-v1|" + str(p)).encode()).hexdigest(), str(p))
        for p in range(1, 23))
    return {p for _, p in ordered[:11]}


def frozen_starts(digest=VIDEO_SHA, n=NATIVE_FRAMES):
    if not isinstance(digest, str) or len(digest) != 64 or n < WINDOW * N_WINDOWS:
        raise InstrumentError("INVALID_SOURCE_WINDOW_UNIVERSE")
    candidates = list(range(0, n - WINDOW + 1, WINDOW))
    ranked = sorted(candidates, key=lambda s: (
        hashlib.sha256(("E002-573-window-v1|" + digest + "|" + str(s))
                       .encode()).hexdigest(), s))
    if len(ranked) < N_WINDOWS:
        raise InstrumentError("INSUFFICIENT_COMPLETE_WINDOWS")
    return ranked[:N_WINDOWS], len(candidates)


def blank_template(rater, clips):
    blank = lambda i: {"frame": i, "upper_y": None, "lower_y": None,
                       "iris_diameter": None, "uncertainty_px": None,
                       "flags": ["UNREVIEWED"]}
    return {"experiment": "E002-574", "rater": rater,
            "clips": {clip: [blank(i) for i in range(WINDOW)] for clip in clips}}


def make_plan():
    if "1" not in development_ids():
        raise InstrumentError("FROZEN_DEVELOPMENT_SPLIT_MISMATCH")
    starts, candidates = frozen_starts()
    mapping = []
    for i, start in enumerate(starts):
        mapping.append({"blind_clip": f"clip_{i:04d}",
                        "participant_id": "1", "video_id": "1",
                        "video_sha256": VIDEO_SHA,
                        "start_native_frame": start,
                        "native_frames": list(range(start, start + WINDOW)),
                        "candidate_windows": candidates})
    owner = {"experiment": "E002-574", "evidence_tier": "SELECTION_PLAN_ONLY",
             "window_count": N_WINDOWS, "owner_mapping": mapping}
    clips = [row["blind_clip"] for row in mapping]
    a, b = blank_template("A", clips), blank_template("B", clips)
    packet.validate_plan(owner, a, b)
    return owner, a, b, candidates


def verify_packet(root, owner, a, b):
    audit = json.loads((root / "OWNER_ONLY_SOURCE_AUDIT.json").read_text())
    if (audit.get("experiment") != "E002-575" or
            audit.get("evidence_tier") != "SOURCE_BOUND_NATIVE_FRAME_PACKET_ONLY" or
            len(audit.get("videos", [])) != 1 or
            len(audit.get("frames", [])) != WINDOW * N_WINDOWS):
        raise InstrumentError("OWNER_AUDIT_SHAPE_MISMATCH")
    v = audit["videos"][0]
    if (v.get("participant_id") != "1" or v.get("video_id") != "1" or
            v.get("video_sha256") != VIDEO_SHA or
            v.get("decoded_frames") != NATIVE_FRAMES or
            (v.get("native_width"), v.get("native_height")) != (WIDTH, HEIGHT) or
            v.get("timestamp_check") != "STRICTLY_MONOTONIC_CONTAINER_PTS_ONLY"):
        raise InstrumentError("OWNER_VIDEO_PROVENANCE_MISMATCH")
    expected = {(m["blind_clip"], j): m["native_frames"][j]
                for m in owner["owner_mapping"] for j in range(WINDOW)}
    seen = set()
    for row in audit["frames"]:
        key = (row.get("blind_clip"), row.get("frame_in_clip"))
        if (key not in expected or key in seen or
                row.get("native_frame_index") != expected[key] or
                row.get("participant_id") != "1" or
                row.get("video_id") != "1"):
            raise InstrumentError("AUDIT_FRAME_SOURCE_BINDING_FAILURE")
        seen.add(key)
        clip, j = key
        digests = []
        for r in ("A", "B"):
            path = root / f"RATER_{r}" / "clips" / clip / f"frame_{j:02d}.png"
            if not path.is_file() or path.is_symlink():
                raise InstrumentError("MISSING_OR_SYMLINKED_REVIEW_FRAME")
            if packet.png_dimensions(path) != (WIDTH, HEIGHT):
                raise InstrumentError("REVIEW_FRAME_GEOMETRY_CHANGED")
            digests.append(packet.sha256(path))
        if len(set(digests + [row.get("decoded_png_sha256")])) != 1:
            raise InstrumentError("REVIEWER_FRAME_BYTES_DISAGREE")
    if seen != set(expected):
        raise InstrumentError("INCOMPLETE_SOURCE_FRAME_BINDING")
    for r, template in (("A", a), ("B", b)):
        p = root / f"RATER_{r}" / "BLANK_ANATOMICAL_RATINGS.json"
        if json.loads(p.read_text()) != template:
            raise InstrumentError("RATER_TEMPLATE_CHANGED")
        manifest = json.loads((root / f"RATER_{r}" / "PACKET_MANIFEST.json").read_text())
        if (manifest.get("human_annotations") != 0 or
                manifest.get("clip_count") != N_WINDOWS or
                manifest.get("frames_per_clip") != WINDOW or
                manifest.get("camera_clock_authenticated") is not False):
            raise InstrumentError("RATER_MANIFEST_FALSE_CLAIM")
    return len(seen)


def probe_stream(video):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
        "-of", "json", str(video)], capture_output=True, text=True,
        timeout=60, check=True)
    streams = json.loads(result.stdout).get("streams", [])
    if len(streams) != 1:
        raise InstrumentError("NONUNIQUE_VIDEO_STREAM")
    s = streams[0]
    if (s.get("width"), s.get("height"), s.get("r_frame_rate"),
            str(s.get("nb_frames"))) != (WIDTH, HEIGHT, RATE, str(NATIVE_FRAMES)):
        raise InstrumentError("FROZEN_STREAM_METADATA_MISMATCH")
    return s


def execute():
    owner, a, b, candidates = make_plan()
    total = source.remote_size(source.URL)
    get = source.remote_getter(source.URL, total)
    entry, eligible = source.archive_entries(total, get)
    if entry["name"] != VIDEO or eligible != 66:
        raise InstrumentError("FROZEN_SOURCE_ENTRY_MISMATCH")
    data = source.extract_member(total, get, entry)
    if hashlib.sha256(data).hexdigest() != VIDEO_SHA:
        raise InstrumentError("FROZEN_SOURCE_SHA256_MISMATCH")
    with tempfile.TemporaryDirectory(prefix="lucent-e002-578-") as td:
        folder = Path(td)
        video = folder / "private_source.avi"
        video.write_bytes(data)
        del data
        probe_stream(video)
        sources = {"videos": [{"participant_id": "1", "video_id": "1",
                              "video_sha256": VIDEO_SHA,
                              "native_frame_count": NATIVE_FRAMES,
                              "absolute_path": str(video)}]}
        root = folder / "private_review_packets"
        result = packet.build_packet(owner, sources, a, b, root)
        if result.get("frames_per_reviewer") != N_WINDOWS * WINDOW:
            raise InstrumentError("INCORRECT_PACKET_FRAME_COUNT")
        audited = verify_packet(root, owner, a, b)
        if packet.sha256(video) != VIDEO_SHA:
            raise InstrumentError("SOURCE_MUTATED_AFTER_DECODE")
    return {"experiment": EXP, "status": "AUTHENTIC_DEVELOPMENT_PACKET_VERIFIED",
            "evidence_tier": "REAL_HUMAN_SOURCE_INSTRUMENT_ONLY",
            "source_member": VIDEO, "source_sha256": VIDEO_SHA,
            "native_video_frames": NATIVE_FRAMES, "reported_stream_rate": RATE,
            "eligible_nonoverlapping_windows": candidates,
            "selected_windows": N_WINDOWS, "frames_per_reviewer": audited,
            "reviewers": 2, "independent_human_raters": 0,
            "anatomical_labels": 0, "camera_clock_authenticated": False,
            "shutter_calibrated": False, "continuous_velocity_ceiling_certified": False,
            "physical_closure_predictions": 0, "private_packets_retained": False,
            "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}


def self_test():
    owner, a, b, n = make_plan()
    starts, n2 = frozen_starts()
    assert n == n2 == 105 and len(starts) == len(set(starts)) == 10
    assert all(s % WINDOW == 0 and 0 <= s <= NATIVE_FRAMES-WINDOW for s in starts)
    assert "1" in development_ids() and len(development_ids()) == 11
    assert len(owner["owner_mapping"]) == 10
    assert set(a) == set(b) == {"experiment", "rater", "clips"}
    assert all(all(f["flags"] == ["UNREVIEWED"] and
                   all(f[k] is None for k in ("upper_y", "lower_y",
                                            "iris_diameter", "uncertainty_px"))
                   for f in frames) for frames in a["clips"].values())
    assert all("participant_id" not in json.dumps(t) and
               "video_sha256" not in json.dumps(t) and
               "start_native_frame" not in json.dumps(t) for t in (a, b))
    assert make_plan() == (owner, a, b, n)
    try:
        frozen_starts(n=10)
    except InstrumentError:
        pass
    else:
        raise AssertionError("Short source was accepted")
    tampered = json.loads(json.dumps(a))
    tampered["clips"]["clip_0000"][0]["flags"] = []
    try:
        packet.validate_plan(owner, tampered, b)
    except ValueError:
        pass
    else:
        raise AssertionError("Prefilled reviewer packet accepted")
    return {"experiment": EXP, "self_test": "PASS",
            "checks": ["frozen participant split", "selection invariance",
                       "source-window bounds", "blinded templates",
                       "reject short source", "reject prefilled template"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True))
        return
    try:
        result = execute()
    except Exception as exc:
        result = {"experiment": EXP, "status": "FAILED_OR_ABSTAINED",
                  "failure_type": type(exc).__name__, "failure_reason": str(exc)[:200],
                  "human_rater_pairs": 0, "product": "ABSTAIN_UNCALIBRATED",
                  "release": "BLOCKED"}
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "AUTHENTIC_DEVELOPMENT_PACKET_VERIFIED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
