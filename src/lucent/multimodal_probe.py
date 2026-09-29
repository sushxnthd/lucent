from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PursuitConfig:
    dt: float = 0.05
    measurement_noise: float = 0.10


PURSUIT_NUISANCE_MEAN = np.array([0.90, 0.18], dtype=float)
PURSUIT_NUISANCE_SD = np.array([0.08, 0.04], dtype=float)


def sample_pursuit_nuisance(
    seed: int,
    n: int,
    *,
    scale: float,
) -> np.ndarray:
    """Sample [steady-state gain, response time constant]."""

    rng = np.random.default_rng(seed)
    out: list[np.ndarray] = []

    for _ in range(n):
        value = PURSUIT_NUISANCE_MEAN + rng.normal(
            0.0,
            PURSUIT_NUISANCE_SD * scale,
        )
        value[0] = np.clip(value[0], 0.65, 1.05)
        value[1] = np.clip(value[1], 0.08, 0.35)
        out.append(value)

    return np.asarray(out)


def sample_pursuit_state_effects(
    seed: int,
    n: int,
    *,
    gain_drop_mean: float,
    tau_increase_mean: float,
) -> np.ndarray:
    """Sample state effects [gain drop, tau increase].

    These are sensitivity-analysis priors, not fitted human effect sizes.
    """

    rng = np.random.default_rng(seed)
    out: list[np.ndarray] = []

    gain_sd = max(0.01, gain_drop_mean * 0.25)
    tau_sd = max(
        0.005,
        tau_increase_mean * 0.35 if tau_increase_mean > 0 else 0.005,
    )

    for _ in range(n):
        effect = np.array(
            [
                rng.normal(gain_drop_mean, gain_sd),
                rng.normal(tau_increase_mean, tau_sd),
            ],
            dtype=float,
        )
        effect[0] = np.clip(effect[0], 0.0, 0.30)
        effect[1] = np.clip(effect[1], 0.0, 0.10)
        out.append(effect)

    return np.asarray(out)


def simulate_pursuit(
    frequency_hz: float,
    nuisance: np.ndarray,
    state: float,
    state_effect: np.ndarray,
    *,
    total_seconds: float,
    config: PursuitConfig,
) -> np.ndarray:
    """First-order smooth-pursuit surrogate.

    The target follows a sinusoid. State can reduce pursuit gain and slow the
    response time constant. The model is a design surrogate, not a digital twin.
    """

    baseline_gain, baseline_tau = np.asarray(nuisance, dtype=float)
    gain_drop, tau_increase = np.asarray(state_effect, dtype=float)

    gain = baseline_gain - gain_drop * state
    tau = baseline_tau + tau_increase * state

    n_steps = int(round(total_seconds / config.dt))
    time = np.arange(n_steps, dtype=float) * config.dt
    target = np.sin(2.0 * np.pi * frequency_hz * time)

    gaze = np.zeros(n_steps, dtype=float)

    for i in range(1, n_steps):
        gaze[i] = gaze[i - 1] + (
            config.dt
            * (gain * target[i] - gaze[i - 1])
            / max(tau, 0.03)
        )

    return gaze


def pursuit_state_information(
    frequency_hz: float,
    nuisance: np.ndarray,
    state_effect: np.ndarray,
    *,
    total_seconds: float,
    nuisance_prior_scale: float,
    measurement_noise: float,
    state: float = 0.5,
) -> float:
    """Efficient Fisher information for state after pursuit nuisance projection."""

    config = PursuitConfig(measurement_noise=measurement_noise)

    h = 1e-3
    state_column = (
        simulate_pursuit(
            frequency_hz,
            nuisance,
            state + h,
            state_effect,
            total_seconds=total_seconds,
            config=config,
        )
        - simulate_pursuit(
            frequency_hz,
            nuisance,
            state - h,
            state_effect,
            total_seconds=total_seconds,
            config=config,
        )
    ) / (2.0 * h)

    nuisance_columns = []
    for j in range(len(nuisance)):
        step = max(abs(nuisance[j]) * 2e-3, 1e-4)
        plus = nuisance.copy()
        minus = nuisance.copy()
        plus[j] += step
        minus[j] -= step

        nuisance_columns.append(
            (
                simulate_pursuit(
                    frequency_hz,
                    plus,
                    state,
                    state_effect,
                    total_seconds=total_seconds,
                    config=config,
                )
                - simulate_pursuit(
                    frequency_hz,
                    minus,
                    state,
                    state_effect,
                    total_seconds=total_seconds,
                    config=config,
                )
            )
            / (2.0 * step)
        )

    jacobian = np.column_stack([state_column, *nuisance_columns])
    fisher = (
        jacobian.T @ jacobian
        / (measurement_noise**2)
    )

    prior_sd = PURSUIT_NUISANCE_SD * nuisance_prior_scale
    nuisance_prior_precision = np.diag(1.0 / (prior_sd**2))

    f_ss = fisher[0, 0]
    f_sn = fisher[0, 1:]
    f_nn = fisher[1:, 1:] + nuisance_prior_precision

    efficient = f_ss - f_sn @ np.linalg.solve(f_nn, f_sn.T)
    return max(float(efficient), 0.0)


def joint_state_information_gain(
    pupil_information: np.ndarray,
    pursuit_information: np.ndarray,
    *,
    state_prior_variance: float = 0.25,
) -> np.ndarray:
    """Combine efficient state information from conditionally independent channels."""

    pupil_information = np.asarray(pupil_information, dtype=float)
    pursuit_information = np.asarray(pursuit_information, dtype=float)

    if pupil_information.shape != pursuit_information.shape:
        raise ValueError("information arrays must have identical shape")

    total = pupil_information + pursuit_information
    return 0.5 * np.log1p(state_prior_variance * total)
