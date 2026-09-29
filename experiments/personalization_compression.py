"""APST5-SIM-002: personalization as temporal compression.

The experiment asks whether a longitudinal personal baseline can substitute for
measurement time by reducing uncertainty about stable nuisance parameters.

The result is model-based and is not a human performance claim.
"""

from __future__ import annotations

import numpy as np

from lucent.state_design import (
    StateProbeConfig,
    best_state_probe,
    sample_nuisance_population,
    sample_state_effects,
    state_information_gain,
)


DESIGN_NUISANCE_SEED = 700
DESIGN_EFFECT_SEED = 701
TEST_NUISANCE_SEED = 702
TEST_EFFECT_SEED = 703


def evaluate(
    probe,
    nuisance_population,
    effect_population,
    config,
    prior_scale,
):
    values = np.asarray(
        [
            state_information_gain(
                probe,
                nuisance,
                effect,
                config,
                nuisance_prior_scale=prior_scale,
            )
            for nuisance in nuisance_population
            for effect in effect_population
        ]
    )
    return {
        "mean": float(values.mean()),
        "median": float(np.median(values)),
        "p10": float(np.quantile(values, 0.10)),
        "p90": float(np.quantile(values, 0.90)),
    }


def independent_replications(probe_2s, probe_5s):
    ratios = []

    for rep in range(10):
        nuisance = sample_nuisance_population(
            7000 + rep,
            25,
            scale=0.75,
        )
        effects = sample_state_effects(8000 + rep, 8)

        two_second = evaluate(
            probe_2s,
            nuisance,
            effects,
            StateProbeConfig(total_seconds=2.0),
            prior_scale=0.75,
        )
        five_second = evaluate(
            probe_5s,
            nuisance,
            effects,
            StateProbeConfig(total_seconds=5.0),
            prior_scale=1.0,
        )
        ratios.append(two_second["mean"] / five_second["mean"])

    return np.asarray(ratios)


def main() -> None:
    design_nuisance = sample_nuisance_population(
        DESIGN_NUISANCE_SEED,
        10,
        scale=0.55,
    )
    design_effects = sample_state_effects(DESIGN_EFFECT_SEED, 6)

    test_nuisance = sample_nuisance_population(
        TEST_NUISANCE_SEED,
        30,
        scale=0.75,
    )
    test_effects = sample_state_effects(TEST_EFFECT_SEED, 10)

    config_5s = StateProbeConfig(total_seconds=5.0)
    _, pos_5s, probe_5s = best_state_probe(
        design_nuisance,
        design_effects,
        config_5s,
        nuisance_prior_scale=1.0,
    )

    baseline_5s = evaluate(
        probe_5s,
        test_nuisance,
        test_effects,
        config_5s,
        prior_scale=1.0,
    )

    print("APST5-SIM-002: personalization compression")
    print("=" * 64)
    print(f"population 5 s probe: {pos_5s}")
    print(f"population 5 s held-out mean IG: {baseline_5s['mean']:.6f}")
    print()

    config_2s = StateProbeConfig(total_seconds=2.0)

    selected_2s = {}
    for prior_scale in [1.0, 0.85, 0.75, 0.50]:
        _, positions, probe = best_state_probe(
            design_nuisance,
            design_effects,
            config_2s,
            nuisance_prior_scale=prior_scale,
        )
        selected_2s[prior_scale] = (positions, probe)

        report = evaluate(
            probe,
            test_nuisance,
            test_effects,
            config_2s,
            prior_scale=prior_scale,
        )
        ratio = report["mean"] / baseline_5s["mean"]

        print(
            f"2 s prior_scale={prior_scale:0.2f} "
            f"probe={positions} meanIG={report['mean']:.6f} "
            f"ratio_vs_5s={ratio:.6f}"
        )

    # Stronger held-out stress test:
    # use the 25%-tighter baseline case on ten independent populations.
    probe_2s_75 = selected_2s[0.75][1]
    ratios = independent_replications(probe_2s_75, probe_5s)

    print()
    print("10 independent held-out replications, 2 s at prior_scale=0.75")
    print(
        "ratios vs population 5 s: "
        + ", ".join(f"{x:.4f}" for x in ratios)
    )
    print(f"mean ratio: {ratios.mean():.6f}")
    print(f"wins: {int(np.sum(ratios > 1.0))}/10")


if __name__ == "__main__":
    main()
