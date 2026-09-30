from pathlib import Path
import sys

import numpy as np

EXPERIMENTS = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from e002_photometric_audit import rankdata, spearman  # noqa: E402


def test_rankdata_handles_ties():
    values = np.array([3.0, 1.0, 1.0, 2.0])
    ranks = rankdata(values)
    np.testing.assert_allclose(ranks, [4.0, 1.5, 1.5, 3.0])


def test_spearman_detects_monotonic_coupling():
    x = np.arange(20, dtype=float)
    y = 7.0 - 2.0 * x
    rho = spearman(x, y)
    assert rho is not None
    assert rho < -0.999


def test_spearman_rejects_constant_channel():
    x = np.arange(20, dtype=float)
    y = np.ones(20)
    assert spearman(x, y) is None
