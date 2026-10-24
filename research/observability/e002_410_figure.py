#!/usr/bin/env python3
"""Vector figure for E002-410 synthetic results; reads frozen CI JSON only."""
import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def wilson_interval(successes, trials, z=1.96):
    p = successes / trials
    den = 1 + z*z/trials
    center = (p + z*z/(2*trials)) / den
    half = z*math.sqrt(p*(1-p)/trials + z*z/(4*trials*trials)) / den
    return center-half, center+half


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    data = json.loads(args.results.read_text(encoding="utf-8"))
    if data["experiment"] != "E002-410" or not data["joint_pass"]:
        raise ValueError("Expected verified E002-410 result")
    labels = ["IID frames", "Clustered frames", "Session maxima", "Shifted participant"]
    keys = ["iid_single", "clustered_single", "session_max", "shifted_single"]
    n = data["trials"]
    rates = [data["rates"][k] for k in keys]
    intervals = [wilson_interval(data["counts"][k], n) for k in keys]
    yerr = [[r-lo for r, (lo, hi) in zip(rates, intervals)],
            [hi-r for r, (lo, hi) in zip(rates, intervals)]]
    fig, ax = plt.subplots(figsize=(8.5, 4.9), layout="constrained")
    ax.errorbar(range(4), rates, yerr=yerr, fmt="o", capsize=4,
                markersize=9, linewidth=1.5, label="40,000 synthetic trials (95% Wilson)")
    ax.axhline(data["theoretical_participant_rank_risk"], linestyle="--",
               linewidth=1.2, label="Participant-rank law: 1/21")
    ax.axhline(data["naive_frame_rank_risk"], linestyle=":",
               linewidth=1.2, label="Naive frame-rank law: 1/2001")
    ax.set_yscale("log")
    ax.set_ylim(0.00015, 0.7)
    ax.set_xticks(range(4), labels)
    ax.set_ylabel("Probability of exceeding calibration maximum (log scale)")
    ax.set_title("E002-410 | Velocity calibration fails under frame pseudoreplication")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper left", fontsize=8)
    ax.text(0.99, 0.04, "Synthetic velocities; not human eyelid error rates",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, format="svg", metadata={"Creator": "Lucent E002-410 reproducible figure"})
    plt.close(fig)


if __name__ == "__main__":
    main()
