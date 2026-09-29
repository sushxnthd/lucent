from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


SEED = 20260929
WINDOWS = (1, 2, 3, 4, 5)
FPS = 2
RIDGE_ALPHA = 10.0


@dataclass
class Sample:
    subject: str
    session: str
    round_id: int
    target: float
    task: np.ndarray
    frames: list[np.ndarray]


def subject_from_session(session: str) -> str:
    parts = session.split("_")
    token = parts[1]
    return token[:-1] if token.endswith("b") else token


def parse_frame_name(path: Path):
    m = re.match(r"^(-?\d+)_(\d+)_(\d+)\.npz$", path.name)
    if not m:
        return None
    return tuple(map(int, m.groups()))


def load_landmarks(path: Path) -> np.ndarray:
    with np.load(path, allow_pickle=False) as z:
        a = np.asarray(z[z.files[0]], dtype=float).reshape(-1)
    if a.size < 136:
        raise ValueError(f"{path} has only {a.size} values")
    return a[:136].reshape(68, 2)


def normalize_landmarks(pts: np.ndarray) -> np.ndarray:
    left = pts[36:42].mean(axis=0)
    right = pts[42:48].mean(axis=0)
    center = (left + right) / 2.0
    scale = float(np.linalg.norm(right - left))
    if not np.isfinite(scale) or scale < 1e-6:
        scale = float(np.linalg.norm(pts.max(axis=0) - pts.min(axis=0)))
    scale = max(scale, 1e-6)
    return (pts - center) / scale


def dist(a, b):
    return float(np.linalg.norm(a - b))


def eye_aspect_ratio(pts: np.ndarray, idx: list[int]) -> float:
    p = pts[idx]
    return (dist(p[1], p[5]) + dist(p[2], p[4])) / (2.0 * dist(p[0], p[3]) + 1e-9)


def mouth_aspect_ratio(pts: np.ndarray) -> float:
    vert = dist(pts[62], pts[66]) + dist(pts[63], pts[65])
    horiz = 2.0 * dist(pts[60], pts[64]) + 1e-9
    return vert / horiz


def summarize_window(frames: list[np.ndarray], n_frames: int) -> np.ndarray:
    chosen = frames[-n_frames:]
    norm = np.stack([normalize_landmarks(x) for x in chosen], axis=0)

    mean = norm.mean(axis=0).reshape(-1)
    std = norm.std(axis=0).reshape(-1)
    delta = (norm[-1] - norm[0]).reshape(-1)

    ears = []
    mars = []
    for p in norm:
        le = eye_aspect_ratio(p, [36, 37, 38, 39, 40, 41])
        re = eye_aspect_ratio(p, [42, 43, 44, 45, 46, 47])
        ears.append((le + re) / 2.0)
        mars.append(mouth_aspect_ratio(p))

    ears = np.asarray(ears)
    mars = np.asarray(mars)

    if len(norm) > 1:
        diff = np.diff(norm, axis=0)
        rms = np.sqrt(np.mean(diff**2, axis=(1, 2)))
    else:
        rms = np.array([0.0])

    t = np.arange(len(norm), dtype=float)

    def slope(x):
        if len(x) < 2 or np.allclose(x, x[0]):
            return 0.0
        return float(np.polyfit(t, x, 1)[0])

    scalars = np.array([
        ears.mean(), ears.std(), ears.min(), ears[-1], ears[-1] - ears[0], slope(ears),
        mars.mean(), mars.std(), mars.max(), mars[-1], mars[-1] - mars[0], slope(mars),
        rms.mean(), rms.std(), rms.max(),
    ], dtype=float)

    out = np.concatenate([mean, std, delta, scalars])
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)


def performance_file(root: Path, session: str) -> Path | None:
    candidates = sorted((root / "user_performance").glob(session + "_*.csv"))
    return candidates[0] if candidates else None


