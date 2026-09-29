"""MARTIN-PVT-TARGET-ALIGNMENT-001.

Independent preregistered replication of Lucent's target-history interaction
in the Martin, Whittaker & Johnston PVT pupillometry dataset.

Preregistration:
experiments/registrations/MARTIN_PVT_TARGET_ALIGNMENT_001.md
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


SENSOR_DURATIONS = (2, 5)
SECONDARY_SENSOR_DURATION = 1
TARGET_HORIZONS = (0, 15, 30, 60)
SAMPLE_RATE_HZ = 250.0
MIN_VALID_FRACTION = 0.70
RT_MIN_MS = 100.0
RT_MAX_MS = 2000.0
RIDGE_ALPHA = 10.0
BOOTSTRAPS = 10_000
SEED = 20260929


@dataclass(frozen=True)
class Trial:
    subject: str
    block: int
    trialn: int
    start_ms: int
    target_ms: int
    rt_ms: float
    foreperiod_s: float
    progress: float


@dataclass
class Anchor:
    subject: str
    block: int
    trialn: int
    task: np.ndarray
    targets: dict[int, float]
    features: dict[int, np.ndarray]


def valid_rt(value: float) -> bool:
    return bool(np.isfinite(value) and RT_MIN_MS <= value <= RT_MAX_MS)


def parse_events(path: Path, subject: str) -> list[Trial]:
    """Parse one EyeLink event stream into trial-level target/RT records."""

    raw_trials = []
    current = None

    def finalize(item):
        if not item:
            return
        required = ("start_ms", "target_ms", "rt_ms", "block", "trialn")
        if not all(key in item for key in required):
            return
        try:
            rt = float(item["rt_ms"])
            start = int(item["start_ms"])
            target = int(item["target_ms"])
            block = int(item["block"])
            trialn = int(item["trialn"])
        except (TypeError, ValueError):
            return
        if target <= start:
            return
        raw_trials.append(
            {
                "block": block,
                "trialn": trialn,
                "start_ms": start,
                "target_ms": target,
                "rt_ms": rt,
            }
        )

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue

            m = re.match(r"MSG\s+\d+\s+TRIALID\s+(\d+)", stripped)
            if m:
                finalize(current)
                current = {"trialid": int(m.group(1))}
                continue

            if current is None:
                continue

            m = re.match(r"START\s+(\d+)", stripped)
            if m:
                current["start_ms"] = int(m.group(1))
                continue

            m = re.match(r"MSG\s+(\d+)\s+.*DISPLAY_target\b", stripped)
            if m and "target_ms" not in current:
                current["target_ms"] = int(m.group(1))
                continue

            m = re.match(
                r"MSG\s+\d+\s+!V\s+TRIAL_VAR\s+RT\s+([+-]?(?:\d+(?:\.\d*)?|\.\d+))",
                stripped,
            )
            if m:
                current["rt_ms"] = float(m.group(1))
                continue

            m = re.match(
                r"MSG\s+\d+\s+!V\s+TRIAL_VAR\s+blockn\s+(\d+)",
                stripped,
            )
            if m:
                current["block"] = int(m.group(1))
                continue

            m = re.match(
                r"MSG\s+\d+\s+!V\s+TRIAL_VAR\s+trialn\s+(\d+)",
                stripped,
            )
            if m:
                current["trialn"] = int(m.group(1))
                continue

    finalize(current)

    # Stable chronological ordering and within-block progress.
    raw_trials.sort(key=lambda x: x["target_ms"])
    block_groups = {}
    for item in raw_trials:
        block_groups.setdefault(item["block"], []).append(item)

    output = []
    for block, items in sorted(block_groups.items()):
        n = len(items)
        for index, item in enumerate(items):
            progress = index / max(n - 1, 1)
            output.append(
                Trial(
                    subject=subject,
                    block=block,
                    trialn=item["trialn"],
                    start_ms=item["start_ms"],
                    target_ms=item["target_ms"],
                    rt_ms=item["rt_ms"],
                    foreperiod_s=(item["target_ms"] - item["start_ms"]) / 1000.0,
                    progress=float(progress),
                )
            )

    output.sort(key=lambda x: x.target_ms)
    return output


def load_samples(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Read timestamp and pupil-area columns from EyeLink ASCII samples."""

    times = []
    pupil = []

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stripped = line.lstrip()
            if not stripped or not stripped[0].isdigit():
                continue

            parts = stripped.split()
            if len(parts) < 4:
                continue

            try:
                timestamp = int(parts[0])
            except ValueError:
                continue

            try:
                value = float(parts[3])
                if not np.isfinite(value) or value <= 0:
                    value = np.nan
            except ValueError:
                value = np.nan

            times.append(timestamp)
            pupil.append(value)

    if not times:
        raise RuntimeError(f"No sample rows parsed from {path}")

    return np.asarray(times, dtype=np.int64), np.asarray(pupil, dtype=float)


