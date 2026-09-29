"""ADHD-REALDATA-001: independent temporal-locality replication.

Preregistered at:
experiments/registrations/ADHD_REALDATA_001.md

Dataset:
Rojas-Libano et al. (2019), Scientific Data.
Figshare 7218725 v3, CC BY 4.0.

MATLAB MCOS decoding approach adapted from D1D2DOPAMINE's MIT-licensed
ADHD_PUPIL_VALIDATOR.py:
https://github.com/d1d2dopamine/allostatic-sprint-hypothesis

This script does not redistribute participant data.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import json
import re

import numpy as np
import pandas as pd
import requests
from mat73_reader import load as mcos_load
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


DATA_URL = "https://figshare.com/ndownloader/files/14298953"
DATA_PATH = Path("/tmp/adhd_pupil_dataset_v3.mat")
DURATIONS = (1, 2, 3, 5)
SAMPLE_RATE_HZ = 1000
PROBE_INDEX = 5000  # documented Task_epoch: -5 s .. +3 s around probe onset
VALID_FRACTION = 0.70
RT_MIN_MS = 100.0
RT_MAX_MS = 1500.0
RIDGE_ALPHA = 10.0
BOOTSTRAPS = 10_000
BOOTSTRAP_SEED = 1517


def norm(x) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(x).lower())


def scalar(x):
    if isinstance(x, np.ndarray) and x.size == 1:
        return scalar(x.reshape(-1)[0])
    if isinstance(x, np.generic):
        return x.item()
    return x


def download() -> None:
    if DATA_PATH.exists() and DATA_PATH.stat().st_size > 1_000_000_000:
        print("Using cached dataset:", DATA_PATH.stat().st_size)
        return

    with requests.get(DATA_URL, stream=True, timeout=(30, 300)) as response:
        response.raise_for_status()
        expected = int(response.headers.get("Content-Length") or 0)
        print("Dataset download:", response.status_code, "expected_bytes=", expected)
        with DATA_PATH.open("wb") as handle:
            done = 0
            for chunk in response.iter_content(8 * 1024 * 1024):
                if chunk:
                    handle.write(chunk)
                    done += len(chunk)
        print("Dataset bytes:", DATA_PATH.stat().st_size)


def records_from_object(obj):
    if isinstance(obj, list):
        return obj
    if isinstance(obj, tuple):
        return list(obj)
    if isinstance(obj, np.ndarray):
        if obj.dtype.names:
            return [
                {name: scalar(row[name]) for name in obj.dtype.names}
                for row in obj.reshape(-1)
            ]
        return [scalar(x) for x in obj.reshape(-1)]
    if isinstance(obj, dict):
        lengths = []
        for value in obj.values():
            if isinstance(value, (str, bytes)):
                continue
            try:
                lengths.append(len(value))
            except Exception:
                pass
        n = max(lengths, default=0)
        if n > 1 and sum(length == n for length in lengths) >= 2:
            rows = []
            for i in range(n):
                rec = {}
                for key, value in obj.items():
                    try:
                        rec[key] = (
                            value[i]
                            if not isinstance(value, (str, bytes))
                            and len(value) == n
                            else value
                        )
                    except Exception:
                        rec[key] = value
                rows.append(rec)
            return rows
        return [obj]
    return [obj]


def record_get(record, aliases):
    if not isinstance(record, dict):
        return None
    lookup = {norm(key): value for key, value in record.items()}
    for alias in aliases:
        if norm(alias) in lookup:
            return lookup[norm(alias)]
    return None


def table_to_dataframe(obj) -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj.copy()
    if isinstance(obj, dict):
        try:
            return pd.DataFrame(
                {
                    str(key): list(np.asarray(value).reshape(-1))
                    for key, value in obj.items()
                }
            )
        except Exception:
            pass
    if isinstance(obj, list) and obj and isinstance(obj[0], dict):
        return pd.DataFrame(obj)
    if isinstance(obj, np.ndarray):
        if obj.dtype.names:
            return pd.DataFrame.from_records(obj.reshape(-1))
        if obj.ndim == 2:
            return pd.DataFrame(obj)
    raise TypeError(f"Unsupported MATLAB table representation: {type(obj).__name__}")


def find_column(df: pd.DataFrame, aliases):
    lookup = {norm(col): col for col in df.columns}
    for alias in aliases:
        if norm(alias) in lookup:
            return lookup[norm(alias)]
    return None


def condition_residual_target(df: pd.DataFrame, rt_col, load_col, distractor_col):
    """Residual reciprocal speed after session-specific load/distractor effects."""

    rt = pd.to_numeric(df[rt_col], errors="coerce").to_numpy(float)
    valid = np.isfinite(rt) & (rt >= RT_MIN_MS) & (rt <= RT_MAX_MS)

    perform_col = find_column(df, ["Perform", "Performance", "Correct"])
    if perform_col is not None:
        perform = pd.to_numeric(df[perform_col], errors="coerce").to_numpy(float)
        valid &= perform == 1

    index = np.flatnonzero(valid)
    if len(index) < 40:
        return {}, len(index)

    speed = 1000.0 / rt[index]
    conditions = pd.DataFrame(
        {
            "load": df.iloc[index][load_col].astype(str).to_numpy(),
            "distractor": df.iloc[index][distractor_col].astype(str).to_numpy(),
        }
    )
    design = pd.get_dummies(
        conditions,
        columns=["load", "distractor"],
        drop_first=True,
        dtype=float,
    )
    X = np.column_stack([np.ones(len(design)), design.to_numpy(float)])
    beta, *_ = np.linalg.lstsq(X, speed, rcond=None)
    residual = speed - X @ beta

    sd = float(np.std(residual, ddof=1))
    if not np.isfinite(sd) or sd <= 1e-12:
        return {}, len(index)

    z = (residual - np.mean(residual)) / sd
    return {int(row): float(target) for row, target in zip(index, z)}, len(index)


def pupil_features(vector, duration_s: int):
    arr = np.asarray(vector, dtype=float).reshape(-1)
    if arr.size < 8000:
        return None

    start = PROBE_INDEX - duration_s * SAMPLE_RATE_HZ
    window = arr[start:PROBE_INDEX]
    finite_mask = np.isfinite(window)
    valid_fraction = float(np.mean(finite_mask))

    if valid_fraction < VALID_FRACTION:
        return None

    values = window[finite_mask]
    if len(values) < 20:
        return None

    q10, q25, q50, q75, q90 = np.quantile(
        values, [0.10, 0.25, 0.50, 0.75, 0.90]
    )

    x = np.flatnonzero(finite_mask).astype(float)
    if len(x) >= 3:
        x = (x - x.mean()) / max(float(x.std()), 1.0)
        slope = float(np.polyfit(x, values, 1)[0])
    else:
        slope = np.nan

    # First differences only across adjacent finite samples so gaps do not
    # become artificial large pupil jumps.
    pair = finite_mask[:-1] & finite_mask[1:]
    diffs = np.diff(window)[pair]

    madiff = float(np.mean(np.abs(diffs))) if len(diffs) else np.nan
    sddiff = float(np.std(diffs, ddof=1)) if len(diffs) > 1 else np.nan

    return np.asarray(
        [
            float(np.mean(values)),
            float(np.std(values, ddof=1)),
            float(q10),
            float(q25),
            float(q50),
            float(q75),
            float(q90),
            slope,
            madiff,
            sddiff,
            valid_fraction,
        ],
        dtype=float,
    )


@dataclass
class TrialRow:
    subject: str
    session: str
    target: float
    features: dict[int, np.ndarray]


def extract_rows(mat_obj):
    sessions = records_from_object(mat_obj)
    output: list[TrialRow] = []
    session_qc = []

    for session_index, record in enumerate(sessions):
        subject_raw = record_get(record, ["Subject", "subject", "ID"])
        try:
            subject = str(int(float(scalar(subject_raw))))
        except Exception:
            subject = str(scalar(subject_raw))

        group = str(scalar(record_get(record, ["Group", "group"])))
        epoch = record_get(
            record,
            ["Task_epocs", "TaskEpocs", "Task_epochs", "Task_epoch", "TaskEpoch"],
        )

        try:
            df = table_to_dataframe(epoch)
        except Exception as exc:
            session_qc.append((subject, group, "decode-failed", str(exc)))
            continue

        trial_col = find_column(df, ["Trial"])
        load_col = find_column(df, ["Load"])
        distractor_col = find_column(df, ["Distractor"])
        rt_col = find_column(df, ["RTime", "Rtime", "ReactionTime", "RT"])
        pupil_col = find_column(df, ["Pupil"])

        if None in (trial_col, load_col, distractor_col, rt_col, pupil_col):
            session_qc.append(
                (subject, group, "missing-columns", "|".join(map(str, df.columns)))
            )
            continue

        targets, n_valid_rt = condition_residual_target(
            df, rt_col, load_col, distractor_col
        )
        if not targets:
            session_qc.append((subject, group, "too-few-valid-rt", n_valid_rt))
            continue

        session_key = f"{subject}:{session_index}:{group}"
        accepted = 0

        for row_index, target in targets.items():
            per_duration = {}
            usable = True
            cell = df.iloc[row_index][pupil_col]

            for duration in DURATIONS:
                features = pupil_features(cell, duration)
                if features is None:
                    usable = False
                    break
                per_duration[duration] = features

            if not usable:
                continue

            output.append(
                TrialRow(
                    subject=subject,
                    session=session_key,
                    target=target,
                    features=per_duration,
                )
            )
            accepted += 1

        session_qc.append((subject, group, "included", accepted))

    return output, session_qc


def pearson(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 10 or np.std(x) <= 1e-12 or np.std(y) <= 1e-12:
        return np.nan
    return float(np.corrcoef(x, y)[0, 1])


def fisher_macro(values):
    r = np.asarray(values, dtype=float)
    r = r[np.isfinite(r)]
    if len(r) == 0:
        return np.nan
    r = np.clip(r, -0.999999, 0.999999)
    return float(np.tanh(np.mean(np.arctanh(r))))


def loso(rows: list[TrialRow], duration: int):
    subjects = sorted({row.subject for row in rows})
    by_subject = defaultdict(list)
    predictions = []
    observations = []

    all_features = np.vstack([row.features[duration] for row in rows])
    all_targets = np.asarray([row.target for row in rows], dtype=float)
    all_subjects = np.asarray([row.subject for row in rows], dtype=object)

    for subject in subjects:
        train = all_subjects != subject
        test = all_subjects == subject

        if train.sum() < 50 or test.sum() < 10:
            continue

        model = make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            Ridge(alpha=RIDGE_ALPHA),
        )
        model.fit(all_features[train], all_targets[train])
        pred = model.predict(all_features[test])
        truth = all_targets[test]

        r = pearson(pred, truth)
        by_subject[subject] = {
            "r": r,
            "n": int(test.sum()),
        }
        predictions.extend(pred.tolist())
        observations.extend(truth.tolist())

    correlations = [entry["r"] for entry in by_subject.values()]
    return {
        "by_subject": dict(by_subject),
        "macro_r": fisher_macro(correlations),
        "pooled_r": pearson(predictions, observations),
        "n_subjects": int(sum(np.isfinite(correlations))),
        "n_samples": len(predictions),
    }


def paired_bootstrap(result_a, result_b):
    subjects = sorted(
        set(result_a["by_subject"]).intersection(result_b["by_subject"])
    )
    subjects = [
        s
        for s in subjects
        if np.isfinite(result_a["by_subject"][s]["r"])
        and np.isfinite(result_b["by_subject"][s]["r"])
    ]

    a = np.asarray([result_a["by_subject"][s]["r"] for s in subjects], dtype=float)
    b = np.asarray([result_b["by_subject"][s]["r"] for s in subjects], dtype=float)

    rng = np.random.default_rng(BOOTSTRAP_SEED)
    differences = np.empty(BOOTSTRAPS, dtype=float)

    for i in range(BOOTSTRAPS):
        idx = rng.integers(0, len(subjects), size=len(subjects))
        differences[i] = fisher_macro(a[idx]) - fisher_macro(b[idx])

    return {
        "n_subjects": len(subjects),
        "difference": fisher_macro(a) - fisher_macro(b),
        "ci_low": float(np.quantile(differences, 0.025)),
        "ci_high": float(np.quantile(differences, 0.975)),
    }


def main():
    download()

    print("Decoding Pupil_data...")
    mat_obj = mcos_load(str(DATA_PATH), variable="Pupil_data")
    rows, session_qc = extract_rows(mat_obj)
    del mat_obj

    print("Usable common-trial rows:", len(rows))
    print("Unique participants:", len({row.subject for row in rows}))
    print("Included sessions:", sum(x[2] == "included" and x[3] >= 10 for x in session_qc))

    if len(rows) < 500 or len({row.subject for row in rows}) < 20:
        raise RuntimeError("Insufficient usable independent data after preregistered QC.")

    results = {}
    for duration in DURATIONS:
        results[duration] = loso(rows, duration)
        r = results[duration]
        print(
            f"{duration}s: macro_r={r['macro_r']:.6f} "
            f"pooled_r={r['pooled_r']:.6f} "
            f"subjects={r['n_subjects']} samples={r['n_samples']}"
        )

    contrasts = {}
    for comparator in (5, 3, 1):
        if comparator == 2:
            continue
        key = f"2s_minus_{comparator}s"
        contrasts[key] = paired_bootstrap(results[2], results[comparator])
        c = contrasts[key]
        print(
            f"{key}: diff={c['difference']:.6f} "
            f"95%CI=[{c['ci_low']:.6f}, {c['ci_high']:.6f}] "
            f"n_subjects={c['n_subjects']}"
        )

    primary = contrasts["2s_minus_5s"]
    confirmed = bool(
        primary["difference"] > 0.0
        and primary["ci_low"] > 0.0
    )

    payload = {
        "experiment": "ADHD-REALDATA-001",
        "confirmed_primary_temporal_locality": confirmed,
        "durations": {
            str(k): {
                "macro_r": v["macro_r"],
                "pooled_r": v["pooled_r"],
                "n_subjects": v["n_subjects"],
                "n_samples": v["n_samples"],
            }
            for k, v in results.items()
        },
        "contrasts": contrasts,
    }

    print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
