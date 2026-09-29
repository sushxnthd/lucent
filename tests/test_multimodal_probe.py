import numpy as np

from lucent.multimodal_probe import (
    joint_state_information_gain,
    pursuit_state_information,
    sample_pursuit_nuisance,
    sample_pursuit_state_effects,
)


def test_joint_information_is_not_less_than_single_channel():
    pupil = np.array([1.0, 2.0, 3.0])
    pursuit = np.array([0.5, 0.5, 0.5])

    joint = joint_state_information_gain(pupil, pursuit)
    pupil_only = 0.5 * np.log1p(0.25 * pupil)

    assert np.all(joint >= pupil_only)


def test_pursuit_information_is_finite():
    nuisance = sample_pursuit_nuisance(1, 1, scale=0.2)[0]
    effect = sample_pursuit_state_effects(
        2,
        1,
        gain_drop_mean=0.10,
        tau_increase_mean=0.03,
    )[0]

    value = pursuit_state_information(
        0.5,
        nuisance,
        effect,
        total_seconds=3.0,
        nuisance_prior_scale=1.0,
        measurement_noise=0.10,
    )

    assert np.isfinite(value)
    assert value >= 0.0