def collect_samples(root: Path) -> list[Sample]:
    face_root = root / "face_keypoints"
    samples: list[Sample] = []

    for session_dir in sorted(p for p in face_root.iterdir() if p.is_dir()):
        session = session_dir.name
        perf_path = performance_file(root, session)
        if perf_path is None:
            continue

        perf = pd.read_csv(perf_path, sep="\t")
        perf.columns = [str(c).strip() for c in perf.columns]

        by_round: dict[int, list[tuple[int, np.ndarray, int]]] = {}
        for path in session_dir.glob("*.npz"):
            parsed = parse_frame_name(path)
            if parsed is None:
                continue
            under_rule, round_id, frame_id = parsed
            try:
                pts = load_landmarks(path)
            except Exception:
                continue
            by_round.setdefault(round_id, []).append((frame_id, pts, under_rule))

        max_round = max(by_round) if by_round else 1

        for _, row in perf.iterrows():
            try:
                round_id = int(row["Round"])
                correct_raw = row["Response"]
                correct = bool(correct_raw) if isinstance(correct_raw, (bool, np.bool_)) else str(correct_raw).strip().lower() == "true"
                rt = float(row["Time"])
            except Exception:
                continue

            if not correct or not np.isfinite(rt) or rt <= 0:
                continue

            items = sorted(by_round.get(round_id, []), key=lambda z: z[0])
            if len(items) < FPS * max(WINDOWS):
                continue

            frames = [x[1] for x in items]
            under_rule = float(items[-1][2])
            level = float(row.get("Level", 0))
            question = float(row.get("Question", 0))
            progress = float(round_id) / max(float(max_round), 1.0)
            task = np.array([level, question, progress, under_rule], dtype=float)

            samples.append(
                Sample(
                    subject=subject_from_session(session),
                    session=session,
                    round_id=round_id,
                    target=float(np.log(rt)),
                    task=task,
                    frames=frames,
                )
            )

    return samples


