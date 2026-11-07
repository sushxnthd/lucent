"""E002-460: exact dark-shutter-gap reachability from LINEAR anatomical aperture means.

This is conditional mathematics, NOT a validated physical blink detector.
Inputs are millimetres and milliseconds. Velocity caps are assumed, not estimated here.
"""
from __future__ import annotations
import json
import math
import sys

NUISANCES = ("geometry", "brightness", "missingness", "blur", "gaze",
             "glasses", "sampling", "clock", "rolling_shutter")

def evaluate(record: dict) -> dict:
    """Evaluate a single frozen E002-460 research-only record.

    EXCLUDED_CONDITIONALLY means no crossing strictly inside the shutter-dark gap
    under the stipulated linear exposure-mean model and assumed speed bounds.
    POSSIBLE_CONDITIONALLY includes an explicit piecewise-affine witness.
    Every uncertain or uncalibrated input abstains. Never returns physical certification.
    """
    abstain = lambda why: {"decision": "ABSTAIN_UNCALIBRATED", "reason": why,
                           "physical_certification": False}
    if not isinstance(record, dict):
        return abstain("INVALID_RECORD")
    if record.get("observable") != "LINEAR_ANATOMICAL_APERTURE_MEAN_MM":
        return abstain("UNSUPPORTED_OBSERVABLE")
    if record.get("linear_mean_calibrated") is not True:
        return abstain("LINEAR_MEAN_NOT_CALIBRATED")
    if record.get("velocity_caps_assumed_for_research") is not True:
        return abstain("CAP_PROVENANCE_UNDECLARED")
    flags = record.get("nuisance")
    if not isinstance(flags, dict) or any(flags.get(k) != "CLEAR" for k in NUISANCES):
        return abstain("NUISANCE_UNRESOLVED")
    try:
        m0 = float(record["mean0_mm"])
        m1 = float(record["mean1_mm"])
        c = float(record["closure_mm"])
        C = float(record["closing_mm_s"]) / 1000.0
        O = float(record["opening_mm_s"]) / 1000.0
        x0, x1 = record["exposures"]
        l0, r0, mu0 = (float(x0[k]) for k in
                        ("support_start_ms", "support_end_ms", "centroid_ms"))
        l1, r1, mu1 = (float(x1[k]) for k in
                        ("support_start_ms", "support_end_ms", "centroid_ms"))
    except (KeyError, TypeError, ValueError, OverflowError):
        return abstain("INVALID_NUMERIC_INPUT")
    values = (m0,m1,c,C,O,l0,r0,mu0,l1,r1,mu1)
    if not all(math.isfinite(v) for v in values):
        return abstain("NONFINITE_INPUT")
    if c < 0 or m0 <= c or m1 <= c or C <= 0 or O <= 0:
        return abstain("INVALID_APERTURE_OR_CAP")
    if not (l0 <= mu0 <= r0 < l1 <= mu1 <= r1):
        return abstain("SHUTTER_SUPPORT_OVERLAP_OR_BAD_CENTROID")
    # No approximation to unknown kernel: its exact first moment must be certified.
    if any(x.get("kernel_normalized") is not True or
           x.get("centroid_authenticated") is not True or
           x.get("support_authenticated") is not True or
           x.get("clock_uncertainty_ms") != 0 for x in (x0, x1)):
        return abstain("KERNEL_OR_CLOCK_UNAUTHENTICATED")
    earliest = max(r0, mu0 + (m0-c)/C)
    latest = min(l1, mu1 - (m1-c)/O)
    # Floating equality is a boundary, never sufficient for a safety exclusion.
    eps = 1e-10 * max(1.0, abs(earliest), abs(latest))
    base = {"physical_certification": False, "earliest_ms": earliest,
            "latest_ms": latest, "dark_gap_ms": l1-r0,
            "centroid_gap_ms": mu1-mu0,
            "critical_centroid_gap_ms": (m0-c)/C+(m1-c)/O}
    if earliest > latest + eps or (earliest >= l1 and latest <= r0):
        return dict(base, decision="EXCLUDED_CONDITIONALLY",
                    reason="NO_DARK_GAP_CROSSING_UNDER_ASSUMPTIONS")
    # On equality, do not exclude; support-boundary equality is inconclusive.
    if latest - earliest <= eps:
        return dict(base, decision="NOT_EXCLUDED_BOUNDARY",
                    reason="NUMERICAL_OR_SUPPORT_BOUNDARY")
    tau = (earliest + latest)/2
    if not (r0 < tau < l1):
        return dict(base, decision="NOT_EXCLUDED_BOUNDARY",
                    reason="CROSSING_TOUCHES_SHUTTER_SUPPORT")
    alpha = (m0-c)/(C*(tau-mu0))
    beta = (m1-c)/(O*(mu1-tau))
    if not (-eps <= alpha <= 1+eps and -eps <= beta <= 1+eps):
        return abstain("WITNESS_CONSTRUCTION_INCONSISTENT")
    return dict(base, decision="POSSIBLE_CONDITIONALLY",
                reason="EXPLICIT_DARK_GAP_WITNESS",
                witness={"tau_ms":tau, "left_slope_mm_ms":-alpha*C,
                         "right_slope_mm_ms":beta*O, "alpha":alpha,"beta":beta})

def example(delta_ms=1000/240, shutter_ms=2):
    return {
        "observable": "LINEAR_ANATOMICAL_APERTURE_MEAN_MM",
        "linear_mean_calibrated": True,
        "velocity_caps_assumed_for_research": True,
        "mean0_mm":3.0, "mean1_mm":3.0, "closure_mm":2.0,
        "closing_mm_s":567.103928, "opening_mm_s":274.616337,
        "nuisance": {k:"CLEAR" for k in NUISANCES},
        "exposures": [
            {"support_start_ms":-shutter_ms/2, "support_end_ms":shutter_ms/2,
             "centroid_ms":0, "kernel_normalized":True,
             "centroid_authenticated":True,"support_authenticated":True,
             "clock_uncertainty_ms":0},
            {"support_start_ms":delta_ms-shutter_ms/2,
             "support_end_ms":delta_ms+shutter_ms/2,
             "centroid_ms":delta_ms, "kernel_normalized":True,
             "centroid_authenticated":True,"support_authenticated":True,
             "clock_uncertainty_ms":0},
        ],
    }

if __name__ == "__main__":
    if len(sys.argv)==2 and sys.argv[1]=="--examples":
        for gap, width in ((1000/240,2),(1000/240,2.3),(6,2),(6,5)):
            print(json.dumps({"gap_ms":gap,"shutter_ms":width,
                              "result":evaluate(example(gap,width))},sort_keys=True))
    elif len(sys.argv)==1:
        print(json.dumps(evaluate(json.load(sys.stdin)),sort_keys=True))
    else:
        raise SystemExit("usage: python e002_460_exposure_centroid.py [--examples] < input.json")
