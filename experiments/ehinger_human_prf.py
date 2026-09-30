"""APST5-EHINGER-001.

Independent human controlled-luminance replication using the public
Ehinger et al. lum_binned.csv table.

Preregistration:
experiments/registrations/APST5_EHINGER_001.md
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


CONTIGUOUS = (4, 5, 6)
E002 = (1, 2, 8)
SIM005 = (1, 2, 9)
EVEN = (2, 5, 8)
SEED = 20260930
THRESHOLD = 1.25

GRID = np.arange(0.0, 5.0001, 0.05)
BRIGHT_SUPPORT = 2.8
DARK_SUPPORT = 4.5


@dataclass
class ResponseParticipant:
    subject: str
    tracker: str
    bright: np.ndarray
    dark: np.ndarray
    sigma: float
    bright_rmse: list[float]
    dark_rmse: list[float]


def rmse(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b)
    if np.sum(ok) < 10:
        return np.nan
    return float(np.sqrt(np.mean((a[ok] - b[ok]) ** 2)))


def preprocess_curve(rows: pd.DataFrame, support: float):
    rows = rows.sort_values("td")
    t = rows["td"].to_numpy(dtype=float)
    y = rows["pa_norm"].to_numpy(dtype=float)

    finite = np.isfinite(t) & np.isfinite(y)
    t = t[finite]
    y = y[finite]

    if len(t) < 20:
        return None

    baseline = y[(t >= -0.9) & (t < 0.0)]
    if len(baseline) < 4:
        return None

    y = y - float(np.median(baseline))

    grid = GRID[GRID <= support + 1e-9]
    if t.min() > grid.min() or t.max() < grid.max():
        return None

    return grid, np.interp(grid, t, y)


def fit_participant(
    df: pd.DataFrame,
    subject: str,
    tracker: str,
):
    subset = df[
        (df["subject"] == subject)
        & (df["eyetracker"] == tracker)
    ].copy()

    fit_bright = []
    fit_dark = []
    val_bright = []
    val_dark = []

    for block in range(1, 7):
        block_rows = subset[np.isclose(subset["block"], float(block))]

        bright_rows = block_rows[np.isclose(block_rows["lum"], 255.0)]
        dark_rows = block_rows[np.isclose(block_rows["lum"], 0.0)]

        b = preprocess_curve(bright_rows, BRIGHT_SUPPORT)
        d = preprocess_curve(dark_rows, DARK_SUPPORT)

        if b is None or d is None:
            continue

        if block <= 3:
            fit_bright.append(b[1])
            fit_dark.append(d[1])
        else:
            val_bright.append(b[1])
            val_dark.append(d[1])

    if len(fit_bright) != 3 or len(fit_dark) != 3:
        return None
    if len(val_bright) != 3 or len(val_dark) != 3:
        return None

    bright = np.nanmedian(np.stack(fit_bright), axis=0)
    dark = np.nanmedian(np.stack(fit_dark), axis=0)

    brmse = [rmse(x, bright) for x in val_bright]
    drmse = [rmse(x, dark) for x in val_dark]
    errors = np.asarray(brmse + drmse, dtype=float)
    errors = errors[np.isfinite(errors)]

    if len(errors) != 6:
        return None

    sigma = float(np.median(errors))
    if not np.isfinite(sigma) or sigma <= 1e-12:
        return None

    return ResponseParticipant(
        subject=subject,
        tracker=tracker,
        bright=bright,
        dark=dark,
        sigma=sigma,
        bright_rmse=brmse,
        dark_rmse=drmse,
    )


def candidate_positions():
    return list(itertools.combinations(range(1, 10), 3))


def binary_probe(positions):
    u = np.zeros(10, dtype=float)
    u[list(positions)] = 1.0
    return u


def predict_waveform(p: ResponseParticipant, positions):
    u = binary_probe(positions)
    y = np.zeros_like(GRID)

    bright_t = GRID[GRID <= BRIGHT_SUPPORT + 1e-9]
    dark_t = GRID[GRID <= DARK_SUPPORT + 1e-9]

    prev = 0.0
    for seg, level in enumerate(u):
        if seg == 0:
            prev = level
            continue

        delta = float(level - prev)
        if abs(delta) > 0:
            t0 = seg * 0.5
            shifted = GRID - t0

            if delta > 0:
                mask = (shifted >= 0.0) & (shifted <= BRIGHT_SUPPORT)
                if np.any(mask):
                    y[mask] += np.interp(
                        shifted[mask],
                        bright_t,
                        p.bright,
                    )
            else:
                mask = (shifted >= 0.0) & (shifted <= DARK_SUPPORT)
                if np.any(mask):
                    y[mask] += np.interp(
                        shifted[mask],
                        dark_t,
                        p.dark,
                    )

        prev = level

    baseline = y[GRID < 0.4]
    y -= float(np.median(baseline))
    return y


def separation(p: ResponseParticipant, positions):
    cand = predict_waveform(p, positions)
    ctrl = predict_waveform(p, CONTIGUOUS)
    return rmse(cand, ctrl) / p.sigma


def summary(participants, positions):
    values = np.asarray(
        [separation(p, positions) for p in participants],
        dtype=float,
    )
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return {
            "n": 0,
            "p10": np.nan,
            "median": np.nan,
            "mean": np.nan,
            "pass_fraction": np.nan,
            "values": values,
        }

    return {
        "n": int(len(values)),
        "p10": float(np.quantile(values, 0.10)),
        "median": float(np.median(values)),
        "mean": float(np.mean(values)),
        "pass_fraction": float(np.mean(values > THRESHOLD)),
        "values": values,
    }


def split_subjects(subjects):
    ordered = sorted(subjects)
    rng = np.random.default_rng(SEED)
    idx = np.arange(len(ordered))
    rng.shuffle(idx)
    n = len(ordered) // 2
    return (
        [ordered[i] for i in idx[:n]],
        [ordered[i] for i in idx[n:]],
    )


def design_search(participants):
    rows = []
    for pos in candidate_positions():
        s = summary(participants, pos)
        rows.append((s["p10"], s["median"], s["mean"], pos))
    rows.sort(reverse=True, key=lambda x: (x[0], x[1], x[2]))
    return rows


def pearson(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b)
    a = a[ok]
    b = b[ok]
    if len(a) < 4 or np.std(a) <= 1e-12 or np.std(b) <= 1e-12:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    df["subject"] = df["subject"].astype(str)
    df["eyetracker"] = df["eyetracker"].astype(str)

    subjects = sorted(df["subject"].unique())

    by_tracker = {}
    exclusions = {}

    for tracker in ("el", "pl"):
        plist = []
        failed = []
        for subject in subjects:
            p = fit_participant(df, subject, tracker)
            if p is None:
                failed.append(subject)
            else:
                plist.append(p)
        by_tracker[tracker] = plist
        exclusions[tracker] = failed

    el = by_tracker["el"]
    if len(el) < 10:
        raise RuntimeError(
            f"Too few EyeLink participants: {len(el)}; excluded={exclusions['el']}"
        )

    el_map = {p.subject: p for p in el}
    design_ids, heldout_ids = split_subjects(sorted(el_map))
    design = [el_map[s] for s in design_ids]
    heldout = [el_map[s] for s in heldout_ids]

    ranking = design_search(design)
    selected = ranking[0][3]
    ranks = {row[3]: i + 1 for i, row in enumerate(ranking)}

    named = {
        "independent_selected": selected,
        "frozen_e002": E002,
        "sim005": SIM005,
        "evenly_spaced": EVEN,
    }

    design_reports = {
        name: summary(design, pos)
        for name, pos in named.items()
    }
    heldout_reports = {
        name: summary(heldout, pos)
        for name, pos in named.items()
    }

    h1 = (
        heldout_reports["independent_selected"]["p10"] > THRESHOLD
        and heldout_reports["independent_selected"]["pass_fraction"] >= 0.90
    )
    h2 = (
        heldout_reports["frozen_e002"]["p10"] > THRESHOLD
        and heldout_reports["frozen_e002"]["pass_fraction"] >= 0.90
    )

    # Secondary transfer: do not reoptimize on Pupil Labs.
    pl_map = {p.subject: p for p in by_tracker["pl"]}
    transfer_ids = [s for s in heldout_ids if s in pl_map]
    pl_heldout = [pl_map[s] for s in transfer_ids]

    transfer_reports = {
        name: summary(pl_heldout, pos)
        for name, pos in {
            "independent_selected": selected,
            "frozen_e002": E002,
        }.items()
    }

    cross_device = {}
    for name, pos in {
        "independent_selected": selected,
        "frozen_e002": E002,
    }.items():
        common = [s for s in heldout_ids if s in pl_map]
        el_s = [separation(el_map[s], pos) for s in common]
        pl_s = [separation(pl_map[s], pos) for s in common]
        cross_device[name] = pearson(el_s, pl_s)

    lines = []
    lines.append(
        "# APST5-EHINGER-001: Independent Human Luminance-Response Replication"
    )
    lines.append("")
    lines.append(
        "**Status:** completed preregistered independent controlled-luminance analysis."
    )
    lines.append("")
    lines.append(
        f"**H1 independently optimized timing:** "
        f"**{'SUPPORTED' if h1 else 'NOT SUPPORTED'}**."
    )
    lines.append("")
    lines.append(
        f"**H2 frozen E002 timing:** **{'SUPPORTED' if h2 else 'NOT SUPPORTED'}**."
    )
    lines.append("")
    lines.append("## Dataset")
    lines.append("")
    lines.append(
        "Ehinger et al. (2019) public luminance benchmark, "
        "using preprocessed event-locked normalized pupil responses."
    )
    lines.append("")
    lines.append(f"- EyeLink usable participants: **{len(el)}**")
    lines.append(f"- EyeLink design participants: **{len(design)}**")
    lines.append(f"- EyeLink held-out participants: **{len(heldout)}**")
    lines.append(
        f"- Pupil Labs usable participants: **{len(by_tracker['pl'])}**"
    )
    lines.append(
        "- fit blocks: 1–3; held-out response-noise blocks: 4–6"
    )
    lines.append("")
    lines.append("## EyeLink equal-exposure result")
    lines.append("")
    lines.append(
        f"Design-set P10 search selected **{selected}**."
    )
    lines.append("")
    lines.append(
        "| Probe | positions | design P10 S | held-out P10 S | "
        "held-out median S | held-out S>1.25 | design rank |"
    )
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")

    for name, pos in named.items():
        dr = design_reports[name]
        hr = heldout_reports[name]
        lines.append(
            f"| {name} | {pos} | {dr['p10']:.3f} | "
            f"**{hr['p10']:.3f}** | {hr['median']:.3f} | "
            f"{100*hr['pass_fraction']:.1f}% | {ranks.get(pos, 'NA')} |"
        )

    lines.append("")
    lines.append("## Held-out repeat-response noise")
    lines.append("")
    lines.append(
        "| subject | sigma | median bright RMSE | median dark RMSE | split |"
    )
    lines.append("| --- | ---: | ---: | ---: | --- |")
    for p in sorted(el, key=lambda x: x.subject):
        lines.append(
            f"| {p.subject} | {p.sigma:.4f} | "
            f"{np.median(p.bright_rmse):.4f} | "
            f"{np.median(p.dark_rmse):.4f} | "
            f"{'design' if p.subject in design_ids else 'held-out'} |"
        )

    lines.append("")
    lines.append("## Secondary mobile-eye-tracker transfer")
    lines.append("")
    lines.append(
        "The EyeLink-selected timing is transferred to the simultaneously "
        "recorded Pupil Labs responses without reoptimization."
    )
    lines.append("")
    lines.append(
        "| Probe | Pupil Labs P10 S | Pupil Labs median S | "
        "Pupil Labs S>1.25 | EL↔PL participant S correlation |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for name in ("independent_selected", "frozen_e002"):
        tr = transfer_reports[name]
        lines.append(
            f"| {name} | {tr['p10']:.3f} | {tr['median']:.3f} | "
            f"{100*tr['pass_fraction']:.1f}% | {cross_device[name]:.3f} |"
        )

    lines.append("")
    lines.append("## Exclusions")
    lines.append("")
    lines.append(
        f"- EyeLink missing incomplete response sets: "
        f"{exclusions['el'] if exclusions['el'] else 'none'}"
    )
    lines.append(
        f"- Pupil Labs missing incomplete response sets: "
        f"{exclusions['pl'] if exclusions['pl'] else 'none'}"
    )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if h2:
        lines.append(
            "Frozen E002 timing satisfies the preregistered held-out EyeLink "
            "separation criterion in this independent luminance-response "
            "dataset under the fixed asymmetric-kernel construction."
        )
    else:
        lines.append(
            "Frozen E002 timing does not satisfy the preregistered held-out "
            "EyeLink separation criterion in this independent dataset."
        )

    lines.append("")
    lines.append(
        "The brightening kernel uses the clean pre-return 0–2.8 s portion of "
        "the 0→255 condition. The darkening kernel uses the released block-level "
        "average of returns to black. This construction is deliberately fixed "
        "but is not a full physical model of the E002 display."
    )

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "A positive result supports human ocular waveform distinguishability "
        "under a second controlled eye-tracking protocol. Pupil Labs is a "
        "mobile infrared eye tracker, not an ordinary RGB front camera. "
        "Nothing here establishes phone RGB observability or fatigue-state "
        "validity."
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(lines[:180]))


if __name__ == "__main__":
    main()
