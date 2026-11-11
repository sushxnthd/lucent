"""E002-555: conservative two-rater video annotation audit.

This does NOT validate eyelid physiology or hardware shutter timing. No private
coordinates or participant IDs are emitted in aggregate results.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

SCHEMA = 'lucent-e002-555-v1'
LABELS = {'closed', 'open', 'uncertain'}
FLAGS = ('geometry', 'blur', 'brightness', 'gaze', 'glasses', 'occlusion', 'missingness')

class InvalidPacket(ValueError):
    pass

def _assert(ok: bool, message: str):
    if not ok:
        raise InvalidPacket(message)

def _nonempty(v):
    return isinstance(v, str) and 0 < len(v) <= 128 and not any(ord(c) < 32 for c in v)

def _point(v):
    return isinstance(v, list) and len(v) == 2 and all(
        isinstance(x, (float, int)) and not isinstance(x, bool)
        and math.isfinite(x) and 0 <= x <= 1 for x in v)

def _load(raw):
    _assert(isinstance(raw, dict), 'packet must be an object')
    _assert(raw.get('schema') == SCHEMA, 'schema mismatch')
    _assert(raw.get('timing_type') == 'browser_presentation_only', 'unverified timing type')
    _assert(_nonempty(raw.get('packet_id')), 'invalid packet_id')
    _assert(_nonempty(raw.get('rater_id')), 'invalid rater_id')
    h = raw.get('video_sha256')
    _assert(isinstance(h, str) and len(h) == 64 and all(c in '0123456789abcdef' for c in h), 'invalid video_sha256')
    a = raw.get('annotations')
    _assert(isinstance(a, list) and 0 < len(a) <= 100000, 'empty or excessive annotations')
    out = {}
    for row in a:
        _assert(isinstance(row, dict), 'invalid annotation')
        sid = row.get('sample_id')
        _assert(_nonempty(sid) and sid not in out, 'invalid or duplicate sample_id')
        t = row.get('presentation_time_s')
        _assert(isinstance(t, (int, float)) and not isinstance(t, bool) and math.isfinite(t) and t >= 0,
                'invalid presentation timestamp')
        _assert(row.get('label') in LABELS, 'invalid closure label')
        _assert(_point(row.get('upper')) and _point(row.get('lower')), 'invalid normalized landmark coordinates')
        flags = row.get('flags')
        _assert(isinstance(flags, dict) and set(flags) == set(FLAGS)
                and all(type(flags[k]) is bool for k in FLAGS), 'invalid nuisance flags')
        sep = row.get('vertical_separation_fraction')
        expected = abs(row['upper'][1] - row['lower'][1])
        _assert(isinstance(sep, (int, float)) and not isinstance(sep, bool) and math.isfinite(sep)
                and abs(sep-expected) <= 1e-8, 'landmark separation mismatch')
        out[sid] = row
    return out

def audit(a, b):
    a_rows, b_rows = _load(a), _load(b)
    _assert(a['video_sha256'] == b['video_sha256'], 'source video digest mismatch')
    _assert(a['packet_id'] == b['packet_id'], 'packet mismatch')
    _assert(a['rater_id'] != b['rater_id'], 'same declared rater')
    _assert(set(a_rows) == set(b_rows), 'sample sets mismatch')
    counts = {'RATER_CONCORDANT_UNCALIBRATED': 0,
              'REFERENCE_NEGATIVE_CENSORED': 0,
              'CENSORED': 0}
    for sid in a_rows:
        x, y = a_rows[sid], b_rows[sid]
        # Browser presentation timestamps are not camera hardware times.
        _assert(abs(x['presentation_time_s'] - y['presentation_time_s']) <= 1e-6,
                'presentation timestamp mismatch')
        if (x['label'] != y['label'] or x['label'] == 'uncertain'
                or any(x['flags'][k] or y['flags'][k] for k in FLAGS)):
            counts['CENSORED'] += 1
        elif x['label'] == 'closed':
            counts['RATER_CONCORDANT_UNCALIBRATED'] += 1
        else:
            counts['REFERENCE_NEGATIVE_CENSORED'] += 1
    return {
        'schema': 'lucent-e002-555-audit-v1',
        'sample_count': len(a_rows),
        'counts': counts,
        'video_hashes_match': True,
        'presentation_timing_only': True,
        'external_rater_independence_unverified': True,
        'anatomical_transfer_uncalibrated': True,
        'human_physical_validation': False,
        'certified_exclusions': 0,
        'release': 'BLOCKED',
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rater_a', type=Path)
    parser.add_argument('rater_b', type=Path)
    args = parser.parse_args()
    try:
        result = audit(json.loads(args.rater_a.read_text()), json.loads(args.rater_b.read_text()))
    except (InvalidPacket, ValueError, OSError) as exc:
        parser.exit(2, 'E002-555 FAIL_CLOSED: ' + str(exc) + '\n')
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
