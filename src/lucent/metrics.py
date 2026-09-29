from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


@dataclass(frozen=True)
class RegressionReport:
    mae: float
    rmse: float
    r2: float
    n: int


def regression_report(y_true: np.ndarray, y_pred: np.ndarray) -> RegressionReport:
    """Return a compact regression report with basic shape checks."""

    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    if y_true.ndim != 1:
        raise ValueError("inputs must be one-dimensional")
    if len(y_true) == 0:
        raise ValueError("inputs cannot be empty")

    return RegressionReport(
        mae=float(mean_absolute_error(y_true, y_pred)),
        rmse=float(np.sqrt(mean_squared_error(y_true, y_pred))),
        r2=float(r2_score(y_true, y_pred)),
        n=int(len(y_true)),
    )
