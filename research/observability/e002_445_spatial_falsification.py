#!/usr/bin/env python3
"""E002-445: preregistered S19 spatial-specificity and brightness nuisance test.

This is image-observability evidence only. No physiological or shutter claims.
Never emits individual frames, per-frame traces, or identifying timestamps.
"""
import argparse
import json
import math
import tempfile
from pathlib import Path

import numpy as np

from e002_441_human_acquisition import download
from e002_444_human_optical_motion import (
    WIDTH, HEIGHT, FIXED_WINDOW, grayscale_frames, verify_and_extract
)

CENTRAL = np.zeros((HEIGHT, WIDTH), dtype=bool)
CENTRAL[72:216, 80:240] = True
BORDER = ~CENTRAL
SHIFTS = 512
SHIFT_MARGIN = 257


def pair_measurements(frames, event_times, limit=FIXED_WINDOW):
    if limit < 3 or len(event_times) < limit:
        raise ValueError("insufficient candidate events")
    selected_times = np.asarray(event_times[:limit], dtype=np.float64)
    if not np.all(np.isfinite(selected_times)) or np.any(np.diff(selected_times) <= 0):
        raise ValueError("invalid candidate event times")
    records = {name: [] for name in ("central_raw", "border_raw", "central_adjusted", "border_adjusted")}
    previous = None
    count = 0
    for frame in frames:
        if count >= limit:
            break
        arr = np.asarray(frame)
        if arr.shape != (HEIGHT, WIDTH) or arr.dtype != np.uint8:
            raise ValueError("invalid grayscale frame shape or dtype")
        if previous is not None:
            signed = arr.astype(np.int16) - previous.astype(np.int16)
            raw = np.abs(signed)
            global_offset = float(np.median(signed))
            adjusted = np.abs(signed.astype(np.float32) - global_offset)
            records["central_raw"].append(float(np.mean(raw[CENTRAL]) / 255.0))
            records["border_raw"].append(float(np.mean(raw[BORDER]) / 255.0))
            records["central_adjusted"].append(float(np.mean(adjusted[CENTRAL]) / 255.0))
            records["border_adjusted"].append(float(np.mean(adjusted[BORDER]) / 255.0))
        previous = arr.copy()
        count += 1
    if count != limit:
        raise ValueError("decoded fewer than frozen frames")
    return {k: np.asarray(v, dtype=np.float64) for k, v in records.items()}, np.diff(selected_times)


def _ratios(center, border, short, medium):
    if short.sum() < 100 or medium.sum() < 10:
        return None
    cs, cm = float(np.median(center[short])), float(np.median(center[medium]))
    bs, bm = float(np.median(border[short])), float(np.median(border[medium]))
    if not all(math.isfinite(x) and x > 0 for x in (cs, cm, bs, bm)):
        return None
    rc, rb = cm / cs, bm / bs
    if not all(math.isfinite(x) and x > 0 for x in (rc, rb)):
        return None
    return {"central": rc, "border": rb, "relative": rc / rb, "log_relative": math.log(rc / rb),
            "central_short_median": cs, "central_medium_median": cm,
            "border_short_median": bs, "border_medium_median": bm}


def evaluate(records, gaps, n_shifts=SHIFTS):
    keys = ("central_raw", "border_raw", "central_adjusted", "border_adjusted")
    if any(k not in records for k in keys):
        raise ValueError("missing optical metrics")
    series = {k: np.asarray(records[k], dtype=np.float64) for k in keys}
    gap = np.asarray(gaps, dtype=np.float64)
    n = len(gap)
    if n < 3 or any(x.shape != (n,) for x in series.values()):
        raise ValueError("mismatched optical series")
    if not np.all(np.isfinite(gap)) or np.any(gap <= 0):
        raise ValueError("invalid event gaps")
    if any(not np.all(np.isfinite(x)) or np.any(x < 0) or np.any(x > 1) for x in series.values()):
        raise ValueError("invalid normalized optical change")
    short = gap <= .01000001
    medium = (gap > .01000001) & (gap <= .10000001)
    long = gap > .10000001
    base = {
        "pairs": n,
        "gap_counts": {"short": int(short.sum()), "medium": int(medium.sum()), "long": int(long.sum())},
        "raw_ratios": _ratios(series["central_raw"], series["border_raw"], short, medium),
        "adjusted_ratios": _ratios(series["central_adjusted"], series["border_adjusted"], short, medium),
        "null_count": 0,
        "spatial_screen": "ABSTAIN_INSUFFICIENT_EVENTS_OR_CONTRAST",
        "e002_371_physical_validation": "NOT_ESTABLISHED",
        "physical_release_authorized": False,
        "product_claim": "ABSTAIN_UNCALIBRATED",
        "event_frame_alignment_authenticated": False,
        "anatomical_aperture_measured": False,
        "physical_shutter_timing_authenticated": False,
    }
    observed = base["adjusted_ratios"]
    if observed is None or n < 2 * SHIFT_MARGIN + 1 or n_shifts < 1:
        return base
    offsets = np.unique(np.linspace(SHIFT_MARGIN, n - SHIFT_MARGIN, n_shifts, dtype=np.int64))
    if len(offsets) != n_shifts:
        return base
    null = []
    for offset in offsets:
        test = _ratios(np.roll(series["central_adjusted"], int(offset)),
                       np.roll(series["border_adjusted"], int(offset)), short, medium)
        if test is None:
            return base
        null.append(test["log_relative"])
    p95 = float(np.quantile(null, .95))
    rank = (1 + sum(x >= observed["log_relative"] for x in null)) / (len(null) + 1)
    base["null_count"] = len(null)
    base["null_log_contrast_p95"] = p95
    base["descriptive_shift_rank_fraction"] = rank
    base["observed_log_contrast"] = observed["log_relative"]
    base["spatial_screen"] = (
        "SPATIALLY_LOCALIZED_OPTICAL_ASSOCIATION_UNVERIFIED"
        if observed["central"] >= 1.5 and observed["relative"] >= 1.5
        and observed["log_relative"] > p95
        else "SPATIAL_SPECIFICITY_NOT_SUPPORTED"
    )
    return base


def run(archive):
    with tempfile.TemporaryDirectory() as td:
        video = Path(td) / "s19.avi"
        times = verify_and_extract(archive, video)
        records, gaps = pair_measurements(grayscale_frames(video), times)
        summary = evaluate(records, gaps)
    return {
        "experiment": "E002-445",
        "source": "MD5-verified published S19 human AVI; first 12000 frames",
        "pilot_only": True,
        "holdout_S21_S22_inspected": False,
        "interpretation": "spatial optical activity proxy, NOT eyelid aperture",
        "null_interpretation": "descriptive circular shifts, NOT exchangeable p-value",
        "summary": summary,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as td:
        archive = args.zip or Path(td) / "S19.zip"
        if args.zip is None:
            download("S19", archive)
        result = run(archive)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"experiment": "E002-445", "screen": result["summary"]["spatial_screen"],
                      "physical_release_authorized": False}))


if __name__ == "__main__":
    main()
