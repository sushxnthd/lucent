"""MTS-TARGET-SMOOTHING-001.

Preregistered direct test of the Temporal Alignment Principle.

The experiment holds the public Massoz eyelid/PVT dataset, feature map, model
family, and LOSO evaluation fixed while manipulating only the temporal support
of the behavioral target.

Preregistration:
experiments/registrations/MTS_TARGET_SMOOTHING_001.md
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import mts_realdata_baseline_compression as mts


SENSOR_DURATIONS = (2, 5, 15, 30, 60)
TARGET_HORIZONS = (0, 15, 30, 60)
MAX_SENSOR = max(SENSOR_DURATIONS)
MAX_TARGET = max(TARGET_HORIZONS)
SEED = 20260929
BOOTSTRAPS = 10_000
MIN_SMOOTH_RESPONSES = 2


@dataclass(frozen=True)
class EventSample:
    subject: int
    session_test: int
    onset_s: float
    end_frame: int
    targets: dict[int, float]


def valid_rt(rt_ms: float) -> bool:
    return bool(np.isfinite(rt_ms) and 100.0 <= rt_ms <= 2000.0)


def speed(rt_ms: float) -> float:
    return 1000.0 / rt_ms


def smoothed_speed(
    event_time_s: np.ndarray,
    rt_ms: np.ndarray,
    index: int,
    horizon_s: int,
) -> float | None:
    if not valid_rt(float(rt_ms[index])):
        return None

    if horizon_s == 0:
        return speed(float(rt_ms[index]))

    t0 = float(event_time_s[index])
    mask = (
        (event_time_s >= t0)
        & (event_time_s <= t0 + float(horizon_s))
        & np.isfinite(rt_ms)
        & (rt_ms >= 100.0)
        & (rt_ms <= 2000.0)
    )
    values = 1000.0 / rt_ms[mask]
    if len(values) < MIN_SMOOTH_RESPONSES:
        return None
    return float(np.mean(values))


def common_indices(session: mts.Session) -> list[int]:
    if len(session.event_time_s) == 0:
        return []

    last_event = float(session.event_time_s[-1])
    output: list[int] = []

    for i, onset in enumerate(session.event_time_s):
        onset = float(onset)
        if not valid_rt(float(session.rt_ms[i])):
            continue
        if onset < MAX_SENSOR:
            continue
        if onset + MAX_TARGET > last_event:
            continue

        ok = True
        for horizon in TARGET_HORIZONS:
            if smoothed_speed(
                session.event_time_s,
                session.rt_ms,
                i,
                horizon,
            ) is None:
                ok = False
                break

        if ok:
            output.append(i)

    return output


def baseline_target_stats(
    data: mts.SubjectData,
) -> dict[int, tuple[float, float]]:
    idx = common_indices(data.baseline)
    if len(idx) < 12:
        raise ValueError(
            f"subject {data.subject}: too few common baseline targets ({len(idx)})"
        )

    result = {}
    for horizon in TARGET_HORIZONS:
        values = np.asarray(
            [
                smoothed_speed(
                    data.baseline.event_time_s,
                    data.baseline.rt_ms,
                    i,
                    horizon,
                )
                for i in idx
            ],
            dtype=float,
        )
        values = values[np.isfinite(values)]
        if len(values) < 12:
            raise ValueError(
                f"subject {data.subject}: insufficient baseline H={horizon}"
            )
        sd = float(np.std(values, ddof=1))
        if not np.isfinite(sd) or sd <= 1e-8:
            raise ValueError(
                f"subject {data.subject}: degenerate baseline H={horizon}"
            )
        result[horizon] = (float(np.mean(values)), sd)

    return result


def collect_subject_events(
    data: mts.SubjectData,
    target_stats: dict[int, tuple[float, float]],
) -> list[EventSample]:
    events: list[EventSample] = []

    for session in data.later:
        idx = common_indices(session)
        for i in idx:
            targets = {}
            for horizon in TARGET_HORIZONS:
                raw = smoothed_speed(
                    session.event_time_s,
                    session.rt_ms,
                    i,
                    horizon,
                )
                if raw is None:
                    targets = {}
                    break
                mean, sd = target_stats[horizon]
                targets[horizon] = (raw - mean) / sd

            if not targets:
                continue

            onset = float(session.event_time_s[i])
            end_frame = int(np.floor(onset * mts.FPS))
            if end_frame > len(session.eye):
                continue

            events.append(
                EventSample(
                    subject=data.subject,
                    session_test=session.test,
                    onset_s=onset,
                    end_frame=end_frame,
                    targets=targets,
                )
            )

    return events


def population_fold_reference(
    dataset: dict[int, mts.SubjectData],
    train_subjects: list[int],
    duration_s: int,
):
    return mts.build_fold_quantities(
        dataset,
        train_subjects,
        duration_s,
    )


def features_for_subject(
    data: mts.SubjectData,
    events: list[EventSample],
    duration_s: int,
    open_ref: np.ndarray,
    baseline_vector: np.ndarray,
) -> np.ndarray:
    n = int(round(duration_s * mts.FPS))
    windows = []
    session_map = {s.test: s for s in data.later}

    for event in events:
        session = session_map[event.session_test]
        start = event.end_frame - n
        end = event.end_frame
        if start < 0 or end > len(session.eye):
            raise RuntimeError("common event unexpectedly lacks requested window")
        windows.append(session.eye[start:end])

    if not windows:
        return np.empty((0, 15), dtype=float)

    x = mts.feature_map_many(
        np.stack(windows, axis=0),
        open_ref,
        duration_s,
    )
    return x - baseline_vector.reshape(1, -1)


def pearson(y: np.ndarray, pred: np.ndarray) -> float:
    if len(y) < 5:
        return np.nan
    if np.std(y) <= 1e-12 or np.std(pred) <= 1e-12:
        return np.nan
    return float(np.corrcoef(y, pred)[0, 1])


def macro_r(subject_r: dict[int, float]) -> float:
    vals = np.asarray(
        [v for v in subject_r.values() if np.isfinite(v)],
        dtype=float,
    )
    if len(vals) == 0:
        return np.nan
    vals = np.clip(vals, -0.999999, 0.999999)
    return float(np.tanh(np.mean(np.arctanh(vals))))


def evaluate_cell(
    dataset: dict[int, mts.SubjectData],
    all_events: dict[int, list[EventSample]],
    duration_s: int,
    target_horizon_s: int,
):
    subject_r: dict[int, float] = {}
    subject_n: dict[int, int] = {}

    for held_out in sorted(dataset):
        train_subjects = [s for s in sorted(dataset) if s != held_out]

        open_ref, baseline_vector = population_fold_reference(
            dataset,
            train_subjects,
            duration_s,
        )

        train_x = []
        train_y = []

        for subject in train_subjects:
            events = all_events[subject]
            if not events:
                continue
            x = features_for_subject(
                dataset[subject],
                events,
                duration_s,
                open_ref,
                baseline_vector,
            )
            y = np.asarray(
                [e.targets[target_horizon_s] for e in events],
                dtype=float,
            )
            keep = np.isfinite(x).all(axis=1) & np.isfinite(y)
            if np.any(keep):
                train_x.append(x[keep])
                train_y.append(y[keep])

        if not train_x:
            continue

        x_train = np.vstack(train_x)
        y_train = np.concatenate(train_y)

        test_events = all_events[held_out]
        if len(test_events) < 10:
            continue

        x_test = features_for_subject(
            dataset[held_out],
            test_events,
            duration_s,
            open_ref,
            baseline_vector,
        )
        y_test = np.asarray(
            [e.targets[target_horizon_s] for e in test_events],
            dtype=float,
        )

        keep = np.isfinite(x_test).all(axis=1) & np.isfinite(y_test)
        x_test = x_test[keep]
        y_test = y_test[keep]

        if len(y_test) < 10:
            continue

        model = make_pipeline(
            StandardScaler(),
            Ridge(alpha=mts.ALPHA),
        )
        model.fit(x_train, y_train)
        pred = model.predict(x_test)

        subject_r[held_out] = pearson(y_test, pred)
        subject_n[held_out] = int(len(y_test))

    return {
        "macro_r": macro_r(subject_r),
        "subject_r": subject_r,
        "subject_n": subject_n,
    }


def fisher_macro_array(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return np.nan
    values = np.clip(values, -0.999999, 0.999999)
    return float(np.tanh(np.mean(np.arctanh(values))))


def interaction_bootstrap(results):
    cells = {
        "short0": results[(2, 0)]["subject_r"],
        "long0": results[(60, 0)]["subject_r"],
        "short60": results[(2, 60)]["subject_r"],
        "long60": results[(60, 60)]["subject_r"],
    }

    subjects = sorted(set.intersection(*(set(v) for v in cells.values())))
    subjects = [
        s
        for s in subjects
        if all(np.isfinite(cells[k][s]) for k in cells)
    ]

    arrays = {
        k: np.asarray([v[s] for s in subjects], dtype=float)
        for k, v in cells.items()
    }

    d0 = fisher_macro_array(arrays["long0"]) - fisher_macro_array(arrays["short0"])
    d60 = fisher_macro_array(arrays["long60"]) - fisher_macro_array(arrays["short60"])
    point = d60 - d0

    rng = np.random.default_rng(SEED)
    boot = np.empty(BOOTSTRAPS, dtype=float)

    for i in range(BOOTSTRAPS):
        idx = rng.integers(0, len(subjects), len(subjects))
        b0 = (
            fisher_macro_array(arrays["long0"][idx])
            - fisher_macro_array(arrays["short0"][idx])
        )
        b60 = (
            fisher_macro_array(arrays["long60"][idx])
            - fisher_macro_array(arrays["short60"][idx])
        )
        boot[i] = b60 - b0

    return {
        "subjects": len(subjects),
        "d0": d0,
        "d60": d60,
        "interaction": point,
        "ci_low": float(np.quantile(boot, 0.025)),
        "ci_high": float(np.quantile(boot, 0.975)),
    }


def paired_duration_diff(results, long_duration, horizon):
    a = results[(long_duration, horizon)]["subject_r"]
    b = results[(2, horizon)]["subject_r"]
    subjects = sorted(set(a).intersection(b))
    subjects = [s for s in subjects if np.isfinite(a[s]) and np.isfinite(b[s])]
    av = np.asarray([a[s] for s in subjects], dtype=float)
    bv = np.asarray([b[s] for s in subjects], dtype=float)
    return fisher_macro_array(av) - fisher_macro_array(bv)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        dataset = mts.load_dataset(Path(tmp))

    target_stats = {}
    usable_dataset = {}

    for subject, data in dataset.items():
        try:
            stats = baseline_target_stats(data)
        except ValueError:
            continue
        events = collect_subject_events(data, stats)
        if len(events) < 10:
            continue
        target_stats[subject] = stats
        usable_dataset[subject] = data

    dataset = usable_dataset
    all_events = {
        subject: collect_subject_events(data, target_stats[subject])
        for subject, data in dataset.items()
    }

    print("MTS-TARGET-SMOOTHING-001")
    print("=" * 80)
    print(f"subjects: {len(dataset)}")
    print(
        "events per subject: "
        + ", ".join(
            f"{s}:{len(all_events[s])}"
            for s in sorted(all_events)
        )
    )
    print()

    results = {}
    for horizon in TARGET_HORIZONS:
        for duration in SENSOR_DURATIONS:
            out = evaluate_cell(
                dataset,
                all_events,
                duration,
                horizon,
            )
            results[(duration, horizon)] = out
            print(
                f"H={horizon:>2}s T={duration:>2}s "
                f"macro_r={out['macro_r']:+.6f} "
                f"subjects={len(out['subject_r'])}"
            )
        print()

    primary = interaction_bootstrap(results)
    supported = (
        primary["interaction"] > 0.0
        and primary["ci_low"] > 0.0
    )

    print("PRIMARY TEMPORAL-ALIGNMENT INTERACTION")
    print(f"D(0s)=r60-r2:  {primary['d0']:+.6f}")
    print(f"D(60s)=r60-r2: {primary['d60']:+.6f}")
    print(f"Delta=D(60)-D(0): {primary['interaction']:+.6f}")
    print(
        f"paired subject bootstrap 95% CI: "
        f"[{primary['ci_low']:+.6f}, {primary['ci_high']:+.6f}] "
        f"(subjects={primary['subjects']}, B={BOOTSTRAPS})"
    )
    print(
        "CONFIRMATORY DECISION: "
        + ("SUPPORTED" if supported else "NOT SUPPORTED")
    )

    print()
    print("SECONDARY LONG-vs-2s DURATION DIFFERENCES")
    for horizon in TARGET_HORIZONS:
        vals = []
        for duration in (5, 15, 30, 60):
            vals.append(
                f"{duration}s:{paired_duration_diff(results, duration, horizon):+.4f}"
            )
        print(f"H={horizon:>2}s  " + "  ".join(vals))

    lines = []
    lines.append("# MTS-TARGET-SMOOTHING-001: Direct Temporal-Alignment Test")
    lines.append("")
    lines.append("**Status:** completed preregistered public-data experiment.")
    lines.append("")
    lines.append(
        f"**Primary prediction:** **{'SUPPORTED' if supported else 'NOT SUPPORTED'}**."
    )
    lines.append("")
    lines.append("## Manipulation")
    lines.append("")
    lines.append(
        "The ocular data, participants, feature family, Ridge model, and LOSO "
        "protocol are held fixed. Only the behavioral target's future temporal "
        "support is broadened from the current PVT response to a 60-second "
        "mean response-speed target."
    )
    lines.append("")
    lines.append("## Duration x target-horizon matrix")
    lines.append("")
    lines.append("| Target support | 2 s sensor | 5 s | 15 s | 30 s | 60 s |")
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: |")
    for horizon in TARGET_HORIZONS:
        row = [f"{horizon} s"]
        for duration in SENSOR_DURATIONS:
            row.append(f"{results[(duration, horizon)]['macro_r']:.4f}")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("## Preregistered interaction")
    lines.append("")
    lines.append(
        "Define D(H) = macro-r(60 s sensor, H) - macro-r(2 s sensor, H)."
    )
    lines.append("")
    lines.append(f"- D(0 s): **{primary['d0']:+.4f}**")
    lines.append(f"- D(60 s): **{primary['d60']:+.4f}**")
    lines.append(
        f"- Delta = D(60) - D(0): **{primary['interaction']:+.4f}**"
    )
    lines.append(
        f"- paired subject-bootstrap 95% CI: "
        f"**[{primary['ci_low']:+.4f}, {primary['ci_high']:+.4f}]**"
    )
    lines.append(f"- paired subjects: **{primary['subjects']}**")
    lines.append("")
    lines.append(
        "The preregistered criterion requires a positive interaction with the "
        "entire 95% interval above zero."
    )
    lines.append("")
    lines.append(
        f"**Decision: {'supported.' if supported else 'not supported.'}**"
    )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if supported:
        lines.append(
            "Within the same human dataset, broadening the behavioral target "
            "from an immediate PVT response to a 60-second performance summary "
            "made the 60-second ocular history significantly more useful "
            "relative to the 2-second history. This directly supports a "
            "target-dependent sensing horizon under the frozen analysis."
        )
    else:
        lines.append(
            "Broadening the behavioral target did not produce the "
            "preregistered positive shift in the relative value of the longer "
            "ocular history. Cross-dataset sign differences therefore remain "
            "descriptive rather than direct evidence of a causal temporal-"
            "alignment mechanism."
        )

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "This experiment tests temporal alignment in public eyelid/PVT data. "
        "It does not validate APST-5 active probing, smartphone pupillometry, "
        "or a clinical fatigue diagnostic."
    )
    lines.append("")
    lines.append("## Reproduction")
    lines.append("")
    lines.append('    pip install -e ".[dev]"')
    lines.append("    python experiments/mts_target_smoothing.py")

    Path("results/MTS_TARGET_SMOOTHING_001.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
