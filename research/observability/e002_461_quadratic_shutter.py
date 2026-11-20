"""E002-461: synthetic quadratic sensor, uniform shutter, conditional dark-gap veto.

This does not calibrate a real RGB camera or validate a physiological speed cap.
For a nonnegative L-Lipschitz aperture a(T), E[a]^2 = E[a^2]-Var(a)
and Var(a) <= L^2 Var(T). All units: mm, mm^2, ms, mm/s.
"""
from __future__ import annotations

import json
import math
import sys

NUISANCES = ("geometry", "brightness", "missingness", "blur", "gaze",
             "glasses", "sampling", "clock", "rolling_shutter")


def example(alpha=0.99, gap_ms=1000 / 240, width_ms=2.3):
    """Exact affine closure witness; values are SYNTHETIC, not observed."""
    c = 2.0
    C = 567.103928 / 1000
    O = 274.616337 / 1000
    tau = gap_ms / 2
    m0 = c + alpha * C * tau
    m1 = c + alpha * O * (gap_ms - tau)
    q0 = m0 * m0 + (alpha * C * width_ms) ** 2 / 12
    q1 = m1 * m1 + (alpha * O * width_ms) ** 2 / 12
    return {
        "observable": "CALIBRATED_QUADRATIC_APERTURE_SHUTTER_MEAN_MM2",
        "transfer_calibrated": True,
        "uniform_kernel_calibrated": True,
        "velocity_caps_assumed_for_research": True,
        "synthetic_uncertainty_authenticated": True,
        "q0_mm2": q0, "q1_mm2": q1,
        "uncertainty0_mm2": 0.0, "uncertainty1_mm2": 0.0,
        "closure_mm": c, "closing_mm_s": 1000 * C,
        "opening_mm_s": 1000 * O,
        "nuisance": {k: "CLEAR" for k in NUISANCES},
        "exposures": [
            {"support_start_ms": -width_ms / 2,
             "support_end_ms": width_ms / 2, "centroid_ms": 0.0,
             "kernel_normalized": True, "centroid_authenticated": True,
             "support_authenticated": True, "clock_uncertainty_ms": 0},
            {"support_start_ms": gap_ms - width_ms / 2,
             "support_end_ms": gap_ms + width_ms / 2,
             "centroid_ms": gap_ms, "kernel_normalized": True,
             "centroid_authenticated": True, "support_authenticated": True,
             "clock_uncertainty_ms": 0},
        ],
        "synthetic_witness_tau_ms": tau,
        "synthetic_witness_alpha": alpha,
    }


def evaluate(record):
    """Conservative exclusion, NEVER a positive possibility or physical certificate."""
    def abstain(reason):
        return {"decision": "ABSTAIN_UNCALIBRATED", "reason": reason,
                "physical_certification": False}
    if not isinstance(record, dict):
        return abstain("INVALID_RECORD")
    if record.get("observable") != "CALIBRATED_QUADRATIC_APERTURE_SHUTTER_MEAN_MM2":
        return abstain("UNSUPPORTED_OBSERVABLE")
    if record.get("transfer_calibrated") is not True or record.get("uniform_kernel_calibrated") is not True:
        return abstain("TRANSFER_OR_KERNEL_UNCALIBRATED")
    if record.get("velocity_caps_assumed_for_research") is not True:
        return abstain("CAP_PROVENANCE_UNDECLARED")
    if record.get("synthetic_uncertainty_authenticated") is not True:
        return abstain("UNCERTAINTY_UNAUTHENTICATED")
    flags = record.get("nuisance")
    if not isinstance(flags, dict) or any(flags.get(k) != "CLEAR" for k in NUISANCES):
        return abstain("NUISANCE_UNRESOLVED")
    try:
        q0, q1 = float(record["q0_mm2"]), float(record["q1_mm2"])
        u0, u1 = float(record["uncertainty0_mm2"]), float(record["uncertainty1_mm2"])
        c = float(record["closure_mm"])
        C = float(record["closing_mm_s"]) / 1000
        O = float(record["opening_mm_s"]) / 1000
        x0, x1 = record["exposures"]
        l0, r0, mu0 = (float(x0[k]) for k in
                       ("support_start_ms", "support_end_ms", "centroid_ms"))
        l1, r1, mu1 = (float(x1[k]) for k in
                       ("support_start_ms", "support_end_ms", "centroid_ms"))
    except (KeyError, ValueError, TypeError, OverflowError):
        return abstain("INVALID_NUMERIC_INPUT")
    nums = (q0, q1, u0, u1, c, C, O, l0, r0, mu0, l1, r1, mu1)
    if not all(math.isfinite(v) for v in nums):
        return abstain("NONFINITE_INPUT")
    if min(q0, q1, u0, u1, c) < 0 or C <= 0 or O <= 0:
        return abstain("INVALID_UNITS_OR_RANGE")
    if not (l0 < r0 < l1 < r1 and l0 < mu0 < r0 and l1 < mu1 < r1):
        return abstain("BAD_SHUTTER_SUPPORT")
    if any(x.get("kernel_normalized") is not True or
           x.get("centroid_authenticated") is not True or
           x.get("support_authenticated") is not True or
           x.get("clock_uncertainty_ms") != 0 for x in (x0, x1)):
        return abstain("UNAUTHENTICATED_KERNEL_OR_CLOCK")
    # Uniform shutter centroids must be exact midpoints; reject mismatched metadata.
    if abs(mu0 - (l0 + r0) / 2) > 1e-9 or abs(mu1 - (l1 + r1) / 2) > 1e-9:
        return abstain("NONUNIFORM_OR_INCONSISTENT_CENTROID")
    L = max(C, O)
    w0, w1 = r0 - l0, r1 - l1
    # The variance bound is valid for all bounded-speed trajectories, not only V witnesses.
    m0_lower = math.sqrt(max(0.0, q0 - u0 - (L * w0) ** 2 / 12))
    m1_lower = math.sqrt(max(0.0, q1 - u1 - (L * w1) ** 2 / 12))
    earliest = max(r0, mu0 + (m0_lower - c) / C)
    latest = min(l1, mu1 - (m1_lower - c) / O)
    eps = 1e-10 * max(1.0, abs(earliest), abs(latest), abs(l1), abs(r0))
    base = {"physical_certification": False, "mean0_lower_mm": m0_lower,
            "mean1_lower_mm": m1_lower, "earliest_ms": earliest,
            "latest_ms": latest, "dark_gap_ms": l1 - r0,
            "critical_centroid_gap_lower_ms": (m0_lower - c) / C +
                                              (m1_lower - c) / O}
    if earliest > latest + eps or earliest > l1 + eps or latest < r0 - eps:
        return dict(base, decision="EXCLUDED_CONDITIONALLY",
                    reason="NO_CROSSING_UNDER_QUADRATIC_MODEL_AND_ASSUMED_CAPS")
    return dict(base, decision="NOT_EXCLUDED",
                reason="CROSSING_NOT_RULED_OUT_OR_BOUNDARY")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--examples":
        for alpha in (0.99, 0.95):
            x = example(alpha)
            d = evaluate(x)
            print(json.dumps({"alpha": alpha, "q0_mm2": x["q0_mm2"],
                              "q1_mm2": x["q1_mm2"], "corrected": d},
                             sort_keys=True))
    elif len(sys.argv) == 1:
        print(json.dumps(evaluate(json.load(sys.stdin)), sort_keys=True))
    else:
        raise SystemExit("usage: python e002_461_quadratic_shutter.py [--examples]")
