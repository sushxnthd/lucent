"""APST5-SIM-003: concurrent pupil + smooth-pursuit temporal compression.

The experiment asks whether measuring an active pursuit response at the same
time as the pupil response can reduce the scan duration required to reach the
state-information level of a five-second pupil-only probe.

This is a model-based sensitivity analysis, not a human-validation result.
"""

from __future__ import annotations

import numpy as np

from lucent.multimodal_probe import (
    joint_state_information_gain,
    pursuit_state_information,
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


def evaluate_pupil(probe, total_seconds: float):
    nuisance = sample_nuisance_population(21, 30, scale=0.75)
    effects = sample_state_effects(22, 10)
    config = StateProbeConfig(total_seconds=total_seconds)

    return np.asarray(
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


def evaluate_pupil_information(probe, total_seconds: float):
    nuisance = sample_nuisance_population(21, 30, scale=0.75)
    effects = sample_state_effects(22, 10)
    config = StateProbeConfig(total_seconds=total_seconds)

    # state_information_gain = .5 log(1 + .25 J)
    # invert it so the independent pursuit information can be added before
    # applying the state prior.
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

    best = None
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

        if best is None or score > best[0]:
            best = (score, float(frequency))

    assert best is not None
    return best[1]


def evaluate_pursuit_information(
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


def evaluate_duration(total_seconds: float, baseline_5s: float):
    _, probe = optimize_pupil(total_seconds)
    pupil_information = evaluate_pupil_information(
        probe,
        total_seconds,
    )

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

                pursuit_information = evaluate_pursuit_information(
                    total_seconds,
                    frequency=frequency,
                    gain_drop_mean=gain_drop,
                    tau_increase_mean=tau_increase,
                    measurement_noise=noise,
                )

                joint_ig = joint_state_information_gain(
                    pupil_information,
                    pursuit_information,
                )
                mean_joint = float(np.mean(joint_ig))

                rows.append(
                    {
                        "gain_drop": gain_drop,
                        "tau_increase": tau_increase,
                        "noise": noise,
                        "frequency": frequency,
                        "joint_ig": mean_joint,
                        "ratio": mean_joint / baseline_5s,
                    }
                )

    return rows


def summarize(label: str, rows):
    ratios = np.asarray([row["ratio"] for row in rows], dtype=float)

    print(label)
    print("-" * len(label))
    print(f"grid cells: {len(rows)}")
    print(f"beats 5s pupil-only: {int(np.sum(ratios > 1.0))}/{len(rows)}")
    print(f"median ratio: {np.median(ratios):.6f}x")
    print(f"minimum ratio: {np.min(ratios):.6f}x")
    print(f"maximum ratio: {np.max(ratios):.6f}x")

    weakest = rows[int(np.argmin(ratios))]
    strongest = rows[int(np.argmax(ratios))]

    print(
        "weakest cell: "
        f"gain_drop={weakest['gain_drop']:.3f}, "
        f"tau_increase={weakest['tau_increase']:.3f}, "
        f"noise={weakest['noise']:.3f}, "
        f"f={weakest['frequency']:.2f}Hz"
    )
    print(
        "strongest cell: "
        f"gain_drop={strongest['gain_drop']:.3f}, "
        f"tau_increase={strongest['tau_increase']:.3f}, "
        f"noise={strongest['noise']:.3f}, "
        f"f={strongest['frequency']:.2f}Hz"
    )
    print()


def main() -> None:
    positions_5s, probe_5s = optimize_pupil(5.0)
    baseline_5s_values = evaluate_pupil(probe_5s, 5.0)
    baseline_5s = float(np.mean(baseline_5s_values))

    print("APST5-SIM-003: concurrent multimodal temporal compression")
    print("=" * 76)
    print(f"5s pupil-only probe positions: {positions_5s}")
    print(f"5s pupil-only held-out state IG: {baseline_5s:.6f} nats")
    print()

    rows_2s = evaluate_duration(2.0, baseline_5s)
    rows_3s = evaluate_duration(3.0, baseline_5s)

    summarize("2-second concurrent pupil + pursuit", rows_2s)
    summarize("3-second concurrent pupil + pursuit", rows_3s)


if __name__ == "__main__":
    main()
