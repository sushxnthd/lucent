from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np

from .active_probe import THETA_MEAN, THETA_SD, level_to_luminance


@dataclass(frozen=True)
class MultimodalConfig:
    total_seconds: float = 5.0
    dt: float = 0.05
    segment_seconds: float = 0.5
    low_level: float = 0.10
    high_level: float = 0.95
    high_segments: int = 3
    pupil_noise_mm: float = 0.05
    saccade_velocity_noise: float = 0.04

    @property
    def n_segments(self) -> int:
        return int(round(self.total_seconds / self.segment_seconds))

    @property
    def n_steps(self) -> int:
        return int(round(self.total_seconds / self.dt))


PUPIL_EFFECT_MEAN = np.array([0.30, 0.00, 0.07, 0.10, 0.18], dtype=float)
PUPIL_EFFECT_SD = np.array([0.08, 0.12, 0.025, 0.035, 0.06], dtype=float)


def sample_nuisance(seed: int, n: int, scale: float) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out: list[np.ndarray] = []

    for _ in range(n):
        theta = THETA_MEAN + rng.normal(0.0, THETA_SD * scale)
        theta[0] = np.clip(theta[0], 4.0, 6.5)
        theta[1] = np.clip(theta[1], 0.30, 1.30)
        theta[2] = np.clip(theta[2], 0.12, 0.45)
        theta[3] = np.clip(theta[3], 0.20, 0.90)
        theta[4] = np.clip(theta[4], 0.60, 2.20)

        # Stable, person-specific normalized saccade-velocity baseline.
        saccade_baseline = np.clip(1.0 + rng.normal(0.0, 0.12 * scale), 0.65, 1.35)
        out.append(np.r_[theta, saccade_baseline])

    return np.asarray(out)


def sample_state_effects(seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out: list[np.ndarray] = []

    for _ in range(n):
        pupil = PUPIL_EFFECT_MEAN + rng.normal(0.0, PUPIL_EFFECT_SD)
        pupil[0] = np.clip(pupil[0], 0.12, 0.50)
        pupil[1] = np.clip(pupil[1], -0.25, 0.25)
        pupil[2] = np.clip(pupil[2], 0.02, 0.14)
        pupil[3] = np.clip(pupil[3], 0.03, 0.20)
        pupil[4] = np.clip(pupil[4], 0.05, 0.35)

        # Literature supports reduced voluntary saccade peak velocity with fatigue.
        # This normalized reduction is intentionally broad, not presented as a
        # fitted population estimate.
        saccade_drop = np.clip(rng.normal(0.16, 0.05), 0.05, 0.30)
        out.append(np.r_[pupil, saccade_drop])

    return np.asarray(out)


def simulate_pupil(
    probe: np.ndarray,
    nuisance: np.ndarray,
    state: float,
    effect: np.ndarray,
    config: MultimodalConfig,
) -> np.ndarray:
    baseline, gain, latency, tau_c, tau_d = nuisance
    d_base, d_gain, d_latency, d_tau_c, d_tau_d = effect

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


def simulate_observation(
    probe: np.ndarray,
    saccade_events: tuple[int, ...],
    nuisance: np.ndarray,
    state: float,
    state_effect: np.ndarray,
    config: MultimodalConfig,
) -> np.ndarray:
    pupil = simulate_pupil(
        probe,
        nuisance[:5],
        state,
        state_effect[:5],
        config,
    )

    baseline_velocity = nuisance[5]
    velocity_drop = state_effect[5]
    saccades = np.asarray(
        [
            baseline_velocity * (1.0 - velocity_drop * state)
            for _ in saccade_events
        ],
        dtype=float,
    )

    return np.r_[pupil, saccades]


def observation_jacobian(
    probe: np.ndarray,
    saccade_events: tuple[int, ...],
    nuisance: np.ndarray,
    state: float,
    state_effect: np.ndarray,
    config: MultimodalConfig,
) -> np.ndarray:
    columns: list[np.ndarray] = []

    state_step = 2e-3
    columns.append(
        (
            simulate_observation(
                probe,
                saccade_events,
                nuisance,
                state + state_step,
                state_effect,
                config,
            )
            - simulate_observation(
                probe,
                saccade_events,
                nuisance,
                state - state_step,
                state_effect,
                config,
            )
        )
        / (2.0 * state_step)
    )

    for j in range(len(nuisance)):
        step = max(abs(nuisance[j]) * 3e-3, 1e-4)
        plus = nuisance.copy()
        minus = nuisance.copy()
        plus[j] += step
        minus[j] -= step

        columns.append(
            (
                simulate_observation(
                    probe,
                    saccade_events,
                    plus,
                    state,
                    state_effect,
                    config,
                )
                - simulate_observation(
                    probe,
                    saccade_events,
                    minus,
                    state,
                    state_effect,
                    config,
                )
            )
            / (2.0 * step)
        )

    return np.column_stack(columns)


def state_information_gain(
    probe: np.ndarray,
    saccade_events: tuple[int, ...],
    nuisance: np.ndarray,
    state_effect: np.ndarray,
    config: MultimodalConfig,
    *,
    nuisance_prior_scale: float = 0.75,
    state_prior_variance: float = 0.25,
) -> float:
    jac = observation_jacobian(
        probe,
        saccade_events,
        nuisance,
        0.5,
        state_effect,
        config,
    )

    noise = np.r_[
        np.full(config.n_steps, config.pupil_noise_mm),
        np.full(len(saccade_events), config.saccade_velocity_noise),
    ]

    weighted = jac / noise[:, None]
    fisher = weighted.T @ weighted

    nuisance_sd = np.r_[THETA_SD, 0.12] * nuisance_prior_scale
    nuisance_prior_precision = np.diag(1.0 / (nuisance_sd**2))

    f_ss = fisher[0, 0]
    f_sn = fisher[0, 1:]
    f_nn = fisher[1:, 1:] + nuisance_prior_precision

    efficient = f_ss - f_sn @ np.linalg.solve(f_nn, f_sn.T)
    efficient = max(float(efficient), 0.0)

    return float(0.5 * np.log1p(state_prior_variance * efficient))


def equal_exposure_probes(config: MultimodalConfig):
    for positions in combinations(
        range(1, config.n_segments),
        config.high_segments,
    ):
        probe = np.full(config.n_segments, config.low_level, dtype=float)
        probe[list(positions)] = config.high_level
        yield positions, probe
