"""MTS-TEMPORAL-ALIGNMENT-NUISANCE-001.

Preregistered nuisance-adjusted audit of the MTS Temporal Alignment crossover.

Preregistration:
experiments/registrations/MTS_TEMPORAL_ALIGNMENT_NUISANCE_001.md
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import mts_realdata_baseline_compression as mts
import mts_target_smoothing as base


def nuisance_matrix(data: mts.SubjectData, events: list[base.EventSample]) -> np.ndarray:
    session_map = {session.test: session for session in data.later}
    rows = []

    for event in events:
        session = session_map[event.session_test]
        last = float(session.event_time_s[-1]) if len(session.event_time_s) else 1.0
        progress = float(event.onset_s) / max(last, 1.0)
        session_indicator = 1.0 if int(event.session_test) == 3 else 0.0
        rows.append(
            [
                progress,
                progress * progress,
                session_indicator,
            ]
        )

    return np.asarray(rows, dtype=float)


def evaluate_adjusted(
    dataset: dict[int, mts.SubjectData],
    all_events: dict[int, list[base.EventSample]],
    duration_s: int,
    horizon_s: int,
    full: bool,
):
    subject_r = {}
    subject_n = {}

    for held_out in sorted(dataset):
        train_subjects = [s for s in sorted(dataset) if s != held_out]

        if full:
            open_ref, baseline_vector = base.population_fold_reference(
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

            nuisance = nuisance_matrix(dataset[subject], events)

            if full:
                ocular = base.features_for_subject(
                    dataset[subject],
                    events,
                    duration_s,
                    open_ref,
                    baseline_vector,
                )
                x = np.concatenate([nuisance, ocular], axis=1)
            else:
                x = nuisance

            y = np.asarray(
                [event.targets[horizon_s] for event in events],
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

        nuisance = nuisance_matrix(dataset[held_out], test_events)

        if full:
            ocular = base.features_for_subject(
                dataset[held_out],
                test_events,
                duration_s,
                open_ref,
                baseline_vector,
            )
            x_test = np.concatenate([nuisance, ocular], axis=1)
        else:
            x_test = nuisance

        y_test = np.asarray(
            [event.targets[horizon_s] for event in test_events],
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

        subject_r[held_out] = base.pearson(y_test, pred)
        subject_n[held_out] = int(len(y_test))

    return {
        "macro_r": base.macro_r(subject_r),
        "subject_r": subject_r,
        "subject_n": subject_n,
    }


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        dataset = mts.load_dataset(Path(tmp))

    target_stats = {}
    usable = {}

    for subject, data in dataset.items():
        try:
            stats = base.baseline_target_stats(data)
        except ValueError:
            continue

        events = base.collect_subject_events(data, stats)
        if len(events) < 10:
            continue

        target_stats[subject] = stats
        usable[subject] = data

    dataset = usable
    all_events = {
        subject: base.collect_subject_events(
            data,
            target_stats[subject],
        )
        for subject, data in dataset.items()
    }

    full = {}
    nuisance = {}

    for horizon in base.TARGET_HORIZONS:
        nuisance[horizon] = evaluate_adjusted(
            dataset,
            all_events,
            duration_s=2,
            horizon_s=horizon,
            full=False,
        )

        for duration in base.SENSOR_DURATIONS:
            full[(duration, horizon)] = evaluate_adjusted(
                dataset,
                all_events,
                duration_s=duration,
                horizon_s=horizon,
                full=True,
            )

    primary = base.interaction_bootstrap(full)
    supported = bool(
        primary["interaction"] > 0
        and primary["ci_low"] > 0
    )

    lines = []
    lines.append(
        "# MTS-TEMPORAL-ALIGNMENT-NUISANCE-001: Time-on-Task Audit"
    )
    lines.append("")
    lines.append(
        "**Status:** completed preregistered nuisance-adjusted audit."
    )
    lines.append("")
    lines.append(
        f"**Original crossover survives frozen nuisance adjustment:** "
        f"**{'YES' if supported else 'NO'}**."
    )
    lines.append("")
    lines.append("## Adjustment")
    lines.append("")
    lines.append(
        "Every duration model receives the same explicit nuisance vector: "
        "normalized time-on-task, squared normalized time-on-task, and "
        "PVT2/PVT3 session indicator."
    )
    lines.append("")
    lines.append("## Adjusted duration x target-horizon matrix")
    lines.append("")
    lines.append(
        "| Target support | 2 s | 5 s | 15 s | 30 s | 60 s | nuisance only |"
    )
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")

    for horizon in base.TARGET_HORIZONS:
        row = [f"{horizon} s"]
        for duration in base.SENSOR_DURATIONS:
            row.append(f"{full[(duration, horizon)]['macro_r']:.4f}")
        row.append(f"{nuisance[horizon]['macro_r']:.4f}")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("## Preregistered adjusted interaction")
    lines.append("")
    lines.append(f"- D(0 s) = r60-r2: **{primary['d0']:+.4f}**")
    lines.append(f"- D(60 s) = r60-r2: **{primary['d60']:+.4f}**")
    lines.append(
        f"- Delta = D(60)-D(0): **{primary['interaction']:+.4f}**"
    )
    lines.append(
        f"- paired subject-bootstrap 95% CI: "
        f"**[{primary['ci_low']:+.4f}, {primary['ci_high']:+.4f}]**"
    )
    lines.append(f"- paired subjects: **{primary['subjects']}**")
    lines.append("")
    lines.append(
        "The frozen robustness criterion requires a positive interaction with "
        "the entire interval above zero."
    )
    lines.append("")
    lines.append(
        f"**Decision: {'survives.' if supported else 'does not survive.'}**"
    )

    lines.append("")
    lines.append("## Increment over nuisance-only")
    lines.append("")
    lines.append(
        "| Target support | 2 s ocular increment | 60 s ocular increment |"
    )
    lines.append("| ---: | ---: | ---: |")
    for horizon in base.TARGET_HORIZONS:
        short = (
            full[(2, horizon)]["macro_r"]
            - nuisance[horizon]["macro_r"]
        )
        long = (
            full[(60, horizon)]["macro_r"]
            - nuisance[horizon]["macro_r"]
        )
        lines.append(
            f"| {horizon} s | {short:+.4f} | {long:+.4f} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if supported:
        lines.append(
            "The Massoz target-history crossover remains significant after "
            "all sensor-duration models are given the same explicit "
            "time-on-task and session identity covariates. The result is "
            "therefore not explained solely by this frozen temporal nuisance "
            "model, although it remains dataset-specific."
        )
    else:
        lines.append(
            "The Massoz target-history crossover no longer satisfies its "
            "confirmatory criterion after explicit time-on-task/session "
            "adjustment. The earlier interaction must therefore be treated as "
            "potentially dependent on slow temporal/session structure rather "
            "than as clean evidence that target support itself determines the "
            "useful ocular history."
        )

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "This audit controls a predeclared low-frequency nuisance model only. "
        "It neither proves nor excludes other physiological temporal effects."
    )

    Path("results/MTS_TEMPORAL_ALIGNMENT_NUISANCE_001.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(lines))


if __name__ == "__main__":
    main()
