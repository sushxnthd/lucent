#!/usr/bin/env python3
"""E002-470: frozen synthetic moving-aperture camera/reference challenge.

Synthetic ONLY. The independent continuous-aperture oracle uses piecewise-linear
geometry; the prediction path calls the existing E002-456 research gate.
"""
from __future__ import annotations

import json
import random
from collections import Counter

from e002_456_prospective_gate import evaluate_interval

SEED = 470371
NUISANCES = ("geometry", "brightness", "missingness", "blur", "gaze",
             "glasses", "sampling", "clock", "rolling_shutter")
C = 2.0
V = 0.25  # mm/ms; illustrative, NOT a validated human bound


def avg_abs(lo: float, hi: float, pivot: float) -> float:
    """Exact integral of |t-pivot| divided by shutter width."""
    if not lo < hi:
        raise ValueError("nonpositive shutter width")
    antiderivative = lambda x: (x - pivot) * abs(x - pivot) / 2.0
    return (antiderivative(hi) - antiderivative(lo)) / (hi - lo)


def shutter_mean(m: float, slope: float, pivot: float,
                 center: float, exposure: float) -> float:
    return m + slope * avg_abs(center - exposure / 2,
                               center + exposure / 2, pivot)


def dark_gap_min(m: float, slope: float, pivot: float,
                 dt: float, exposure: float) -> float:
    left, right = exposure / 2, dt - exposure / 2
    if left >= right:
        raise ValueError("no dark gap")
    distance = max(left - pivot, pivot - right, 0.0)
    return m + slope * distance


def make_case(dt: float, exposure: float, y0: float, y1: float,
              bad_nuisance: str | None = None) -> dict:
    if bad_nuisance is not None and bad_nuisance not in NUISANCES:
        raise ValueError("unknown nuisance")
    return {
        "nuisance": {k: "FAIL" if k == bad_nuisance else "PASS"
                     for k in NUISANCES},
        "instrument": {
            "geometry_calibration_id": "synthetic-geometry-not-verified",
            "clock_calibration_id": "synthetic-clock-not-verified",
            "exposure_calibration_id": "synthetic-shutter-not-verified",
            "reference_annotation_id": "analytic-oracle-not-human",
            "independent_reference": True,
        },
        "velocity": {"limit_mm_s": 250.0, "provenance": "ILLUSTRATIVE"},
        "closure_threshold_mm": C,
        "endpoint_aperture_mm": [y0, y1],
        "endpoint_uncertainty_mm": [0.0, 0.0],
        "endpoint_time_ms": [0.0, dt],
        "shutter": {"kernel": "uniform_symmetric", "exposure_ms": exposure,
                    "clock_error_ms": 0.0, "reference_exposure_ms": 0.0,
                    "reference_clock_error_ms": 0.0},
        "reference": [],
    }


def numerical_shutter_mean(m, slope, pivot, center, exposure, n=8192):
    lo, hi = center - exposure / 2, center + exposure / 2
    h = (hi - lo) / n
    total = (m + slope * abs(lo - pivot) +
             m + slope * abs(hi - pivot)) / 2
    for i in range(1, n):
        total += m + slope * abs(lo + i * h - pivot)
    return total / n


def clean_sweep() -> dict:
    rng = random.Random(SEED)
    strata = {}
    total = Counter()
    for fps in (30, 60, 120, 240):
        dt = 1000.0 / fps
        for exposure in (0.5, 1.5):
            count = Counter()
            for _ in range(1500):
                slope = rng.uniform(0.01, V)
                m = rng.uniform(1.5, 2.8)
                pivot = rng.uniform(-dt / 4, 5 * dt / 4)
                y0 = shutter_mean(m, slope, pivot, 0.0, exposure)
                y1 = shutter_mean(m, slope, pivot, dt, exposure)
                actual_closure = dark_gap_min(m, slope, pivot, dt, exposure) < C
                predicted = evaluate_interval(make_case(dt, exposure, y0, y1))
                decision = predicted["decision"]
                count[decision] += 1
                count["true_hidden_closures"] += int(actual_closure)
                count["false_exclusions"] += int(
                    actual_closure and decision == "EXCLUDED_CONDITIONALLY")
                count["unexpected_abstentions"] += int(decision == "ABSTAIN")
            strata[f"{fps}fps_{exposure:g}ms"] = dict(sorted(count.items()))
            total.update(count)
    return {"by_stratum": strata, "total": dict(sorted(total.items()))}


