#!/usr/bin/env python3
"""E002-570: exact global-shutter exposure-mean counterexample.

Research-only: assumes a physically ideal *linear aperture sensor*, known boxcar
shutter and a hard Lipschitz speed bound. None is certified for Lucent humans.
"""
from __future__ import annotations

from fractions import Fraction as Q
import json

V = Q(25)
THETA = Q(1, 5)
F = Q(1, 30)
W = Q(1, 100)
H = F - W
A = Q(123, 200)
MINIMUM = Q(119, 600)
KNOTS = ((Q(0), Q(37, 50)), (W, Q(49, 100)),
         ((W + F) / 2, MINIMUM), (F, Q(49, 100)),
         (F + W, Q(37, 50)))


def q(value):
    if type(value) is bool:
        raise ValueError('boolean is not a physical quantity')
    try:
        x = value if isinstance(value, Q) else Q(str(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('invalid rational') from exc
    return x


def validate_path(knots=KNOTS, ceiling=V):
    ceiling = q(ceiling)
    if ceiling <= 0 or len(knots) < 2:
        raise ValueError('invalid speed ceiling or knots')
    for (t0, a0), (t1, a1) in zip(knots, knots[1:]):
        if not (0 <= a0 <= 1 and 0 <= a1 <= 1 and t0 < t1):
            raise ValueError('invalid time/aperture geometry')
        if abs(a1 - a0) > ceiling * (t1 - t0):
            raise ValueError('violates hard Lipschitz speed ceiling')
    return True


def at(t, knots=KNOTS):
    t = q(t)
    if t < knots[0][0] or t > knots[-1][0]:
        raise ValueError('time outside path')
    for (t0, a0), (t1, a1) in zip(knots, knots[1:]):
        if t0 <= t <= t1:
            return a0 + (a1 - a0) * (t - t0) / (t1 - t0)
    raise AssertionError('unreachable')


def mean_on(start, end, knots=KNOTS):
    start, end = q(start), q(end)
    if not (knots[0][0] <= start < end <= knots[-1][0]):
        raise ValueError('invalid exposure interval')
    points = [start] + [t for t, _ in knots if start < t < end] + [end]
    area = sum((at(t0, knots) + at(t1, knots)) * (t1 - t0) / 2
               for t0, t1 in zip(points, points[1:]))
    return area / (end - start)


def bound(meana, meanb, *, v, gap, width_a, width_b, aperture_error=0,
          clock_error=0, boxcar_authenticated=False):
    """Conditional gap lower bound; NOT a physiological certification.

    Each aperture error is a worst-case absolute error in an exposure mean.
    clock_error is a per-edge timing bound, so the gap expands by 2*error.
    """
    a, b, v, h = map(q, (meana, meanb, v, gap))
    w1, w2, e, u = map(q, (width_a, width_b, aperture_error, clock_error))
    if not (0 <= a <= 1 and 0 <= b <= 1 and v > 0 and h >= 0
            and w1 > 0 and w2 > 0 and e >= 0 and u >= 0):
        raise ValueError('invalid instrument inputs')
    if not boxcar_authenticated:
        return {'decision': 'ABSTAIN_UNCALIBRATED', 'lower_bound': None}
    effective = h + (w1 + w2) / 2 + 2 * u
    lower = max(Q(0), (a + b - 2 * e - v * effective) / 2)
    return {'decision': 'RESEARCH_BOUND_ONLY', 'lower_bound': lower}


def ratio(x):
    return {'numerator': x.numerator, 'denominator': x.denominator}


def report():
    validate_path()
    first, second = mean_on(0, W), mean_on(F, F + W)
    naive = (first + second - V * H) / 2
    corrected = bound(first, second, v=V, gap=H, width_a=W, width_b=W,
                      boxcar_authenticated=True)['lower_bound']
    assert first == A == second
    assert naive == Q(97, 300)
    assert corrected == MINIMUM == at((F + W) / 2)
    assert MINIMUM < THETA < naive
    return {
        'experiment': 'E002-570', 'evidence_tier': 'exact_synthetic_instrument_model_only',
        'period_s': ratio(F), 'exposure_s': ratio(W), 'gap_s': ratio(H),
        'normalized_velocity_per_s': ratio(V), 'threshold': ratio(THETA),
        'exposure_means': [ratio(first), ratio(second)],
        'naive_point_endpoint_lower_bound': ratio(naive),
        'correct_boxcar_lower_bound': ratio(corrected),
        'actual_hidden_minimum': ratio(MINIMUM),
        'naive_false_exclusion': True,
        'corrected_conditional_exclusion': False,
        'human_measurement': False, 'physical_shutter_capture': False,
        'independent_human_rater_pairs': 0, 'certified_human_velocity_upper_bounds': 0,
        'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED',
    }


if __name__ == '__main__':
    print(json.dumps(report(), sort_keys=True, indent=2))
