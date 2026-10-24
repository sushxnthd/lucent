#!/usr/bin/env python3
"""E002-425: preregistered SYNTHETIC finite-bin shutter identifiability experiment.

This is not hardware calibration, human validation, or product authorization.
Frozen before numerical evaluation: E002_425_FROZEN.md.
"""
from __future__ import annotations

import json
import math
import numpy as np
from scipy.optimize import lsq_linear

EXPOSURE_MS = 2.4
BINS = 48
BIN_MS = EXPOSURE_MS / BINS
EDGES = np.linspace(0.0, EXPOSURE_MS, BINS + 1)
PULSE_WIDTHS_MS = np.array([0.37, 0.43, 0.51])
CALIBRATION_N = 256
HELDOUT_N = 128
SEED_DESIGN = 20261025
SEED_NOISE = 20261026
NOISE_SD = 0.0005


def pulse_matrix(starts: np.ndarray, widths: np.ndarray) -> np.ndarray:
    """Exact binwise pulse-overlap fractions. Columns multiply bin *masses*."""
    s = np.asarray(starts, dtype=float)
    w = np.asarray(widths, dtype=float)
    if (s.ndim != 1 or w.ndim != 1 or len(s) == 0 or s.shape != w.shape
            or not np.isfinite(s).all() or not np.isfinite(w).all()
            or np.any(w <= 0)):
        raise ValueError("starts and positive widths must be matching finite vectors")
    left = np.maximum(EDGES[:-1][None, :], s[:, None])
    right = np.minimum(EDGES[1:][None, :], (s + w)[:, None])
    return np.maximum(0.0, right - left) / BIN_MS


def kernels() -> tuple[np.ndarray, np.ndarray]:
    j = np.arange(BINS)
    uniform = np.full(BINS, 1.0 / BINS)
    alternating = (1.0 + 0.99 * np.where(j % 2 == 0, 1.0, -1.0)) / BINS
    assert np.isclose(uniform.sum(), 1.0) and np.isclose(alternating.sum(), 1.0)
    return uniform, alternating


def designs() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    legacy_starts = np.arange(-10, 25, dtype=float) * 0.10
    legacy = pulse_matrix(legacy_starts, np.full(legacy_starts.size, 0.50))
    rng = np.random.default_rng(SEED_DESIGN)
    starts = rng.uniform(-0.8, 2.4, CALIBRATION_N + HELDOUT_N)
    widths = PULSE_WIDTHS_MS[rng.integers(0, len(PULSE_WIDTHS_MS), len(starts))]
    return legacy, pulse_matrix(starts, widths), starts, widths


def recover(A: np.ndarray, responses: np.ndarray) -> np.ndarray:
    """Nonnegative bin masses with a heavily weighted sum-to-one equation."""
    mat = np.asarray(A, dtype=float)
    y = np.asarray(responses, dtype=float)
    if (mat.ndim != 2 or mat.shape[1] != BINS or y.shape != (mat.shape[0],)
            or not np.isfinite(mat).all() or not np.isfinite(y).all()
            or np.any(mat < 0)):
        raise ValueError("invalid design matrix or responses")
    augmented = np.vstack((mat, np.full((1, BINS), 10.0)))
    target = np.concatenate((y, [10.0]))
    result = lsq_linear(augmented, target, bounds=(0, 1),
                        tol=1e-12, max_iter=1000, lsmr_tol="auto")
    if not result.success:
        raise RuntimeError("bounded least-squares solver failed")
    return result.x


def policy() -> dict:
    return {"evidence_tier": "SYNTHETIC_FINITE_BIN_INSTRUMENT",
            "camera_hardware_authenticated": False,
            "pulse_waveform_authenticated": False,
            "human_aperture_or_velocity_authenticated": False,
            "product_claim_authorized": False,
            "product": "ABSTAIN_UNCALIBRATED"}


def experiment() -> dict:
    legacy, design, starts, widths = designs()
    x_uniform, x_alias = kernels()
    A_train = design[:CALIBRATION_N]
    A_test = design[CALIBRATION_N:]
    truth_train = A_train @ x_alias
    truth_test = A_test @ x_alias
    singular = np.linalg.svd(A_train, compute_uv=False)
    noiseless = recover(A_train, truth_train)
    noise = np.random.default_rng(SEED_NOISE).normal(0.0, NOISE_SD, CALIBRATION_N)
    noisy = recover(A_train, truth_train + noise)

    def score(x):
        return {"heldout_mae": float(np.mean(np.abs(A_test @ x - truth_test))),
                "mass_l1_error": float(np.sum(np.abs(x - x_alias))),
                "minimum_mass": float(np.min(x)),
                "mass_sum": float(np.sum(x))}

    legacy_diff = float(np.max(np.abs(legacy @ (x_uniform - x_alias))))
    heldout_difference = np.abs(A_test @ (x_uniform - x_alias))
    result = {
        "study": "E002-425",
        "frozen_protocol": "E002_425_FROZEN.md",
        "provenance": "exact synthetic rectangular pulses; no camera, photodiode, or human",
        "bins": BINS, "bin_width_ms": BIN_MS,
        "legacy_observations": int(legacy.shape[0]),
        "legacy_rank": int(np.linalg.matrix_rank(legacy)),
        "legacy_alias_max_difference": legacy_diff,
        "calibration_observations": CALIBRATION_N,
        "heldout_observations": HELDOUT_N,
        "design_seed": SEED_DESIGN,
        "noise_seed": SEED_NOISE,
        "noise_sd": NOISE_SD,
        "calibration_rank": int(np.linalg.matrix_rank(A_train)),
        "calibration_min_singular_value": float(singular[-1]),
        "calibration_condition_number": float(singular[0] / singular[-1]),
        "heldout_max_kernel_separation": float(np.max(heldout_difference)),
        "heldout_uniform_wrong_model_mae": float(np.mean(heldout_difference)),
        "noiseless_recovery": score(noiseless),
        "noisy_recovery": score(noisy),
        "policy": policy(),
    }
    result["frozen_tests"] = {
        "H1_legacy_rank_deficient_and_aliases": result["legacy_rank"] < BINS
            and legacy_diff < 1e-12,
        "H2_offgrid_full_column_rank": result["calibration_rank"] == BINS,
        "H3_heldout_discriminates_fixed_alias":
            result["heldout_max_kernel_separation"] > 0.01,
        "H4_noiseless_recovery": result["noiseless_recovery"]["heldout_mae"] < 1e-8
            and result["noiseless_recovery"]["mass_l1_error"] < 1e-5,
        "H5_noisy_recovery": result["noisy_recovery"]["heldout_mae"] < 0.01
            and result["noisy_recovery"]["mass_l1_error"] < 0.25,
        "H6_no_physical_claim": not policy()["product_claim_authorized"]
            and policy()["product"] == "ABSTAIN_UNCALIBRATED",
    }
    return result


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
