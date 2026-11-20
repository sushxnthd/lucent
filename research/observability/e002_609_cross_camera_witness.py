#!/usr/bin/env python3
"""E002-609 prospective cross-camera falsification bridge.

Pure interval arithmetic. No camera/human evidence is authenticated by code.
Every result is research-only; no production absence-of-blink claims.
"""
import argparse
from fractions import Fraction
import json
import re

EVIDENCE = ('ordinary_clock_shutter', 'reference_clock_shutter',
            'linear_anatomy', 'reference_annotation', 'prediction_seal')
ATTEST = ('independent_clock_sync', 'both_shutters_physically_calibrated',
          'reference_linear_anatomy_calibrated', 'two_blinded_reviewers_adjudicated',
          'heldout_prediction_precommitted')
NUISANCE = ('geometry', 'brightness', 'missingness', 'blur', 'gaze',
            'glasses', 'sampling', 'clock_error', 'occlusion', 'saturation',
            'rolling_shutter')
DECIMAL = re.compile(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?\Z')
SHA = re.compile(r'[0-9a-f]{64}\Z')


def number(v):
    if isinstance(v, bool) or not isinstance(v, (str, int, float)):
        raise ValueError('not a decimal number')
    s = str(v)
    if not DECIMAL.fullmatch(s):
        raise ValueError('invalid finite decimal')
    return Fraction(s)


def output(status, **kw):
    return {'experiment': 'E002-609', 'status': status,
            'evidence_tier': 'CONDITIONAL_PHYSICAL_WITNESS_PROTOCOL_ONLY',
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED',
            'authentication': 'NOT_VERIFIED_BY_THIS_PROGRAM', **kw}


def evaluate(d):
    if not isinstance(d, dict) or d.get('experiment') != 'E002-609':
        return output('ABSTAIN_INVALID_SCHEMA')
    if not isinstance(d.get('gap_id'), str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', d['gap_id']):
        return output('ABSTAIN_INVALID_SCHEMA', reason='gap_id')
    if d.get('prediction') not in ('MODEL_EXCLUDE_CONDITIONAL', 'ABSTAIN_HIDDEN_CLOSURE_POSSIBLE'):
        return output('ABSTAIN_INVALID_SCHEMA', reason='prediction')
    if not isinstance(d.get('prediction_sha256'), str) or not SHA.fullmatch(d['prediction_sha256']):
        return output('ABSTAIN_UNVERIFIED_PREMISE', reason='prediction_sha256')
    for key in ('ordinary_gap', 'reference', 'attestations', 'nuisances', 'evidence_sha256'):
        if not isinstance(d.get(key), dict):
            return output('ABSTAIN_MISSING_INPUT', reason=key)
    for k in ATTEST:
        if d['attestations'].get(k) is not True:
            return output('ABSTAIN_UNVERIFIED_PREMISE', reason=k)
    for k in NUISANCE:
        if d['nuisances'].get(k) is not False:
            return output('ABSTAIN_NUISANCE', reason=k)
    for k in EVIDENCE:
        v = d['evidence_sha256'].get(k)
        if not isinstance(v, str) or not SHA.fullmatch(v):
            return output('ABSTAIN_MISSING_EVIDENCE_DIGEST', reason=k)
    if d['evidence_sha256']['prediction_seal'] != d['prediction_sha256']:
        return output('ABSTAIN_UNVERIFIED_PREMISE', reason='prediction_seal_mismatch')
    try:
        gap = d['ordinary_gap']; ref = d['reference']
        l = number(gap['left_end_latest_ms'])
        r = number(gap['right_start_earliest_ms'])
        a = number(ref['start_earliest_ms'])
        b = number(ref['end_latest_ms'])
        upper = number(ref['linear_aperture_upper'])
        tau = number(ref['threshold'])
    except (KeyError, ValueError):
        return output('ABSTAIN_INVALID_NUMERIC_INPUT')
    if not (l < r and a < b and 0 <= upper <= 1 and 0 <= tau <= 1):
        return output('ABSTAIN_INVALID_INTERVAL_OR_APERTURE')
    if not (l < a and b < r):
        return output('ABSTAIN_REFERENCE_NOT_STRICTLY_INSIDE_GAP')
    if upper > tau:
        return output('NO_REFERENCE_WITNESS', note='No witness is not proof of absence')
    if d['prediction'] == 'MODEL_EXCLUDE_CONDITIONAL':
        return output('WITNESS_CONTRADICTS_CONDITIONAL_EXCLUSION',
                      note='Review physical premises; mathematical theorem not automatically falsified')
    return output('HIDDEN_CLOSURE_WITNESS_CONDITIONAL',
                  note='Existential witness only; not closure throughout exposure')


def fixture():
    return {
        'experiment': 'E002-609', 'gap_id': 'synthetic-001',
        'prediction': 'MODEL_EXCLUDE_CONDITIONAL',
        'prediction_sha256': 'a' * 64,
        'ordinary_gap': {'left_end_latest_ms': '0', 'right_start_earliest_ms': '10'},
        'reference': {'start_earliest_ms': '3', 'end_latest_ms': '5',
                      'linear_aperture_upper': '0.15', 'threshold': '0.20'},
        'attestations': {k: True for k in ATTEST},
        'nuisances': {k: False for k in NUISANCE},
        'evidence_sha256': {k: ('a' if k == 'prediction_seal' else 'b') * 64 for k in EVIDENCE}
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='private deidentified prospective gap JSON')
    parser.add_argument('--synthetic-example', action='store_true')
    args = parser.parse_args()
    if not (args.input or args.synthetic_example) or (args.input and args.synthetic_example):
        parser.error('choose --input or --synthetic-example')
    if args.synthetic_example:
        d = fixture()
    else:
        try:
            with open(args.input, encoding='utf8') as f:
                d = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(json.dumps(output('ABSTAIN_INVALID_INPUT', reason=str(e)[:100]), sort_keys=True))
            return
    print(json.dumps(evaluate(d), sort_keys=True))


if __name__ == '__main__':
    main()
