#!/usr/bin/env python3
"""E002-472: prospective instrument-feasibility envelope; synthetic, not physiology.

Quantifies when the existing E002-456 shutter-aware exclusion *could* be
informative for symmetric endpoint measurements. No physical release is possible.
"""
import argparse
import json
import math
from pathlib import Path

ABSTAIN = "ABSTAIN_UNCALIBRATED"


def scalar(x, *, positive=False):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError("expected numeric scalar")
    x = float(x)
    if not math.isfinite(x) or x < 0 or (positive and x <= 0):
        raise ValueError("invalid scalar")
    return x


def design_case(*, fps, exposure_ms, aperture_margin_mm,
                aperture_uncertainty_mm, clock_error_ms,
                reference_exposure_ms, reference_clock_error_ms,
                hypothetical_velocity_mm_s, shutter_kernel="uniform_symmetric"):
    """No camera setting or illustrative velocity is authenticated here."""
    fps = scalar(fps, positive=True)
    w = scalar(exposure_ms)
    m = scalar(aperture_margin_mm)
    u = scalar(aperture_uncertainty_mm)
    e = scalar(clock_error_ms)
    r = scalar(reference_exposure_ms)
    er = scalar(reference_clock_error_ms)
    V = scalar(hypothetical_velocity_mm_s, positive=True)
    if shutter_kernel not in ("uniform_symmetric", "support_symmetric"):
        return {"decision": "ABSTAIN_DESIGN", "reason": "UNSUPPORTED_SHUTTER",
                "physical_release_authorized": False, "product_claim": ABSTAIN}
    T = 1000.0 / fps
    k = 0.25 if shutter_kernel == "uniform_symmetric" else 0.5
    if w >= T:
        return {"decision": "ABSTAIN_DESIGN", "reason": "OVERLAPPING_EXPOSURES",
                "physical_release_authorized": False, "product_claim": ABSTAIN}
    if w + 2 * e >= T:
        return {"decision": "ABSTAIN_DESIGN", "reason": "NO_GUARANTEED_DARK_GAP",
                "physical_release_authorized": False, "product_claim": ABSTAIN}
    denominator_ms = k * w + (T + 2 * e) / 2
    vcrit = 1000.0 * (m - u) / denominator_ms if m > u else 0.0
    # Exact same sufficient envelope as E002-456 for symmetric endpoints.
    excess_lower_mm = m - u - V * denominator_ms / 1000.0
    reference_feasible = w + r + 2 * (e + er) < T
    decision = ("ABSTAIN_DESIGN" if not reference_feasible else
                "EXCLUSION_FEASIBLE_CONDITIONALLY" if m > u and V < vcrit else
                "EXCLUSION_NOT_SUPPORTED")
    return {
        "decision": decision,
        "reason": "NONE" if reference_feasible else "REFERENCE_SUPPORT_CANNOT_FIT",
        "fps_nominal": fps,
        "exposure_ms": w,
        "critical_hypothetical_velocity_mm_s": vcrit,
        "hypothetical_velocity_mm_s": V,
        "lower_envelope_excess_over_threshold_mm": excess_lower_mm,
        "dark_gap_feasible": True,
        "reference_support_feasible": reference_feasible,
        "hard_human_velocity_bound_established": False,
        "shutter_calibration_authenticated": False,
        "physical_release_authorized": False,
        "product_claim": ABSTAIN,
    }


def frozen_matrix():
    """Preregistered sensitivity grid; no human velocity distribution."""
    rows = []
    for fps in (30, 60, 120, 240):
        for w in (1.0, 4.0, 8.0):
            for V in (50.0, 100.0, 200.0, 400.0):
                result = design_case(
                    fps=fps, exposure_ms=w, aperture_margin_mm=1.0,
                    aperture_uncertainty_mm=0.1, clock_error_ms=0.1,
                    reference_exposure_ms=0.2, reference_clock_error_ms=0.1,
                    hypothetical_velocity_mm_s=V)
                if result["reason"] == "OVERLAPPING_EXPOSURES":
                    continue
                rows.append(result)
    return {
        "experiment": "E002-472",
        "evidence_tier": "PROSPECTIVE_SYNTHETIC_DESIGN_ONLY",
        "all_velocity_values_are_hypothetical": True,
        "n_rows": len(rows),
        "counts": {k: sum(r["decision"] == k for r in rows) for k in (
            "EXCLUSION_FEASIBLE_CONDITIONALLY",
            "EXCLUSION_NOT_SUPPORTED", "ABSTAIN_DESIGN")},
        "rows": rows,
        "physical_release_authorized": False,
        "product_claim": ABSTAIN,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    a.output.write_text(json.dumps(frozen_matrix(), sort_keys=True,
                                   indent=2, allow_nan=False) + "\n",
                        encoding="utf-8")
    print("Synthetic design grid written; human/physical release remains blocked")


if __name__ == "__main__":
    main()