def pupil_features(
    times_ms: np.ndarray,
    pupil: np.ndarray,
    target_ms: int,
    duration_s: int,
) -> np.ndarray | None:
    start_ms = target_ms - int(duration_s * 1000)
    lo = int(np.searchsorted(times_ms, start_ms, side="left"))
    hi = int(np.searchsorted(times_ms, target_ms, side="left"))

    if hi <= lo:
        return None

    t = times_ms[lo:hi].astype(float)
    x = pupil[lo:hi].astype(float)

    expected = int(round(duration_s * SAMPLE_RATE_HZ))
    finite = np.isfinite(x)

    valid_fraction = float(finite.sum() / max(expected, 1))
    valid_fraction = min(valid_fraction, 1.0)

    if valid_fraction < MIN_VALID_FRACTION or finite.sum() < 20:
        return None

    tf = t[finite]
    xf = x[finite]

    median = float(np.median(xf))
    if not np.isfinite(median) or median <= 1e-9:
        return None

    normalized = xf / median

    q10, q25, q50, q75, q90 = np.quantile(
        normalized,
        [0.10, 0.25, 0.50, 0.75, 0.90],
    )

    time_s = (tf - target_ms) / 1000.0
    if len(time_s) >= 3 and np.std(time_s) > 1e-12:
        slope = float(np.polyfit(time_s, normalized, 1)[0])
    else:
        slope = np.nan

    # First differences only across temporally adjacent finite samples.
    if len(tf) > 1:
        dt = np.diff(tf)
        dx = np.diff(normalized)
        adjacent = (dt >= 2.0) & (dt <= 8.0) & np.isfinite(dx)
        diffs = dx[adjacent]
    else:
        diffs = np.empty(0, dtype=float)

    mean_abs_diff = (
        float(np.mean(np.abs(diffs))) if len(diffs) else np.nan
    )
    diff_sd = (
        float(np.std(diffs, ddof=1)) if len(diffs) > 1 else np.nan
    )

    out = np.asarray(
        [
            float(np.mean(normalized)),
            float(np.std(normalized, ddof=1)),
            float(q10),
            float(q25),
            float(q50),
            float(q75),
            float(q90),
            slope,
            mean_abs_diff,
            diff_sd,
            valid_fraction,
        ],
        dtype=float,
    )

    return out


def raw_target(
    trials: list[Trial],
    anchor_index: int,
    horizon_s: int,
) -> float | None:
    anchor = trials[anchor_index]

    if not valid_rt(anchor.rt_ms):
        return None

    if horizon_s == 0:
        return 1000.0 / anchor.rt_ms

    deadline = anchor.target_ms + int(horizon_s * 1000)
    values = []

    for trial in trials[anchor_index:]:
        if trial.target_ms > deadline:
            break
        if valid_rt(trial.rt_ms):
            values.append(1000.0 / trial.rt_ms)

    if len(values) < 2:
        return None

    return float(np.mean(values))


