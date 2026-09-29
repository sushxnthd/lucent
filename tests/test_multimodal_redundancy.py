
import numpy as np
import pytest

from lucent.multimodal_probe import redundant_joint_state_information_gain


def test_redundancy_envelope_endpoints():
    pupil = np.array([2.0, 1.0])
    gaze = np.array([1.0, 3.0])

    full = redundant_joint_state_information_gain(
        pupil,
        gaze,
        incremental_fraction=1.0,
    )
    zero = redundant_joint_state_information_gain(
        pupil,
        gaze,
        incremental_fraction=0.0,
    )

    expected_full = 0.5 * np.log1p(0.25 * (pupil + gaze))
    expected_zero = 0.5 * np.log1p(0.25 * np.maximum(pupil, gaze))

    assert np.allclose(full, expected_full)
    assert np.allclose(zero, expected_zero)


def test_redundancy_fraction_is_monotone():
    pupil = np.array([1.0, 2.0, 3.0])
    gaze = np.array([3.0, 2.0, 1.0])

    low = redundant_joint_state_information_gain(
        pupil,
        gaze,
        incremental_fraction=0.25,
    )
    high = redundant_joint_state_information_gain(
        pupil,
        gaze,
        incremental_fraction=0.75,
    )

    assert np.all(high >= low)


def test_redundancy_fraction_bounds():
    with pytest.raises(ValueError):
        redundant_joint_state_information_gain(
            np.array([1.0]),
            np.array([1.0]),
            incremental_fraction=1.1,
        )
