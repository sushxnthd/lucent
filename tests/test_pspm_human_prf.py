from pathlib import Path
import sys

import numpy as np

EXPERIMENTS = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from pspm_human_prf import (  # noqa: E402
    CONTIGUOUS,
    E002,
    ParticipantPRF,
    binary_probe,
    canonical_code,
    predicted_probe_waveform,
    trial_partition,
)


def test_canonical_luminance_codes():
    assert canonical_code(0.0) == 0.0
    assert canonical_code(0.25) == 0.25
    assert canonical_code(0.75) == 0.75
    assert canonical_code(1.0) == 1.0
    assert canonical_code(9.0) == 9.0


def test_trial_partition_balances_each_disc_level():
    stimulus = np.asarray(
        [9.0] + sum(
            ([code, 9.0] for code in [0.0, 0.25, 0.75, 1.0] * 6),
            [],
        ),
        dtype=float,
    )
    fit, validation = trial_partition(stimulus)

    assert len(fit) == 12
    assert len(validation) == 12

    for code in (0.0, 0.25, 0.75, 1.0):
        assert sum(stimulus[i] == code for i in fit) == 3
        assert sum(stimulus[i] == code for i in validation) == 3


def test_split_and_contiguous_have_equal_exposure_but_different_waveforms():
    time = np.arange(0.0, 4.5, 0.02)
    step = -np.exp(-time / 0.8)
    participant = ParticipantPRF(
        subject="x",
        step_time=time,
        step_response=step,
        sigma=0.05,
        validation_rmse=0.05,
        validation_r2=0.5,
        n_fit=24,
        n_validation=24,
    )

    assert binary_probe(E002).sum() == binary_probe(CONTIGUOUS).sum() == 3

    _, split = predicted_probe_waveform(participant, E002)
    _, contiguous = predicted_probe_waveform(participant, CONTIGUOUS)

    assert not np.allclose(split, contiguous)
