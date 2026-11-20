#!/usr/bin/env python3
"""E002-473: published-human-velocity stress scenarios against Lucent's existing design gate.

Published cohort statistics are NOT physical hard velocity caps. No new human
raw data, physical shutter calibration, or product release is implied.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

from e002_472_design_feasibility import design_case

SOURCES = {
    "2019_spontaneous_mean": {
        "velocity_mm_s": 93, "kind": "reported mean closure velocity",
        "source": "https://pubmed.ncbi.nlm.nih.gov/30893187/",
        "directly_comparable_to_optical_peak": False,
    },
    "2019_spontaneous_reported_max": {
        "velocity_mm_s": 160, "kind": "reported maximum closure velocity in sample",
        "source": "https://pubmed.ncbi.nlm.nih.gov/30893187/",
        "directly_comparable_to_optical_peak": False,
    },
    "2013_voluntary_optical_mean_peak": {
        "velocity_mm_s": 243, "kind": "mean of individual peak closing aperture speeds (SEM 9)",
        "source": "https://doi.org/10.1098/rsif.2013.0227",
        "directly_comparable_to_optical_peak": True,
    },
    "1997_coil_secondary_table_mean_peak": {
        "velocity_mm_s": 427,
        "kind": "coil-based mean peak for age 40-49 (n=8), secondarily tabulated",
        "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/",
        "directly_comparable_to_optical_peak": False,
    },
}

DESIGNS = ((30, 4), (240, 1), (300, 1))
ABSTAIN = "ABSTAIN_UNCALIBRATED"


def independent_rational_envelope(fps, exposure_ms, velocity_mm_s):
    """Exact independent arithmetic for the prespecified E002-472 model."""
    f, w, v = Fraction(fps), Fraction(exposure_ms), Fraction(velocity_mm_s)
    period = Fraction(1000) / f
    denom = w / 4 + (period + Fraction(1, 5)) / 2
    critical_v = Fraction(900) / denom
    critical_margin = Fraction(1, 10) + v * denom / 1000
    dark = w + Fraction(1, 5) < period
    reference = w + Fraction(1, 5) + Fraction(2, 5) < period
    return critical_v, critical_margin, dark and reference


def run():
    rows = []
    for fps, exposure in DESIGNS:
        for source_id, src in SOURCES.items():
            v = src["velocity_mm_s"]
            exact_v, exact_m, timing_feasible = independent_rational_envelope(fps, exposure, v)
            model = design_case(
                fps=fps, exposure_ms=exposure, aperture_margin_mm=1.0,
                aperture_uncertainty_mm=0.1, clock_error_ms=0.1,
                reference_exposure_ms=0.2, reference_clock_error_ms=0.1,
                hypothetical_velocity_mm_s=v)
            if abs(float(exact_v) - model["critical_hypothetical_velocity_mm_s"]) > 1e-9:
                raise AssertionError("independent velocity disagreement")
            if model["physical_release_authorized"] or model["product_claim"] != ABSTAIN:
                raise AssertionError("physical release not supported")
            expected = ("ABSTAIN_DESIGN" if not timing_feasible else
                        "EXCLUSION_FEASIBLE_CONDITIONALLY" if Fraction(v) < exact_v else
                        "EXCLUSION_NOT_SUPPORTED")
            if model["decision"] != expected:
                raise AssertionError("design gate disagreement")
            rows.append({
                "fps_nominal": fps,
                "exposure_ms": exposure,
                "literature_scenario": source_id,
                "velocity_mm_s": v,
                "measurement_kind": src["kind"],
                "optical_peak_comparable": src["directly_comparable_to_optical_peak"],
                "published_statistic_is_hard_cap": False,
                "critical_velocity_mm_s": round(float(exact_v), 9),
                "strict_minimum_margin_mm": round(float(exact_m), 9),
                "velocity_to_critical_ratio": round(float(Fraction(v) / exact_v), 9),
                "design_decision": expected,
                "physical_release_authorized": False,
                "product_claim": ABSTAIN,
            })
    return {
        "experiment": "E002-473",
        "evidence_tier": "PUBLISHED_HUMAN_COHORT_STATISTICS_PLUS_SYNTHETIC_DESIGN_STRESS",
        "not_new_raw_human_measurements": True,
        "not_hard_physiological_velocity_caps": True,
        "physical_release_authorized": False,
        "product_claim": ABSTAIN,
        "sources": SOURCES,
        "n_rows": len(rows),
        "counts": {k: sum(r["design_decision"] == k for r in rows)
                   for k in ("EXCLUSION_FEASIBLE_CONDITIONALLY",
                             "EXCLUSION_NOT_SUPPORTED", "ABSTAIN_DESIGN")},
        "rows": rows,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    args.output.write_text(json.dumps(run(), sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("E002-473 published-human stress grid complete; physical release blocked")
