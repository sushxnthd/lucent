#!/usr/bin/env python3
"""E002-424: exact SYNTHETIC shutter subphase alias, never a human/camera measurement.
Frozen protocol: E002_424_FROZEN.md. Pure Python standard library.
"""
from __future__ import annotations

import json
import math

try:
    from . import e002_423_pulse_metrology as previous
except ImportError:
    import e002_423_pulse_metrology as previous

EXPOSURE_MS = 2.4
CENTERS_MS = (0.0, 3.2)
CELL_MS = 0.1
HALF_CELL_MS = CELL_MS / 2
N_CELLS = 24
ALPHA = 0.99
PULSE_MS = 0.50
RESCUE_PULSE_MS = 0.45
PHASES_MS = tuple(k / 10 for k in range(-30, 71))
SPEED_PER_MS = 0.05
THETA = 0.20
OBSERVED_APERTURE_MEAN = 0.281
VERTEX_MS = (CENTERS_MS[0] + CENTERS_MS[1]) / 2
TOL = 1e-11


def validate(row: int, mode: str, phase_ms: float | None = None,
             pulse_ms: float | None = None) -> None:
    if row not in (0, 1) or mode not in ("boxcar", "subphase"):
        raise ValueError("unknown row or shutter model")
    if phase_ms is not None and (not isinstance(phase_ms, (float, int)) or
                                 not math.isfinite(phase_ms)):
        raise ValueError("nonfinite phase")
    if pulse_ms is not None and (not isinstance(pulse_ms, (float, int)) or
                                 not math.isfinite(pulse_ms) or pulse_ms <= 0):
        raise ValueError("pulse must be positive and finite")


def segments(row: int, mode: str) -> list[tuple[float, float, float]]:
    """Exact piecewise-constant, normalized exposure response h(t), 1/ms."""
    validate(row, mode)
    lo = CENTERS_MS[row] - EXPOSURE_MS / 2
    if mode == "boxcar":
        return [(lo, lo + EXPOSURE_MS, 1 / EXPOSURE_MS)]
    result = []
    for j in range(N_CELLS):
        left = lo + j * CELL_MS
        middle = left + HALF_CELL_MS
        right = lo + (j + 1) * CELL_MS
        sign = 1 if row == 0 else -1
        result.append((left, middle, (1 + sign * ALPHA) / EXPOSURE_MS))
        result.append((middle, right, (1 - sign * ALPHA) / EXPOSURE_MS))
    return result


def pulse_response(row: int, mode: str, phase_ms: float,
                   pulse_ms: float = PULSE_MS) -> float:
    validate(row, mode, phase_ms, pulse_ms)
    return sum(max(0.0, min(hi, phase_ms + pulse_ms) - max(lo, phase_ms)) * weight
               for lo, hi, weight in segments(row, mode))


def abs_primitive(t: float, vertex: float = VERTEX_MS) -> float:
    z = t - vertex
    return z * abs(z) / 2


def aperture_response(row: int, mode: str, minimum: float) -> float:
    """Exact integral of (minimum + V*abs(t-vertex)) against shutter."""
    validate(row, mode)
    if not isinstance(minimum, (int, float)) or not math.isfinite(minimum):
        raise ValueError("invalid aperture minimum")
    return sum(weight * (minimum * (hi - lo) + SPEED_PER_MS *
                         (abs_primitive(hi) - abs_primitive(lo)))
               for lo, hi, weight in segments(row, mode))


def policy() -> dict:
    return {"evidence_tier": "SYNTHETIC_SHUTTER_ONLY",
            "physical_camera_authenticated": False,
            "human_velocity_authenticated": False,
            "product_claim_authorized": False,
            "product": "ABSTAIN_UNCALIBRATED"}


