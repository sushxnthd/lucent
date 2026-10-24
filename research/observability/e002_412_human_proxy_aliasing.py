#!/usr/bin/env python3
"""E002-412: high-speed human optical-proxy phase-decimation; NOT physical aperture.

No source frames, timestamps, per-clip scores, EEG event/control labels, or
private linkage are written to disk or CI artifacts. All outputs aggregate.
"""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
import shutil
import statistics
import tempfile
import zipfile
from pathlib import Path

import cv2
import numpy as np

import e002_397_human_motion as source
import e002_398_blinded_annotation as blind
import e002_406_human_window_adequacy as windows

RATE_HZ = (15, 30, 60)
PHASES = 16
MAX_NEAREST_S = 0.007
VARIANTS = ("gain_070", "gain_130", "blur_sigma2", "glare", "translation_8_6")


def score(gray):
    """Fixed photometric darkness proxy, not an eyelid-landmark estimator."""
    if gray.shape != (130, 190) or gray.dtype != np.uint8:
        raise ValueError("Wrong crop shape or dtype")
    center = gray[30:100, 55:135]
    skin = np.concatenate((gray[5:25, 55:135].ravel(),
                           gray[105:125, 55:135].ravel()))
    baseline = float(np.median(skin))
    if baseline <= 35 or baseline >= 240 or np.mean(center >= 250) >= .02:
        return None
    return float(np.clip((baseline - np.percentile(center, 20)) / baseline, -1., 1.))


def transform(gray, variant):
    if variant == "gain_070":
        return np.clip(gray.astype(np.float32) * .70, 0, 255).astype(np.uint8)
    if variant == "gain_130":
        return np.clip(gray.astype(np.float32) * 1.30, 0, 255).astype(np.uint8)
    if variant == "blur_sigma2":
        return cv2.GaussianBlur(gray, (0, 0), 2)
    if variant == "glare":
        out = gray.copy()
        out[60:90, 75:105] = 255
        return out
    if variant == "translation_8_6":
        return cv2.warpAffine(gray, np.float32([[1, 0, 8], [0, 1, 6]]),
                              (190, 130), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_REFLECT_101)
    raise ValueError("Unknown variant")


def nearest_indices(times, rate, phase, tolerance=MAX_NEAREST_S):
    """Return only observed source indices; None for unsupported sample times."""
    if not times or any(not math.isfinite(x) for x in times):
        raise ValueError("Invalid time series")
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("Nonmonotone source clock")
    if rate <= 0 or not (0 <= phase < 1.0 / rate):
        raise ValueError("Invalid phase/rate")
    start, stop = times[0] + phase, times[-1]
    n = int(math.floor((stop - start) * rate + 1e-10)) + 1
    result = []
    for k in range(max(n, 0)):
        target = start + k / rate
        j = bisect.bisect_left(times, target)
        candidates = [i for i in (j - 1, j) if 0 <= i < len(times)]
        if not candidates:
            result.append(None)
            continue
        best = min(candidates, key=lambda i: (abs(times[i] - target), i))
        result.append(best if abs(times[best] - target) <= tolerance else None)
    return result


def captured_range(times, values, rate, phase):
    indices = nearest_indices(times, rate, phase)
    selected = [values[i] for i in indices if i is not None and values[i] is not None]
    clean = [v for v in values if v is not None]
    if len(clean) < 2 or len(selected) < 2:
        return None
    full = max(clean) - min(clean)
    if full < .02:
        return None
    ratio = (max(selected) - min(selected)) / full
    if not (-1e-10 <= ratio <= 1 + 1e-10):
        raise AssertionError("Sampled extrema exceed observed extrema")
    return min(1., max(0., ratio))


