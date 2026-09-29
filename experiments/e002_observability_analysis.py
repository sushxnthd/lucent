"""Aggregate repeated E002 phone captures against the frozen observability gates.

Expected per-capture files in one directory:

    <stem>.pupil.json
    <stem>.trace.csv
    <stem>.quality.json

The script does not use raw video and does not estimate fatigue.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path

import numpy as np


ACTIVE = ("contiguous", "split")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def stem_from_pupil(path: Path) -> str:
    suffix = ".pupil.json"
    if not path.name.endswith(suffix):
        raise ValueError(path)
    return path.name[: -len(suffix)]


def timing_pass(pupil: dict) -> bool:
    timing = pupil.get("captureTiming") or {}
    duration = timing.get("actualDurationMs")
    max_error = timing.get("maxStimulusSchedulingErrorMs")
    cadence = timing.get("frameCadence") or {}

    if duration is None or not (4800 <= float(duration) <= 5300):
        return False
    if max_error is None or float(max_error) > 35:
        return False

    if cadence.get("available"):
        median = cadence.get("medianIntervalMs")
        p95 = cadence.get("p95IntervalMs")
        if median is None or p95 is None:
            return False
        if float(median) > 45 or float(p95) > 75:
            return False

    return True


def offline_visibility_pass(quality: dict | None) -> bool:
    if not quality:
        return False
    q = quality.get("quality") or {}
    face = q.get("faceDetectionRate")
    eyes = q.get("twoEyeDetectionRate")
    if face is None or eyes is None:
        return False
    return float(face) >= 0.90 and float(eyes) >= 0.70


def pupil_pass(pupil: dict) -> bool:
    summary = pupil.get("summary") or {}
    rate = summary.get("validPupilRate")
    return rate is not None and float(rate) >= 0.60


def read_trace(path: Path):
    rows = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                t = float(row["offsetS"])
                ratio = float(row["pupilRatio"])
                quality = float(row["quality"])
            except (ValueError, TypeError, KeyError):
                continue
            if not (np.isfinite(t) and np.isfinite(ratio) and np.isfinite(quality)):
                continue
            if quality < 0.45:
                continue
            rows.append((t, ratio))

    if len(rows) < 20:
        return None

    rows.sort()
    t = np.asarray([x[0] for x in rows], dtype=float)
    y = np.asarray([x[1] for x in rows], dtype=float)

    # Remove duplicate timestamps for stable interpolation.
    unique_t, unique_idx = np.unique(t, return_index=True)
    y = y[unique_idx]
    t = unique_t

    grid = np.arange(0.0, 5.0001, 0.05)
    if t[0] > 0.15 or t[-1] < 4.85:
        return None

    interp = np.interp(grid, t, y)

    baseline = interp[grid <= 0.40]
    if len(baseline) < 4:
        return None

    centered = interp - float(np.median(baseline))
    return grid, centered


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sqrt(np.mean((a - b) ** 2)))


def cv(values):
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) < 2:
        return np.nan
    mean = float(np.mean(values))
    if abs(mean) <= 1e-9:
        return np.nan
    return float(np.std(values, ddof=1) / abs(mean))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    captures = []

    for pupil_path in sorted(args.directory.glob("*.pupil.json")):
        pupil = load_json(pupil_path)
        if pupil.get("schemaVersion") != "lucent-e002-pupil-v1":
            continue

        stem = stem_from_pupil(pupil_path)
        quality_path = args.directory / f"{stem}.quality.json"
        trace_path = args.directory / f"{stem}.trace.csv"

        quality = load_json(quality_path) if quality_path.exists() else None
        trace = read_trace(trace_path) if trace_path.exists() else None

        summary = pupil.get("summary") or {}
        dynamic = summary.get("dynamicResponse") or {}

        capture = {
            "stem": stem,
            "condition": pupil.get("condition") or summary.get("condition"),
            "participant": pupil.get("participantPseudonym"),
            "session": pupil.get("session"),
            "timingPass": timing_pass(pupil),
            "visibilityPass": offline_visibility_pass(quality),
            "pupilPass": pupil_pass(pupil),
            "validPupilRate": summary.get("validPupilRate"),
            "constrictionAmplitude": dynamic.get("constrictionAmplitude"),
            "timeToMinimumS": dynamic.get("timeToMinimumS"),
            "trace": trace,
        }
        captures.append(capture)

    if not captures:
        raise RuntimeError("No *.pupil.json captures found")

    timing_count = sum(c["timingPass"] for c in captures)
    visibility_count = sum(c["visibilityPass"] for c in captures)
    pupil_count = sum(c["pupilPass"] for c in captures)

    o1 = timing_count >= min(8, len(captures))
    o2 = (
        visibility_count >= min(8, len(captures))
        and pupil_count >= min(6, len(captures))
    )

    condition_stats = {}
    o3 = False

    for condition in ACTIVE:
        subset = [
            c
            for c in captures
            if c["condition"] == condition
            and c["timingPass"]
            and c["visibilityPass"]
            and c["pupilPass"]
        ]

        amplitudes = [
            float(c["constrictionAmplitude"])
            for c in subset
            if c["constrictionAmplitude"] is not None
        ]
        times = [
            float(c["timeToMinimumS"])
            for c in subset
            if c["timeToMinimumS"] is not None
        ]

        amplitude_cv = cv(amplitudes)
        time_cv = cv(times)

        condition_stats[condition] = {
            "usableCaptures": len(subset),
            "amplitudeCV": amplitude_cv,
            "timeToMinimumCV": time_cv,
        }

        if len(amplitudes) >= 3 and np.isfinite(amplitude_cv) and amplitude_cv <= 0.25:
            o3 = True

    traces = {
        condition: [
            c["trace"][1]
            for c in captures
            if c["condition"] == condition
            and c["trace"] is not None
            and c["timingPass"]
            and c["pupilPass"]
        ]
        for condition in ACTIVE
    }

    within_distances = []
    for condition in ACTIVE:
        for a, b in itertools.combinations(traces[condition], 2):
            within_distances.append(rmse(a, b))

    between_distances = [
        rmse(a, b)
        for a in traces["contiguous"]
        for b in traces["split"]
    ]

    if within_distances and between_distances:
        within_median = float(np.median(within_distances))
        between_median = float(np.median(between_distances))
        separation = (
            between_median / within_median
            if within_median > 1e-12
            else np.inf
        )
    else:
        within_median = None
        between_median = None
        separation = None

    o4 = (
        separation is not None
        and np.isfinite(separation)
        and separation > 1.25
        and len(traces["contiguous"]) >= 2
        and len(traces["split"]) >= 2
    )

    clears = bool(o1 and o2 and (o3 or o4))

    report = {
        "schemaVersion": "lucent-e002-aggregate-v1",
        "captures": len(captures),
        "gates": {
            "O1_timing": o1,
            "O2_observability": o2,
            "O3_repeatability": o3,
            "O4_temporal_distinguishability": o4,
        },
        "counts": {
            "timingPass": timing_count,
            "visibilityPass": visibility_count,
            "pupilPass": pupil_count,
        },
        "conditionStats": condition_stats,
        "traceSeparation": {
            "withinMedianRmse": within_median,
            "betweenMedianRmse": between_median,
            "separationRatio": separation,
            "contiguousTraces": len(traces["contiguous"]),
            "splitTraces": len(traces["split"]),
        },
        "E002_clears": clears,
        "claimBoundary": (
            "E002 clearance establishes instrumentation observability only, "
            "not fatigue or cognitive-state validity."
        ),
    }

    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
