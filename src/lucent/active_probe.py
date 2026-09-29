from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np


@dataclass(frozen=True)
class ProbeConfig:
    total_seconds: float = 5.0
    dt: float = 0.05
    segment_seconds: float = 0.5
    low_level: float = 0.10
    high_level: float = 0.95
    high_segments: int = 3
    measurement_noise_mm: float = 0.05

    @property
    def n_segments(self) -> int:
        return int(round(self.total_seconds / self.segment_seconds))

    @property
    def n_steps(self) -> int:
        return int(round(self.total_seconds / self.dt))


THETA_MEAN = np.array([5.0, 0.75, 0.25, 0.45, 1.20], dtype=float)
THETA_SD = np.array([0.50, 0.20, 0.06, 0.12, 0.25], dtype=float)
STATE_INDEX = np.array([1, 2, 3, 4])


def level_to_luminance(level: np.ndarray | float) -> np.ndarray:
    """Map normalized display level to a log-spaced 1..200 cd/m^2 surrogate."""

    x = np.asarray(level, dtype=float)
    return np.exp(np.log(1.0) + (np.log(200.0) - np.log(1.0)) * x)


def sample_parameter_population(
    seed: int,
    n: int,
    *,
    scale: float,
) -> np.ndarray:
    """Sample a bounded heterogeneous surrogate population."""

    rng = np.random.default_rng(seed)
    samples: list[np.ndarray] = []

    for _ in range(n):
        theta = THETA_MEAN + rng.normal(0.0, THETA_SD * scale)
        theta[0] = np.clip(theta[0], 4.0, 6.5)
        theta[1] = np.clip(theta[1], 0.30, 1.30)
        theta[2] = np.clip(theta[2], 0.12, 0.45)
        theta[3] = np.clip(theta[3], 0.20, 0.90)
        theta[4] = np.clip(theta[4], 0.60, 2.20)
        samples.append(theta)

    return np.asarray(samples)


def simulate_pupil(
    probe: np.ndarray,
    theta: np.ndarray,
    config: ProbeConfig = ProbeConfig(),
) -> np.ndarray:
    """Literature-inspired delayed asymmetric PLR surrogate.

    theta = [baseline_diameter, luminance_gain, latency, tau_constrict, tau_dilate]

    This is a design surrogate, not a validated biological model.
    """

    baseline, gain, latency, tau_c, tau_d = np.asarray(theta, dtype=float)

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


def finite_difference_jacobian(
    probe: np.ndarray,
    theta: np.ndarray,
    config: ProbeConfig = ProbeConfig(),
) -> np.ndarray:
    """Sensitivity of the pupil trace to the surrogate parameters."""

    theta = np.asarray(theta, dtype=float)
    jac = np.empty((config.n_steps, len(theta)), dtype=float)

    for j in range(len(theta)):
        step = max(abs(theta[j]) * 2e-3, 1e-4)
        plus = theta.copy()
        minus = theta.copy()
        plus[j] += step
        minus[j] -= step
        jac[:, j] = (
            simulate_pupil(probe, plus, config)
            - simulate_pupil(probe, minus, config)
        ) / (2.0 * step)

    return jac


def information_gain(
    probe: np.ndarray,
    theta: np.ndarray,
    config: ProbeConfig = ProbeConfig(),
) -> float:
    """Bayesian D-optimal information gain for dynamic parameters."""

    prior_cov = np.diag(THETA_SD**2)
    prior_precision = np.diag(1.0 / (THETA_SD**2))

    jac = finite_difference_jacobian(probe, theta, config)
    fisher = jac.T @ jac / (config.measurement_noise_mm**2)
    posterior = np.linalg.inv(prior_precision + fisher)

    prior_state = prior_cov[np.ix_(STATE_INDEX, STATE_INDEX)]
    post_state = posterior[np.ix_(STATE_INDEX, STATE_INDEX)]

    logdet_prior = np.linalg.slogdet(prior_state)[1]
    logdet_post = np.linalg.slogdet(post_state)[1]

    return float(0.5 * (logdet_prior - logdet_post))


def expected_information_gain(
    probe: np.ndarray,
    population: np.ndarray,
    config: ProbeConfig = ProbeConfig(),
) -> float:
    return float(
        np.mean([information_gain(probe, theta, config) for theta in population])
    )


def equal_exposure_probes(
    config: ProbeConfig = ProbeConfig(),
):
    """Enumerate binary probes with identical high-luminance exposure."""

    for high_positions in combinations(
        range(1, config.n_segments),
        config.high_segments,
    ):
        probe = np.full(config.n_segments, config.low_level, dtype=float)
        probe[list(high_positions)] = config.high_level
        yield high_positions, probe


def best_equal_exposure_probe(
    design_population: np.ndarray,
    config: ProbeConfig = ProbeConfig(),
):
    best_score = -np.inf
    best_positions: tuple[int, ...] | None = None
    best_probe: np.ndarray | None = None

    for positions, probe in equal_exposure_probes(config):
        score = expected_information_gain(probe, design_population, config)
        if score > best_score:
            best_score = score
            best_positions = positions
            best_probe = probe

    assert best_positions is not None and best_probe is not None
    return best_score, best_positions, best_probe
