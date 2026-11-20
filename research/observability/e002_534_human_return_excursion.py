#!/usr/bin/env python3
"""E002-534: native human-image return excursion, NOT anatomical blink truth.
Only anonymous aggregate counts are printed; never upload frames or linkage.
"""
from __future__ import annotations
import argparse
from collections import deque
import json
from pathlib import Path
import shutil
import tempfile
import zipfile
import cv2
import numpy as np

EYE = np.s_[118:190, 100:230]
BACKGROUND = np.s_[20:100, 30:290]
LIMIT = 12006
PHASES = (0, 2)

def measurements(frames):
    if len(frames) != 6 or any(f.shape != (288, 320) for f in frames):
        raise ValueError("Expected six native 288x320 grayscale frames")
    base = float(np.median(frames[0][BACKGROUND]))
    normalized = []
    for frame in frames:
        delta = base - float(np.median(frame[BACKGROUND]))
        normalized.append(np.clip(frame.astype(np.float32) + delta, 0, 255))
    result = {}
    for name, roi in (("eye", EYE), ("background", BACKGROUND)):
        a, b = normalized[0][roi], normalized[-1][roi]
        d = float(np.mean(np.abs(b - a)))
        e = max(float(np.mean(np.abs(normalized[j][roi] -
                        ((1-j/5)*a + (j/5)*b)))) for j in range(1, 5))
        result[name] = (d, e)
    return result

def candidate(m):
    de, ee = m["eye"]
    return de <= 8 and ee >= 18 and m["background"][1] <= 8

def quality_ok(frame_ids, times):
    if len(frame_ids) != 6 or len(times) != 6:
        return False
    try:
        if any(int(frame_ids[i+1]) != int(frame_ids[i]) + 1 for i in range(5)):
            return False
        dt = [float(times[i+1]) - float(times[i]) for i in range(5)]
    except (ValueError, TypeError, OverflowError):
        return False
    return (all(0.002 <= d <= 0.020 for d in dt)
            and 0.020 <= sum(dt) <= 0.050)

def transform(frames, variant):
    if variant == "gain_120":
        return [np.clip(f.astype(np.float32)*1.2, 0, 255).astype(np.uint8)
                for f in frames]
    if variant == "blur_sigma2":
        return [cv2.GaussianBlur(f, (0, 0), 2) for f in frames]
    raise ValueError("Unknown frozen nuisance")

def new_counts():
    return {"eligible": 0, "rejected_time_or_id": 0,
            "eye_return": 0, "eye_specific": 0,
            "background_return": 0, "blur_survivors": 0,
            "gain_survivors": 0}

def accumulate(stats, frames):
    m = measurements(frames)
    stats["eligible"] += 1
    if m["eye"][0] <= 8 and m["eye"][1] >= 18:
        stats["eye_return"] += 1
    if m["background"][0] <= 8 and m["background"][1] >= 18:
        stats["background_return"] += 1
    if candidate(m):
        stats["eye_specific"] += 1
        stats["blur_survivors"] += int(candidate(measurements(transform(frames, "blur_sigma2"))))
        stats["gain_survivors"] += int(candidate(measurements(transform(frames, "gain_120"))))

def finalize(stats):
    n = stats["eye_specific"]
    stats["blur_survival_fraction"] = stats["blur_survivors"]/n if n else None
    stats["gain_survival_fraction"] = stats["gain_survivors"]/n if n else None
    stats["H2_blur_80pct"] = (stats["blur_survivors"]*5 >= 4*n) if n else "NOT_TESTABLE"
    stats["H3_gain_80pct"] = (stats["gain_survivors"]*5 >= 4*n) if n else "NOT_TESTABLE"
    return stats

def analyze_stream(images, frame_ids, times):
    stats = {str(p): new_counts() for p in PHASES}
    ring = deque(maxlen=6)
    n = 0
    for n, gray in enumerate(images, 1):
        if n > LIMIT:
            break
        if gray.shape != (288, 320):
            raise ValueError("Unexpected native video geometry")
        ring.append(gray)
        k = n - 6
        if k < 0 or k % 5 not in PHASES:
            continue
        p = str(k % 5)
        if not quality_ok(frame_ids[k:k+6], times[k:k+6]):
            stats[p]["rejected_time_or_id"] += 1
            continue
        accumulate(stats[p], list(ring))
    if n < LIMIT:
        raise ValueError("Source ended before frozen 12006-frame window")
    return {p: finalize(v) for p, v in stats.items()}

def evaluate_archive(archive, participant):
    import e002_397_human_motion as prior
    if participant not in prior.MD5 or prior.prior.md5(archive) != prior.MD5[participant]:
        raise ValueError("Source checksum/participant mismatch")
    with zipfile.ZipFile(archive) as z:
        video, records, _ = prior.load_archive(z, participant)
        if len(records) < LIMIT:
            raise ValueError("Insufficient source frames")
        ids = [x for x, _ in records]
        times = [t for _, t in records]
        with tempfile.TemporaryDirectory() as tmp:
            avi = Path(tmp) / "native.avi"
            with z.open(video) as source, avi.open("wb") as target:
                shutil.copyfileobj(source, target, 1 << 20)
            cap = cv2.VideoCapture(str(avi))
            if not cap.isOpened() or int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) != len(records):
                raise ValueError("Native video decode/record count mismatch")
            def images():
                for _ in range(LIMIT):
                    ok, bgr = cap.read()
                    if not ok:
                        raise ValueError("Truncated native video")
                    yield cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            try:
                counts = analyze_stream(images(), ids, times)
            finally:
                cap.release()
    return {"experiment": "E002-534", "participant": participant,
            "source_checksum_verified": True, "native_frames_analyzed": LIMIT,
            "phases": counts, "human_anatomical_closure_measured": False,
            "physical_camera_timing_authenticated": False,
            "participant_disjoint_holdout": False,
            "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--participant", choices=("S01", "S19"), required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate_archive(args.archive, args.participant),
                     sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
