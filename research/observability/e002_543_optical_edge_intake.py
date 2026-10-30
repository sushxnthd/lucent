#!/usr/bin/env python3
"""E002-543: owner-private, noncertifying optical edge challenge intake.

The input contains owner-supplied timing and photometry; this program does not
authenticate physical sources or establish eyelid physiology. No raw input is
copied to output. Frozen protocol: E002_543_FROZEN.md.
"""
from __future__ import annotations
import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

SCHEMA = 'E002-543-v1'
SESSION_KEYS = frozenset(('schema', 'session_id', 'calibration_id',
                          'prelabel_commitment', 'optical_trace_sha256',
                          'native_capture_sha256', 'photodiode_sample_rate_hz',
                          'sync_error_ms', 'trials'))
TRIAL_KEYS = frozenset(('trial_id', 'frame_id', 'row_id', 'partition',
                        'pulse_onset_ms', 'pulse_offset_ms',
                        'shutter_start_ms', 'shutter_end_ms', 'control_roi',
                        'flash_roi', 'noise_upper', 'quality'))
QUALITY_KEYS = frozenset(('native_identity', 'independent_photodiode',
                          'paired_control', 'fixed_camera_settings',
                          'no_clipping', 'no_motion', 'no_occlusion',
                          'stable_illumination', 'blur_characterized',
                          'no_missing_frames'))
DECISIONS = ('TRANSFER_FALSIFICATION_CANDIDATE',
             'NO_FALSIFICATION_CENSORED', 'ABSTAIN_NOT_OUTSIDE',
             'ABSTAIN_QUALITY')
HEX64 = re.compile(r'^[0-9a-f]{64}$')


def finite_number(v):
    return type(v) in (int, float) and math.isfinite(v)


def interval(v):
    if type(v) is not list or len(v) != 2 or not all(finite_number(x) for x in v):
        return None
    lo, hi = v
    return (lo, hi) if lo <= hi else None


def invalid_result(reason):
    return {'schema': SCHEMA, 'decision': 'ABSTAIN_INVALID_SESSION',
            'reason': reason, 'evidence_tier': 'OWNER_SUPPLIED_OPTICAL_RECORDS_UNAUTHENTICATED',
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def evaluate(payload):
    if type(payload) is not dict or set(payload) != SESSION_KEYS:
        return invalid_result('session_schema')
    if payload['schema'] != SCHEMA:
        return invalid_result('version')
    if any(type(payload[k]) is not str or not payload[k].strip()
           for k in ('session_id', 'calibration_id')):
        return invalid_result('session_identity')
    if any(type(payload[k]) is not str or HEX64.fullmatch(payload[k]) is None
           for k in ('prelabel_commitment', 'optical_trace_sha256',
                     'native_capture_sha256')):
        return invalid_result('unverified_digest_format')
    rate, sync = payload['photodiode_sample_rate_hz'], payload['sync_error_ms']
    if not finite_number(rate) or rate <= 0 or not finite_number(sync) or sync < 0:
        return invalid_result('clock_schema')
    trials = payload['trials']
    if type(trials) is not list or not trials:
        return invalid_result('empty_or_invalid_trials')
    ids, frame_rows = set(), set()
    for t in trials:
        if type(t) is not dict or set(t) != TRIAL_KEYS:
            return invalid_result('trial_schema')
        q = t['quality']
        if type(q) is not dict or set(q) != QUALITY_KEYS or any(type(v) is not bool for v in q.values()):
            return invalid_result('quality_schema')
        if type(t['trial_id']) is not str or not t['trial_id'].strip():
            return invalid_result('trial_identity')
        if type(t['frame_id']) is not str or not t['frame_id'].strip():
            return invalid_result('frame_identity')
        if type(t['row_id']) is not int or t['row_id'] < 0:
            return invalid_result('row_identity')
        key = (t['frame_id'], t['row_id'])
        if t['trial_id'] in ids or key in frame_rows:
            return invalid_result('duplicate_identity')
        ids.add(t['trial_id'])
        frame_rows.add(key)
        if t['partition'] != 'heldout':
            return invalid_result('unsealed_partition')
    counts = Counter({k: 0 for k in DECISIONS})
    for t in trials:
        pulse_on, pulse_off = interval(t['pulse_onset_ms']), interval(t['pulse_offset_ms'])
        shutter_on, shutter_off = interval(t['shutter_start_ms']), interval(t['shutter_end_ms'])
        values = (t['control_roi'], t['flash_roi'], t['noise_upper'])
        if (None in (pulse_on, pulse_off, shutter_on, shutter_off)
                or pulse_on[1] >= pulse_off[0] or shutter_on[1] >= shutter_off[0]
                or not all(finite_number(v) for v in values)
                or not (0 <= values[0] <= 1 and 0 <= values[1] <= 1 and values[2] >= 0)
                or not all(t['quality'].values())):
            counts['ABSTAIN_QUALITY'] += 1
            continue
        # Expand optical pulse uncertainty by the independently bounded
        # photodiode/camera clock alignment error. Strict separation only.
        before = pulse_off[1] + sync < shutter_on[0]
        after = pulse_on[0] - sync > shutter_off[1]
        if not (before or after):
            counts['ABSTAIN_NOT_OUTSIDE'] += 1
        elif abs(t['flash_roi'] - t['control_roi']) > t['noise_upper']:
            counts['TRANSFER_FALSIFICATION_CANDIDATE'] += 1
        else:
            counts['NO_FALSIFICATION_CENSORED'] += 1
    return {'schema': SCHEMA, 'decision': 'AGGREGATE_NONCERTIFYING',
            'total_trials': len(trials), 'counts': dict(counts),
            'evidence_tier': 'OWNER_SUPPLIED_OPTICAL_RECORDS_UNAUTHENTICATED',
            'physical_source_authenticated': False,
            'human_anatomical_validation': False,
            'shutter_support_certified': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON object key')
        result[key] = value
    return result


def load_private(path):
    with Path(path).open('r', encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=no_duplicate_keys,
                         parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON number')))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True, help='owner-private optical capture manifest JSON')
    p.add_argument('--output', default='-', help='aggregate JSON only; default stdout')
    args = p.parse_args()
    try:
        result = evaluate(load_private(args.input))
    except (ValueError, TypeError, OSError, UnicodeError, json.JSONDecodeError):
        result = invalid_result('unreadable_or_invalid_json')
    out = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.output == '-':
        print(out, end='')
    else:
        Path(args.output).write_text(out, encoding='utf-8')


if __name__ == '__main__':
    main()
