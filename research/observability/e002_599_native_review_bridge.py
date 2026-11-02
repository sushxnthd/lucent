#!/usr/bin/env python3
"""E002-599: fail-closed native LPW two-rater bridge for E002-598 exports.

Development index-witness instrument only. No physical shutter/velocity or
reviewer independence verification. Do not upload private ratings or imagery.
"""
import argparse
import json
import math
from collections import Counter

PHASES = ((0, 3, 6, 10, 13, 16),
          (1, 4, 7, 11, 14, 17),
          (2, 5, 8, 12, 15, 18))
CLIPS = {f"clip_{i:04d}" for i in range(10)}
FLAGS = {"UNREVIEWED", "OCCLUSION", "BLUR", "GAZE", "GLASSES",
         "GEOMETRY", "BRIGHTNESS", "MISSING", "OTHER"}
THRESHOLD = 0.20
CORE = {"frame", "upper_y", "lower_y", "iris_diameter", "uncertainty_px", "flags"}
MEASURED = CORE | {"measurement_x"}


def finite(x):
    return type(x) in (float, int) and math.isfinite(x)


def validate_export(data, rater):
    if (not isinstance(data, dict) or data.get("experiment") != "E002-574"
            or data.get("rater") != rater or "arm" in data
            or not isinstance(data.get("clips"), dict)
            or set(data["clips"]) != CLIPS):
        raise ValueError("INVALID_NATIVE_REVIEW_EXPORT")
    for rows in data["clips"].values():
        if not isinstance(rows, list) or len(rows) != 19:
            raise ValueError("INVALID_FRAME_COUNT")
        for i, f in enumerate(rows):
            if not isinstance(f, dict) or f.get("frame") != i:
                raise ValueError("INVALID_FRAME_INDEX")
            flags = f.get("flags")
            if (not isinstance(flags, list) or len(flags) > 1
                    or any(v not in FLAGS for v in flags)):
                raise ValueError("INVALID_NUISANCE_FLAGS")
            if flags:
                if set(f) != CORE or any(f.get(k) is not None for k in
                    ("upper_y", "lower_y", "iris_diameter", "uncertainty_px")):
                    raise ValueError("INVALID_FLAGGED_ROW")
            else:
                if set(f) != MEASURED or f.get("iris_diameter") is not None:
                    raise ValueError("INVALID_MEASURED_ROW")
                u, l, e, x = (f[k] for k in
                    ("upper_y", "lower_y", "uncertainty_px", "measurement_x"))
                if (not all(finite(v) for v in (u, l, e, x))
                        or not 0 <= u < l <= 480 or not 0.5 <= e <= 50
                        or not 0 <= x <= 639):
                    raise ValueError("INVALID_LANDMARK_COORDINATES")


def calibration_budgets(cal):
    """External calibration assertions are not verified by this function."""
    if not isinstance(cal, dict) or (cal.get("experiment") != "E002-599"
            or cal.get("independently_validated") is not True
            or cal.get("frozen_before_review") is not True
            or not isinstance(cal.get("external_reference_id"), str)
            or not 8 <= len(cal["external_reference_id"]) <= 160
            or not isinstance(cal.get("clips"), list)):
        return {}
    budgets = {}
    for row in cal["clips"]:
        if not isinstance(row, dict):
            raise ValueError("INVALID_CALIBRATION_ROW")
        clip = row.get("blind_clip")
        d = row.get("iris_diameter_px")
        delta = row.get("iris_error_px")
        xref = row.get("x_ref_px")
        tol = row.get("registration_tolerance_px")
        if (clip not in CLIPS or clip in budgets
                or not all(finite(v) for v in (d, delta, xref, tol))
                or not 0 < delta < d <= 480 or not 0 <= xref <= 639
                or not 0 < tol <= 1):
            raise ValueError("INVALID_CALIBRATION_BUDGET")
        budgets[clip] = (d, delta, xref, tol)
    return budgets


def classify(a, b, budget):
    if budget is None or a["flags"] or b["flags"]:
        return "UNCERTAIN"
    d, delta, xref, tol = budget
    xa, xb = a["measurement_x"], b["measurement_x"]
    if abs(xa - xb) > 1:
        return "DISAGREEMENT"
    if abs(xa - xref) > tol or abs(xb - xref) > tol:
        return "UNCERTAIN"
    intervals = []
    for f in (a, b):
        u, l, e = f["upper_y"], f["lower_y"], f["uncertainty_px"]
        intervals.append((max(0.0, l - u - 2*e)/(d+delta),
                          max(0.0, l - u + 2*e)/(d-delta)))
    (al, ah), (bl, bh) = intervals
    if max(al, bl) > min(ah, bh):
        return "DISAGREEMENT"
    if ah <= THRESHOLD and bh <= THRESHOLD:
        return "CLOSED"
    if al > THRESHOLD and bl > THRESHOLD:
        return "OPEN"
    return "UNCERTAIN"


def analyze(rater_a, rater_b, calibration=None):
    validate_export(rater_a, "A")
    validate_export(rater_b, "B")
    budgets = calibration_budgets(calibration)
    counts = Counter()
    witnesses = [0, 0, 0]
    eligible = [0, 0, 0]
    windows_positive = 0
    for clip in sorted(CLIPS):
        states = []
        for a, b in zip(rater_a["clips"][clip], rater_b["clips"][clip]):
            state = classify(a, b, budgets.get(clip))
            states.append(state)
            counts[state] += 1
        positive = False
        for p, indices in enumerate(PHASES):
            for left, right in zip(indices, indices[1:]):
                if states[left] == states[right] == "OPEN":
                    eligible[p] += 1
                    if "CLOSED" in states[left+1:right]:
                        witnesses[p] += 1
                        positive = True
        windows_positive += int(positive)
    return {
        "experiment": "E002-599",
        "evidence_tier": "CONDITIONAL_DEVELOPMENT_NATIVE_INDEX_ONLY",
        "native_frames": 190, "development_windows": 10,
        "frame_states": {s: counts[s] for s in
            ("OPEN", "CLOSED", "UNCERTAIN", "DISAGREEMENT")},
        "phase_eligible_open_endpoint_pairs": eligible,
        "phase_positive_alias_pairs": witnesses,
        "windows_with_any_positive_alias": windows_positive,
        "independent_calibration_provenance_verified": False,
        "source_authenticity_verified_by_this_tool": False,
        "rater_independence_verified_by_this_tool": False,
        "three_phases_exhaust_continuous_phase": False,
        "zero_witness_excludes_hidden_closure": False,
        "physical_shutter_validated": False,
        "velocity_ceiling_certified": False,
        "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rater-a", required=True)
    parser.add_argument("--rater-b", required=True)
    parser.add_argument("--calibration")
    args = parser.parse_args()
    try:
        def read(path):
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        out = analyze(read(args.rater_a), read(args.rater_b),
                      read(args.calibration) if args.calibration else None)
        print(json.dumps(out, sort_keys=True))
    except (ValueError, TypeError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"experiment": "E002-599", "status": "ABSTAIN",
                          "error_type": type(exc).__name__,
                          "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
