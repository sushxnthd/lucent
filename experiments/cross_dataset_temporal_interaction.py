"""TEMPORAL-INTERACTION-001.

Post-hoc cross-dataset test after ADHD-REALDATA-001.

Question:
Does the 2s-vs-5s duration effect differ between the Massoz PVT dataset and
the independent Rojas-Libano working-memory pupil dataset?

This analysis is explicitly exploratory because the cross-dataset interaction
was formulated after observing the independent replication result.
"""

from __future__ import annotations

import tempfile
import numpy as np

import adhd_realdata_temporal_locality as adhd
import mts_realdata_baseline_compression as mts


B = 10_000
SEED = 1517


def fisher_macro(values):
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    x = np.clip(x, -0.999999, 0.999999)
    return float(np.tanh(np.mean(np.arctanh(x))))


def common_arrays(a: dict, b: dict):
    keys = sorted(
        k
        for k in set(a).intersection(b)
        if np.isfinite(a[k]) and np.isfinite(b[k])
    )
    return (
        keys,
        np.asarray([a[k] for k in keys], dtype=float),
        np.asarray([b[k] for k in keys], dtype=float),
    )


def main():
    # Independent ADHD pupil dataset.
    adhd.download()
    obj = adhd.mcos_load(str(adhd.DATA_PATH), variable="Pupil_data")
    rows, _ = adhd.extract_rows(obj)
    del obj

    adhd_2 = adhd.loso(rows, 2)
    adhd_5 = adhd.loso(rows, 5)
    adhd_keys, adhd_r2, adhd_r5 = common_arrays(
        {k: v["r"] for k, v in adhd_2["by_subject"].items()},
        {k: v["r"] for k, v in adhd_5["by_subject"].items()},
    )

    # Massoz PVT dataset, population-normalized condition.
    with tempfile.TemporaryDirectory() as tmp:
        dataset = mts.load_dataset(mts.Path(tmp))

    mts_2 = mts.evaluate_condition(dataset, 2, personalized=False)
    mts_5 = mts.evaluate_condition(dataset, 5, personalized=False)
    mts_keys, mts_r2, mts_r5 = common_arrays(
        mts_2["subject_r"],
        mts_5["subject_r"],
    )

    adhd_delta = fisher_macro(adhd_r2) - fisher_macro(adhd_r5)
    mts_delta = fisher_macro(mts_r2) - fisher_macro(mts_r5)
    interaction = mts_delta - adhd_delta

    rng = np.random.default_rng(SEED)
    boot = np.empty(B, dtype=float)

    for i in range(B):
        ia = rng.integers(0, len(adhd_keys), len(adhd_keys))
        im = rng.integers(0, len(mts_keys), len(mts_keys))

        da = fisher_macro(adhd_r2[ia]) - fisher_macro(adhd_r5[ia])
        dm = fisher_macro(mts_r2[im]) - fisher_macro(mts_r5[im])
        boot[i] = dm - da

    low, high = np.quantile(boot, [0.025, 0.975])

    print("TEMPORAL-INTERACTION-001")
    print("=" * 72)
    print(f"ADHD working-memory subjects: {len(adhd_keys)}")
    print(f"MTS PVT subjects:             {len(mts_keys)}")
    print(f"ADHD delta (2s-5s):           {adhd_delta:+.6f}")
    print(f"MTS delta (2s-5s):            {mts_delta:+.6f}")
    print(f"cross-dataset interaction:    {interaction:+.6f}")
    print(f"independent-bootstrap 95% CI: [{low:+.6f}, {high:+.6f}]")
    print(f"bootstrap draws:              {B}")


if __name__ == "__main__":
    main()
