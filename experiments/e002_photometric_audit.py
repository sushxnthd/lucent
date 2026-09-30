"""E002 photometric/geometry specificity audit.

This script implements the pre-data amendment in:
experiments/registrations/E002_PHOTOMETRIC_AUDIT.md

It does not change the original E002 O1-O4 engineering exit criterion.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path

import numpy as np


ACTIVE = ("contiguous", "split")
GRID = np.arange(0.0, 5.0001, 0.05)
BASELINE_END = 0.40
CHANNELS = (
    "pupilRatio",
    "faceMedianGray",
    "irisMedianGray",
    "irisRadiusPx",
    "interEyeDistancePx",
)


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


def pupil_pass(pupil: dict) -> bool:
    summary = pupil.get("summary") or {}
    rate = summary.get("validPupilRate")
    return rate is not None and float(rate) >= 0.60


def parse_float(value):
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if np.isfinite(out) else None


def read_trace(path: Path):
    rows = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            t = parse_float(raw.get("offsetS"))
            q = parse_float(raw.get("quality"))
            if t is None:
                continue

            row = {"offsetS": t, "quality": q}
            for channel in CHANNELS:
                row[channel] = parse_float(raw.get(channel))
            rows.append(row)

    rows.sort(key=lambda x: x["offsetS"])
    return rows


def interpolate_channel(rows, channel, require_pupil_quality=False):
    points = []
    for row in rows:
        value = row.get(channel)
        if value is None:
            continue
        if require_pupil_quality:
            quality = row.get("quality")
            if quality is None or quality < 0.45:
                continue
        points.append((row["offsetS"], value))

    if len(points) < 20:
        return None

    t = np.asarray([x[0] for x in points], dtype=float)
    y = np.asarray([x[1] for x in points], dtype=float)

    order = np.argsort(t)
    t = t[order]
    y = y[order]

    t, unique = np.unique(t, return_index=True)
    y = y[unique]

    if t[0] > 0.15 or t[-1] < 4.85:
        return None

    interp = np.interp(GRID, t, y)
    baseline = interp[GRID <= BASELINE_END]
    if len(baseline) < 4:
        return None

    return interp - float(np.median(baseline))


def rmse(a, b):
    return float(np.sqrt(np.mean((a - b) ** 2)))


def separation_ratio(captures, channel):
    traces = {
        condition: [
            c["channels"][channel]
            for c in captures
            if c["condition"] == condition
            and c["channels"].get(channel) is not None
        ]
        for condition in ACTIVE
    }

    within = []
    for condition in ACTIVE:
        within.extend(
            rmse(a, b)
            for a, b in itertools.combinations(traces[condition], 2)
        )

    between = [
        rmse(a, b)
        for a in traces["contiguous"]
        for b in traces["split"]
    ]

    if not within or not between:
        return {
            "separationRatio": None,
            "withinMedianRmse": None,
            "betweenMedianRmse": None,
            "contiguousTraces": len(traces["contiguous"]),
            "splitTraces": len(traces["split"]),
        }

    within_median = float(np.median(within))
    between_median = float(np.median(between))

    ratio = (
        between_median / within_median
        if within_median > 1e-12
        else np.inf
    )

    return {
        "separationRatio": float(ratio),
        "withinMedianRmse": within_median,
        "betweenMedianRmse": between_median,
        "contiguousTraces": len(traces["contiguous"]),
        "splitTraces": len(traces["split"]),
    }


def rankdata(values):
    values = np.asarray(values, dtype=float)
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and values[order[j]] == values[order[i]]:
            j += 1
        rank = 0.5 * (i + j - 1) + 1.0
        ranks[order[i:j]] = rank
        i = j
    return ranks


def spearman(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b)
    a = a[ok]
    b = b[ok]
    if len(a) < 8:
        return None
    ra = rankdata(a)
    rb = rankdata(b)
    if np.std(ra) <= 1e-12 or np.std(rb) <= 1e-12:
        return None
    return float(np.corrcoef(ra, rb)[0, 1])


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
        if (pupil.get("condition") or "") not in ACTIVE:
            continue
        if not timing_pass(pupil) or not pupil_pass(pupil):
            continue

        stem = stem_from_pupil(pupil_path)
        trace_path = args.directory / f"{stem}.trace.csv"
        if not trace_path.exists():
            continue

        rows = read_trace(trace_path)
        channels = {}
        for channel in CHANNELS:
            channels[channel] = interpolate_channel(
                rows,
                channel,
                require_pupil_quality=(channel == "pupilRatio"),
            )

        pupil_trace = channels["pupilRatio"]
        face_trace = channels["faceMedianGray"]
        iris_brightness = channels["irisMedianGray"]

        pupil_face_rho = (
            spearman(pupil_trace, face_trace)
            if pupil_trace is not None and face_trace is not None
            else None
        )
        pupil_iris_rho = (
            spearman(pupil_trace, iris_brightness)
            if pupil_trace is not None and iris_brightness is not None
            else None
        )

        captures.append(
            {
                "stem": stem,
                "condition": pupil.get("condition"),
                "channels": channels,
                "pupilFaceSpearman": pupil_face_rho,
                "pupilIrisBrightnessSpearman": pupil_iris_rho,
            }
        )

    if not captures:
        raise RuntimeError(
            "No usable active captures with trace controls were found."
        )

    separation = {
        channel: separation_ratio(captures, channel)
        for channel in CHANNELS
    }

    pupil_s = separation["pupilRatio"]["separationRatio"]
    face_s = separation["faceMedianGray"]["separationRatio"]
    iris_brightness_s = separation["irisMedianGray"]["separationRatio"]
    iris_radius_s = separation["irisRadiusPx"]["separationRatio"]
    inter_eye_s = separation["interEyeDistancePx"]["separationRatio"]

    iris_rhos = [
        abs(c["pupilIrisBrightnessSpearman"])
        for c in captures
        if c["pupilIrisBrightnessSpearman"] is not None
    ]
    face_rhos = [
        abs(c["pupilFaceSpearman"])
        for c in captures
        if c["pupilFaceSpearman"] is not None
    ]

    median_abs_iris_rho = (
        float(np.median(iris_rhos)) if iris_rhos else None
    )
    median_abs_face_rho = (
        float(np.median(face_rhos)) if face_rhos else None
    )

    photometric_reasons = []
    geometry_reasons = []

    if pupil_s is not None:
        if face_s is not None and face_s >= pupil_s:
            photometric_reasons.append(
                "face-brightness condition separation >= pupil separation"
            )
        if (
            iris_brightness_s is not None
            and iris_brightness_s >= pupil_s
        ):
            photometric_reasons.append(
                "iris-brightness condition separation >= pupil separation"
            )
        if (
            median_abs_iris_rho is not None
            and median_abs_iris_rho >= 0.80
        ):
            photometric_reasons.append(
                "median |pupil vs iris-brightness Spearman| >= 0.80"
            )

        if iris_radius_s is not None and iris_radius_s >= pupil_s:
            geometry_reasons.append(
                "iris-radius condition separation >= pupil separation"
            )
        if inter_eye_s is not None and inter_eye_s >= pupil_s:
            geometry_reasons.append(
                "inter-eye condition separation >= pupil separation"
            )

    report = {
        "schemaVersion": "lucent-e002-photometric-audit-v1",
        "usableActiveCaptures": len(captures),
        "channelSeparation": separation,
        "coupling": {
            "medianAbsPupilFaceSpearman": median_abs_face_rho,
            "medianAbsPupilIrisBrightnessSpearman": median_abs_iris_rho,
        },
        "flags": {
            "photometric_confounded": bool(photometric_reasons),
            "geometry_confounded": bool(geometry_reasons),
            "photometricReasons": photometric_reasons,
            "geometryReasons": geometry_reasons,
        },
        "biologicalSpecificitySupported": bool(
            pupil_s is not None
            and pupil_s > 1.25
            and not photometric_reasons
            and not geometry_reasons
        ),
        "claimBoundary": (
            "This audit checks same-video photometric and geometry negative "
            "controls only. It cannot rule out all RGB-camera confounds."
        ),
    }

    args.output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
