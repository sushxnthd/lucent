"""MTS-REALDATA-001: preregistered real-data test of baseline compression.

Downloads the public eyelid-distance and reaction-time files from the repository
accompanying Massoz et al. (Sensors, 2018). No source data are redistributed.

The analysis plan is frozen in:
experiments/registrations/MTS_REALDATA_001.md
"""

from __future__ import annotations

import datetime as dt
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torchfile
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


BASE = "https://raw.githubusercontent.com/QMassoz/mts-drowsiness/master/data/raw"
SUBJECTS = [
    1, 2, 3, 4, 5, 6, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 33, 34, 35,
]
DURATIONS = [2, 5, 15, 30, 60]
FPS = 30.0
ALPHA = 10.0
BOOTSTRAP_SEED = 1517
N_BOOTSTRAP = 10_000


@dataclass
class Session:
    subject: int
    test: int
    eye: np.ndarray
    event_time_s: np.ndarray
    rt_ms: np.ndarray


@dataclass
class SubjectData:
    subject: int
    baseline: Session
    later: list[Session]
    speed_mean: float
    speed_sd: float
    personal_open_ref: np.ndarray


def download(url: str, target: Path) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            target.write_bytes(response.read())
        return True
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False
        raise


def parse_timestamp(text: str) -> dt.datetime:
    return dt.datetime.strptime(text.strip(), "%Y-%m-%d_%H.%M.%S.%f")


def load_rt(path: Path) -> tuple[np.ndarray, np.ndarray]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    lines = [line for line in lines if line]

    t0 = parse_timestamp(lines[0])
    event_time = []
    rt = []

    for line in lines[1:]:
        start_text, end_text = line.split(";")
        start = parse_timestamp(start_text)
        end = parse_timestamp(end_text)
        event_time.append((start - t0).total_seconds())
        rt.append((end - start).total_seconds() * 1000.0)

    return np.asarray(event_time, dtype=float), np.asarray(rt, dtype=float)


def load_session(root: Path, subject: int, test: int) -> Session | None:
    eld = root / f"{subject}-{test}.t7"
    rt = root / f"{subject}-{test}.txt"

    ok_eld = download(
        f"{BASE}/eld-seq/{subject}-{test}.t7",
        eld,
    )
    ok_rt = download(
        f"{BASE}/rt/{subject}-{test}.txt",
        rt,
    )

    if not (ok_eld and ok_rt):
        return None

    eye = np.asarray(torchfile.load(str(eld)), dtype=float)
    event_time, rt_ms = load_rt(rt)

    if eye.ndim != 2 or eye.shape[1] != 2:
        raise ValueError(
            f"unexpected eye array for subject={subject} test={test}: {eye.shape}"
        )

    return Session(
        subject=subject,
        test=test,
        eye=eye,
        event_time_s=event_time,
        rt_ms=rt_ms,
    )


def valid_baseline_speed(rt_ms: np.ndarray) -> np.ndarray:
    keep = np.isfinite(rt_ms) & (rt_ms >= 100.0) & (rt_ms <= 2000.0)
    return 1000.0 / rt_ms[keep]


def robust_open_ref(eye: np.ndarray) -> np.ndarray:
    ref = np.quantile(eye, 0.95, axis=0)
    return np.maximum(ref, 1e-6)


def load_dataset(root: Path) -> dict[int, SubjectData]:
    dataset: dict[int, SubjectData] = {}

    for subject in SUBJECTS:
        baseline = load_session(root, subject, 1)
        if baseline is None:
            continue

        later = [
            session
            for test in (2, 3)
            if (session := load_session(root, subject, test)) is not None
        ]
        if not later:
            continue

        speed = valid_baseline_speed(baseline.rt_ms)
        if len(speed) < 20 or np.std(speed, ddof=1) <= 1e-8:
            continue

        dataset[subject] = SubjectData(
            subject=subject,
            baseline=baseline,
            later=later,
            speed_mean=float(np.mean(speed)),
            speed_sd=float(np.std(speed, ddof=1)),
            personal_open_ref=robust_open_ref(baseline.eye),
        )

    return dataset


def feature_map_many(
    windows: np.ndarray,
    open_ref: np.ndarray,
    duration_s: int,
) -> np.ndarray:
    """Vectorized deterministic feature map.

    windows shape: [n_windows, n_frames, 2].
    """

    windows = np.asarray(windows, dtype=float)
    if windows.ndim != 3 or windows.shape[2] != 2:
        raise ValueError(f"unexpected window shape: {windows.shape}")

    x = windows / open_ref.reshape(1, 1, 2)
    x = np.clip(x, 0.0, 1.5)

    aperture = np.mean(x, axis=2)
    asymmetry = np.abs(x[:, :, 0] - x[:, :, 1])
    diff = np.diff(aperture, axis=1)

    quantiles = np.quantile(
        aperture,
        [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95],
        axis=1,
    ).T

    closed = aperture < 0.70
    closure_entries = np.sum(
        (~closed[:, :-1]) & closed[:, 1:],
        axis=1,
    )

    parts = [
        np.mean(aperture, axis=1, keepdims=True),
        np.std(aperture, axis=1, keepdims=True),
        quantiles,
        np.mean(aperture < 0.80, axis=1, keepdims=True),
        np.mean(aperture < 0.70, axis=1, keepdims=True),
        np.mean(aperture < 0.50, axis=1, keepdims=True),
        np.mean(np.abs(diff), axis=1, keepdims=True),
        np.std(diff, axis=1, keepdims=True),
        (closure_entries / max(float(duration_s), 1.0)).reshape(-1, 1),
        np.mean(asymmetry, axis=1, keepdims=True),
    ]
    return np.concatenate(parts, axis=1)


