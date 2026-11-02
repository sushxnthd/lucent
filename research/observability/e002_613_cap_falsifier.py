#!/usr/bin/env python3
"""E002-613: prospective one-sided aperture-speed cap falsifier.

Exact rational arithmetic. Does NOT authenticate physical evidence, and does NOT
certify a velocity ceiling. Do not upload human data to GitHub/CI.
"""
import argparse
from fractions import Fraction
import json
import re

DECIMAL = re.compile(r'(?:0|[1-9][0-9]*)(?:\.[0-9]+)?\Z')
SHA = re.compile(r'[0-9a-f]{64}\Z')
ID = re.compile(r'[A-Za-z0-9_-]{1,64}\Z')
ATTEST = ('independent_anatomical_aperture_calibration',
          'independent_error_bounds', 'independent_time_bound',
          'paired_upper_lower_lid_geometry', 'participant_holdout_sealed')
NUISANCE = ('geometry', 'brightness', 'missingness', 'blur', 'gaze',
            'glasses', 'sampling', 'clock_error', 'occlusion', 'saturation',
            'rolling_shutter')
EVIDENCE = ('anatomy_calibration', 'timing_calibration', 'annotation',
            'precommitted_ceiling')


def decimal(v):
    if not isinstance(v, str) or not DECIMAL.fullmatch(v):
        raise ValueError('must be a nonnegative finite decimal string')
    return Fraction(v)


def answer(status, **extra):
    return {'experiment': 'E002-613', 'status': status,
            'evidence_tier': 'CONDITIONAL_FALSIFICATION_INSTRUMENT_ONLY',
            'human_data_used': False, 'physical_authentication': 'NOT_VERIFIED_BY_CODE',
            'velocity_ceiling_certified': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED', **extra}


def evaluate(d):
    if not isinstance(d, dict) or d.get('experiment') != 'E002-613' or not isinstance(d.get('pair_id'), str) or not ID.fullmatch(d['pair_id']):
        return answer('ABSTAIN_INVALID_SCHEMA')
    if d.get('units') != 'mm_and_seconds':
        return answer('ABSTAIN_UNIT_MISMATCH')
    if not isinstance(d.get('attestations'), dict) or not isinstance(d.get('nuisances'), dict) or not isinstance(d.get('evidence_sha256'), dict):
        return answer('ABSTAIN_MISSING_PREMISES')
    for k in ATTEST:
        if d['attestations'].get(k) is not True:
            return answer('ABSTAIN_UNVERIFIED_PREMISE', reason=k)
    for k in NUISANCE:
        if d['nuisances'].get(k) is not False:
            return answer('ABSTAIN_NUISANCE', reason=k)
    for k in EVIDENCE:
        v = d['evidence_sha256'].get(k)
        if not isinstance(v, str) or not SHA.fullmatch(v):
            return answer('ABSTAIN_MISSING_EVIDENCE_DIGEST', reason=k)
    try:
        z0, z1, e0, e1, dt, cap = [decimal(d[k]) for k in (
            'z0_mm', 'z1_mm', 'error0_mm', 'error1_mm',
            'dt_max_s', 'claimed_ceiling_mm_s')]
    except (KeyError, ValueError):
        return answer('ABSTAIN_INVALID_NUMERIC_INPUT')
    if dt <= 0:
        return answer('ABSTAIN_INVALID_TIME')
    # z0/z1, errors and cap are nonnegative by strict decimal parser.
    lower = max(Fraction(0), abs(z1 - z0) - e0 - e1) / dt
    status = ('CONDITIONAL_REJECT_CLAIMED_CEILING' if lower > cap
              else 'NO_CEILING_REJECTION_NOT_A_CERTIFICATE')
    return answer(status, lower_speed_mm_s=str(lower),
                  claimed_ceiling_mm_s=str(cap),
                  inference='ONE_SIDED_ONLY; observed intervals cannot prove a global speed ceiling')


def synthetic():
    return {'experiment': 'E002-613', 'pair_id': 'synthetic-001',
            'units': 'mm_and_seconds', 'z0_mm': '8.0', 'z1_mm': '7.5',
            'error0_mm': '0.05', 'error1_mm': '0.05',
            'dt_max_s': '0.0025', 'claimed_ceiling_mm_s': '150',
            'attestations': {k: True for k in ATTEST},
            'nuisances': {k: False for k in NUISANCE},
            'evidence_sha256': {k: 'a' * 64 for k in EVIDENCE}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--input', help='private, authorized, deidentified interval JSON')
    g.add_argument('--synthetic-example', action='store_true')
    args = p.parse_args()
    if args.synthetic_example:
        d = synthetic()
    else:
        try:
            with open(args.input, encoding='utf8') as f:
                d = json.load(f)
        except (OSError, json.JSONDecodeError):
            print(json.dumps(answer('ABSTAIN_INVALID_INPUT'), sort_keys=True))
            return
    print(json.dumps(evaluate(d), sort_keys=True))


if __name__ == '__main__':
    main()
