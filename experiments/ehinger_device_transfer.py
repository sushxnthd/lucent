"""EHINGER-DEVICE-TRANSFER-001.

Preregistered cross-device controlled-luminance pupil waveform transfer test.

Plan:
experiments/registrations/EHINGER_DEVICE_TRANSFER_001.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 20260930
BOOTSTRAPS = 10_000
TRAIN_BLOCKS = (1, 2, 3)
TEST_BLOCKS = (4, 5, 6)
LUMINANCES = (0.0, 64.0, 128.0, 192.0, 255.0)
T_MIN = 0.0
T_MAX = 2.8


def pearson(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b)
    a = a[ok]
    b = b[ok]
    if len(a) < 3 or np.std(a) <= 1e-12 or np.std(b) <= 1e-12:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def fisher_macro(values):
    values = np.asarray(
        [x for x in values if np.isfinite(x)],
        dtype=float,
    )
    if len(values) == 0:
        return np.nan
    values = np.clip(values, -0.999999, 0.999999)
    return float(np.tanh(np.mean(np.arctanh(values))))


def nrmse(y, pred):
    y = np.asarray(y, dtype=float)
    pred = np.asarray(pred, dtype=float)
    ok = np.isfinite(y) & np.isfinite(pred)
    y = y[ok]
    pred = pred[ok]
    if len(y) < 3:
        return np.nan
    denom = float(np.quantile(y, 0.95) - np.quantile(y, 0.05))
    if denom <= 1e-12:
        return np.nan
    return float(np.sqrt(np.mean((pred - y) ** 2)) / denom)


def paired_table(df):
    """Return exact paired EL/PL rows on released binned time support."""
    window = df[
        (df["td"] >= T_MIN)
        & (df["td"] <= T_MAX)
        & (df["eyetracker"].isin(["el", "pl"]))
        & (df["lum"].isin(LUMINANCES))
    ].copy()

    # The released file contains a stable binned td grid. Round only to remove
    # harmless CSV floating representation differences.
    window["td_key"] = window["td"].round(6)

    wide = window.pivot_table(
        index=["subject", "block", "lum", "td_key"],
        columns="eyetracker",
        values="pa_norm",
        aggfunc="mean",
    ).reset_index()

    if "el" not in wide or "pl" not in wide:
        raise RuntimeError("Released table does not contain both devices.")

    wide = wide[np.isfinite(wide["el"]) & np.isfinite(wide["pl"])].copy()

    # Frozen complete-cell requirement: >=15 finite paired samples.
    counts = (
        wide.groupby(["subject", "block", "lum"])
        .size()
        .rename("n")
        .reset_index()
    )
    good = counts[counts["n"] >= 15][["subject", "block", "lum"]]
    wide = wide.merge(
        good,
        on=["subject", "block", "lum"],
        how="inner",
    )

    return wide


def fit_affine(train):
    x = train["pl"].to_numpy(dtype=float)
    y = train["el"].to_numpy(dtype=float)
    X = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(coef[0]), float(coef[1])


def participant_result(paired, subject):
    sub = paired[paired["subject"] == subject].copy()
    train = sub[sub["block"].isin(TRAIN_BLOCKS)].copy()
    test = sub[sub["block"].isin(TEST_BLOCKS)].copy()

    if len(train) < 100 or len(test) < 100:
        return None

    a, b = fit_affine(train)

    test["pred_calibrated"] = a + b * test["pl"]
    test["pred_uncalibrated"] = test["pl"]

    y = test["el"].to_numpy(dtype=float)
    calibrated = test["pred_calibrated"].to_numpy(dtype=float)
    uncalibrated = test["pl"].to_numpy(dtype=float)

    by_lum = {}
    for lum in LUMINANCES:
        part = test[test["lum"] == lum]
        by_lum[lum] = {
            "r_calibrated": pearson(part["el"], part["pred_calibrated"]),
            "r_uncalibrated": pearson(part["el"], part["pl"]),
            "n": int(len(part)),
        }

    # Secondary response amplitude in the late response interval.
    amp = (
        test[(test["td_key"] >= 1.5) & (test["td_key"] <= 2.5)]
        .groupby(["block", "lum"])[["el", "pred_calibrated"]]
        .median()
        .reset_index()
    )
    amplitude_r = pearson(amp["el"], amp["pred_calibrated"])

    # Secondary nonzero-luminance-only result.
    nonzero = test[test["lum"] != 0.0]

    return {
        "subject": str(subject),
        "a": a,
        "b": b,
        "train_n": int(len(train)),
        "test_n": int(len(test)),
        "r_calibrated": pearson(y, calibrated),
        "r_uncalibrated": pearson(y, uncalibrated),
        "nrmse": nrmse(y, calibrated),
        "amplitude_r": amplitude_r,
        "nonzero_r": pearson(
            nonzero["el"],
            nonzero["pred_calibrated"],
        ),
        "by_lum": by_lum,
    }


def bootstrap_macro(results):
    values = np.asarray(
        [r["r_calibrated"] for r in results],
        dtype=float,
    )
    values = values[np.isfinite(values)]

    point = fisher_macro(values)
    rng = np.random.default_rng(SEED)
    boot = np.empty(BOOTSTRAPS, dtype=float)
    for i in range(BOOTSTRAPS):
        idx = rng.integers(0, len(values), len(values))
        boot[i] = fisher_macro(values[idx])

    return (
        point,
        float(np.quantile(boot, 0.025)),
        float(np.quantile(boot, 0.975)),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    required = {
        "block", "eyetracker", "lum", "pa_norm", "subject", "td"
    }
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing required columns: {sorted(missing)}")

    paired = paired_table(df)
    subjects = sorted(paired["subject"].astype(str).unique())

    results = []
    for subject in subjects:
        result = participant_result(paired, subject)
        if result is not None:
            results.append(result)

    if len(results) < 10:
        raise RuntimeError(
            f"Only {len(results)} participants pass frozen paired-cell rules."
        )

    macro_r, ci_low, ci_high = bootstrap_macro(results)
    pass_fraction = float(
        np.mean(
            [
                np.isfinite(r["r_calibrated"])
                and r["r_calibrated"] > 0.70
                for r in results
            ]
        )
    )
    supported = bool(ci_low > 0.70 and pass_fraction >= 0.80)

    lines = []
    lines.append(
        "# EHINGER-DEVICE-TRANSFER-001: Concurrent Lower-Cost Eye-Tracker Transfer"
    )
    lines.append("")
    lines.append(
        "**Status:** completed preregistered public-human cross-device analysis."
    )
    lines.append("")
    lines.append(
        f"**Primary waveform-preservation criterion:** "
        f"**{'SUPPORTED' if supported else 'NOT SUPPORTED'}**."
    )
    lines.append("")
    lines.append("## Frozen design")
    lines.append("")
    lines.append(
        "Concurrent EyeLink 1000 and Pupil Labs measurements from the "
        "public Ehinger et al. controlled-luminance task."
    )
    lines.append("")
    lines.append(f"- usable participants: **{len(results)}**")
    lines.append("- calibration blocks: **1–3**")
    lines.append("- held-out blocks: **4–6**")
    lines.append("- fixed post-onset window: **0–2.8 s**")
    lines.append(
        "- per-participant calibration: EyeLink = a + b × Pupil Labs, "
        "fit only on blocks 1–3"
    )
    lines.append("")
    lines.append("## Participant-level held-out results")
    lines.append("")
    lines.append(
        "| participant | calibrated r | uncalibrated r | NRMSE | "
        "late-amplitude r | nonzero-luminance r |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")

    for r in sorted(results, key=lambda x: x["subject"]):
        lines.append(
            f"| {r['subject']} | **{r['r_calibrated']:.4f}** | "
            f"{r['r_uncalibrated']:.4f} | {r['nrmse']:.4f} | "
            f"{r['amplitude_r']:.4f} | {r['nonzero_r']:.4f} |"
        )

    lines.append("")
    lines.append("## Preregistered aggregate")
    lines.append("")
    lines.append(f"- Fisher-z macro-r: **{macro_r:.4f}**")
    lines.append(
        f"- participant bootstrap 95% CI: **[{ci_low:.4f}, {ci_high:.4f}]**"
    )
    lines.append(
        f"- participants with held-out r > 0.70: "
        f"**{100*pass_fraction:.1f}% ({int(round(pass_fraction*len(results)))}/{len(results)})**"
    )
    lines.append(
        f"- median held-out NRMSE: "
        f"**{np.nanmedian([r['nrmse'] for r in results]):.4f}**"
    )
    lines.append("")
    lines.append(
        "Frozen support requires CI lower bound >0.70 and >=80% of "
        "participants with individual held-out r>0.70."
    )
    lines.append("")
    lines.append(
        f"**Decision: {'supported.' if supported else 'not supported.'}**"
    )

    lines.append("")
    lines.append("## Per-luminance secondary agreement")
    lines.append("")
    lines.append("| luminance code | macro calibrated r |")
    lines.append("| ---: | ---: |")
    for lum in LUMINANCES:
        vals = [
            r["by_lum"][lum]["r_calibrated"]
            for r in results
            if np.isfinite(r["by_lum"][lum]["r_calibrated"])
        ]
        lines.append(f"| {lum:g} | {fisher_macro(vals):.4f} |")

    lines.append("")
    lines.append("## Secondary summaries")
    lines.append("")
    lines.append(
        f"- median participant late-response amplitude correlation: "
        f"**{np.nanmedian([r['amplitude_r'] for r in results]):.4f}**"
    )
    lines.append(
        f"- macro-r restricted to nonzero luminance codes: "
        f"**{fisher_macro([r['nonzero_r'] for r in results]):.4f}**"
    )
    lines.append(
        f"- macro uncalibrated waveform r: "
        f"**{fisher_macro([r['r_uncalibrated'] for r in results]):.4f}**"
    )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if supported:
        lines.append(
            "After a simple participant-specific affine calibration learned "
            "only on the first three blocks, the lower-cost Pupil Labs system "
            "preserved the concurrent EyeLink luminance-evoked waveform "
            "structure in held-out blocks under the frozen criterion."
        )
    else:
        lines.append(
            "The lower-cost Pupil Labs system did not satisfy the frozen "
            "held-out waveform-preservation criterion relative to EyeLink."
        )

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "Pupil Labs is a dedicated video eye tracker, not an ordinary RGB "
        "smartphone front camera. This result therefore cannot clear Lucent "
        "E002 or establish phone-based pupil observability."
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
