import numpy as np

from lucent.active_probe import (
    ProbeConfig,
    equal_exposure_probes,
    information_gain,
    level_to_luminance,
    sample_parameter_population,
    simulate_pupil,
)


def test_equal_exposure_design_count_and_budget():
    config = ProbeConfig()
    probes = list(equal_exposure_probes(config))

    assert len(probes) == 84
    for _, probe in probes:
        assert int(np.sum(probe == config.high_level)) == config.high_segments
        assert probe[0] == config.low_level


def test_luminance_mapping_is_monotonic():
    levels = np.array([0.1, 0.5, 0.9])
    luminance = level_to_luminance(levels)
    assert np.all(np.diff(luminance) > 0)


def test_simulator_and_information_gain_are_finite():
    config = ProbeConfig()
    population = sample_parameter_population(1, 1, scale=0.2)
    probe = np.full(config.n_segments, config.low_level)
    probe[[1, 2, 8]] = config.high_level

    trace = simulate_pupil(probe, population[0], config)
    score = information_gain(probe, population[0], config)

    assert trace.shape == (config.n_steps,)
    assert np.isfinite(trace).all()
    assert np.isfinite(score)
    assert score > 0
