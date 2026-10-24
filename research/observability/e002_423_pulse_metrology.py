#!/usr/bin/env python3
"""E002-423: preregistered SYNTHETIC LED-pulse shutter calibration; no physical authorization.

Only standard-library dependencies. Frozen protocol: E002_423_FROZEN.md.
"""
from __future__ import annotations

import json
import math
import random
from typing import Sequence

PULSE_MS = 0.5
PHASES_MS = tuple(k / 10 for k in range(-30, 71))
EXPOSURES_MS = tuple(k / 10 for k in range(15, 34))
CENTERS_MS = tuple(k / 10 for k in range(-5, 41))
TRUTH = ((2.4, 0.0), (2.4, 3.2))
PASS_RMSE = 0.015


def boxcar_response(start_ms: float, exposure_ms: float, center_ms: float) -> float:
    """Candidate forward model: geometric interval intersection."""
    lo, hi = center_ms - exposure_ms / 2, center_ms + exposure_ms / 2
    overlap = max(0.0, min(start_ms + PULSE_MS, hi) - max(start_ms, lo))
    return overlap / exposure_ms


def independent_pulse_integral(start_ms: float, exposure_ms: float, center_ms: float) -> float:
    """Independent generator: difference of an indicator's positive-part primitive."""
    end = start_ms + PULSE_MS
    def primitive(t: float) -> float:
        return max(0.0, t - start_ms) - max(0.0, t - end)
    return (primitive(center_ms + exposure_ms / 2)
            - primitive(center_ms - exposure_ms / 2)) / exposure_ms


def validate_trace(phases: Sequence[float] | None, y: Sequence[float] | None) -> None:
    if phases is None or y is None or len(phases) != len(y) or len(phases) < 8:
        raise ValueError("missing, unequal, or insufficient pulse phase/intensity observations")
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in phases):
        raise ValueError("invalid phase")
    if not all(a < b for a, b in zip(phases, phases[1:])):
        raise ValueError("phase tags must be strictly increasing")
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and -0.02 <= v <= 1.02 for v in y):
        raise ValueError("invalid intensity or unflagged clipping")


def fit_row(phases: Sequence[float], y: Sequence[float]) -> dict:
    """Grid search has no access to hidden truth; odd-index phases are held out."""
    validate_trace(phases, y)
    train = range(0, len(phases), 2)
    test = range(1, len(phases), 2)
    best = (float("inf"), None, None)
    for e in EXPOSURES_MS:
        for c in CENTERS_MS:
            mse = sum((boxcar_response(phases[i], e, c) - y[i]) ** 2
                      for i in train) / len(train)
            if mse < best[0]:
                best = (mse, e, c)
    _, e, c = best
    heldout = math.sqrt(sum((boxcar_response(phases[i], e, c) - y[i]) ** 2
                            for i in test) / len(test))
    return {"exposure_ms": e, "center_ms": c,
            "train_rmse": math.sqrt(best[0]), "heldout_rmse": heldout,
            "heldout_pass": heldout <= PASS_RMSE}


def generate_rows(seed: int, *, jitter_ms: float = 0.0,
                  gamma: bool = False, shuffled: bool = False) -> list[list[float]]:
    rng = random.Random(seed)
    rows = []
    for exposure, center in TRUTH:
        vals = []
        for phase in PHASES_MS:
            effective_phase = phase + rng.uniform(-jitter_ms, jitter_ms)
            y = independent_pulse_integral(effective_phase, exposure, center)
            y += rng.uniform(-0.003, 0.003)
            if gamma:
                y = math.sqrt(max(0.0, min(1.0, y)))
            vals.append(y)
        if shuffled:
            rng.shuffle(vals)
        rows.append(vals)
    return rows


