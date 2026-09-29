import numpy as np

from lucent.state_design import (
    StateProbeConfig,
    equal_exposure_state_probes,
    sample_nuisance_population,
    sample_state_effects,
    state_information_gain,
)


def test_short_probe_count():
    config = StateProbeConfig(total_seconds=2.0)
    probes = list(equal_exposure_state_probes(config))
    assert len(probes) == 3


def test_tighter_nuisance_prior_never_reduces_local_state_information():
    config = StateProbeConfig(total_seconds=2.0)
    nuisance = sample_nuisance_population(1, 1, scale=0.2)[0]
    effect = sample_state_effects(2, 1)[0]

    probe = np.full(config.n_segments, config.low_level)
    probe[2] = config.high_level

    loose = state_information_gain(
        probe,
        nuisance,
        effect,
        config,
        nuisance_prior_scale=1.0,
    )
    tight = state_information_gain(
        probe,
        nuisance,
        effect,
        config,
        nuisance_prior_scale=0.75,
    )

    assert tight >= loose
