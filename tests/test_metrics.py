import numpy as np
import pytest

from lucent.metrics import regression_report


def test_perfect_regression_report():
    y = np.array([1.0, 2.0, 3.0])
    report = regression_report(y, y)

    assert report.mae == pytest.approx(0.0)
    assert report.rmse == pytest.approx(0.0)
    assert report.r2 == pytest.approx(1.0)
    assert report.n == 3


def test_regression_report_rejects_shape_mismatch():
    with pytest.raises(ValueError):
        regression_report(np.array([1.0, 2.0]), np.array([1.0]))
