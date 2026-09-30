from pathlib import Path
import sys

import numpy as np
import pandas as pd

EXPERIMENTS = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from ehinger_device_transfer import (  # noqa: E402
    fit_affine,
    paired_table,
    pearson,
)


def synthetic_table():
    rows = []
    subjects = ["S1", "S2"]
    for subject_index, subject in enumerate(subjects):
        for block in range(1, 7):
            for lum in (0.0, 64.0, 128.0, 192.0, 255.0):
                for k in range(24):
                    td = 0.05 + 0.11 * k
                    base = (
                        1.0
                        + 0.001 * lum
                        + 0.02 * np.sin(td)
                        + 0.01 * subject_index
                        + 0.002 * block
                    )
                    for tracker in ("el", "pl"):
                        value = base if tracker == "el" else (base - 0.1) / 1.4
                        rows.append(
                            {
                                "subject": subject,
                                "block": float(block),
                                "lum": lum,
                                "td": td,
                                "eyetracker": tracker,
                                "pa_norm": value,
                            }
                        )
    return pd.DataFrame(rows)


def test_paired_table_keeps_complete_cells():
    paired = paired_table(synthetic_table())
    assert set(paired["subject"]) == {"S1", "S2"}
    assert set(paired["block"].astype(int)) == set(range(1, 7))
    assert paired.groupby(["subject", "block", "lum"]).size().min() >= 15


def test_affine_calibration_recovers_synthetic_mapping():
    paired = paired_table(synthetic_table())
    train = paired[
        (paired["subject"] == "S1")
        & (paired["block"].isin((1, 2, 3)))
    ]
    a, b = fit_affine(train)
    assert abs(a - 0.1) < 1e-10
    assert abs(b - 1.4) < 1e-10


def test_pearson_is_affine_invariant():
    x = np.arange(50, dtype=float)
    y = 7.0 + 3.0 * x
    assert pearson(x, y) > 0.999999
