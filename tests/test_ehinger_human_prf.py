from pathlib import Path
import sys

import numpy as np

EXPERIMENTS = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from ehinger_human_prf import (  # noqa: E402
    CONTIGUOUS,
    E002,
    ResponseParticipant,
    binary_probe,
    predict_waveform,
    separation,
)


def participant():
    grid = np.arange(0.0, 5.0001, 0.05)
    bright = -0.55 * (1.0 - np.exp(-grid[grid <= 2.8] / 0.55))
    dark = 0.45 * (1.0 - np.exp(-grid[grid <= 4.5] / 1.2))
    return ResponseParticipant(
        subject="synthetic",
        tracker="el",
        bright=bright,
        dark=dark,
        sigma=0.05,
        bright_rmse=[0.05, 0.05, 0.05],
        dark_rmse=[0.05, 0.05, 0.05],
    )


def test_equal_exposure_is_preserved():
    assert binary_probe(E002).sum() == 3
    assert binary_probe(CONTIGUOUS).sum() == 3


def test_e002_and_contiguous_generate_different_asymmetric_waveforms():
    p = participant()
    split = predict_waveform(p, E002)
    contiguous = predict_waveform(p, CONTIGUOUS)
    assert not np.allclose(split, contiguous)
    assert separation(p, E002) > 0


def test_contiguous_self_separation_is_zero():
    p = participant()
    assert separation(p, CONTIGUOUS) == 0.0