def candidate_indices(
    trials: list[Trial],
    block: int,
    times_ms: np.ndarray,
    pupil: np.ndarray,
    require_future_60: bool,
) -> list[int]:
    indices = [i for i, trial in enumerate(trials) if trial.block == block]
    if not indices:
        return []

    block_trials = [trials[i] for i in indices]
    valid_target_times = [
        trial.target_ms for trial in block_trials if valid_rt(trial.rt_ms)
    ]
    if not valid_target_times:
        return []

    last_valid_target = max(valid_target_times)
    accepted = []

    for global_index in indices:
        trial = trials[global_index]

        if not valid_rt(trial.rt_ms):
            continue

        if require_future_60 and trial.target_ms + 60_000 > last_valid_target:
            continue

        if trial.foreperiod_s < max(SENSOR_DURATIONS):
            continue

        ok_targets = True
        for horizon in TARGET_HORIZONS:
            if raw_target(trials, global_index, horizon) is None:
                ok_targets = False
                break
        if not ok_targets:
            continue

        f2 = pupil_features(
            times_ms,
            pupil,
            trial.target_ms,
            2,
        )
        f5 = pupil_features(
            times_ms,
            pupil,
            trial.target_ms,
            5,
        )

        if f2 is None or f5 is None:
            continue

        accepted.append(global_index)

    return accepted


def target_stats_from_block1(
    trials: list[Trial],
    indices: list[int],
) -> dict[int, tuple[float, float]] | None:
    if len(indices) < 12:
        return None

    stats = {}
    for horizon in TARGET_HORIZONS:
        values = np.asarray(
            [raw_target(trials, i, horizon) for i in indices],
            dtype=float,
        )
        values = values[np.isfinite(values)]
        if len(values) < 12:
            return None

        sd = float(np.std(values, ddof=1))
        if not np.isfinite(sd) or sd <= 1e-8:
            return None

        stats[horizon] = (float(np.mean(values)), sd)

    return stats


def subject_from_dir(path: Path) -> str:
    match = re.search(r"sub(\d+)", path.name, flags=re.IGNORECASE)
    if not match:
        return path.name
    return str(int(match.group(1)))


def collect_anchors(root: Path) -> tuple[list[Anchor], dict]:
    anchors = []
    qc = {
        "subjects_seen": 0,
        "subjects_included": 0,
        "excluded_no_block1": 0,
        "excluded_no_eval": 0,
    }

    subject_dirs = sorted(
        p for p in root.glob("sub*") if p.is_dir()
    )

    for subject_dir in subject_dirs:
        subject = subject_from_dir(subject_dir)
        events_path = subject_dir / f"sub{int(subject):03d}_events.asc"
        samples_path = subject_dir / f"sub{int(subject):03d}_samples.asc"

        if not events_path.exists() or not samples_path.exists():
            continue

        qc["subjects_seen"] += 1

        trials = parse_events(events_path, subject)
        if not trials:
            continue

        times_ms, pupil = load_samples(samples_path)

        baseline_indices = candidate_indices(
            trials,
            block=1,
            times_ms=times_ms,
            pupil=pupil,
            require_future_60=True,
        )
        stats = target_stats_from_block1(
            trials,
            baseline_indices,
        )
        if stats is None:
            qc["excluded_no_block1"] += 1
            continue

        subject_anchors = []

        for block in (2, 3):
            eval_indices = candidate_indices(
                trials,
                block=block,
                times_ms=times_ms,
                pupil=pupil,
                require_future_60=True,
            )

            for index in eval_indices:
                trial = trials[index]

                features = {}
                for duration in SENSOR_DURATIONS:
                    feat = pupil_features(
                        times_ms,
                        pupil,
                        trial.target_ms,
                        duration,
                    )
                    if feat is None:
                        features = {}
                        break
                    features[duration] = feat

                if not features:
                    continue

                # 1 s is secondary only and does not define the common set.
                f1 = pupil_features(
                    times_ms,
                    pupil,
                    trial.target_ms,
                    SECONDARY_SENSOR_DURATION,
                )
                if f1 is not None:
                    features[SECONDARY_SENSOR_DURATION] = f1

                targets = {}
                for horizon in TARGET_HORIZONS:
                    raw = raw_target(
                        trials,
                        index,
                        horizon,
                    )
                    if raw is None:
                        targets = {}
                        break
                    mean, sd = stats[horizon]
                    targets[horizon] = (raw - mean) / sd

                if not targets:
                    continue

                task = np.asarray(
                    [
                        trial.foreperiod_s,
                        trial.progress,
                    ],
                    dtype=float,
                )

                subject_anchors.append(
                    Anchor(
                        subject=subject,
                        block=block,
                        trialn=trial.trialn,
                        task=task,
                        targets=targets,
                        features=features,
                    )
                )

        counts = {
            block: sum(
                anchor.block == block
                for anchor in subject_anchors
            )
            for block in (2, 3)
        }

        if max(counts.values(), default=0) < 12:
            qc["excluded_no_eval"] += 1
            continue

        anchors.extend(subject_anchors)
        qc["subjects_included"] += 1

    return anchors, qc


