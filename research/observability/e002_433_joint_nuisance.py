"""E002-433: preregistered joint-nuisance false-certification experiment.

Synthetic scalar-optical model only. No physiological hard velocity cap,
human eyelid ground truth, real shutter calibration or product certification.
"""
from __future__ import annotations

import json
import math
import random

D = 1.0 / 30.0
E = 0.002
THETA = 2.0
V = 1.5  # hypothetical mm/s, NOT a physiological bound
Y = 2.0
G_RANGE = (0.97, 1.03)
ANGLE_RANGE = (15.0, 20.0)
ENDPOINT_B = 2.012
MIN_B = 1.991


def _finite(*xs):
    return all(isinstance(x, (float, int)) and not isinstance(x, bool)
               and math.isfinite(x) for x in xs)


def cosd(angle):
    return math.cos(math.radians(angle))


def conditional_lower(y0, y1, gain_upper, angle_min_deg, speed_cap=V,
                      center_spacing=D, exposure_s=E):
    """Conservative restricted two-boxcar bound, not a real certificate.

    y_i = mean(g(t) cos(phi(t)) a(t)), a>=0 and |a'|<=V.
    Assumes 0<g<=gain_upper and 0<=angle_min<=phi(t)<90 degrees.
    Each shutter's mean physical aperture >= y_i/(gain_upper*cos(angle_min)).
    Lipschitz recovery over the two centers gives the stated lower bound.
    """
    vals = (y0, y1, gain_upper, angle_min_deg, speed_cap,
            center_spacing, exposure_s)
    if not _finite(*vals):
        raise ValueError("nonfinite or missing optical calibration")
    if min(y0, y1) < 0 or gain_upper <= 0 or speed_cap < 0:
        raise ValueError("invalid intensity, gain or velocity")
    if not 0 <= angle_min_deg < 90 or center_spacing <= 0:
        raise ValueError("invalid geometry or timestamp")
    if not 0 < exposure_s <= center_spacing:
        raise ValueError("unsupported exposure")
    return max(0.0, min(y0, y1) /
               (gain_upper * cosd(angle_min_deg)) -
               speed_cap * center_spacing / 2.0)


def world_b_aperture(t):
    if not _finite(t):
        raise ValueError("nonfinite time")
    shoulder = E / 2
    middle = D / 2
    if t <= shoulder or t >= D - shoulder:
        return ENDPOINT_B
    if t <= middle:
        return ENDPOINT_B - (ENDPOINT_B - MIN_B) * (t - shoulder) / (middle - shoulder)
    return MIN_B + (ENDPOINT_B - MIN_B) * (t - middle) / (middle - shoulder)


def world_a(t):
    if not _finite(t):
        raise ValueError("nonfinite time")
    return Y / cosd(20.0), 1.0, 20.0


def world_b(t):
    if not _finite(t):
        raise ValueError("nonfinite time")
    return world_b_aperture(t), Y / (ENDPOINT_B * cosd(15.0)), 15.0


def optical(world, t):
    a, g, angle = world(t)
    return a * g * cosd(angle)


def exposure_mean(world, center, subdivisions=2000):
    if not _finite(center) or not isinstance(subdivisions, int) or isinstance(subdivisions, bool) or subdivisions < 1:
        raise ValueError("invalid shutter integration")
    return sum(optical(world, center + E * ((j + .5) / subdivisions - .5))
               for j in range(subdivisions)) / subdivisions


def _interp(x, xs, ys):
    if x <= xs[0]:
        return ys[0]
    for j in range(len(xs) - 1):
        if x <= xs[j + 1]:
            u = (x - xs[j]) / (xs[j + 1] - xs[j])
            return ys[j] * (1 - u) + ys[j + 1] * u
    return ys[-1]


def stress(n=2000, seed=433):
    """Frozen 2000 unseen synthetic trajectories; no training or tuning."""
    if not isinstance(n, int) or isinstance(n, bool) or n != 2000:
        raise ValueError("frozen sample count")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("invalid seed")
    rng = random.Random(seed)
    knots = (-E / 2, E / 2, D / 2, D - E / 2, D + E / 2)
    out = dict(n=n, seed=seed, candidates=0, true_closures=0,
               false_certificates=0, min_truth_minus_bound_mm=float("inf"))
    for _ in range(n):
        a = [rng.uniform(1.90, 2.20)]
        for t0, t1 in zip(knots, knots[1:]):
            a.append(a[-1] + rng.uniform(-V, V) * (t1 - t0))
        gain = [rng.uniform(*G_RANGE) for _ in knots]
        angle = [rng.uniform(*ANGLE_RANGE) for _ in knots]

        def signal(t):
            return (_interp(t, knots, a) *
                    _interp(t, knots, gain) *
                    cosd(_interp(t, knots, angle)))

        def mean(c):
            return sum(signal(c + E * ((j + .5) / 96 - .5))
                       for j in range(96)) / 96

        y0, y1 = mean(0), mean(D)
        lower = conditional_lower(y0, y1, G_RANGE[1], ANGLE_RANGE[0])
        truth_min = min(a)
        candidate = lower > THETA
        closed = truth_min <= THETA
        out["candidates"] += int(candidate)
        out["true_closures"] += int(closed)
        out["false_certificates"] += int(candidate and closed)
        out["min_truth_minus_bound_mm"] = min(
            out["min_truth_minus_bound_mm"], truth_min - lower)
    return out


def experiment():
    observed_a = [exposure_mean(world_a, t) for t in (0, D)]
    observed_b = [exposure_mean(world_b, t) for t in (0, D)]
    modes = {
        "naive": (1.0, 20.0),
        "geometry_only": (1.0, 15.0),
        "gain_only": (1.03, 20.0),
        "joint": (1.03, 15.0),
    }
    lowers = {k: conditional_lower(Y, Y, g, phi)
              for k, (g, phi) in modes.items()}
    slope = (ENDPOINT_B - MIN_B) / (D / 2 - E / 2)
    return dict(
        evidence_tier="SYNTHETIC_COMPOSITIONAL_NUISANCE_FALSIFICATION",
        observation_a=observed_a, observation_b=observed_b,
        max_observation_discrepancy=max(abs(x - y) for x, y in zip(observed_a, observed_b)),
        world_a_min_aperture_mm=world_a(0)[0],
        world_b_min_aperture_mm=MIN_B,
        world_b_gain=world_b(0)[1],
        world_b_peak_speed_mm_s=slope,
        threshold_mm=THETA,
        conditional_lowers_mm=lowers,
        incomplete_checks_false_candidates=all(
            lowers[k] > THETA for k in ("naive", "geometry_only", "gain_only")),
        joint_abstains=lowers["joint"] <= THETA,
        holdout=stress(),
        physical_certificate_authorized=False,
        product="ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    print(json.dumps(experiment(), sort_keys=True, indent=2))
