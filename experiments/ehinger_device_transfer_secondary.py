"""Secondary person-specific specificity audit for EHINGER-DEVICE-TRANSFER-001."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

import ehinger_device_transfer as base


SEED = 20260930
PERMUTATIONS = 10_000


def leave_one_out_residuals(paired):
    test = paired[paired["block"].isin(base.TEST_BLOCKS)].copy()
    subjects = sorted(test["subject"].astype(str).unique())
    rows = []

    keys = ["block", "lum", "td_key"]

    for subject in subjects:
        own = test[test["subject"].astype(str) == subject].copy()
        others = test[test["subject"].astype(str) != subject].copy()

        ref = (
            others.groupby(keys)[["el", "pl"]]
            .mean()
            .rename(columns={"el": "el_ref", "pl": "pl_ref"})
            .reset_index()
        )
        own = own.merge(ref, on=keys, how="inner")
        own["el_resid"] = own["el"] - own["el_ref"]
        own["pl_resid"] = own["pl"] - own["pl_ref"]
        own["subject_str"] = subject
        rows.append(own)

    return pd.concat(rows, ignore_index=True)


def participant_vectors(resid):
    vectors = {}
    for subject, group in resid.groupby("subject_str"):
        ordered = group.sort_values(["block", "lum", "td_key"])
        key = list(
            zip(
                ordered["block"].astype(int),
                ordered["lum"].astype(float),
                ordered["td_key"].astype(float),
            )
        )
        vectors[str(subject)] = {
            "key": key,
            "el": ordered["el_resid"].to_numpy(dtype=float),
            "pl": ordered["pl_resid"].to_numpy(dtype=float),
        }
    return vectors


def derangement(rng, n):
    base_idx = np.arange(n)
    for _ in range(1000):
        perm = rng.permutation(n)
        if np.all(perm != base_idx):
            return perm
    # Deterministic cyclic fallback is always a derangement for n>1.
    return np.roll(base_idx, 1)


def paired_r(vectors, el_subject, pl_subject):
    a = vectors[el_subject]
    b = vectors[pl_subject]

    # Exact held-out rows should match, but intersect mechanically to avoid
    # relying on ordering.
    map_b = {
        key: value for key, value in zip(b["key"], b["pl"])
    }
    x = []
    y = []
    for key, value in zip(a["key"], a["el"]):
        if key in map_b:
            x.append(value)
            y.append(map_b[key])

    return base.pearson(x, y)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    paired = base.paired_table(df)
    resid = leave_one_out_residuals(paired)
    vectors = participant_vectors(resid)
    subjects = sorted(vectors)

    observed_scores = {
        subject: paired_r(vectors, subject, subject)
        for subject in subjects
    }
    observed = base.fisher_macro(observed_scores.values())

    rng = np.random.default_rng(SEED)
    null = np.empty(PERMUTATIONS, dtype=float)

    for i in range(PERMUTATIONS):
        perm = derangement(rng, len(subjects))
        scores = [
            paired_r(vectors, subjects[j], subjects[perm[j]])
            for j in range(len(subjects))
        ]
        null[i] = base.fisher_macro(scores)

    p = float((1 + np.sum(null >= observed)) / (PERMUTATIONS + 1))
    supported = bool(np.isfinite(observed) and observed > 0 and p < 0.05)

    lines = []
    lines.append(
        "# EHINGER-DEVICE-TRANSFER-001 Secondary: Person-Specific Residual Transfer"
    )
    lines.append("")
    lines.append(
        "**Status:** completed post-primary specificity diagnostic."
    )
    lines.append("")
    lines.append(
        "**This result is secondary and does not alter the preregistered primary result.**"
    )
    lines.append("")
    lines.append("## Same-person leave-one-out residual correlations")
    lines.append("")
    lines.append("| participant | residual r |")
    lines.append("| --- | ---: |")
    for subject in subjects:
        lines.append(
            f"| {subject} | {observed_scores[subject]:+.4f} |"
        )

    lines.append("")
    lines.append("## Aggregate and mismatched-person negative control")
    lines.append("")
    lines.append(
        f"- observed same-person residual macro-r: **{observed:+.4f}**"
    )
    lines.append(
        f"- mismatched-person permutation median: "
        f"**{np.median(null):+.4f}**"
    )
    lines.append(
        f"- mismatched-person 95% interval: "
        f"**[{np.quantile(null,0.025):+.4f}, {np.quantile(null,0.975):+.4f}]**"
    )
    lines.append(
        f"- one-sided empirical p: **{p:.6f}** "
        f"({PERMUTATIONS:,} derangements)"
    )
    lines.append("")
    lines.append(
        f"**Person-specific residual transfer diagnostic: "
        f"{'SUPPORTED' if supported else 'NOT SUPPORTED'}.**"
    )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    if supported:
        lines.append(
            "After subtracting leave-one-person-out stimulus-locked group "
            "waveforms, concurrent EyeLink and Pupil Labs measurements still "
            "share person-specific held-out pupil dynamics beyond mismatched-"
            "participant pairings."
        )
    else:
        lines.append(
            "The very high primary cross-device correlations appear largely "
            "compatible with generic stimulus-locked structure; person-specific "
            "residual dynamics do not pass this secondary specificity test."
        )

    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(
        "This is a post-primary specificity diagnostic on dedicated laboratory "
        "eye trackers. It does not establish RGB smartphone pupil tracking or "
        "state/fatigue inference."
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