def select_clips(archive, participant):
    if source.prior.md5(archive) != source.MD5[participant]:
        raise ValueError("Source MD5 mismatch")
    z = zipfile.ZipFile(archive)
    try:
        video, frames, markers = source.load_archive(z, participant)
        pairs, _ = source.select_pairs(frames, markers, participant)
        selected = blind.selected_pairs(pairs)
        times, ids = [t for _, t in frames], [i for i, _ in frames]
        complete = [(k, j) for _, (k, j) in selected
                    if windows.evaluate_window(times, ids, k)["eligible"]
                    and windows.evaluate_window(times, ids, j)["eligible"]]
        if len(complete) < 2:
            raise ValueError("Missing frozen complete pairs")
        chosen = complete[:2]
        ranges = []
        for k, j in chosen:
            for center in (k, j):
                left = bisect.bisect_right(times, times[center] - .25) - 1
                right = bisect.bisect_left(times, times[center] + .25)
                ranges.append((left, right))
        return z, video, times, len(frames), ranges
    except BaseException:
        z.close()
        raise


def evaluate_archive(archive, participant):
    z, video, times, frame_count, ranges = select_clips(archive, participant)
    needed = {i for a, b in ranges for i in range(a, b + 1)}
    frame_scores = {}
    try:
        with tempfile.TemporaryDirectory(prefix="e002-412-") as tmp:
            path = Path(tmp) / "source.avi"
            with z.open(video) as inp, path.open("wb") as out:
                shutil.copyfileobj(inp, out, 1 << 20)
            cap = cv2.VideoCapture(str(path))
            if not cap.isOpened() or int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) != frame_count:
                raise ValueError("Video/sync mismatch")
            i = 0
            try:
                while True:
                    ok, frame = cap.read()
                    if not ok:
                        break
                    if i in needed:
                        if frame.shape[:2] != (288, 320):
                            raise ValueError("Unexpected frame geometry")
                        gray = cv2.cvtColor(frame[90:220, 70:260], cv2.COLOR_BGR2GRAY)
                        frame_scores[i] = {"clean": score(gray)}
                        for v in VARIANTS:
                            frame_scores[i][v] = score(transform(gray, v))
                    i += 1
            finally:
                cap.release()
            if i != frame_count or set(frame_scores) != needed:
                raise ValueError("Missing decoded frame")
    finally:
        z.close()
    clips = []
    for a, b in ranges:
        t = times[a:b + 1]
        vals = {v: [frame_scores[i][v] for i in range(a, b + 1)]
                for v in ("clean",) + VARIANTS}
        clips.append((t, vals))
    return clips


