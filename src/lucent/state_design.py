from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np

from .active_probe import THETA_MEAN, THETA_SD, level_to_luminance


@dataclass(frozen=True)
class StateProbeConfig:
    total_seconds: float
    dt: float = 0.05
    segment_seconds: float = 0.5
    low_level: float = 0.10
    high_level: float = 0.95
    high_fraction: float = 0.30
    measurement_noise_mm: float = 0.05

    @property
    def n_segments(self) -> int:
        return int(round(self.total_seconds / self.segment_seconds))

    @property
    def n_steps(self) -> int:
        return int(round(self.total_seconds / self.dt))

    @property
    def high_segments(self) -> int:
        return min(
            self.n_segments - 1,
            max(1, round(self.high_fraction * self.n_segments)),
        )


# Broad literature-informed directions for a latent fatigue / reduced-alertness
# perturbation. These are NOT claimed as fitted population effect sizes.
#
# [baseline_drop_mm, gain_shift, latency_increase_s,
#  constriction_tau_increase_s, dilation_tau_increase_s]
STATE_EFFECT_MEAN = np.array([0.30, 0.00, 0.07, 0.10, 0.18], dtype=float)
STATE_EFFECT_SD = np.array([0.08, 0.12, 0.025, 0.035, 0.06], dtype=float)


def sample_state_effects(seed: int, n: int) -> np.ndarray:
    """Sample heterogeneous state-effect directions.

    Gain is intentionally allowed to change in either direction because the
    fatigue / recovery literature does not support one universal phasic-gain
    direction across paradigms.
    """

    rng = np.random.default_rng(seed)
    out: list[np.ndarray] = []

    for _ in range(n):
        effect = STATE_EFFECT_MEAN + rng.normal(0.0, STATE_EFFECT_SD)
        effect[0] = np.clip(effect[0], 0.12, 0.50)
        effect[1] = np.clip(effect[1], -0.25, 0.25)
        effect[2] = np.clip(effect[2], 0.02, 0.14)
        effect[3] = np.clip(effect[3], 0.03, 0.20)
        effect[4] = np.clip(effect[4], 0.05, 0.35)
        out.append(effect)

    return np.asarray(out)


def sample_nuisance_population(seed: int, n: int, scale: float) -> np.ndarray:
    """Sample stable person/device nuisance parameters."""

    rng = np.random.default_rng(seed)
    out: list[np.ndarray] = []

    for _ in range(n):
        theta = THETA_MEAN + rng.normal(0.0, THETA_SD * scale)
        theta[0] = np.clip(theta[0], 4.0, 6.5)
        theta[1] = np.clip(theta[1], 0.30, 1.30)
        theta[2] = np.clip(theta[2], 0.12, 0.45)
        theta[3] = np.clip(theta[3], 0.20, 0.90)
        theta[4] = np.clip(theta[4], 0.60, 2.20)
        out.append(theta)

    return np.asarray(out)


def simulate_state_response(
    probe: np.ndarray,
    nuisance: np.ndarray,
    state: float,
    state_effect: np.ndarray,
    config: StateProbeConfig,
) -> np.ndarray:
    """Delayed asymmetric pupil surrogate with a latent state perturbation."""

    baseline, gain, latency, tau_c, tau_d = np.asarray(nuisance, dtype=float)
    d_base, d_gain, d_latency, d_tau_c, d_tau_d = np.asarray(
        state_effect,
        dtype=float,
    )

    baseline = baseline - d_base * state
    gain = gain + d_gain * state
    latency = latency + d_latency * state
    tau_c = tau_c + d_tau_c * state
    tau_d = tau_d + d_tau_d * state

    repeats = int(round(config.segment_seconds / config.dt))
    level = np.repeat(np.asarray(probe, dtype=float), repeats)[: config.n_steps]
    luminance = level_to_luminance(level)

    equilibrium = np.clip(
        baseline - gain * np.log(luminance / 20.0),
        2.0,
        8.0,
    )

    time = np.arange(config.n_steps) * config.dt
    delayed = np.interp(
        time - latency,
        time,
        equilibrium,
        left=baseline,
        right=equilibrium[-1],
    )

    pupil = np.empty(config.n_steps, dtype=float)
    pupil[0] = baseline

    for i in range(1, config.n_steps):
        tau = tau_c if delayed[i] < pupil[i - 1] else tau_d
        pupil[i] = pupil[i - 1] + (
            config.dt * (delayed[i] - pupil[i - 1]) / max(tau, 0.05)
        )

    return pupil


