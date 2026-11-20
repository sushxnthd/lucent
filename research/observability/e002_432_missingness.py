"""E002-432: missing-frame falsification in an idealized boxcar/physical-aperture model.

Synthetic evidence only. No real camera, physiological velocity cap, or physical certification.
"""
from __future__ import annotations

import json
import math
import random

FPS = 30
D = 1.0 / FPS
EXPOSURE = 0.002
V = 4.0  # hypothetical mm/s, NOT a human physiological limit
THETA = 2.0
OPEN = 2.10
DEPTH = 0.12
APERTURE_ERROR = 0.005
CLOCK_ERROR = 0.0005


def _finite(*xs):
    return all(isinstance(x, (int, float)) and not isinstance(x, bool)
               and math.isfinite(x) for x in xs)


def aperture(t, depth=DEPTH):
    """A flat-shouldered triangular dip; endpoint exposure averages equal OPEN."""
    if not _finite(t, depth) or depth < 0 or depth > V * (D - EXPOSURE / 2):
        raise ValueError("invalid trajectory parameters")
    shoulder = EXPOSURE / 2
    if t <= shoulder or t >= 2 * D - shoulder:
        return OPEN
    if t <= D:
        return OPEN - depth * (t - shoulder) / (D - shoulder)
    return OPEN - depth * (2 * D - shoulder - t) / (D - shoulder)


def boxcar_mean(center, depth):
    """Exact integration of the piecewise-linear aperture over a boxcar."""
    if not _finite(center, depth) or depth < 0 or depth > V * (D - EXPOSURE / 2):
        raise ValueError("invalid exposure")
    start, end = center - EXPOSURE / 2, center + EXPOSURE / 2
    knots = sorted({start, end, *[t for t in (EXPOSURE / 2, D, 2 * D - EXPOSURE / 2)
                                 if start < t < end]})
    return sum((aperture(l, depth) + aperture(r, depth)) * (r - l) / 2
               for l, r in zip(knots, knots[1:])) / EXPOSURE


def conditional_lower(y0, y1, t0, t1, speed=V, aperture_error=0.0,
                      clock_error=0.0, exposure=EXPOSURE):
    """Conservative lower over the CENTER-TO-CENTER interval in ideal boxcar model.

    Uses actual acquisition timestamps, never retained-row adjacency. This is
    conditional on an independently valid speed cap, physical aperture inversion,
    shutter response and error bounds. It is NOT a physical product certificate.
    """
    if not _finite(y0, y1, t0, t1, speed, aperture_error, clock_error, exposure):
        raise ValueError("missing/nonfinite measurement or timestamp")
    gap = t1 - t0
    if min(y0, y1) < 0 or gap <= 0 or speed < 0 or aperture_error < 0 or clock_error < 0:
        raise ValueError("invalid measurements or clock")
    if exposure <= 0 or exposure > gap:
        raise ValueError("unsupported shutter geometry")
    return max(0.0, min(y0, y1) - aperture_error -
               speed * (gap + 2 * clock_error) / 2)


def study_decision(frame_ids, timestamps, observations, compressed=False,
                   aperture_error=0.0, clock_error=0.0):
    """Evaluate a synthetic 3-frame interval with possible missing center frame.

    The intentionally WRONG compressed mode models a pipeline discarding missing
    rows and pretending surviving observations are adjacent at 30 Hz.
    """
    if len(frame_ids) != len(timestamps) or len(frame_ids) != len(observations):
        raise ValueError("misaligned frame metadata")
    if len(frame_ids) < 2 or frame_ids[0] != 0 or frame_ids[-1] != 2:
        raise ValueError("missing interval endpoints")
    if any(not isinstance(i, int) or isinstance(i, bool) for i in frame_ids):
        raise ValueError("invalid frame ids")
    if any(b <= a for a, b in zip(frame_ids, frame_ids[1:])):
        raise ValueError("duplicate/reordered frame ids")
    if any(not _finite(t) for t in timestamps):
        raise ValueError("timestamps required")
    if any(not _finite(y) for y in observations):
        raise ValueError("invalid aperture")
    if any(abs(t - i * D) > 1e-8 for i, t in zip(frame_ids, timestamps)):
        raise ValueError("clock mismatch requires independent calibration")
    lowers = []
    for j in range(len(frame_ids) - 1):
        t0, t1 = ((0.0, D) if compressed else (timestamps[j], timestamps[j + 1]))
        lowers.append(conditional_lower(
            observations[j], observations[j + 1], t0, t1,
            aperture_error=aperture_error, clock_error=clock_error))
    candidate = all(x > THETA for x in lowers)
    return dict(study_only="CONDITIONAL_CANDIDATE" if candidate else "ABSTAIN",
                candidate=candidate, minimum_lower_mm=min(lowers),
                physical_certificate_authorized=False,
                product="ABSTAIN_UNCALIBRATED")