def pearson(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 3 or np.std(x) < 1e-12 or np.std(y) < 1e-12:
        return np.nan
    return float(np.corrcoef(x, y)[0, 1])


def fisher_macro(rs):
    rs = np.asarray([r for r in rs if np.isfinite(r)], dtype=float)
    if len(rs) == 0:
        return np.nan
    rs = np.clip(rs, -0.999999, 0.999999)
    return float(np.tanh(np.mean(np.arctanh(rs))))


def build_matrix(samples: list[Sample], window: int, full: bool):
    rows = []
    y = []
    for s in samples:
        feat = summarize_window(s.frames, window * FPS)
        x = np.concatenate([s.task, feat]) if full else s.task.copy()
        rows.append(x)
        y.append(s.target)
    return np.asarray(rows, dtype=float), np.asarray(y, dtype=float)


def evaluate(samples: list[Sample], window: int, full: bool):
    subjects = sorted(set(s.subject for s in samples))
    X, y = build_matrix(samples, window, full)
    session_scores: dict[str, float] = {}
    predictions = np.full(len(samples), np.nan)

    for subject in subjects:
        train = np.array([s.subject != subject for s in samples])
        test = ~train
        model = make_pipeline(StandardScaler(), Ridge(alpha=RIDGE_ALPHA))
        model.fit(X[train], y[train])
        predictions[test] = model.predict(X[test])

    for session in sorted(set(s.session for s in samples)):
        idx = np.array([s.session == session for s in samples])
        if idx.sum() < 12:
            continue
        session_scores[session] = pearson(y[idx], predictions[idx])

    return {
        "macro_r": fisher_macro(session_scores.values()),
        "session_scores": session_scores,
    }


def paired_bootstrap(a: dict[str, float], b: dict[str, float], n=10000):
    sessions = sorted(set(a).intersection(b))
    pairs = [(a[s], b[s]) for s in sessions if np.isfinite(a[s]) and np.isfinite(b[s])]
    if not pairs:
        return np.nan, np.nan, np.nan, 0

    arr = np.asarray(pairs, dtype=float)
    rng = np.random.default_rng(SEED)
    diffs = np.empty(n, dtype=float)

    for i in range(n):
        take = rng.integers(0, len(arr), len(arr))
        diffs[i] = fisher_macro(arr[take, 0]) - fisher_macro(arr[take, 1])

    point = fisher_macro(arr[:, 0]) - fisher_macro(arr[:, 1])
    return point, float(np.quantile(diffs, 0.025)), float(np.quantile(diffs, 0.975)), len(arr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    samples = collect_samples(args.data_root)
    if len(samples) < 100:
        raise RuntimeError(f"Only {len(samples)} eligible samples found")

    subjects = sorted(set(s.subject for s in samples))
    sessions = sorted(set(s.session for s in samples))

    full = {}
    task = {}
    for w in WINDOWS:
        full[w] = evaluate(samples, w, True)
        task[w] = evaluate(samples, w, False)

    point, lo, hi, paired_n = paired_bootstrap(full[2]["session_scores"], full[5]["session_scores"])
    p3, lo3, hi3, paired_n3 = paired_bootstrap(full[3]["session_scores"], full[5]["session_scores"])

    supported = bool(np.isfinite(point) and point > 0 and lo > 0)

    lines = []
    lines.append("# COGBEACON-REALDATA-001: Independent Temporal-Locality Test")
    lines.append("")
    lines.append("**Status:** completed independent public-human-data analysis.")
    lines.append("")
    lines.append(f"**Preregistered 2 s > 5 s hypothesis:** **{'SUPPORTED' if supported else 'NOT SUPPORTED'}**.")
    lines.append("")
    lines.append("## Dataset")
    lines.append("")
    lines.append("CogBeacon (Papakostas, Rajavenkatanarayanan & Makedon, 2019), using published 68-point facial landmarks and per-round WCST response times.")
    lines.append("")
    lines.append(f"- eligible correct rounds with >=10 facial frames: **{len(samples):,}**")
    lines.append(f"- unique people: **{len(subjects)}**")
    lines.append(f"- sessions represented: **{len(sessions)}**")
    lines.append("- facial sampling rate: **2 FPS**")
    lines.append("- generalization: **strict leave-one-person-out**")
    lines.append("")
    lines.append("## Frozen duration comparison")
    lines.append("")
    lines.append("| Final facial window | Full model macro-r | Task-only macro-r | Increment over task-only |")
    lines.append("| ---: | ---: | ---: | ---: |")
    for w in WINDOWS:
        inc = full[w]["macro_r"] - task[w]["macro_r"]
        lines.append(f"| {w} s | **{full[w]['macro_r']:.4f}** | {task[w]['macro_r']:.4f} | {inc:+.4f} |")

    lines.append("")
    lines.append("Macro-r is the Fisher-z average of within-session Pearson correlations on held-out people.")
    lines.append("")
    lines.append("## Preregistered primary contrast")
    lines.append("")
    lines.append(f"2 s - 5 s macro-r difference: **{point:+.4f}**")
    lines.append("")
    lines.append(f"Paired session bootstrap (10,000 resamples; {paired_n} paired sessions):")
    lines.append("")
    lines.append(f"**95% CI [{lo:+.4f}, {hi:+.4f}]**")
    lines.append("")
    lines.append("The confirmatory criterion required both a positive point difference and a confidence interval entirely above zero.")
    lines.append("")
    lines.append(f"**Decision: {'supported.' if supported else 'not supported.'}**")
    lines.append("")
    lines.append("## Secondary 3 s contrast")
    lines.append("")
    lines.append(f"3 s - 5 s macro-r difference: **{p3:+.4f}**, 95% CI **[{lo3:+.4f}, {hi3:+.4f}]** across {paired_n3} paired sessions.")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if supported:
        lines.append("The independent dataset supports the target-specific temporal-locality hypothesis: under the frozen feature and model family, the most recent 2 seconds of facial behavior preserved more information about the current response-time target than the final 5 seconds.")
    else:
        lines.append("The independent dataset does not confirm the preregistered 2-second temporal-locality hypothesis. This result is retained rather than replaced with a post-hoc duration claim.")
    lines.append("")
    lines.append("CogBeacon differs materially from the earlier MTS analysis: it uses a WCST-like cognitive task, 68-point facial landmarks at 2 FPS, and per-round response time rather than PVT-linked eyelid distance. Agreement would therefore be cross-task evidence; disagreement bounds the hypothesis.")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append("This analysis does **not** validate APST-5 active probing or a smartphone fatigue diagnostic. It tests only whether very recent passive facial dynamics can dominate a longer within-round history for an immediate performance target.")
    lines.append("")
    lines.append("## Reproduction")
    lines.append("")
    lines.append("The source dataset is not redistributed. The workflow downloads the public CogBeacon facial-keypoint and performance archives, runs the frozen script, and writes this report.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:60]))


if __name__ == "__main__":
    main()
