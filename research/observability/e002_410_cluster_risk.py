#!/usr/bin/env python3
"""E002-410: clustered-velocity calibration falsification (synthetic only).

Preregistered in E002_410_FROZEN.md. Does NOT certify physical eyelid velocity.
"""
from __future__ import annotations

import argparse
import json
import math

import numpy as np

SEED = 4102026
TRIALS = 40000
PARTICIPANTS = 20
FRAMES = 100
EPSILON = 0.001


def exact_batch_exceedance(n: int, m: int) -> float:
    """Probability a future maximum outranks n exchangeable calibration maxima."""
    if isinstance(n, bool) or isinstance(m, bool) or not isinstance(n, int) or not isinstance(m, int):
        raise ValueError("Counts must be integer participant units")
    if n < 1 or m < 1:
        raise ValueError("Positive independent participant counts required")
    return m / (n + m)


def research_risk_gate(*, participant_maxima, future_participants: int,
                       alpha: float, calibration_unit: str,
                       exchangeability_reviewed: bool,
                       physical_aperture_reviewed: bool,
                       same_device_domain: bool) -> dict:
    """Fail-closed research eligibility check; never authorizes a physical product certificate.

    These flags are self-declarations, NOT authentication of calibration evidence.
    """
    reasons = []
    try:
        vals = list(participant_maxima)
        if not vals or any(not isinstance(x, (float, int)) or isinstance(x, bool)
                           or not math.isfinite(x) or x < 0 for x in vals):
            reasons.append("invalid_or_missing_participant_maxima")
        if calibration_unit != "independent_participant_session_maximum":
            reasons.append("frame_pseudoreplication")
        if len(vals) != len(set(vals)):
            # Ties are allowed by rank theory; do not reject ties, but report their existence.
            tied = True
        else:
            tied = False
    except (TypeError, ValueError):
        vals = []
        tied = False
        reasons.append("invalid_or_missing_participant_maxima")
    if not exchangeability_reviewed:
        reasons.append("participant_exchangeability_not_reviewed")
    if not physical_aperture_reviewed:
        reasons.append("physical_aperture_not_reviewed")
    if not same_device_domain:
        reasons.append("device_domain_shift")
    if not isinstance(alpha, (int, float)) or isinstance(alpha, bool) or not math.isfinite(alpha) or not 0 < alpha < 1:
        reasons.append("invalid_alpha")
    if isinstance(future_participants, bool) or not isinstance(future_participants, int) or future_participants < 1:
        reasons.append("invalid_future_participant_count")
    if vals and not reasons:
        risk = exact_batch_exceedance(len(vals), future_participants)
        if risk > alpha + 1e-12:
            reasons.append("insufficient_independent_participants")
    else:
        risk = None
    return {
        "research_rank_eligibility": "CONDITIONAL_ONLY" if not reasons else "REJECT",
        "product": "ABSTAIN_UNCALIBRATED",
        "calibration_participants": len(vals),
        "future_participants": future_participants,
        "marginal_exceedance_risk_if_exchangeable": risk,
        "ties_present": tied,
        "reasons": reasons,
        "warning": "No self-reported flags authenticate physical aperture, exchangeability, "
                   "camera timing, optical inversion, or shutter calibration. This is not a "
                   "deterministic E002-371 closure certificate."
    }


def run(*, seed: int = SEED, trials: int = TRIALS,
        participants: int = PARTICIPANTS, frames: int = FRAMES) -> dict:
    rng = np.random.default_rng(seed)
    if trials < 1000 or participants < 2 or frames < 2:
        raise ValueError("Insufficient trial or cluster counts")
    counts = dict(clustered_single=0, iid_single=0, shifted_single=0, session_max=0)
    for start in range(0, trials, 250):
        batch = min(250, trials - start)
        u_cal = rng.random((batch, participants, 1))
        eps_cal = rng.random((batch, participants, frames)) * EPSILON
        cal_max = np.max(u_cal + eps_cal, axis=(1, 2))
        u_future = rng.random(batch)
        eps_future = rng.random(batch) * EPSILON
        counts["clustered_single"] += int(np.count_nonzero(u_future + eps_future > cal_max))
        counts["shifted_single"] += int(np.count_nonzero(u_future + 0.25 + eps_future > cal_max))
        future_session = u_future[:, None] + rng.random((batch, frames)) * EPSILON
        counts["session_max"] += int(np.count_nonzero(np.max(future_session, axis=1) > cal_max))
        iid_cal_max = np.max(rng.random((batch, participants * frames)), axis=1)
        iid_future = rng.random(batch)
        counts["iid_single"] += int(np.count_nonzero(iid_future > iid_cal_max))
    rates = {key: value / trials for key, value in counts.items()}
    participant_rank = exact_batch_exceedance(participants, 1)
    naive_frame_rank = exact_batch_exceedance(participants * frames, 1)
    predictions = {
        "clustered_near_participant_rank": abs(rates["clustered_single"] - participant_rank) <= 0.006,
        "clustered_over_40x_naive_frame_risk": rates["clustered_single"] > 40 * naive_frame_rank,
        "iid_near_frame_rank": abs(rates["iid_single"] - naive_frame_rank) <= 0.0007,
        "session_max_near_participant_rank": abs(rates["session_max"] - participant_rank) <= 0.006,
        "shift_exceeds_20pct": rates["shifted_single"] > 0.20,
    }
    return {
        "experiment": "E002-410",
        "evidence_tier": "synthetic clustered velocities, NOT human aperture data",
        "seed": seed, "trials": trials, "calibration_participants": participants,
        "frames_per_participant": frames, "future_participants": 1,
        "counts": counts, "rates": rates,
        "theoretical_participant_rank_risk": participant_rank,
        "naive_frame_rank_risk": naive_frame_rank,
        "clustered_to_naive_risk_ratio": rates["clustered_single"] / naive_frame_rank,
        "predictions": predictions,
        "joint_pass": all(predictions.values()),
        "product": "ABSTAIN_UNCALIBRATED",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default=None)
    args = p.parse_args()
    report = run()
    payload = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(payload + "\n")
    print(payload)
    if not report["joint_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