def feature_map(
    window: np.ndarray,
    open_ref: np.ndarray,
    duration_s: int,
) -> np.ndarray:
    return feature_map_many(
        np.asarray(window)[None, :, :],
        open_ref,
        duration_s,
    )[0]


def baseline_feature(
    session: Session,
    duration_s: int,
    open_ref: np.ndarray,
) -> np.ndarray:
    n = int(round(duration_s * FPS))
    if n <= 0 or n > len(session.eye):
        raise ValueError("invalid duration")

    usable = (len(session.eye) // n) * n
    windows = session.eye[:usable].reshape(-1, n, 2)
    features = feature_map_many(windows, open_ref, duration_s)

    return np.median(features, axis=0)


def later_samples(
    data: SubjectData,
    duration_s: int,
    open_ref: np.ndarray,
    baseline_vector: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    n = int(round(duration_s * FPS))
    windows = []
    targets = []

    for session in data.later:
        for onset_s, rt_ms in zip(session.event_time_s, session.rt_ms, strict=True):
            if not np.isfinite(rt_ms) or rt_ms < 100.0 or rt_ms > 2000.0:
                continue

            end = int(np.floor(onset_s * FPS))
            start = end - n

            if start < 0 or end > len(session.eye) or end <= start:
                continue

            windows.append(session.eye[start:end])

            speed = 1000.0 / rt_ms
            targets.append((speed - data.speed_mean) / data.speed_sd)

    if not windows:
        return np.empty((0, 15)), np.empty((0,))

    feature_matrix = feature_map_many(
        np.stack(windows, axis=0),
        open_ref,
        duration_s,
    )
    feature_matrix = feature_matrix - baseline_vector.reshape(1, -1)
    target_array = np.asarray(targets, dtype=float)

    keep = (
        np.isfinite(feature_matrix).all(axis=1)
        & np.isfinite(target_array)
    )

    return feature_matrix[keep], target_array[keep]


def pearson(y: np.ndarray, pred: np.ndarray) -> float:
    if len(y) < 3 or np.std(y) <= 1e-12 or np.std(pred) <= 1e-12:
        return np.nan
    return float(np.corrcoef(y, pred)[0, 1])


def macro_fisher_r(subject_rs: dict[int, float]) -> float:
    values = np.asarray(
        [r for r in subject_rs.values() if np.isfinite(r) and abs(r) < 1.0],
        dtype=float,
    )
    if len(values) == 0:
        return np.nan
    z = np.arctanh(np.clip(values, -0.999999, 0.999999))
    return float(np.tanh(np.mean(z)))


def build_fold_quantities(
    dataset: dict[int, SubjectData],
    train_subjects: list[int],
    duration_s: int,
):
    train_open = np.vstack(
        [dataset[s].personal_open_ref for s in train_subjects]
    )
    population_open = np.median(train_open, axis=0)

    pop_baselines = [
        baseline_feature(
            dataset[s].baseline,
            duration_s,
            population_open,
        )
        for s in train_subjects
    ]
    population_baseline = np.median(np.vstack(pop_baselines), axis=0)

    return population_open, population_baseline


def evaluate_condition(
    dataset: dict[int, SubjectData],
    duration_s: int,
    personalized: bool,
):
    predictions: dict[int, tuple[np.ndarray, np.ndarray]] = {}

    for held_out in sorted(dataset):
        train_subjects = [s for s in sorted(dataset) if s != held_out]

        population_open, population_baseline = build_fold_quantities(
            dataset,
            train_subjects,
            duration_s,
        )

        train_x = []
        train_y = []

        for s in train_subjects:
            data = dataset[s]
            if personalized:
                open_ref = data.personal_open_ref
                baseline = baseline_feature(
                    data.baseline,
                    duration_s,
                    open_ref,
                )
            else:
                open_ref = population_open
                baseline = population_baseline

            x, y = later_samples(
                data,
                duration_s,
                open_ref,
                baseline,
            )
            if len(y):
                train_x.append(x)
                train_y.append(y)

        train_x_arr = np.vstack(train_x)
        train_y_arr = np.concatenate(train_y)

        test_data = dataset[held_out]
        if personalized:
            test_open = test_data.personal_open_ref
            test_baseline = baseline_feature(
                test_data.baseline,
                duration_s,
                test_open,
            )
        else:
            test_open = population_open
            test_baseline = population_baseline

        test_x, test_y = later_samples(
            test_data,
            duration_s,
            test_open,
            test_baseline,
        )

        model = make_pipeline(
            StandardScaler(),
            Ridge(alpha=ALPHA),
        )
        model.fit(train_x_arr, train_y_arr)
        pred = model.predict(test_x)

        predictions[held_out] = (test_y, pred)

    subject_r = {
        subject: pearson(y, pred)
        for subject, (y, pred) in predictions.items()
    }

    y_all = np.concatenate([v[0] for v in predictions.values()])
    p_all = np.concatenate([v[1] for v in predictions.values()])

    return {
        "subject_r": subject_r,
        "macro_r": macro_fisher_r(subject_r),
        "pooled_r": pearson(y_all, p_all),
        "mae": float(mean_absolute_error(y_all, p_all)),
        "r2": float(r2_score(y_all, p_all)),
        "n": int(len(y_all)),
    }


def paired_bootstrap_diff(
    personal_r: dict[int, float],
    population_r: dict[int, float],
):
    subjects = sorted(set(personal_r).intersection(population_r))
    subjects = [
        s
        for s in subjects
        if np.isfinite(personal_r[s]) and np.isfinite(population_r[s])
    ]

    p = np.asarray([personal_r[s] for s in subjects], dtype=float)
    q = np.asarray([population_r[s] for s in subjects], dtype=float)

    rng = np.random.default_rng(BOOTSTRAP_SEED)
    diffs = np.empty(N_BOOTSTRAP, dtype=float)

    for i in range(N_BOOTSTRAP):
        idx = rng.integers(0, len(subjects), size=len(subjects))
        p_macro = float(np.tanh(np.mean(np.arctanh(np.clip(p[idx], -0.999999, 0.999999)))))
        q_macro = float(np.tanh(np.mean(np.arctanh(np.clip(q[idx], -0.999999, 0.999999)))))
        diffs[i] = p_macro - q_macro

    return (
        float(np.quantile(diffs, 0.025)),
        float(np.quantile(diffs, 0.975)),
        len(subjects),
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        dataset = load_dataset(Path(tmp))

    print("MTS-REALDATA-001")
    print("=" * 78)
    print(f"subjects included: {len(dataset)}")
    print(f"subject IDs: {sorted(dataset)}")
    print()

    all_results = {}

    for duration in DURATIONS:
        for personalized in (False, True):
            label = "personal" if personalized else "population"
            result = evaluate_condition(
                dataset,
                duration,
                personalized,
            )
            all_results[(duration, label)] = result
            print(
                f"{duration:>2}s {label:>10}: "
                f"macro_r={result['macro_r']:+.4f} "
                f"pooled_r={result['pooled_r']:+.4f} "
                f"MAE={result['mae']:.4f} "
                f"R2={result['r2']:+.4f} "
                f"n={result['n']}"
            )

    primary_personal = all_results[(5, "personal")]
    primary_population = all_results[(5, "population")]
    ci_low, ci_high, n_subjects = paired_bootstrap_diff(
        primary_personal["subject_r"],
        primary_population["subject_r"],
    )
    primary_diff = (
        primary_personal["macro_r"] - primary_population["macro_r"]
    )

    print()
    print("PRIMARY COMPARISON")
    print(
        f"5s macro-r difference personal-population: "
        f"{primary_diff:+.4f}"
    )
    print(
        f"paired subject bootstrap 95% CI: "
        f"[{ci_low:+.4f}, {ci_high:+.4f}] "
        f"(subjects={n_subjects}, B={N_BOOTSTRAP})"
    )

    print()
    print("DURATION COMPRESSION RATIOS")
    personal_5 = primary_personal["macro_r"]
    for duration in DURATIONS:
        pop = all_results[(duration, "population")]["macro_r"]
        print(
            f"personal 5s / population {duration:>2}s macro-r: "
            f"{personal_5 / pop if abs(pop) > 1e-12 else np.nan:+.4f}"
        )

    # Exploratory follow-up added only after the preregistered primary result
    # was observed. These paired duration contrasts were not the primary test.
    print()
    print("EXPLORATORY PAIRED DURATION CONTRASTS")
    for label in ("population", "personal"):
        short = all_results[(2, label)]
        for duration in (5, 15, 30, 60):
            long = all_results[(duration, label)]
            low, high, n_subjects = paired_bootstrap_diff(
                short["subject_r"],
                long["subject_r"],
            )
            diff = short["macro_r"] - long["macro_r"]
            print(
                f"{label:>10} 2s-{duration:>2}s: "
                f"macro_r_diff={diff:+.4f} "
                f"95%CI=[{low:+.4f}, {high:+.4f}] "
                f"subjects={n_subjects}"
            )


if __name__ == "__main__":
    main()
