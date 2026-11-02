#!/usr/bin/env python3
"""E002-608: conservative shutter-averaged gap gate. MODEL ONLY.

No input attestation/digest is authenticated by this script. No human
or camera evidence is implied by a conditional model classification.
"""
import argparse
from fractions import Fraction
import json
import re

DIGESTS = ('clock_shutter', 'linear_aperture', 'geometry', 'velocity')
ATTESTATIONS = ('independent_clock_sync', 'shutter_boxcar_calibrated',
                'linear_aperture_calibrated', 'geometry_calibrated',
                'continuous_velocity_ceiling_independent')
NUISANCES = ('geometry', 'brightness', 'missingness', 'blur', 'gaze',
             'glasses', 'sampling', 'clock_error', 'occlusion',
             'saturation', 'rolling_shutter')


def q(v):
    if isinstance(v, bool) or not isinstance(v, (int, float, str)):
        raise ValueError('invalid numeric value')
    try:
        z = Fraction(str(v))
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError('invalid numeric value') from exc
    return z


def nonneg(v):
    z = q(v)
    if z < 0:
        raise ValueError('negative physical budget')
    return z


def result(status, **extra):
    return {'experiment': 'E002-608', 'status': status,
            'evidence_tier': 'CONDITIONAL_BOXCAR_MODEL_ONLY',
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED',
            'note': 'supplied attestations and digests are not independently authenticated',
            **extra}


def evaluate(d):
    if not isinstance(d, dict) or d.get('experiment') != 'E002-608':
        raise ValueError('wrong experiment/schema')
    for k in ('left', 'right', 'uncertainty_ms', 'attestations', 'nuisances', 'evidence_sha256'):
        if not isinstance(d.get(k), dict):
            return result('ABSTAIN_MISSING_CALIBRATION', reason=k)
    for k in ATTESTATIONS:
        if d['attestations'].get(k) is not True:
            return result('ABSTAIN_UNVERIFIED_PREMISE', reason=k)
    for k in NUISANCES:
        if d['nuisances'].get(k) is not False:
            return result('ABSTAIN_NUISANCE', reason=k)
    for k in DIGESTS:
        v = d['evidence_sha256'].get(k)
        if not isinstance(v, str) or re.fullmatch('[0-9a-f]{64}', v) is None:
            return result('ABSTAIN_MISSING_EVIDENCE_DIGEST', reason=k)
    try:
        l, r, u = d['left'], d['right'], d['uncertainty_ms']
        ls, le, la = q(l['start_ms']), q(l['end_ms']), q(l['aperture_lower'])
        rs, re_, ra = q(r['start_ms']), q(r['end_ms']), q(r['aperture_lower'])
        tau, v = q(d['threshold']), nonneg(d['velocity_upper_per_ms'])
        gextra, lextra, rextra = (nonneg(u[k]) for k in
             ('gap_extra', 'left_exposure_extra', 'right_exposure_extra'))
    except (KeyError, ValueError) as exc:
        raise ValueError('invalid physical input') from exc
    if not (ls < le <= rs < re_):
        raise ValueError('invalid, overlapping, or reversed exposures')
    if not all(0 <= x <= 1 for x in (la, ra, tau)):
        raise ValueError('aperture/threshold outside [0,1]')
    g = rs - le + gextra
    e1 = le - ls + lextra
    e2 = re_ - rs + rextra
    lhs = la + ra - 2*tau
    rhs = v * (g + (e1 + e2)/2)
    margin = lhs - rhs
    details = {'strict_margin': str(margin),
               'measured_lower_sum_minus_thresholds': str(lhs),
               'maximum_lipschitz_budget': str(rhs),
               'dimensionless_ratio': str(lhs/rhs) if rhs > 0 else None,
               'gap_upper_ms': str(g),
               'exposure_upper_ms': [str(e1), str(e2)]}
    return result('MODEL_EXCLUDE_CONDITIONAL' if margin > 0 else
                  'ABSTAIN_HIDDEN_CLOSURE_POSSIBLE', **details)


def example():
    return {'experiment':'E002-608',
            'left':{'start_ms':-20,'end_ms':0,'aperture_lower':'0.5'},
            'right':{'start_ms':10,'end_ms':30,'aperture_lower':'0.5'},
            'threshold':'0.2','velocity_upper_per_ms':'0.02',
            'uncertainty_ms':{'gap_extra':0,'left_exposure_extra':0,'right_exposure_extra':0},
            'attestations':{k:True for k in ATTESTATIONS},
            'nuisances':{k:False for k in NUISANCES},
            'evidence_sha256':{k:'a'*64 for k in DIGESTS}}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', help='local custodian JSON; do not commit private measurements')
    p.add_argument('--example', action='store_true', help='synthetic falsification fixture')
    args = p.parse_args()
    if not args.input and not args.example:
        p.error('supply --input or --example')
    try:
        if args.example:
            d = example()
        else:
            with open(args.input, encoding='utf-8') as f:
                d = json.load(f)
        output = evaluate(d)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        output = result('ABSTAIN_INVALID_INPUT', reason=str(exc)[:100])
    print(json.dumps(output, sort_keys=True))


if __name__ == '__main__':
    main()