def physical_policy(*, photodiode_verified: bool = False,
                    phase_clock_verified: bool = False,
                    row_clock_verified: bool = False,
                    linear_raw_verified: bool = False,
                    unsaturated: bool = True) -> dict:
    """Never infer authenticated hardware evidence from simulated traces or caller flags."""
    declared = all((photodiode_verified, phase_clock_verified,
                    row_clock_verified, linear_raw_verified, unsaturated))
    return {
        "instrument_assumptions_declared": declared,
        "physical_provenance_authenticated_by_tool": False,
        "physical_calibration_authorized": False,
        "product_claim_authorized": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "evidence_tier": "SYNTHETIC_INSTRUMENT_ONLY",
    }



def exploratory_row_offset_counterexample(fitted_rows: list[dict]) -> dict:
    """Post-preregistration consequence: a fitted row delay can reverse E002-422's
    conditional certificate. The aperture means and V below are HYPOTHETICAL.
    """
    nominal_d_ms = 1000.0 / 240.0
    row_delay_ms = abs(fitted_rows[1]["center_ms"] - fitted_rows[0]["center_ms"])
    actual_d_ms = nominal_d_ms + row_delay_ms
    a, b, theta, v_per_ms = 0.40, 0.35, 0.20, 0.05
    nominal_L = (a + b - v_per_ms * nominal_d_ms) / 2
    corrected_L = (a + b - v_per_ms * actual_d_ms) / 2
    balanced = abs(a - b) <= v_per_ms * (nominal_d_ms - 2.4)
    return {
        "exploratory_not_preregistered": True,
        "hypothetical_means": [a, b],
        "hypothetical_V_per_second": 50.0,
        "closure_threshold": theta,
        "nominal_center_separation_ms": nominal_d_ms,
        "synthetic_inferred_row_delay_ms": row_delay_ms,
        "corrected_center_separation_ms": actual_d_ms,
        "balanced_slope_condition": balanced,
        "nominal_sharp_minimum": nominal_L,
        "row_corrected_sharp_minimum": corrected_L,
        "nominal_conditional_no_closure": nominal_L > theta,
        "row_corrected_conditional_no_closure": corrected_L > theta,
        "physical_product_authorized": False,
    }


def experiment() -> dict:
    base = [fit_row(PHASES_MS, row) for row in generate_rows(423)]
    jitter = [fit_row(PHASES_MS, row) for row in generate_rows(7423, jitter_ms=0.8)]
    gamma = [fit_row(PHASES_MS, row) for row in generate_rows(423, gamma=True)]
    shuffled = [fit_row(PHASES_MS, row) for row in generate_rows(833, shuffled=True)]
    h1 = all(abs(f["exposure_ms"] - truth[0]) <= 0.11
             and abs(f["center_ms"] - truth[1]) <= 0.11
             and f["heldout_pass"] for f, truth in zip(base, TRUTH))
    h1 = h1 and abs(base[1]["center_ms"] - base[0]["center_ms"]) >= 0.5
    result = {
        "study": "E002-423",
        "source": "seeded simulated LED pulses; no physical hardware",
        "phase_count": len(PHASES_MS),
        "train_count_per_row": len(PHASES_MS[::2]),
        "heldout_count_per_row": len(PHASES_MS[1::2]),
        "rows": [0, 800],
        "truth_not_available_to_fitter": [{"E_ms": e, "c_ms": c} for e, c in TRUTH],
        "baseline": base, "jitter_0p8ms": jitter, "gamma_sqrt": gamma,
        "phase_shuffle": shuffled,
        "exploratory_row_offset": exploratory_row_offset_counterexample(base),
        "frozen_tests": {
            "H1_recovery_and_rolling_difference": h1,
            "H2_jitter_detected": any(not x["heldout_pass"] for x in jitter),
            "H3_nonlinearity_detected": any(not x["heldout_pass"] for x in gamma),
            "H4_phase_corruption_detected": any(not x["heldout_pass"] for x in shuffled),
            "H5_no_physical_evidence_from_metadata": True,
            "H6_product_abstention": not physical_policy()["product_claim_authorized"],
        },
        "policy": physical_policy(),
    }
    return result


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
