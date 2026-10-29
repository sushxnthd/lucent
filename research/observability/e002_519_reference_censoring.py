#!/usr/bin/env python3
"""E002-519: one-sided, reference-censored human falsification intake.

Consumes owner-private adjudicated evidence, never raw images. A valid closure
witness can falsify a frozen exclusion. No input can certify no hidden closure.
The program cannot authenticate human independence or physical clock provenance.
"""
import argparse
import json
import math
from pathlib import Path

VERSION = 'E002-519-v1'
FLAGS = ('two_independent_raters', 'photometry_valid', 'clock_valid',
         'native_provenance_valid', 'nuisance_clear')
ANATOMY = {'CLOSED_WITNESS', 'OPEN_OBSERVED', 'UNKNOWN'}


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('INVALID_TIME')
    return float(value)


def evaluate(payload):
    if not isinstance(payload, dict) or payload.get('version') != VERSION:
        raise ValueError('INVALID_VERSION')
    gaps = payload.get('gaps')
    if not isinstance(gaps, list) or not gaps or len(gaps) > 20000:
        raise ValueError('INVALID_GAPS')
    output = []
    ids = set()
    for gap in gaps:
        if not isinstance(gap, dict) or not isinstance(gap.get('id'), str) or not gap['id'] or gap['id'] in ids:
            raise ValueError('INVALID_GAP_ID')
        ids.add(gap['id'])
        if gap.get('prediction') not in ('EXCLUDE', 'ABSTAIN'):
            raise ValueError('INVALID_PREDICTION')
        left = number(gap.get('left_end_max_ms'))
        right = number(gap.get('right_start_min_ms'))
        refs = gap.get('references')
        if not isinstance(refs, list) or len(refs) > 20000:
            raise ValueError('INVALID_REFERENCES')
        seen_refs = set()
        witness = None
        ambiguous = False
        for ref in refs:
            if not isinstance(ref, dict) or not isinstance(ref.get('id'), str) or not ref['id'] or ref['id'] in seen_refs:
                raise ValueError('INVALID_REFERENCE_ID')
            seen_refs.add(ref['id'])
            s = number(ref.get('start_min_ms'))
            e = number(ref.get('end_max_ms'))
            if e <= s or ref.get('anatomy') not in ANATOMY:
                raise ValueError('INVALID_REFERENCE_RECORD')
            if any(not isinstance(ref.get(k), bool) for k in FLAGS):
                raise ValueError('INVALID_REFERENCE_FLAGS')
            qualified = all(ref[k] for k in FLAGS)
            if ref['anatomy'] == 'UNKNOWN' or not qualified:
                ambiguous = True
            if (gap['prediction'] == 'EXCLUDE' and right > left
                and ref['anatomy'] == 'CLOSED_WITNESS' and qualified
                and s > left and e < right):
                witness = ref['id']
        if gap['prediction'] != 'EXCLUDE' or right <= left:
            decision = 'NOT_TESTABLE'
        elif witness is not None:
            decision = 'FALSIFIED_BY_REFERENCE_WITNESS'
        elif not refs or ambiguous:
            decision = 'UNKNOWN'
        else:
            decision = 'REFERENCE_CENSORED_NOT_FALSIFIED'
        output.append({'gap_id': gap['id'], 'decision': decision,
                       'witness_reference_id': witness if decision == 'FALSIFIED_BY_REFERENCE_WITNESS' else None})
    counts = {d: sum(x['decision'] == d for x in output) for d in
              ('FALSIFIED_BY_REFERENCE_WITNESS', 'REFERENCE_CENSORED_NOT_FALSIFIED', 'UNKNOWN', 'NOT_TESTABLE')}
    return {'version': VERSION, 'decisions': output, 'counts': counts,
            'verified_no_hidden_closure': False, 'physical_reference_authenticated_by_code': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Input and output must be different files')
    try:
        result = evaluate(json.loads(args.input.read_text(encoding='utf-8')))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        parser.error('FAIL_CLOSED: ' + str(exc))
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
