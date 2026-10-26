#!/usr/bin/env python3
"""E002-456: fail-closed, research-only prospective anatomical-reference challenge.

All input claims are declared provenance, NOT authenticated by this evaluator.
No empirical sample maximum can establish a deterministic physiological cap.
No real human data are bundled. Outputs omit participant IDs and raw measurements.
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path

NUISANCES = ("geometry", "brightness", "missingness", "blur", "gaze",
             "glasses", "sampling", "clock", "rolling_shutter")
CALIBRATIONS = ("geometry_calibration_id", "clock_calibration_id",
                "exposure_calibration_id", "reference_annotation_id")
ABSTAIN = "ABSTAIN_UNCALIBRATED"


def number(value, *, nonnegative=True):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("numeric scalar required")
    x = float(value)
    if not math.isfinite(x) or (nonnegative and x < 0):
        raise ValueError("nonfinite or negative scalar")
    return x


def pair(case, key):
    v = case.get(key)
    if not isinstance(v, list) or len(v) != 2:
        raise ValueError("two endpoints required: " + key)
    return number(v[0]), number(v[1])


def abstain(reason):
    return {"decision": "ABSTAIN", "reason": reason,
            "reference": "NOT_EVALUATED", "joint_falsification": False}


def evaluate_interval(case):
    """A counterexample falsifies the *joint* measurement and bound assumptions."""
    if not isinstance(case, dict):
        return abstain("INVALID_SCHEMA")
    try:
        nuisance = case["nuisance"]
        if not isinstance(nuisance, dict) or any(
            nuisance.get(k) != "PASS" for k in NUISANCES
        ):
            return abstain("NUISANCE_NOT_CLEARED")
        instrument = case["instrument"]
        if not isinstance(instrument, dict) or any(
            not isinstance(instrument.get(k), str) or not instrument[k].strip()
            for k in CALIBRATIONS
        ) or instrument.get("independent_reference") is not True:
            return abstain("INDEPENDENT_CALIBRATION_NOT_DECLARED")
        velocity = case["velocity"]
        if not isinstance(velocity, dict) or velocity.get("provenance") not in (
            "ILLUSTRATIVE", "EXTERNAL_HARD_BOUND_DECLARED"
        ):
            return abstain("VELOCITY_CAP_PROVENANCE_INVALID")
        V = number(velocity["limit_mm_s"])
        if V <= 0:
            return abstain("INVALID_VELOCITY_CAP")
        c = number(case["closure_threshold_mm"])
        a0, a1 = pair(case, "endpoint_aperture_mm")
        u0, u1 = pair(case, "endpoint_uncertainty_mm")
        t0, t1 = pair(case, "endpoint_time_ms")
        if t1 <= t0:
            return abstain("INVALID_ENDPOINT_TIME")
        shutter = case["shutter"]
        if not isinstance(shutter, dict):
            return abstain("UNKNOWN_SHUTTER")
        kernel = shutter.get("kernel")
        if kernel not in ("uniform_symmetric", "support_symmetric"):
            return abstain("UNKNOWN_SHUTTER")
        exposure = number(shutter["exposure_ms"])
        clock_error = number(shutter["clock_error_ms"])
        reference_exposure = number(shutter["reference_exposure_ms"])
        reference_clock_error = number(shutter["reference_clock_error_ms"])
        if exposure > t1 - t0:
            return abstain("OVERLAPPING_EXPOSURES")
        if clock_error * 2 >= t1 - t0:
            return abstain("CLOCK_UNCERTAINTY_TOO_LARGE")
        # A shutter-aware dark-gap witness requires a nonempty gap even
        # under the worst permitted ordinary-camera center-time error.
        if exposure + 2 * clock_error >= t1 - t0:
            return abstain("NO_GUARANTEED_DARK_GAP")
        # The entire reference exposure, with both independent clock
        # uncertainties, must fit strictly between ordinary exposures.
        if (exposure + reference_exposure +
                2 * (clock_error + reference_clock_error) >= t1 - t0):
            return abstain("REFERENCE_TIME_SUPPORT_TOO_WIDE")
        shutter_error = V * exposure / 1000.0 * (
            0.25 if kernel == "uniform_symmetric" else 0.5
        )
        max_gap_s = (t1 - t0 + 2 * clock_error) / 1000.0
        if abs(a1 - a0) > V * max_gap_s + u0 + u1 + 2 * shutter_error + 1e-12:
            return abstain("MODEL_INCONSISTENT_ENDPOINTS")
        L = max(0.0, (a0 - u0 - shutter_error +
                      a1 - u1 - shutter_error - V * max_gap_s) / 2)
        decision = "EXCLUDED_CONDITIONALLY" if L > c else "NOT_EXCLUDED"
        references = case["reference"]
        if not isinstance(references, list):
            return abstain("REFERENCE_SCHEMA_INVALID")
        witnessed = False
        incomplete = len(references) == 0
        uncertain = False
        for r in references:
            if not isinstance(r, dict):
                return abstain("REFERENCE_SCHEMA_INVALID")
            rt = number(r["time_ms"])
            ra = number(r["aperture_mm"])
            ru = number(r["uncertainty_mm"])
            if not t0 < rt < t1:
                return abstain("REFERENCE_NOT_INTERIOR")
            if r.get("quality") != "PASS":
                incomplete = True
                continue
            # Require full reference support inside the guaranteed
            # UNEXPOSED gap, not merely between ordinary frame centers.
            guard = (exposure / 2 + clock_error + reference_clock_error +
                     reference_exposure / 2)
            if rt <= t0 + guard or rt >= t1 - guard:
                incomplete = True
                continue
            if ra + ru <= c:
                witnessed = True
            elif ra - ru <= c:
                uncertain = True
        reference = ("WITNESSED_CROSSING" if witnessed else
                     "REFERENCE_INCOMPLETE" if incomplete else
                     "REFERENCE_INDETERMINATE" if uncertain else
                     "NO_WITNESSED_CROSSING")
        falsified = decision == "EXCLUDED_CONDITIONALLY" and witnessed
        return {"decision": decision, "reason": "NONE", "reference": reference,
                "joint_falsification": falsified,
                "lower_envelope_mm": L,
                "velocity_cap_tier": velocity["provenance"]}
    except (KeyError, TypeError, ValueError, OverflowError):
        return abstain("INVALID_OR_MISSING_MEASUREMENT")


def evaluate_dataset(payload):
    """Aggregate by declared split, never emit case IDs, landmarks or video."""
    if not isinstance(payload, dict) or payload.get("schema_version") != "E002-456-v1":
        raise ValueError("unsupported schema")
    cases = payload.get("intervals")
    if not isinstance(cases, list) or not cases:
        raise ValueError("nonempty intervals required")
    subjects = {"development": set(), "holdout": set()}
    seen_ids = set()
    counts = {"development": Counter(), "holdout": Counter()}
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("invalid interval record")
        split = case.get("split")
        subject = case.get("participant_id")
        ident = case.get("interval_id")
        if split not in subjects or not isinstance(subject, str) or not subject or (
            not isinstance(ident, str) or not ident or ident in seen_ids
        ):
            raise ValueError("invalid split, participant or duplicate interval")
        seen_ids.add(ident)
        subjects[split].add(subject)
        result = evaluate_interval(case)
        counts[split]["intervals"] += 1
        counts[split][result["decision"]] += 1
        counts[split][result["reference"]] += 1
        if result["joint_falsification"]:
            counts[split]["FALSIFIED_JOINT_ASSUMPTIONS"] += 1
    if subjects["development"] & subjects["holdout"]:
        raise ValueError("participant leakage across development/holdout")
    return {
        "experiment": "E002-456",
        "evidence_tier": "RESEARCH_CONDITIONAL_ONLY",
        "counts": {s: {"participants": len(subjects[s]),
                       **dict(sorted(counts[s].items()))} for s in subjects},
        "physical_release_authorized": False,
        "product_claim": ABSTAIN,
        "no_witness_does_not_establish_no_closure": True,
        "external_hard_bound_verified_by_this_program": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    result = evaluate_dataset(json.loads(a.input.read_text(encoding="utf-8")))
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True,
                                   allow_nan=False) + "\n", encoding="utf-8")
    print("E002-456 aggregate written; physical release remains blocked")


if __name__ == "__main__":
    main()
