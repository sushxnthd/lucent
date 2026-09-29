
"""APST5-SIM-004: multimodal redundancy stress test.

APST5-SIM-003 assumes conditionally independent pupil and pursuit information.
This experiment deliberately weakens that assumption.

For each held-out pupil/pursuit pair, only a fraction kappa of the weaker
channel's state information is allowed to count as incremental:

    J_joint = max(J_pupil, J_pursuit) + kappa * min(J_pupil, J_pursuit)

kappa=1 is the additive result.
kappa=0 means complete redundancy and no multimodal bonus beyond the stronger
single channel.

This is an information-overlap sensitivity analysis, not a biological model.
"""

from __future__ import annotations

import numpy as np

from lucent.multimodal_probe import (
    pursuit_state_information,
    redundant_joint_state_information_gain,
    sample_pursuit_nuisance,
    sample_pursuit_state_effects,
)
from lucent.state_design import (
    StateProbeConfig,
    best_state_probe,
    sample_nuisance_population,
    sample_state_effects,
    state_information_gain,
)


FREQUENCIES = np.round(np.arange(0.3, 1.51, 0.1), 2)
GAIN_DROP_GRID = [0.03, 0.06, 0.10, 0.14, 0.18]
TAU_INCREASE_GRID = [0.0, 0.015, 0.03, 0.05]
NOISE_GRID = [0.05, 0.10, 0.15, 0.20]
REDUNDANCY_GRID = [1.0, 0.75, 0.50, 0.25, 0.0]


def optimize_pupil(total_seconds: float):
    design_nuisance = sample_nuisance_population(11, 8, scale=0.55)
    design_effects = sample_state_effects(12, 5)
    config = StateProbeConfig(total_seconds=total_seconds)
    _, positions, probe = best_state_probe(
        design_nuisance,
        design_effects,
        config,
        nuisance_prior_scale=1.0,
    )
    return positions, probe


def pupil_information(probe, total_seconds: float):
    nuisance = sample_nuisance_population(21, 30, scale=0.75)
    effects = sample_state_effects(22, 10)
    config = StateProbeConfig(total_seconds=total_seconds)

    ig = np.asarray(
        [
            state_information_gain(
                probe,
                n,
                e,
                config,
                nuisance_prior_scale=1.0,
                state_prior_variance=0.25,
            )
            for n in nuisance
            for e in effects
        ],
        dtype=float,
    )
    return (np.exp(2.0 * ig) - 1.0) / 0.25


def optimize_frequency(
    total_seconds: float,
    *,
    gain_drop_mean: float,
    tau_increase_mean: float,
    measurement_noise: float,
):
    nuisance = sample_pursuit_nuisance(13, 8, scale=0.55)
    effects = sample_pursuit_state_effects(
        14,
        5,
        gain_drop_mean=gain_drop_mean,
        tau_increase_mean=tau_increase_mean,
    )

    best_score = -np.inf
    best_frequency = None

    for frequency in FREQUENCIES:
        values = np.asarray(
            [
                pursuit_state_information(
                    frequency,
                    n,
                    e,
                    total_seconds=total_seconds,
                    nuisance_prior_scale=1.0,
                    measurement_noise=measurement_noise,
                )
                for n in nuisance
                for e in effects
            ],
            dtype=float,
        )
        score = float(np.mean(0.5 * np.log1p(0.25 * values)))
        if score > best_score:
            best_score = score
            best_frequency = float(frequency)

    assert best_frequency is not None
    return best_frequency


def pursuit_information(
    total_seconds: float,
    *,
    frequency: float,
    gain_drop_mean: float,
    tau_increase_mean: float,
    measurement_noise: float,
):
    nuisance = sample_pursuit_nuisance(23, 30, scale=0.75)
    effects = sample_pursuit_state_effects(
        24,
        10,
        gain_drop_mean=gain_drop_mean,
        tau_increase_mean=tau_increase_mean,
    )

    return np.asarray(
        [
            pursuit_state_information(
                frequency,
                n,
                e,
                total_seconds=total_seconds,
                nuisance_prior_scale=1.0,
                measurement_noise=measurement_noise,
            )
            for n in nuisance
            for e in effects
        ],
        dtype=float,
    )


def condition_grid(total_seconds: float):
    _, pupil_probe = optimize_pupil(total_seconds)
    jp = pupil_information(pupil_probe, total_seconds)

    rows = []
    for gain_drop in GAIN_DROP_GRID:
        for tau_increase in TAU_INCREASE_GRID:
            for noise in NOISE_GRID:
                frequency = optimize_frequency(
                    total_seconds,
                    gain_drop_mean=gain_drop,
                    tau_increase_mean=tau_increase,
                    measurement_noise=noise,
                )
                jg = pursuit_information(
                    total_seconds,
                    frequency=frequency,
                    gain_drop_mean=gain_drop,
                    tau_increase_mean=tau_increase,
                    measurement_noise=noise,
                )
                rows.append((jp, jg))

    return rows


def five_second_pupil_baseline() -> float:
    _, probe = optimize_pupil(5.0)
    jp = pupil_information(probe, 5.0)
    return float(np.mean(0.5 * np.log1p(0.25 * jp)))


def summarize(total_seconds: float, rows, baseline: float):
    print(f"{total_seconds:.0f}-second scan")
    print("-" * 40)

    for incremental_fraction in REDUNDANCY_GRID:
        ratios = []
        for jp, jg in rows:
            ig = redundant_joint_state_information_gain(
                jp,
                jg,
                incremental_fraction=incremental_fraction,
            )
            ratios.append(float(np.mean(ig)) / baseline)

        ratios = np.asarray(ratios)
        print(
            f"kappa={incremental_fraction:0.2f}: "
            f"wins={int(np.sum(ratios > 1.0)):>2}/{len(ratios)} "
            f"median={np.median(ratios):.6f}x "
            f"min={np.min(ratios):.6f}x "
            f"max={np.max(ratios):.6f}x"
        )

    print()


def main() -> None:
    baseline = five_second_pupil_baseline()
    rows_2s = condition_grid(2.0)
    rows_3s = condition_grid(3.0)

    print("APST5-SIM-004: multimodal redundancy stress test")
    print("=" * 72)
    print(f"five-second pupil-only comparator: {baseline:.6f} nats")
    print()
    summarize(2.0, rows_2s, baseline)
    summarize(3.0, rows_3s, baseline)


if __name__ == "__main__":
    main()
