"""APST5-SIM-001: equal-exposure active-probe design.

This experiment is intentionally in silico. It tests whether stimulus timing
changes local parameter identifiability when total scan duration and total
high-luminance exposure are held fixed.

It is NOT evidence that Lucent can infer fatigue in humans.
"""

from __future__ import annotations

import numpy as np

from lucent.active_probe import (
    ProbeConfig,
    best_equal_exposure_probe,
    expected_information_gain,
    information_gain,
    level_to_luminance,
    sample_parameter_population,
)


DESIGN_SEED = 20260929
TEST_SEED = 1517


def build_probe(positions: tuple[int, ...], config: ProbeConfig) -> np.ndarray:
    probe = np.full(config.n_segments, config.low_level, dtype=float)
    probe[list(positions)] = config.high_level
    return probe


def heldout_summary(
    probe: np.ndarray,
    population: np.ndarray,
    config: ProbeConfig,
):
    values = np.asarray(
        [information_gain(probe, theta, config) for theta in population]
    )
    return {
        "mean": float(values.mean()),
        "std": float(values.std()),
        "p10": float(np.quantile(values, 0.10)),
        "median": float(np.quantile(values, 0.50)),
        "p90": float(np.quantile(values, 0.90)),
    }


def main() -> None:
    config = ProbeConfig()

    design_population = sample_parameter_population(
        DESIGN_SEED,
        32,
        scale=0.55,
    )
    heldout_population = sample_parameter_population(
        TEST_SEED,
        500,
        scale=0.70,
    )

    design_score, positions, optimized = best_equal_exposure_probe(
        design_population,
        config,
    )

    contiguous_candidates = []
    for start in range(1, config.n_segments - config.high_segments + 1):
        pos = tuple(range(start, start + config.high_segments))
        probe = build_probe(pos, config)
        score = expected_information_gain(probe, design_population, config)
        contiguous_candidates.append((score, pos, probe))

    contiguous_candidates.sort(reverse=True, key=lambda row: row[0])
    _, contiguous_positions, contiguous = contiguous_candidates[0]

    evenly_spaced_positions = (2, 5, 8)
    evenly_spaced = build_probe(evenly_spaced_positions, config)

    optimized_test = heldout_summary(optimized, heldout_population, config)
    contiguous_test = heldout_summary(contiguous, heldout_population, config)
    even_test = heldout_summary(evenly_spaced, heldout_population, config)

    delta_contiguous = optimized_test["mean"] - contiguous_test["mean"]
    posterior_volume_advantage = float(np.exp(2.0 * delta_contiguous))

    print("APST5-SIM-001")
    print("=" * 60)
    print("design combinations: 84")
    print(f"optimized high positions: {positions}")
    print(f"best contiguous positions: {contiguous_positions}")
    print(
        "optimized luminance surrogate (cd/m^2): "
        + np.array2string(
            np.round(level_to_luminance(optimized), 1),
            separator=", ",
        )
    )
    print()
    print(f"design-population IG: {design_score:.6f} nats")
    print()
    print("held-out population (n=500)")
    print(f"optimized:       {optimized_test['mean']:.6f} nats")
    print(f"best contiguous: {contiguous_test['mean']:.6f} nats")
    print(f"evenly spaced:   {even_test['mean']:.6f} nats")
    print()
    print(
        "gain vs best contiguous: "
        f"{100.0 * (optimized_test['mean'] / contiguous_test['mean'] - 1.0):.3f}%"
    )
    print(
        "gain vs evenly spaced:   "
        f"{100.0 * (optimized_test['mean'] / even_test['mean'] - 1.0):.3f}%"
    )
    print(
        "posterior uncertainty-volume advantage vs best contiguous: "
        f"{posterior_volume_advantage:.3f}x"
    )


if __name__ == "__main__":
    main()
