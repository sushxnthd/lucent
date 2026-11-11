#!/usr/bin/env python3
"""E002-455: preregistered S19 optical aliasing after frame-index decimation.

Image-space scalar contrast only. Not eyelid aperture, physical shutter validation,
blink detection, or a certified no-hidden-closure measurement.
"""
import argparse
import json
import math
import statistics
import tempfile
from pathlib import Path

import numpy as np

from e002_441_human_acquisition import download
from e002_444_human_optical_motion import (
    FIXED_WINDOW, HEIGHT, WIDTH, grayscale_frames, verify_and_extract
)

CALIBRATION = 2000
STRIDES = (8, 17)
C = np.zeros((HEIGHT, WIDTH), dtype=bool)
C[72:216, 80:240] = True
B = ~C
X = np.arange(WIDTH)[None, :]
BL = B & (X < WIDTH // 2)
BR = B & (X >= WIDTH // 2)


def frame_observables(frame):
    a = np.asarray(frame)
    if a.shape != (HEIGHT, WIDTH) or a.dtype != np.uint8:
        raise ValueError("invalid decoded frame")
    z = (float(a[C].mean()) - float(a[B].mean())) / 255.0
    w = (float(a[BL].mean()) - float(a[BR].mean())) / 255.0
    if not all(math.isfinite(v) for v in (z, w)):
        raise ValueError("nonfinite optical observable")
    return z, w


def read_series(frames, limit=FIXED_WINDOW):
    if limit < 3:
        raise ValueError("insufficient frames requested")
    z, w = [], []
    for frame in frames:
        if len(z) >= limit:
            break
        a, b = frame_observables(frame)
        z.append(a)
        w.append(b)
    if len(z) != limit:
        raise ValueError("missing or undecodable high-rate frame")
    return np.asarray(z, dtype=np.float64), np.asarray(w, dtype=np.float64)


def _channel(values, threshold, start, stride):
    per_phase = []
    total = near = hidden = 0
    fractions = []
    t = np.arange(1, stride, dtype=np.float64) / stride
    for phase in range(stride):
        n = q = h = 0
        for a in range(start + phase, len(values) - stride, stride):
            b = a + stride
            n += 1
            if abs(values[b] - values[a]) <= threshold / 2:
                q += 1
                interpolation = values[a] + (values[b] - values[a]) * t
                excursion = float(np.max(np.abs(values[a + 1:b] - interpolation)))
                if excursion >= threshold:
                    h += 1
        if n == 0:
            raise ValueError("empty decimation phase")
        per_phase.append({"phase": phase, "intervals": n,
                          "near_endpoint_intervals": q, "hidden_excursions": h})
        fractions.append(h / n)
        total += n
        near += q
        hidden += h
    expected = len(values) - start - stride
    if total != expected:
        raise AssertionError("phase coverage accounting failure")
    return {"intervals": total, "near_endpoint_intervals": near,
            "hidden_excursions": hidden, "excursion_fraction": hidden / total,
            "phase_fraction_min": min(fractions),
            "phase_fraction_median": statistics.median(fractions),
            "phase_fraction_max": max(fractions),
            "per_phase": per_phase}


def evaluate(z, w, start=CALIBRATION, strides=STRIDES):
    z, w = np.asarray(z, dtype=np.float64), np.asarray(w, dtype=np.float64)
    if z.ndim != 1 or w.shape != z.shape or not np.all(np.isfinite(z)) or not np.all(np.isfinite(w)):
        raise ValueError("invalid or nonfinite series")
    if start < 3 or start >= len(z):
        raise ValueError("invalid calibration split")
    if len(set(strides)) != len(strides) or any(type(k) is not int or k < 3 or len(z)-start <= 2*k for k in strides):
        raise ValueError("invalid decimation strides or insufficient evaluation frames")
    threshold = max(4 / 255.0, 8 * float(np.median(np.abs(np.diff(z[:start])))))
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("invalid calibration threshold")
    results = {}
    for k in strides:
        primary = _channel(z, threshold, start, k)
        control = _channel(w, threshold, start, k)
        results[str(k)] = {"primary": primary, "border_lr_control": control,
                           "primary_greater_than_control": (
                               primary["excursion_fraction"] > control["excursion_fraction"])}
    seen = all(results[str(k)]["primary"]["hidden_excursions"] > 0 for k in strides)
    spatial = all(results[str(k)]["primary_greater_than_control"] for k in strides)
    label = ("NOT_OBSERVED" if not seen else
             "PRIMARY_OPTICAL_ALIASING_OBSERVED_CONTROL_LOWER" if spatial else
             "SPATIAL_SPECIFICITY_NOT_ESTABLISHED")
    return {"experiment": "E002-455", "calibration_frames": start,
            "evaluation_frames": len(z) - start,
            "threshold_contrast_normalized": threshold,
            "stride_results": results, "optical_decision": label,
            "observable": "center-minus-border mean grayscale contrast, not anatomical aperture",
            "clock": "frame index only; not authenticated exposure time",
            "participant_holdouts_inspected": False,
            "independent_anatomical_labels": False,
            "physical_shutter_calibration": False,
            "physiological_velocity_upper_bound_validated": False,
            "e002_371_physical_validation": "NOT_ESTABLISHED",
            "physical_release_authorized": False,
            "product_claim": "ABSTAIN_UNCALIBRATED"}


def run(archive):
    with tempfile.TemporaryDirectory() as td:
        video = Path(td) / "S19.avi"
        times = verify_and_extract(archive, video)
        if len(times) < FIXED_WINDOW:
            raise ValueError("incomplete S19 synchronization inventory")
        z, w = read_series(grayscale_frames(video))
    return {"source": "published-MD5-verified S19 Phantom AVI",
            "decoded_frames": FIXED_WINDOW,
            "pilot_subject": "S19", "raw_frames_exported": False,
            "analysis": evaluate(z, w)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zip", type=Path)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    with tempfile.TemporaryDirectory() as td:
        archive = a.zip or Path(td) / "S19.zip"
        if a.zip is None:
            download("S19", archive)
        result = run(archive)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    summary = result["analysis"]
    print(json.dumps({"experiment": "E002-455",
                      "optical_decision": summary["optical_decision"],
                      "physical_release_authorized": False}, sort_keys=True))


if __name__ == "__main__":
    main()