def pearson(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    ok = np.isfinite(x) & np.isfinite(y)
    x = x[ok]
    y = y[ok]

    if len(x) < 3 or np.std(x) <= 1e-12 or np.std(y) <= 1e-12:
        return np.nan

    return float(np.corrcoef(x, y)[0, 1])


def fisher_macro(values):
    values = np.asarray(
        [v for v in values if np.isfinite(v)],
        dtype=float,
    )
    if len(values) == 0:
        return np.nan

    values = np.clip(values, -0.999999, 0.999999)
    return float(np.tanh(np.mean(np.arctanh(values))))


def build_matrix(
    anchors: list[Anchor],
    duration: int,
    horizon: int,
    full: bool,
):
    rows = []
    targets = []
    kept = []

    for index, anchor in enumerate(anchors):
        if full:
            feature = anchor.features.get(duration)
            if feature is None or not np.isfinite(feature).all():
                continue
            row = np.concatenate([anchor.task, feature])
        else:
            row = anchor.task.copy()

        target = anchor.targets[horizon]
        if not np.isfinite(row).all() or not np.isfinite(target):
            continue

        rows.append(row)
        targets.append(target)
        kept.append(index)

    return (
        np.asarray(rows, dtype=float),
        np.asarray(targets, dtype=float),
        np.asarray(kept, dtype=int),
    )


def evaluate(
    anchors: list[Anchor],
    duration: int,
    horizon: int,
    full: bool,
    min_block_n: int = 12,
):
    X, y, kept = build_matrix(
        anchors,
        duration,
        horizon,
        full,
    )

    subjects = sorted(set(anchors[i].subject for i in kept))
    pred = np.full(len(y), np.nan)

    for held_out in subjects:
        train = np.asarray(
            [anchors[i].subject != held_out for i in kept],
            dtype=bool,
        )
        test = ~train

        if train.sum() < 50 or test.sum() < 10:
            continue

        model = make_pipeline(
            StandardScaler(),
            Ridge(alpha=RIDGE_ALPHA),
        )
        model.fit(X[train], y[train])
        pred[test] = model.predict(X[test])

    block_scores = {}
    for subject in subjects:
        for block in (2, 3):
            mask = np.asarray(
                [
                    anchors[i].subject == subject
                    and anchors[i].block == block
                    for i in kept
                ],
                dtype=bool,
            )

            if mask.sum() < min_block_n:
                continue

            score = pearson(
                y[mask],
                pred[mask],
            )
            if np.isfinite(score):
                block_scores[(subject, block)] = score

    person_scores = {}
    for subject in subjects:
        values = [
            block_scores[(subject, block)]
            for block in (2, 3)
            if (subject, block) in block_scores
        ]
        if values:
            person_scores[subject] = fisher_macro(values)

    return {
        "macro_r": fisher_macro(person_scores.values()),
        "person_scores": person_scores,
        "block_scores": block_scores,
        "n_people": len(person_scores),
        "n_blocks": len(block_scores),
        "n_rows": len(y),
    }


def primary_interaction(results):
    cells = {
        "short0": results[(2, 0)]["person_scores"],
        "long0": results[(5, 0)]["person_scores"],
        "short60": results[(2, 60)]["person_scores"],
        "long60": results[(5, 60)]["person_scores"],
    }

    people = sorted(
        set.intersection(*(set(cell) for cell in cells.values()))
    )
    people = [
        person
        for person in people
        if all(
            np.isfinite(cells[key][person])
            for key in cells
        )
    ]

    if len(people) < 5:
        return {
            "people": len(people),
            "d0": np.nan,
            "d60": np.nan,
            "interaction": np.nan,
            "ci_low": np.nan,
            "ci_high": np.nan,
        }

    arrays = {
        key: np.asarray(
            [cell[person] for person in people],
            dtype=float,
        )
        for key, cell in cells.items()
    }

    def statistic(indices):
        d0 = (
            fisher_macro(arrays["long0"][indices])
            - fisher_macro(arrays["short0"][indices])
        )
        d60 = (
            fisher_macro(arrays["long60"][indices])
            - fisher_macro(arrays["short60"][indices])
        )
        return d0, d60, d60 - d0

    full_index = np.arange(len(people))
    d0, d60, point = statistic(full_index)

    rng = np.random.default_rng(SEED)
    boot = np.empty(BOOTSTRAPS, dtype=float)

    for i in range(BOOTSTRAPS):
        sample = rng.integers(
            0,
            len(people),
            len(people),
        )
        _, _, boot[i] = statistic(sample)

    return {
        "people": len(people),
        "d0": d0,
        "d60": d60,
        "interaction": point,
        "ci_low": float(np.quantile(boot, 0.025)),
        "ci_high": float(np.quantile(boot, 0.975)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-root",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )
    args = parser.parse_args()

    anchors, qc = collect_anchors(args.data_root)

    if len(anchors) < 200:
        raise RuntimeError(
            f"Only {len(anchors)} evaluation anchors survived frozen QC"
        )

    subjects = sorted(set(anchor.subject for anchor in anchors))

    full = {}
    nuisance = {}

    for horizon in TARGET_HORIZONS:
        for duration in SENSOR_DURATIONS:
            full[(duration, horizon)] = evaluate(
                anchors,
                duration,
                horizon,
                full=True,
            )
        nuisance[horizon] = evaluate(
            anchors,
            duration=2,
            horizon=horizon,
            full=False,
        )

    primary = primary_interaction(full)
    supported = bool(
        np.isfinite(primary["interaction"])
        and primary["interaction"] > 0
        and primary["ci_low"] > 0
    )

    # Secondary 1-second window uses the subset on which 1 s features exist.
    secondary_1s = {
        horizon: evaluate(
            anchors,
            duration=1,
            horizon=horizon,
            full=True,
        )
        for horizon in TARGET_HORIZONS
    }

    sensitivity = {}
    for threshold in (15, 20):
        temp = {}
        for horizon in (0, 60):
            for duration in SENSOR_DURATIONS:
                temp[(duration, horizon)] = evaluate(
                    anchors,
                    duration,
                    horizon,
                    full=True,
                    min_block_n=threshold,
                )
        if all(
            np.isfinite(temp[key]["macro_r"])
            for key in temp
        ):
            interaction = (
                (
                    temp[(5, 60)]["macro_r"]
                    - temp[(2, 60)]["macro_r"]
                )
                - (
                    temp[(5, 0)]["macro_r"]
                    - temp[(2, 0)]["macro_r"]
                )
            )
        else:
            interaction = np.nan
        sensitivity[threshold] = interaction

    lines = []
    lines.append(
        "# MARTIN-PVT-TARGET-ALIGNMENT-001: Independent PVT Replication"
    )
    lines.append("")
    lines.append(
        "**Status:** completed preregistered independent public-human-data analysis."
    )
    lines.append("")
    lines.append(
        f"**Primary Temporal Alignment interaction:** "
        f"**{'SUPPORTED' if supported else 'NOT SUPPORTED'}**."
    )
    lines.append("")
    lines.append("## Dataset and frozen protocol")
    lines.append("")
    lines.append(
        "Martin, Whittaker & Johnston (2022), Experiment 2; "
        "250 Hz EyeLink pupil area during a psychomotor-vigilance task."
    )
    lines.append("")
    lines.append(f"- participant folders seen: **{qc['subjects_seen']}**")
    lines.append(
        f"- participants included after frozen Block-1/evaluation QC: "
        f"**{qc['subjects_included']}**"
    )
    lines.append(f"- common Block 2/3 anchors: **{len(anchors):,}**")
    lines.append(
        "- strict leave-one-participant-out prediction; "
        "held-out Block 1 used only for that person's target normalization"
    )
    lines.append(
        "- predictors end immediately before target onset; "
        "no target-evoked pupil samples are used"
    )
    lines.append("")
    lines.append("## Duration x target-horizon matrix")
    lines.append("")
    lines.append(
        "| Target horizon | 2 s pupil history | 5 s pupil history | "
        "D(H)=5 s - 2 s |"
    )
    lines.append("| ---: | ---: | ---: | ---: |")

    for horizon in TARGET_HORIZONS:
        short = full[(2, horizon)]["macro_r"]
        long = full[(5, horizon)]["macro_r"]
        lines.append(
            f"| H{horizon} | **{short:.4f}** | **{long:.4f}** | "
            f"{long - short:+.4f} |"
        )

    lines.append("")
    lines.append(
        "Macro-r is the Fisher-z average of held-out participant scores; "
        "Block 2 and Block 3 correlations are first combined within person."
    )
    lines.append("")
    lines.append("## Preregistered primary interaction")
    lines.append("")
    lines.append(f"- D(H0): **{primary['d0']:+.4f}**")
    lines.append(f"- D(H60): **{primary['d60']:+.4f}**")
    lines.append(
        f"- Delta = D(H60) - D(H0): "
        f"**{primary['interaction']:+.4f}**"
    )
    lines.append(
        f"- paired participant-bootstrap 95% CI: "
        f"**[{primary['ci_low']:+.4f}, "
        f"{primary['ci_high']:+.4f}]**"
    )
    lines.append(
        f"- paired participants: **{primary['people']}**"
    )
    lines.append("")
    lines.append(
        "The frozen criterion requires a positive interaction and a "
        "95% interval entirely above zero."
    )
    lines.append("")
    lines.append(
        f"**Decision: {'supported.' if supported else 'not supported.'}**"
    )

    lines.append("")
    lines.append("## Nuisance-only baseline")
    lines.append("")
    lines.append(
        "The nuisance model uses only actual foreperiod and normalized "
        "block progress."
    )
    lines.append("")
    lines.append("| Target horizon | nuisance-only macro-r |")
    lines.append("| ---: | ---: |")
    for horizon in TARGET_HORIZONS:
        lines.append(
            f"| H{horizon} | {nuisance[horizon]['macro_r']:.4f} |"
        )

    lines.append("")
    lines.append("## Secondary 1-second history")
    lines.append("")
    lines.append("| Target horizon | 1 s macro-r |")
    lines.append("| ---: | ---: |")
    for horizon in TARGET_HORIZONS:
        lines.append(
            f"| H{horizon} | {secondary_1s[horizon]['macro_r']:.4f} |"
        )

    lines.append("")
    lines.append("## Block-count sensitivity")
    lines.append("")
    lines.append("| Minimum anchors/block | unbootstrapped interaction |")
    lines.append("| ---: | ---: |")
    for threshold in (15, 20):
        lines.append(
            f"| {threshold} | {sensitivity[threshold]:+.4f} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if supported:
        lines.append(
            "The positive target-horizon x pupil-history interaction "
            "replicated in an independent PVT cohort measured with a "
            "different eye tracker and pupil signal. This supports the "
            "specific claim that, within PVT-style vigilance prediction, "
            "broadening the behavioral estimand can increase the relative "
            "value of longer pre-target ocular history."
        )
    else:
        lines.append(
            "The independent PVT cohort did not satisfy the preregistered "
            "positive interaction criterion. The Massoz crossover therefore "
            "remains dataset-specific under the current evidence."
        )

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "This analysis concerns pre-target pupil history and PVT performance. "
        "It does not validate APST-5 active probing, smartphone pupillometry, "
        "fatigue diagnosis, or a universal temporal-alignment law."
    )
    lines.append("")
    lines.append("## Reproduction")
    lines.append("")
    lines.append(
        "The workflow downloads the public CC BY 4.0 Figshare archive, "
        "extracts only the published ASCII event/sample files, and runs this "
        "committed analysis. Participant data are not redistributed by Lucent."
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(lines[:100]))


if __name__ == "__main__":
    main()
