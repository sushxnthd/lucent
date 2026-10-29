#!/usr/bin/env python3
"""E002-495 exact scalar exposure-mean hidden-closure boundary.

Synthetic measurement model only; not a physiological velocity estimate, human
anatomical label, or calibrated physical shutter observation.
"""
import argparse
from fractions import Fraction as F
import json
import random


def Q(x):
    if isinstance(x, bool):
        raise ValueError('BOOLEAN_NOT_A_MEASUREMENT')
    return F(str(x))


def evaluate(T, e, V, b, c, aperture_cap=None):
    T, e, V, b, c = map(Q, (T, e, V, b, c))
    if not (T > 0 and 0 < e <= T and V > 0 and 0 <= c < b):
        raise ValueError('INVALID_SCALAR_MODEL')
    g = T - e
    m = 2 * (b-c) / T
    tau = g / 2
    peak = c + m * (g/2 + e)
    if aperture_cap is not None:
        cap = Q(aperture_cap)
        if cap < b or cap <= c:
            raise ValueError('INVALID_APERTURE_CAP')
    else:
        cap = None
    feasible = m <= V
    # This witness is sufficient for the uncapped model. A cap can invalidate
    # this particular witness without proving that all possible witnesses fail.
    cap_allows_witness = cap is None or cap >= peak
    left_start = c + m * (tau + e)
    left_end = c + m * tau
    right_start = c + m * (g-tau)
    right_end = c + m * (g+e-tau)
    left_mean = (left_start+left_end)/2
    right_mean = (right_start+right_end)/2
    assert left_mean == b and right_mean == b
    assert right_start == left_end
    assert m > 0
    return {
        'experiment': 'E002-495',
        'model': 'EXACT_EQUAL_SCALAR_EXPOSURE_MEANS_AND_GLOBAL_LIPSCHITZ_BOUND',
        'T': str(T), 'e': str(e), 'g': str(g), 'V': str(V),
        'b': str(b), 'c': str(c), 'tent_slope': str(m),
        'closure_time': str(tau), 'tent_peak': str(peak),
        'left_exposure_mean': str(left_mean), 'right_exposure_mean': str(right_mean),
        'endpoint_aperture': str(left_end),
        'R_endpoint': str(V*g/(2*(b-c))),
        'R_average': str(V*T/(2*(b-c))),
        'hidden_closure_excluded_by_mean_bound': not feasible,
        'closing_tent_admissible_by_velocity': feasible,
        'constructed_witness_respects_cap': cap_allows_witness,
        'naive_endpoint_substitution_false_exclusion': V*g < 2*(b-c) <= V*T,
        'physical_camera_calibrated': False,
        'human_reference_validated': False,
        'anatomical_closure_labels': 0,
        'product': 'ABSTAIN_UNCALIBRATED',
        'release': 'BLOCKED',
    }


def independent_midpoint(T, e, b, c, n=100000):
    """Independent floating-point midpoint quadrature of the tent witness."""
    T, e, b, c = map(float, (T, e, b, c))
    g = T-e
    tau = g/2
    m = 2*(b-c)/T
    def average(start):
        return sum(c+m*abs(start+(k+.5)*e/n-tau) for k in range(n))/n
    return average(-e), average(g)


def sweep(seed=495, n=1000):
    rng = random.Random(seed)
    false_exclusions = 0
    feasible = excluded = 0
    for _ in range(n):
        T = F(rng.randint(2, 100), 10)
        e = T * F(rng.randint(1, 10), 10)
        V = F(rng.randint(1, 50), 100)
        c = F(rng.randint(0, 30), 100)
        b = c + F(rng.randint(1, 100), 100)
        result = evaluate(T, e, V, b, c)
        if result['hidden_closure_excluded_by_mean_bound']:
            excluded += 1
        else:
            feasible += 1
        if result['naive_endpoint_substitution_false_exclusion']:
            false_exclusions += 1
    return {'cases': n, 'feasible': feasible, 'excluded': excluded,
            'naive_endpoint_false_exclusions': false_exclusions,
            'evidence_tier': 'EXACT_SYNTHETIC_MEASUREMENT_MODEL_ONLY',
            'human_reference_validated': False, 'release': 'BLOCKED'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    args = p.parse_args()
    case = evaluate('15', '5', '.1', '.7', '.1', '1')
    fail = evaluate('15', '5', '.1', '.9', '.1')
    cap = evaluate('15', '5', '.1', '.7', '.1', '.8')
    quad = independent_midpoint(15, 5, .7, .1)
    if not all(abs(x-.7)<1e-10 for x in quad):
        raise AssertionError('INDEPENDENT_QUADRATURE_FAILED')
    if not (case['naive_endpoint_substitution_false_exclusion'] and
            case['closing_tent_admissible_by_velocity'] and
            fail['hidden_closure_excluded_by_mean_bound'] and
            not cap['constructed_witness_respects_cap']):
        raise AssertionError('FROZEN_PREDICTION_FAILED')
    report = {'frozen_case': case, 'strict_exclusion_control': fail,
              'cap_warning_control': cap, 'independent_midpoint_means': [float(f'{x:.12g}') for x in quad],
              'deterministic_adversarial_sweep': sweep()}
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps(report['deterministic_adversarial_sweep'], sort_keys=True))


if __name__ == '__main__':
    main()