def summarize(all_clips):
    n = sum(len(t) for t, _ in all_clips)
    eligible = sum(v is not None for _, scores in all_clips for v in scores["clean"])
    active = sum(len([v for v in s["clean"] if v is not None]) > 1
                 and max(v for v in s["clean"] if v is not None)
                 - min(v for v in s["clean"] if v is not None) >= .02
                 for _, s in all_clips)
    nuisance = {}
    for variant in VARIANTS:
        paired = [(a, b) for _, s in all_clips
                  for a, b in zip(s["clean"], s[variant])
                  if a is not None and b is not None]
        diff = [abs(a - b) for a, b in paired]
        total = sum(len(t) for t, _ in all_clips)
        nuisance[variant] = {
            "joint_valid_frames": len(diff),
            "joint_valid_fraction": round(len(diff) / total, 6),
            "fraction_abs_change_le_008": round(sum(d <= .08 for d in diff) / len(diff), 6)
            if diff else None,
            "median_abs_change": round(statistics.median(diff), 6) if diff else None,
            "rejected_frames": total - sum(
                x is not None for _, s in all_clips for x in s[variant]),
        }
    alias = {}
    for rate in RATE_HZ:
        ratios = []
        for times, s in all_clips:
            for phase_index in range(PHASES):
                v = captured_range(times, s["clean"], rate,
                                   phase_index / (rate * PHASES))
                if v is not None:
                    ratios.append(v)
        alias[str(rate)] = {
            "valid_clip_phases": len(ratios),
            "min_capture_ratio": round(min(ratios), 6) if ratios else None,
            "median_capture_ratio": round(statistics.median(ratios), 6) if ratios else None,
            "fraction_loss_gt_010": round(sum(r < .9 for r in ratios) / len(ratios), 6)
            if ratios else None,
        }
    glare_rejected = nuisance["glare"]["rejected_frames"] / n
    gain_blur_pass = all(nuisance[v]["fraction_abs_change_le_008"] is not None
                         and nuisance[v]["fraction_abs_change_le_008"] >= .95
                         for v in ("gain_070", "gain_130", "blur_sigma2"))
    trans = nuisance["translation_8_6"]["fraction_abs_change_le_008"]
    hypotheses = {
        "H1_eight_clips_ge_600_frames": len(all_clips) == 8 and n >= 600,
        "H2_clean_90pct_valid_four_dynamic": eligible / n >= .9 and active >= 4,
        "H3_30Hz_phase_aliasing_gt_10pct": alias["30"]["min_capture_ratio"] is not None
                                         and alias["30"]["min_capture_ratio"] < .9,
        "H4_gain_blur_95pct_stable": gain_blur_pass,
        "H5_glare_95pct_rejected": glare_rejected >= .95,
        "H6_range_ratios_valid": all(
            alias[str(rate)]["min_capture_ratio"] is None
            or 0 <= alias[str(rate)]["min_capture_ratio"] <= 1
            for rate in RATE_HZ),
    }
    return {
        "experiment": "E002-412",
        "evidence_tier": "real human video, exploratory fixed optical proxy, no physical aperture",
        "source_md5_verified": True, "clips": len(all_clips), "total_frames": n,
        "clean_valid_frames": eligible, "dynamic_clips": active,
        "nuisance": nuisance, "point_decimation": alias,
        "translation_transfer_rejected": trans is None or trans < .95,
        "glare_rejected_fraction": round(glare_rejected, 6),
        "hypotheses": hypotheses, "all_hypotheses_pass": all(hypotheses.values()),
        "camera_exposure_calibrated": False, "physical_aperture_validated": False,
        "hard_velocity_bound_established": False,
        "product": "ABSTAIN_UNCALIBRATED",
    }


def self_test():
    """Brute-force independent oracle and synthetic photometric controls."""
    import random
    rng = random.Random(412)
    for _ in range(500):
        dt = rng.uniform(.005, .009)
        times = [i * dt for i in range(rng.randint(70, 100))]
        rate = rng.choice(RATE_HZ)
        phase = rng.random() / rate
        got = nearest_indices(times, rate, phase)
        start = times[0] + phase
        expected = []
        for k in range(len(got)):
            t = start + k / rate
            best = min(range(len(times)), key=lambda i: (abs(times[i] - t), i))
            expected.append(best if abs(times[best] - t) <= MAX_NEAREST_S else None)
        assert got == expected, "Independent decimation oracle mismatch"
    for bad in ([0., .01, .01], [0., .02, .01], [0., float("nan"), .03]):
        try:
            nearest_indices(bad, 30, 0)
        except ValueError:
            pass
        else:
            raise AssertionError("Bad clock accepted")
    img = np.full((130, 190), 160, dtype=np.uint8)
    img[50:85, 65:125] = 40
    assert score(img) is not None
    assert score(transform(img, "glare")) is None
    assert abs(score(img) - score(transform(img, "gain_070"))) < .02
    return {"independent_decimation_trials": 500, "synthetic_controls": "passed"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--s01", type=Path)
    p.add_argument("--s19", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        print(json.dumps(self_test(), sort_keys=True))
        return
    if not (a.s01 and a.s19 and a.output):
        p.error("--s01, --s19 and --output required")
    all_clips = evaluate_archive(a.s01, "S01") + evaluate_archive(a.s19, "S19")
    result = summarize(all_clips)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
