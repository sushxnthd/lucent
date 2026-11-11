#!/usr/bin/env python3
"""E002-493: pre-registered nuisance falsification on 20 authentic S01 clips.

Outputs aggregate proxy statistics only. Not blink, shutter, or anatomical inference.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile
import zipfile

from e002_491_calibration_motion import SIZE, MAX_FRAMES, motion_pair, read_frames
from e002_492_anatomical_review import (
    EXPECTED_MD5, build_manifest, md5_file, safe_member,
)

CONDITIONS = (
    "baseline", "brightness_plus8", "contrast_90pct",
    "blur_3x3", "alternating_jitter_1px", "stride2",
)


def clip_frames(indexed):
    manifest = build_manifest()
    clips = []
    for item in manifest["review_clips"]:
        indices = item["native_frames"]
        if len(indices) != 13 or any(i not in indexed for i in indices):
            raise ValueError("MISSING_FROZEN_NATIVE_FRAME")
        clip = [indexed[i] for i in indices]
        if any(len(frame) != SIZE for frame in clip):
            raise ValueError("INVALID_FRAME_SIZE")
        clips.append((item["candidate"], clip))
    if len(clips) != 20 or sum(c for c, _ in clips) != 1:
        raise ValueError("INVALID_FROZEN_CLIPS")
    return clips


def transform(frame, condition, j):
    if len(frame) != SIZE:
        raise ValueError("INVALID_FRAME_SIZE")
    if condition in ("baseline", "stride2"):
        return frame
    if condition == "brightness_plus8":
        return bytes(min(255, v + 8) for v in frame)
    if condition == "contrast_90pct":
        return bytes(max(0, min(255, round(128 + .9 * (v - 128)))) for v in frame)
    if condition == "blur_3x3":
        result = bytearray(SIZE)
        for y in range(64):
            for x in range(64):
                s = 0
                for dy in (-1, 0, 1):
                    yy = min(63, max(0, y + dy))
                    for dx in (-1, 0, 1):
                        xx = min(63, max(0, x + dx))
                        s += frame[yy * 64 + xx]
                result[y * 64 + x] = (s + 4) // 9
        return bytes(result)
    if condition == "alternating_jitter_1px":
        # Alternating +/-1-pixel apparent image registration, edge replication.
        shift = 1 if j % 2 else -1
        return bytes(frame[y * 64 + min(63, max(0, x - shift))]
                     for y in range(64) for x in range(64))
    raise ValueError("UNKNOWN_CONDITION")


def screen(clips, condition):
    if condition not in CONDITIONS:
        raise ValueError("UNKNOWN_CONDITION")
    counts = dict(analyzed_pairs=0, eligible_pairs=0, nuisance_abstentions=0,
                  duplicate_pairs=0, proxy_candidates=0,
                  candidate_clip_candidates=0, control_clip_candidates=0)
    for is_candidate, frames in clips:
        if len(frames) != 13:
            raise ValueError("CLIP_LENGTH_MISMATCH")
        positions = range(0, 13, 2) if condition == "stride2" else range(13)
        transformed = [transform(frames[j], condition, j) for j in positions]
        for a, b in zip(transformed, transformed[1:]):
            p = motion_pair(a, b)
            counts["analyzed_pairs"] += 1
            if p["status"] == "NUISANCE":
                counts["nuisance_abstentions"] += 1
            elif p["status"] == "DUPLICATE":
                counts["duplicate_pairs"] += 1
            else:
                counts["eligible_pairs"] += 1
                if p["candidate"]:
                    counts["proxy_candidates"] += 1
                    key = ("candidate_clip_candidates" if is_candidate
                           else "control_clip_candidates")
                    counts[key] += 1
    counts["candidate_clip_positive"] = counts["candidate_clip_candidates"] > 0
    counts["eligible_fraction"] = round(
        counts["eligible_pairs"] / max(1, counts["analyzed_pairs"]), 6)
    return counts


def analyze(indexed):
    clips = clip_frames(indexed)
    results = {name: screen(clips, name) for name in CONDITIONS}
    base = results["baseline"]
    baseline_ok = (base["candidate_clip_positive"]
                   and base["control_clip_candidates"] == 0)
    for name, data in results.items():
        if not baseline_ok:
            data["verdict"] = "BASELINE_NOT_REPRODUCED"
        else:
            fail = (not data["candidate_clip_positive"]
                    or data["control_clip_candidates"] > 0
                    or data["eligible_fraction"] < .8)
            data["verdict"] = ("FAIL" if fail else
                               ("REPRODUCED" if name == "baseline"
                                else "SURVIVES_THIS_FIXTURE_ONLY"))
    return {
        "experiment": "E002-493",
        "subject": "S01_CALIBRATION_ONLY",
        "evidence_tier": "AUTHENTIC_HUMAN_IMAGE_PROXY_NUISANCE_TEST_ONLY",
        "frozen_review_clips": 20,
        "native_frame_positions": 260,
        "baseline_reproduced": baseline_ok,
        "conditions": results,
        "anatomical_closure_labels": 0,
        "human_reference_validated": False,
        "acquisition_fps_authenticated": False,
        "physical_hidden_closure_certified": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }


def inspect(archive):
    archive = Path(archive)
    if archive.stat().st_size > 600_000_000 or md5_file(archive) != EXPECTED_MD5:
        raise ValueError("ARCHIVE_SIZE_OR_CHECKSUM_MISMATCH")
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        if not all(safe_member(i) for i in infos):
            raise ValueError("UNSAFE_ARCHIVE")
        vids = sorted((i for i in infos if i.filename.lower().endswith("_phantom.avi")),
                      key=lambda i: i.filename)
        if not vids or vids[0].file_size > 1_000_000_000:
            raise ValueError("MISSING_OR_OVERSIZE_VIDEO")
        with tempfile.TemporaryDirectory(prefix="lucent493_") as td:
            video = Path(td) / "source.avi"
            with z.open(vids[0]) as src, video.open("wb") as dst:
                shutil.copyfileobj(src, dst, 1024 * 1024)
            if video.stat().st_size != vids[0].file_size:
                raise ValueError("TRUNCATED_VIDEO")
            required = {j for item in build_manifest()["review_clips"]
                        for j in item["native_frames"]}
            if len(required) != 260 or max(required) >= MAX_FRAMES:
                raise ValueError("INVALID_FROZEN_SELECTION")
            indexed = {}
            for j, frame in enumerate(read_frames(video)):
                if j in required:
                    indexed[j] = frame
            if set(indexed) != required:
                raise ValueError("INCOMPLETE_NATIVE_DECODE")
            return analyze(indexed)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    try:
        report = inspect(args.archive)
        rc = 0
    except Exception as e:
        report = {"experiment": "E002-493", "status": "FAILED_OR_ABSTAINED",
                  "reason": str(e)[:160], "anatomical_closure_labels": 0,
                  "physical_hidden_closure_certified": False,
                  "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}
        rc = 2
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))
    return rc


if __name__ == "__main__":
    sys.exit(main())