def nuisance_challenge() -> dict:
    nominal_dt = 1000.0 / 240.0
    exposure = 1.0
    m, slope = 1.99, V
    baseline_pivot = nominal_dt / 2
    base = [shutter_mean(m, slope, baseline_pivot, center, exposure)
            for center in (0.0, nominal_dt)]
    baseline = evaluate_interval(make_case(nominal_dt, exposure, *base))
    if dark_gap_min(m, slope, baseline_pivot, nominal_dt, exposure) >= C:
        raise AssertionError("adversarial base world must cross threshold")
    outcomes = {}
    for nuisance in NUISANCES:
        if nuisance == "geometry":
            corrupted = [1.03 * y for y in base]
            mechanism = "3% aperture scale inflation"
        elif nuisance in ("sampling", "clock", "rolling_shutter"):
            actual_dt = nominal_dt + 0.65
            corrupted = [shutter_mean(m, slope, actual_dt / 2, t, exposure)
                         for t in (0.0, actual_dt)]
            mechanism = "+0.65 ms unreported effective frame separation"
        else:
            corrupted = [y + 0.075 for y in base]
            mechanism = "+0.075 mm apparent-aperture offset"
        unsafe = evaluate_interval(make_case(nominal_dt, exposure, *corrupted))
        guarded = evaluate_interval(make_case(nominal_dt, exposure, *corrupted,
                                              bad_nuisance=nuisance))
        outcomes[nuisance] = {
            "injection": mechanism,
            "misdeclared_pass_decision": unsafe["decision"],
            "declared_fail_decision": guarded["decision"],
            "misdeclared_pass_false_exclusion":
                unsafe["decision"] == "EXCLUDED_CONDITIONALLY",
            "declared_fail_abstains": guarded["decision"] == "ABSTAIN",
        }
    return {"baseline_decision": baseline["decision"],
            "baseline_dark_gap_min_mm": m,
            "baseline_true_hidden_closure": True,
            "by_nuisance": outcomes,
            "false_exclusions_if_pass_misdeclared": sum(
                x["misdeclared_pass_false_exclusion"] for x in outcomes.values()),
            "abstentions_if_fail_declared": sum(
                x["declared_fail_abstains"] for x in outcomes.values()),
            "total_fault_strata": len(NUISANCES)}


def integration_control() -> dict:
    rng = random.Random(SEED + 1)
    errors = []
    for _ in range(12):
        exposure = rng.uniform(0.2, 2.0)
        center = rng.uniform(-2, 5)
        pivot = rng.uniform(center - exposure, center + exposure)
        m, slope = rng.uniform(1.5, 2.5), rng.uniform(0.01, V)
        exact = shutter_mean(m, slope, pivot, center, exposure)
        numeric = numerical_shutter_mean(m, slope, pivot, center, exposure)
        errors.append(abs(exact - numeric))
    return {"controls": len(errors), "max_absolute_difference_mm": max(errors),
            "within_1e_minus_6_mm": all(x < 1e-6 for x in errors)}


def run() -> dict:
    clean = clean_sweep()
    nuisance = nuisance_challenge()
    quadrature = integration_control()
    assert sum(v.get("EXCLUDED_CONDITIONALLY", 0) +
               v.get("NOT_EXCLUDED", 0) + v.get("ABSTAIN", 0)
               for v in clean["by_stratum"].values()) == 12000
    assert clean["total"].get("false_exclusions", 0) == 0
    assert clean["total"].get("unexpected_abstentions", 0) == 0
    assert nuisance["baseline_decision"] == "NOT_EXCLUDED"
    assert nuisance["abstentions_if_fail_declared"] == 9
    assert quadrature["within_1e_minus_6_mm"]
    return {
        "experiment": "E002-470", "seed": SEED,
        "evidence_tier": "SYNTHETIC_INDEPENDENT_CONTINUOUS_APERTURE_ORACLE",
        "source_gate": "E002-456 research evaluator; declarations not verified",
        "clean": clean, "nuisance": nuisance,
        "independent_numeric_integration_control": quadrature,
        "real_human_anatomical_measurements": 0,
        "real_physical_instrument_acquisitions": 0,
        "velocity_cap_independently_verified": False,
        "shutter_timing_independently_verified": False,
        "physical_release_authorized": False,
        "product_claim": "ABSTAIN_UNCALIBRATED",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True, allow_nan=False))