def evaluate_trial(depth, dropout):
    if not _finite(depth) or depth < 0 or depth > V * (D - EXPOSURE / 2):
        raise ValueError("invalid depth")
    if not isinstance(dropout, bool):
        raise ValueError("dropout must be boolean")
    ids = [0, 2] if dropout else [0, 1, 2]
    times = [i * D for i in ids]
    means = [boxcar_mean(t, depth) for t in times]
    naive = study_decision(ids, times, means, compressed=True)
    aware = study_decision(ids, times, means, compressed=False)
    truth_closed = OPEN - depth <= THETA
    return dict(truth_closed=truth_closed, naive=naive["candidate"],
                timestamp_aware=aware["candidate"],
                observed_frames=len(ids))


def stress(n=1200, seed=432):
    if not isinstance(n, int) or isinstance(n, bool) or n != 1200:
        raise ValueError("frozen trial count is 1200")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("invalid seed")
    rng = random.Random(seed)
    # Precommit the trial depths, then evaluate both missingness regimes.
    depths = [0.0] * (n // 2) + [rng.uniform(0.08, 0.125) for _ in range(n // 2)]
    rng.shuffle(depths)
    results = {}
    for regime in ("MCAR", "MNAR"):
        counts = dict(n=n, true_closures=0, dropped=0, naive_candidates=0,
                      aware_candidates=0, naive_false=0, aware_false=0,
                      witnessed_when_retained=0)
        for depth in depths:
            truth = OPEN - depth <= THETA
            p = 0.15 if regime == "MCAR" else (0.90 if truth else 0.05)
            missing = rng.random() < p
            row = evaluate_trial(depth, missing)
            counts["true_closures"] += int(truth)
            counts["dropped"] += int(missing)
            counts["naive_candidates"] += int(row["naive"])
            counts["aware_candidates"] += int(row["timestamp_aware"])
            counts["naive_false"] += int(truth and row["naive"])
            counts["aware_false"] += int(truth and row["timestamp_aware"])
            counts["witnessed_when_retained"] += int(truth and not missing and
                boxcar_mean(D, depth) <= THETA)
        results[regime] = counts
    return results


def experiment():
    closed = evaluate_trial(DEPTH, True)
    open_world = evaluate_trial(0.0, True)
    y0 = boxcar_mean(0, DEPTH)
    y2 = boxcar_mean(2 * D, DEPTH)
    with_midpoint = evaluate_trial(DEPTH, False)
    naive_lower = conditional_lower(y0, y2, 0, D)
    aware_lower = conditional_lower(y0, y2, 0, 2 * D)
    uncertain_lower = conditional_lower(
        y0, y2, 0, 2 * D, aperture_error=APERTURE_ERROR,
        clock_error=CLOCK_ERROR)
    return dict(evidence_tier="SYNTHETIC_MISSINGNESS_ALIAS",
                physical_aperture_mm=[OPEN, OPEN - DEPTH],
                actual_peak_speed_mm_s=DEPTH / (D - EXPOSURE / 2),
                surviving_exposure_means_mm=[y0, y2],
                open_world_surviving_means_mm=[boxcar_mean(0, 0), boxcar_mean(2 * D, 0)],
                midpoint_exposure_mean_mm=boxcar_mean(D, DEPTH),
                naive_compressed_lower_mm=naive_lower,
                actual_timestamp_lower_mm=aware_lower,
                uncertain_timestamp_lower_mm=uncertain_lower,
                hidden_world_naive_false=closed["naive"],
                hidden_world_aware_abstains=not closed["timestamp_aware"],
                open_world_aware_abstains=not open_world["timestamp_aware"],
                retained_midpoint_blocks_false_certificate=not with_midpoint["naive"],
                holdout=stress(), physical_certificate_authorized=False,
                product="ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
