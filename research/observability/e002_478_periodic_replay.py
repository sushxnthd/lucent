"""E002-478: necessary two-period shutter-response repeatability test.

A passing synthetic/model test is NOT a physical shutter certificate.
"""
from __future__ import annotations
import argparse
import bisect
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

from e002_477_optical_intake import evaluate as intake_evaluate

BLOCKED = {"physical_shutter_support_authenticated": False,
           "physical_release_authorized": False,
           "product_claim": "ABSTAIN_UNCALIBRATED"}

def indeterminate(reason):
    return {"periodicity_status": "INDETERMINATE", "reason": reason, **BLOCKED}

def evaluate_periodicity(manifest_path, camera_path, clock_path, raw_path, *,
                         verified_period_ms=None, period_error_bound_ms=None,
                         response_slope_bound_per_ms=None, contrast_error_bound=None,
                         interperiod_drift_bound=None, pulse_phase_error_bound_ms=None,
                         minimum_detectable_contrast=None):
    """Test only a necessary condition; external budgets must be independently justified."""
    intake = intake_evaluate(manifest_path, camera_path, clock_path, raw_path)
    if intake["qa_status"] != "PASS_INTAKE_ONLY":
        return {"periodicity_status": "REJECT_INTAKE", "reason": intake.get("reason"), **BLOCKED}
    budgets = (verified_period_ms, period_error_bound_ms, response_slope_bound_per_ms,
               contrast_error_bound, interperiod_drift_bound, pulse_phase_error_bound_ms,
               minimum_detectable_contrast)
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in budgets):
        return indeterminate("INDEPENDENT_BUDGETS_REQUIRED")
    T, p, L, b, d, u, floor = budgets
    if T <= 0 or p < 0 or L <= 0 or b < 0 or d < 0 or u < 0 or floor <= 0:
        return indeterminate("INVALID_INDEPENDENT_BUDGET")
    try:
        manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        step = float(manifest["phase_step_ms"])
        if abs(float(manifest["frame_period_ms"]) - T) > p:
            return indeterminate("FRAME_PERIOD_NOT_AUTHENTICATED")
        if int(manifest["scan_periods"]) < 2:
            return indeterminate("INSUFFICIENT_PERIODS")
        camera = defaultdict(list)
        clock = defaultdict(list)
        with Path(camera_path).open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                camera[(r["row_stratum"], int(r["phase_index"]))].append(
                    float(r["response"]) - float(r["dark_reference"]))
        with Path(clock_path).open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                clock[(r["row_stratum"], int(r["phase_index"]))].append(
                    float(r["pulse_start_ms"]))
        by_row = defaultdict(list)
        for key, values in camera.items():
            if key not in clock:
                return indeterminate("CLOCK_PAIR_MISSING")
            by_row[key[0]].append((statistics.median(clock[key]), statistics.median(values)))
        if not by_row:
            return indeterminate("NO_ROWS")
        peak = max((v for rows in by_row.values() for _, v in rows), default=0.0)
        if peak < floor:
            return indeterminate("INSUFFICIENT_OPTICAL_RESPONSE")
        violations = []
        checked = 0
        max_ratio = 0.0
        for row, entries in sorted(by_row.items()):
            entries.sort()
            first = [(t, c) for t, c in entries if 0 <= t < T]
            second = [(t, c) for t, c in entries if T <= t < 2 * T + step]
            if not first or not second:
                return indeterminate("PERIOD_COVERAGE_MISSING")
            second_times = [t for t, _ in second]
            row_checked = 0
            for t, c in first:
                target = t + T
                j = bisect.bisect_left(second_times, target)
                candidates = [k for k in (j - 1, j) if 0 <= k < len(second)]
                if not candidates:
                    continue
                k = min(candidates, key=lambda k: abs(second[k][0] - target))
                t2, c2 = second[k]
                mismatch = abs(t2 - target)
                if mismatch > step / 2 + 2 * u + p + 1e-10:
                    continue
                allowed = L * (mismatch + 2 * u + p) + 2 * b + d
                discrepancy = abs(c2 - c)
                checked += 1
                row_checked += 1
                max_ratio = max(max_ratio, discrepancy / allowed if allowed else (math.inf if discrepancy else 0))
                if discrepancy > allowed + 1e-10:
                    violations.append({"row": row, "phase_ms": round(t, 6),
                                       "difference": round(discrepancy, 8),
                                       "allowed": round(allowed, 8)})
            if row_checked < 10:
                return indeterminate("INSUFFICIENT_MATCHED_PHASES")
        return {"periodicity_status": ("REJECT_STATIONARY_PERIODIC_MODEL" if violations
                                        else "CONSISTENT_WITH_PERIODICITY_ONLY"),
                "matched_phase_pairs": checked, "violations": len(violations),
                "first_violation": violations[0] if violations else None,
                "maximum_discrepancy_to_budget_ratio": round(max_ratio, 6),
                "instrument_budgets_authenticated": False, **BLOCKED}
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return indeterminate("SOURCE_PARSE_ERROR")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ("manifest", "camera", "clock", "raw"):
        ap.add_argument(name)
    for name in ("verified_period_ms", "period_error_bound_ms", "response_slope_bound_per_ms",
                 "contrast_error_bound", "interperiod_drift_bound", "pulse_phase_error_bound_ms",
                 "minimum_detectable_contrast"):
        ap.add_argument("--" + name.replace("_", "-"), type=float, required=True)
    a = vars(ap.parse_args())
    paths = [a.pop(k) for k in ("manifest", "camera", "clock", "raw")]
    result = evaluate_periodicity(*paths, **a)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["periodicity_status"] == "REJECT_STATIONARY_PERIODIC_MODEL" else (
        0 if result["periodicity_status"] == "CONSISTENT_WITH_PERIODICITY_ONLY" else 3)

if __name__ == "__main__":
    raise SystemExit(main())
