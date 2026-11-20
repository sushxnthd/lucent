#!/usr/bin/env python3
"""E002-528 exact conditional reference-camera phase sensitivity.

Synthetic instrument geometry only. No anatomical measurement, camera attestation,
validated speed cap, or physical product authorization.
"""
import argparse
import json
from fractions import Fraction as F


def exact(x):
    """Reject binary floats to prevent silently changing frozen rational boundaries."""
    if isinstance(x, bool) or not isinstance(x, (str, int, F)):
        raise TypeError('EXACT_RATIONAL_REQUIRED')
    return F(x)


def clamp01(x):
    return max(F(0), min(F(1), x))


def check(period, exposure, duration, uncertainty):
    p, e, d, u = map(exact, (period, exposure, duration, uncertainty))
    if not (p > e > 0 and d >= 0 and u >= 0):
        raise ValueError('INVALID_INSTRUMENT_PARAMETERS')
    return p, e, d, u


def opportunities(period, exposure, duration, uncertainty=F(0)):
    p, e, d, u = check(period, exposure, duration, uncertainty)
    full = clamp01((d - e - 2*u)/p)
    overlap = clamp01((d + e)/p) if d > 0 else F(0)
    return {'strict_full_uniform_phase': full,
            'ideal_positive_overlap_uniform_phase': overlap,
            'every_phase_strict_full_guaranteed': d > p + e + 2*u,
            'phase_model': 'HYPOTHETICAL_UNIFORM_INDEPENDENT',
            'evidence_tier': 'EXACT_INSTRUMENT_DESIGN_ONLY',
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def bounded_phase_probability(p_full, tv_epsilon):
    p, eps = exact(p_full), exact(tv_epsilon)
    if not (0 <= p <= 1 and 0 <= eps <= 1):
        raise ValueError('INVALID_PHASE_DISTRIBUTION_BOUND')
    return {'lower': clamp01(p - eps), 'upper': clamp01(p + eps)}


def independent_trial_probability(p_full, n, *, phase_independence_attested=False):
    p = exact(p_full)
    if not 0 <= p <= 1 or type(n) is not int or n < 1 or type(phase_independence_attested) is not bool:
        raise ValueError('INVALID_TRIAL_MODEL')
    if not phase_independence_attested:
        return None
    return 1 - (1-p)**n


def brute_strict_full(period, exposure, duration, phase, uncertainty=F(0)):
    """Independent lattice scan for checking the closed-form probability."""
    p, e, d, u = check(period, exposure, duration, uncertainty)
    phi = exact(phase)
    if not 0 <= phi < p:
        raise ValueError('INVALID_PHASE')
    for k in range(-2, int(d//p) + 3):
        a = phi + k*p
        if a-u > 0 and a+e+u < d:
            return True
    return False


def phase_grid_count(period, exposure, duration, uncertainty=F(0), n=10000):
    p, e, d, u = check(period, exposure, duration, uncertainty)
    if type(n) is not int or n < 1 or n > 100000:
        raise ValueError('INVALID_GRID_SIZE')
    count = sum(brute_strict_full(p, e, d, p*F(j,n), u) for j in range(n))
    return {'witnesses': count, 'grid': n, 'fraction': F(count,n)}


def format_fraction(x):
    return {'exact': str(x), 'decimal': float(x)}


def example(name, p, e, d, u=F(0)):
    r = opportunities(p,e,d,u)
    return {'name': name, 'period_ms': str(p), 'exposure_ms': str(e),
            'closure_duration_ms': str(d), 'endpoint_uncertainty_ms': str(u),
            'strict_full_probability': format_fraction(r['strict_full_uniform_phase']),
            'positive_overlap_probability': format_fraction(r['ideal_positive_overlap_uniform_phase']),
            'every_phase_strict_full_guaranteed': r['every_phase_strict_full_guaranteed']}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', default='-')
    args = ap.parse_args()
    p,e,u = F(25,6),F(1),F(1,10)
    prob = opportunities(p,e,F(4),u)['strict_full_uniform_phase']
    out = {'experiment': 'E002-528',
           'evidence_tier': 'EXACT_SYNTHETIC_INSTRUMENT_DESIGN_ONLY',
           'cases': [example('240Hz_3ms',p,e,F(3),u),
                     example('240Hz_4ms',p,e,F(4),u),
                     example('240Hz_5ms_HELDOUT',p,e,F(5),u),
                     example('1000Hz_1p2ms_HELDOUT',F(1),F(1,2),F(6,5))],
           'three_independent_uniform_phase_opportunities':
                format_fraction(independent_trial_probability(prob,3,phase_independence_attested=True)),
           'unattested_independence_probability': None,
           'tv_0p1_interval': {k:format_fraction(v) for k,v in bounded_phase_probability(prob,F(1,10)).items()},
           'physical_phase_randomization_authenticated': False,
           'human_raters': 0, 'physical_camera_calibrations': 0,
           'participant_disjoint_physical_predictions': 0,
           'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}
    payload=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if args.output=='-': print(payload,end='')
    else:
        with open(args.output,'w',encoding='utf-8') as f: f.write(payload)


if __name__ == '__main__':
    main()
