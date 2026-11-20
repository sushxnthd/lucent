#!/usr/bin/env python3
"""E002-529: exact adversarial speed-limited aperture with arbitrarily short closure dwell.

Research-only scalar construction. Never a camera, physiological, or product certificate.
"""
import json
from fractions import Fraction as F


def q(x):
    if isinstance(x, bool) or not isinstance(x, (str, int, F)):
        raise TypeError("EXACT_RATIONAL_REQUIRED")
    return F(x)


def clamp01(x):
    return max(F(0), min(F(1), x))


def phase_opportunity(period, exposure, dwell, uncertainty=0):
    p, e, d, u = map(q, (period, exposure, dwell, uncertainty))
    if not (p > e > 0 and d >= 0 and u >= 0):
        raise ValueError("INVALID_REFERENCE_CAMERA")
    return {
        "strict_full": clamp01((d - e - 2 * u) / p),
        "ideal_overlap": clamp01((d + e) / p) if d else F(0),
    }


def construct(b, c, speed, gap, dwell):
    """Construct a continuous V-Lipschitz trajectory with exactly 'dwell' below c."""
    b, c, v, H, eps = map(q, (b, c, speed, gap, dwell))
    if not (0 < c < b <= 1 and v > 0 and H > 0 and eps > 0):
        raise ValueError("INVALID_APERTURE_PARAMETERS")
    min_excursion = 2 * (b - c) / v
    h = v * eps / 4
    total = min_excursion + eps
    if not (h < c and total < H):
        raise ValueError("NO_INTERIOR_POSITIVE_DWELL_CONSTRUCTION")
    start = (H - total) / 2
    descend = (b - c + h) / v
    t1 = start + descend
    t2 = t1 + eps / 2
    t3 = t2 + descend
    knots = ((F(0), b), (start, b), (t1, c - h),
             (t2, c - h), (t3, b), (H, b))
    return {
        "knots": knots, "below_threshold_dwell": eps,
        "minimum_excursion": min_excursion, "total_excursion": total,
        "gap": H, "speed": v, "threshold": c, "open_aperture": b,
    }


def integrate_below_threshold(knots, threshold):
    """Independent piecewise-linear geometric dwell oracle (strict a<c)."""
    c = q(threshold)
    total = F(0)
    for (t0, a0), (t1, a1) in zip(knots, knots[1:]):
        dt = t1 - t0
        if dt <= 0:
            raise ValueError("INVALID_KNOT_TIMING")
        if a0 < c and a1 < c:
            total += dt
        elif a0 >= c and a1 < c:
            total += dt * (c - a1) / (a0 - a1)
        elif a0 < c and a1 >= c:
            total += dt * (c - a0) / (a1 - a0)
    return total


def validate_trajectory(model):
    knots, v, c, b, H = (model[k] for k in
                         ("knots", "speed", "threshold", "open_aperture", "gap"))
    if knots[0] != (0, b) or knots[-1] != (H, b):
        return False
    for (t0, a0), (t1, a1) in zip(knots, knots[1:]):
        if not (t1 > t0 and 0 <= a0 <= 1 and 0 <= a1 <= 1):
            return False
        if abs(a1 - a0) > v * (t1 - t0):
            return False
    return integrate_below_threshold(knots, c) == model["below_threshold_dwell"]


def phase_grid_full(period, exposure, dwell, uncertainty=0, n=10000):
    p, e, d, u = map(q, (period, exposure, dwell, uncertainty))
    if not (p > e > 0 and d >= 0 and u >= 0 and type(n) is int and 0 < n <= 100000):
        raise ValueError("INVALID_GRID")
    count = 0
    for j in range(n):
        phi = p * F(j, n)
        for k in range(-2, int(d // p) + 3):
            start = phi + k * p
            if start - u > 0 and start + e + u < d:
                count += 1
                break
    return F(count, n)


def as_json_fraction(x):
    return {"exact": str(x), "decimal": float(x)}


def run_examples():
    b, c, v, H, eps = F(1), F(1, 5), F(60), F(1, 30), F(1, 10000)
    model = construct(b, c, v, H, eps)
    assert validate_trajectory(model)
    p240 = phase_opportunity(F(1, 240), F(1, 1000), eps, F(1, 10000))
    p1000 = phase_opportunity(F(1, 1000), F(1, 2000), eps)
    invalid = phase_opportunity(F(1, 240), F(1, 1000), model["minimum_excursion"], F(1, 10000))
    return {
        "experiment": "E002-529", "evidence_tier": "EXACT_SYNTHETIC_FALSIFICATION_ONLY",
        "minimum_excursion_seconds": as_json_fraction(model["minimum_excursion"]),
        "whole_excursion_seconds": as_json_fraction(model["total_excursion"]),
        "true_below_threshold_dwell_seconds": as_json_fraction(eps),
        "trajectory_valid": validate_trajectory(model),
        "240hz_full": as_json_fraction(p240["strict_full"]),
        "240hz_overlap": as_json_fraction(p240["ideal_overlap"]),
        "1000hz_full": as_json_fraction(p1000["strict_full"]),
        "1000hz_overlap": as_json_fraction(p1000["ideal_overlap"]),
        "invalid_240hz_excursion_substitution_full": as_json_fraction(invalid["strict_full"]),
        "authenticated_camera": False, "human_anatomical_raters": 0,
        "certified_human_speed_bound": False,
        "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED",
    }


if __name__ == "__main__":
    print(json.dumps(run_examples(), sort_keys=True, indent=2))