def experiment() -> dict:
    pulse_errors = []
    original_fits = []
    for row in (0, 1):
        baseline = [pulse_response(row, "boxcar", p) for p in PHASES_MS]
        adversary = [pulse_response(row, "subphase", p) for p in PHASES_MS]
        pulse_errors.append(max(abs(a - b) for a, b in zip(baseline, adversary)))
        original_fits.append({"row": row,
                              "boxcar": previous.fit_row(PHASES_MS, baseline),
                              "adversary": previous.fit_row(PHASES_MS, adversary)})

    d = CENTERS_MS[1] - CENTERS_MS[0]
    delta = ALPHA * SPEED_PER_MS * CELL_MS / 4
    m0 = OBSERVED_APERTURE_MEAN - SPEED_PER_MS * d / 2
    m1 = m0 - delta
    means_base = [aperture_response(row, "boxcar", m0) for row in (0, 1)]
    means_alias = [aperture_response(row, "subphase", m1) for row in (0, 1)]
    max_rescue = []
    for row in (0, 1):
        max_rescue.append(max(abs(pulse_response(row, "boxcar", s, RESCUE_PULSE_MS)
                                  - pulse_response(row, "subphase", s, RESCUE_PULSE_MS))
                              for s in PHASES_MS))
    normalization = [sum((hi-lo)*w for lo, hi, w in segments(row, mode))
                     for row in (0, 1) for mode in ("boxcar", "subphase")]
    min_weights = [min(w for _, _, w in segments(row, mode))
                   for row in (0, 1) for mode in ("boxcar", "subphase")]
    max_aperture = max(m0, m1) + SPEED_PER_MS * max(
        abs(CENTERS_MS[0]-EXPOSURE_MS/2-VERTEX_MS),
        abs(CENTERS_MS[1]+EXPOSURE_MS/2-VERTEX_MS))
    frozen = {
        "H1_original_phase_grid_indistinguishable": max(pulse_errors) <= TOL,
        "H1_heldout_fits_indistinguishable": all(
            abs(f["boxcar"]["heldout_rmse"] - f["adversary"]["heldout_rmse"]) <= TOL
            and f["boxcar"]["heldout_pass"] and f["adversary"]["heldout_pass"]
            for f in original_fits),
        "H2_opposite_closure_worlds_identical_means": (
            m0 > THETA and m1 < THETA and
            max(abs(v-OBSERVED_APERTURE_MEAN) for v in means_base+means_alias) <= TOL and
            m1 >= 0 and max_aperture <= 1),
        "H3_changed_pulse_width_discriminates": min(max_rescue) > 0.015,
        "H4_nonnegative_normalized": min(min_weights) > 0 and
            max(abs(x-1) for x in normalization) <= TOL,
        "H5_physical_abstention": not policy()["product_claim_authorized"] and
            policy()["product"] == "ABSTAIN_UNCALIBRATED",
    }
    return {
        "study": "E002-424",
        "provenance": "exact synthetic scalar shutter and moving aperture; no hardware or humans",
        "frozen_protocol": "E002_424_FROZEN.md",
        "phase_count": len(PHASES_MS), "original_pulse_width_ms": PULSE_MS,
        "rescue_pulse_width_ms": RESCUE_PULSE_MS,
        "max_original_grid_response_difference_per_row": pulse_errors,
        "fitted_boxcar_models": original_fits,
        "max_changed_width_response_difference_per_row": max_rescue,
        "minimum_aperture_boxcar_world": m0,
        "minimum_aperture_subphase_world": m1,
        "closure_threshold": THETA,
        "hypothetical_velocity_per_second": SPEED_PER_MS * 1000,
        "observed_means_boxcar": means_base,
        "observed_means_subphase": means_alias,
        "normalization_checks": normalization,
        "minimum_shutter_weights": min_weights,
        "max_aperture_over_exposures": max_aperture,
        "frozen_tests": frozen, "policy": policy(),
    }


if __name__ == "__main__":
    print(json.dumps(experiment(), sort_keys=True, indent=2))
