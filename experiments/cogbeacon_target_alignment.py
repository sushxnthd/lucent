"""COGBEACON-TARGET-ALIGNMENT-001.

Preregistered independent replication of the Temporal Alignment interaction.

Preregistration:
experiments/registrations/COGBEACON_TARGET_ALIGNMENT_001.md
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import cogbeacon_temporal_locality as base


SEED = 20260929
BOOTSTRAPS = 10_000
SENSOR_WINDOWS = (2, 5)
TARGET_HORIZONS = (1, 3, 5)
FPS = 2
RIDGE_ALPHA = 10.0


@dataclass
class Anchor:
    subject: str
    session: str
    round_id: int
    task: np.ndarray
    frames: list[np.ndarray]
    targets: dict[int, float]


def bool_response(value) -> bool:
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    return str(value).strip().lower() == "true"


def performance_file(root: Path, session: str) -> Path | None:
    candidates = sorted((root / "user_performance").glob(session + "_*.csv"))
    return candidates[0] if candidates else None


def collect_anchors(root: Path) -> list[Anchor]:
    face_root = root / "face_keypoints"
    anchors: list[Anchor] = []

    for session_dir in sorted(p for p in face_root.iterdir() if p.is_dir()):
        session = session_dir.name
        perf_path = performance_file(root, session)
        if perf_path is None:
            continue

        perf = pd.read_csv(perf_path, sep="\t")
        perf.columns = [str(c).strip() for c in perf.columns]
        perf = perf.sort_values("Round").reset_index(drop=True)

        by_round: dict[int, list[tuple[int, np.ndarray, int]]] = {}
        for path in session_dir.glob("*.npz"):
            parsed = base.parse_frame_name(path)
            if parsed is None:
                continue
            under_rule, round_id, frame_id = parsed
            try:
                pts = base.load_landmarks(path)
            except Exception:
                continue
            by_round.setdefault(round_id, []).append(
                (frame_id, pts, under_rule)
            )

        max_round = max(by_round) if by_round else int(perf["Round"].max())

        correct_rows = []
        for _, row in perf.iterrows():
            try:
                round_id = int(row["Round"])
                rt = float(row["Time"])
                correct = bool_response(row["Response"])
            except Exception:
                continue

            if not correct or not np.isfinite(rt) or rt <= 0:
                continue

            correct_rows.append(
                {
                    "round_id": round_id,
                    "log_rt": float(np.log(rt)),
                    "row": row,
                }
            )

        for pos, item in enumerate(correct_rows):
            # H5 requires current + four future correct rounds.
            if pos + max(TARGET_HORIZONS) > len(correct_rows):
                continue

            round_id = item["round_id"]
            frames = sorted(
                by_round.get(round_id, []),
                key=lambda z: z[0],
            )
            if len(frames) < FPS * max(SENSOR_WINDOWS):
                continue

            frame_arrays = [x[1] for x in frames]
            under_rule = float(frames[-1][2])
            row = item["row"]

            level = float(row.get("Level", 0))
            question = float(row.get("Question", 0))
            progress = float(round_id) / max(float(max_round), 1.0)
            task = np.array(
                [level, question, progress, under_rule],
                dtype=float,
            )

            targets = {}
            for horizon in TARGET_HORIZONS:
                values = [
                    correct_rows[j]["log_rt"]
                    for j in range(pos, pos + horizon)
                ]
                targets[horizon] = float(np.mean(values))

            anchors.append(
                Anchor(
                    subject=base.subject_from_session(session),
                    session=session,
                    round_id=round_id,
                    task=task,
                    frames=frame_arrays,
                    targets=targets,
                )
            )

    return anchors


def pearson(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 3 or np.std(x) < 1e-12 or np.std(y) < 1e-12:
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


def matrix(anchors: list[Anchor], duration: int, horizon: int, full: bool):
    rows = []
    target = []

    for anchor in anchors:
        if full:
            face = base.summarize_window(
                anchor.frames,
                duration * FPS,
            )
            x = np.concatenate([anchor.task, face])
        else:
            x = anchor.task.copy()

        rows.append(x)
        target.append(anchor.targets[horizon])

    return np.asarray(rows, dtype=float), np.asarray(target, dtype=float)


def evaluate(
    anchors: list[Anchor],
    duration: int,
    horizon: int,
    full: bool,
    min_session_n: int = 12,
):
    subjects = sorted(set(a.subject for a in anchors))
    X, y = matrix(anchors, duration, horizon, full)
    pred = np.full(len(anchors), np.nan)

    for held_out in subjects:
        train = np.array([a.subject != held_out for a in anchors])
        test = ~train

        model = make_pipeline(
            StandardScaler(),
            Ridge(alpha=RIDGE_ALPHA),
        )
        model.fit(X[train], y[train])
        pred[test] = model.predict(X[test])

    session_scores: dict[str, float] = {}
    for session in sorted(set(a.session for a in anchors)):
        idx = np.array([a.session == session for a in anchors])
        if idx.sum() < min_session_n:
            continue
        session_scores[session] = pearson(y[idx], pred[idx])

    person_scores: dict[str, float] = {}
    for subject in subjects:
        sessions = sorted(
            set(
                a.session
                for a in anchors
                if a.subject == subject
                and a.session in session_scores
            )
        )
        scores = [
            session_scores[s]
            for s in sessions
            if np.isfinite(session_scores[s])
        ]
        if scores:
            person_scores[subject] = fisher_macro(scores)

    return {
        "macro_r": fisher_macro(person_scores.values()),
        "person_scores": person_scores,
        "session_scores": session_scores,
        "n_people": len(person_scores),
        "n_sessions": sum(
            np.isfinite(v) for v in session_scores.values()
        ),
    }


def primary_interaction(results):
    cells = {
        "h1_short": results[(2, 1)]["person_scores"],
        "h1_long": results[(5, 1)]["person_scores"],
        "h5_short": results[(2, 5)]["person_scores"],
        "h5_long": results[(5, 5)]["person_scores"],
    }

    people = sorted(set.intersection(*(set(v) for v in cells.values())))
    people = [
        p
        for p in people
        if all(np.isfinite(cells[k][p]) for k in cells)
    ]

    arrays = {
        key: np.asarray([value[p] for p in people], dtype=float)
        for key, value in cells.items()
    }

    def interaction_at(indices):
        h1_short = fisher_macro(arrays["h1_short"][indices])
        h1_long = fisher_macro(arrays["h1_long"][indices])
        h5_short = fisher_macro(arrays["h5_short"][indices])
        h5_long = fisher_macro(arrays["h5_long"][indices])

        d1 = h1_long - h1_short
        d5 = h5_long - h5_short
        return d1, d5, d5 - d1

    all_idx = np.arange(len(people))
    d1, d5, point = interaction_at(all_idx)

    rng = np.random.default_rng(SEED)
    boot = np.empty(BOOTSTRAPS, dtype=float)

    for i in range(BOOTSTRAPS):
        idx = rng.integers(0, len(people), len(people))
        _, _, boot[i] = interaction_at(idx)

    return {
        "people": len(people),
        "d_h1": d1,
        "d_h5": d5,
        "interaction": point,
        "ci_low": float(np.quantile(boot, 0.025)),
        "ci_high": float(np.quantile(boot, 0.975)),
    }


def sensitivity(
    anchors: list[Anchor],
    duration: int,
    horizon: int,
    min_session_n: int,
):
    return evaluate(
        anchors,
        duration,
        horizon,
        full=True,
        min_session_n=min_session_n,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    anchors = collect_anchors(args.data_root)
    if len(anchors) < 500:
        raise RuntimeError(
            f"Only {len(anchors)} common anchors found"
        )

    subjects = sorted(set(a.subject for a in anchors))
    sessions = sorted(set(a.session for a in anchors))

    full = {}
    task = {}

    for horizon in TARGET_HORIZONS:
        for duration in SENSOR_WINDOWS:
            full[(duration, horizon)] = evaluate(
                anchors,
                duration,
                horizon,
                full=True,
            )
            task[(duration, horizon)] = evaluate(
                anchors,
                duration,
                horizon,
                full=False,
            )

    primary = primary_interaction(full)
    supported = bool(
        np.isfinite(primary["interaction"])
        and primary["interaction"] > 0
        and primary["ci_low"] > 0
    )

    # Secondary H3 relative long-history advantage.
    d_h3 = (
        full[(5, 3)]["macro_r"]
        - full[(2, 3)]["macro_r"]
    )

    sensitivity_rows = []
    for threshold in (15, 20):
        short_h1 = sensitivity(anchors, 2, 1, threshold)
        long_h1 = sensitivity(anchors, 5, 1, threshold)
        short_h5 = sensitivity(anchors, 2, 5, threshold)
        long_h5 = sensitivity(anchors, 5, 5, threshold)

        delta = (
            (long_h5["macro_r"] - short_h5["macro_r"])
            - (long_h1["macro_r"] - short_h1["macro_r"])
        )
        sensitivity_rows.append(
            (threshold, delta, short_h1, long_h1, short_h5, long_h5)
        )

    lines = []
    lines.append(
        "# COGBEACON-TARGET-ALIGNMENT-001: Independent Target-Horizon Replication"
    )
    lines.append("")
    lines.append(
        "**Status:** completed preregistered independent public-human-data analysis."
    )
    lines.append("")
    lines.append(
        f"**Primary Temporal Alignment prediction:** "
        f"**{'SUPPORTED' if supported else 'NOT SUPPORTED'}**."
    )
    lines.append("")
    lines.append("## Dataset and frozen design")
    lines.append("")
    lines.append(
        "CogBeacon facial landmarks and WCST-like response times; "
        "strict leave-one-person-out evaluation."
    )
    lines.append("")
    lines.append(f"- common anchor rounds: **{len(anchors):,}**")
    lines.append(f"- unique people: **{len(subjects)}**")
    lines.append(f"- sessions represented: **{len(sessions)}**")
    lines.append("- sensor histories: **2 s** and **5 s**")
    lines.append(
        "- targets: current log RT (H1), mean over current + next 2 correct "
        "rounds (H3), and mean over current + next 4 correct rounds (H5)"
    )
    lines.append("")
    lines.append("## Duration x target-horizon matrix")
    lines.append("")
    lines.append(
        "| Target horizon | 2 s facial history | 5 s facial history | "
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
        "Macro-r is the Fisher-z mean of person-level held-out correlations; "
        "each person's score first combines eligible session correlations in "
        "Fisher-z space."
    )
    lines.append("")
    lines.append("## Preregistered primary interaction")
    lines.append("")
    lines.append(
        f"- D(H1): **{primary['d_h1']:+.4f}**"
    )
    lines.append(
        f"- D(H5): **{primary['d_h5']:+.4f}**"
    )
    lines.append(
        f"- Delta = D(H5) - D(H1): "
        f"**{primary['interaction']:+.4f}**"
    )
    lines.append(
        f"- paired person-bootstrap 95% CI: "
        f"**[{primary['ci_low']:+.4f}, "
        f"{primary['ci_high']:+.4f}]**"
    )
    lines.append(
        f"- paired people: **{primary['people']}**"
    )
    lines.append("")
    lines.append(
        "The frozen confirmatory criterion requires a positive interaction "
        "with the entire 95% interval above zero."
    )
    lines.append("")
    lines.append(
        f"**Decision: {'supported.' if supported else 'not supported.'}**"
    )
    lines.append("")
    lines.append("## Secondary H3")
    lines.append("")
    lines.append(
        f"D(H3) = r(5 s,H3) - r(2 s,H3) = **{d_h3:+.4f}**."
    )
    lines.append("")
    lines.append("## Task-only baselines")
    lines.append("")
    lines.append("| Target horizon | task-only macro-r |")
    lines.append("| ---: | ---: |")
    for horizon in TARGET_HORIZONS:
        # Duration is irrelevant for task-only; use the 2 s cell.
        lines.append(
            f"| H{horizon} | {task[(2, horizon)]['macro_r']:.4f} |"
        )

    lines.append("")
    lines.append("## Session-count sensitivity")
    lines.append("")
    lines.append(
        "| Minimum anchors/session | unbootstrapped interaction |"
    )
    lines.append("| ---: | ---: |")
    for threshold, delta, *_ in sensitivity_rows:
        lines.append(f"| {threshold} | {delta:+.4f} |")

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if supported:
        lines.append(
            "Broadening the behavioral target across future correct WCST "
            "rounds significantly increased the relative value of the longer "
            "facial sensing history. This independently replicates the "
            "directional Temporal Alignment interaction in a different task, "
            "dataset, and camera-derived signal."
        )
    else:
        lines.append(
            "Broadening the behavioral target did not produce the "
            "preregistered positive long-versus-short history interaction. "
            "The independent replication therefore does not confirm Temporal "
            "Alignment in this task, and the null/reversed result is retained."
        )

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "The target horizon here is defined in future task rounds rather than "
        "wall-clock seconds. The result concerns predictive temporal "
        "alignment in this observational dataset. It does not establish an "
        "active-probe effect, smartphone pupil validity, fatigue diagnosis, "
        "or a neurophysiological mechanism."
    )
    lines.append("")
    lines.append("## Reproduction")
    lines.append("")
    lines.append(
        "The source participant data are not redistributed. The workflow "
        "downloads CogBeacon's public facial-landmark and performance archives "
        "and executes this committed analysis."
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(lines[:80]))


if __name__ == "__main__":
    main()