def state_nuisance_jacobian(
    probe: np.ndarray,
    nuisance: np.ndarray,
    state: float,
    state_effect: np.ndarray,
    config: StateProbeConfig,
) -> np.ndarray:
    """Jacobian with columns [state, five nuisance parameters]."""

    state_step = 1e-3
    columns = [
        (
            simulate_state_response(
                probe,
                nuisance,
                state + state_step,
                state_effect,
                config,
            )
            - simulate_state_response(
                probe,
                nuisance,
                state - state_step,
                state_effect,
                config,
            )
        )
        / (2.0 * state_step)
    ]

    for j in range(len(nuisance)):
        step = max(abs(nuisance[j]) * 2e-3, 1e-4)
        plus = nuisance.copy()
        minus = nuisance.copy()
        plus[j] += step
        minus[j] -= step
        columns.append(
            (
                simulate_state_response(
                    probe,
                    plus,
                    state,
                    state_effect,
                    config,
                )
                - simulate_state_response(
                    probe,
                    minus,
                    state,
                    state_effect,
                    config,
                )
            )
            / (2.0 * step)
        )

    return np.column_stack(columns)


def effective_state_information(
    probe: np.ndarray,
    nuisance: np.ndarray,
    state_effect: np.ndarray,
    config: StateProbeConfig,
    *,
    nuisance_prior_scale: float = 1.0,
    state: float = 0.5,
) -> float:
    """Efficient Fisher information for state after nuisance projection.

    Let the Fisher matrix be partitioned into state and nuisance blocks:

        F = [[F_ss, F_sn],
             [F_ns, F_nn]]

    and let Lambda_h be nuisance prior precision from longitudinal history.
    The efficient state information is the Schur complement

        J_s = F_ss - F_sn (F_nn + Lambda_h)^-1 F_ns.

    Smaller nuisance_prior_scale means a tighter prior / better personal
    baseline.
    """

    if nuisance_prior_scale <= 0:
        raise ValueError("nuisance_prior_scale must be positive")

    jac = state_nuisance_jacobian(
        probe,
        nuisance,
        state,
        state_effect,
        config,
    )
    fisher = jac.T @ jac / (config.measurement_noise_mm**2)

    prior_sd = THETA_SD * nuisance_prior_scale
    nuisance_prior_precision = np.diag(1.0 / (prior_sd**2))

    f_ss = fisher[0, 0]
    f_sn = fisher[0, 1:]
    f_nn = fisher[1:, 1:] + nuisance_prior_precision

    efficient = f_ss - f_sn @ np.linalg.solve(f_nn, f_sn.T)
    return max(float(efficient), 0.0)


def state_information_gain(
    probe: np.ndarray,
    nuisance: np.ndarray,
    state_effect: np.ndarray,
    config: StateProbeConfig,
    *,
    nuisance_prior_scale: float = 1.0,
    state_prior_variance: float = 0.25,
    state: float = 0.5,
) -> float:
    efficient = effective_state_information(
        probe,
        nuisance,
        state_effect,
        config,
        nuisance_prior_scale=nuisance_prior_scale,
        state=state,
    )
    return float(0.5 * np.log1p(state_prior_variance * efficient))


def equal_exposure_state_probes(config: StateProbeConfig):
    for positions in combinations(
        range(1, config.n_segments),
        config.high_segments,
    ):
        probe = np.full(config.n_segments, config.low_level, dtype=float)
        probe[list(positions)] = config.high_level
        yield positions, probe


def best_state_probe(
    nuisance_population: np.ndarray,
    state_effect_population: np.ndarray,
    config: StateProbeConfig,
    *,
    nuisance_prior_scale: float,
):
    best_score = -np.inf
    best_positions: tuple[int, ...] | None = None
    best_probe: np.ndarray | None = None

    for positions, probe in equal_exposure_state_probes(config):
        values = [
            state_information_gain(
                probe,
                nuisance,
                effect,
                config,
                nuisance_prior_scale=nuisance_prior_scale,
            )
            for nuisance in nuisance_population
            for effect in state_effect_population
        ]
        score = float(np.mean(values))

        if score > best_score:
            best_score = score
            best_positions = positions
            best_probe = probe

    assert best_positions is not None and best_probe is not None
    return best_score, best_positions, best_probe
