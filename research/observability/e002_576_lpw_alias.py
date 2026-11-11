#!/usr/bin/env python3
"""E002-576: private two-rater LPW native-frame alias evaluator.

This is a conditional index-alias test, NOT camera/shutter/physiology validation.
Never commit human ratings, private source mappings, or image data.
"""
import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

HEX = re.compile(r'^[a-f0-9]{64}$')
CLIP = re.compile(r'^clip_[0-9]{4}$')
FLAGS = {'GAZE', 'GLASSES', 'BLUR', 'LIGHTING', 'OCCLUSION',
         'MISSING_ANATOMY', 'POOR_GEOMETRY', 'UNREVIEWED'}
THRESHOLD = 0.20
WINDOW = 19


def number(v):
    return type(v) in (int, float) and math.isfinite(v)


def read_private(path):
    p = Path(path)
    if p.is_symlink() or not p.is_file():
        raise ValueError('UNSAFE_INPUT')
    return json.loads(p.read_text(encoding='utf-8'))


def check_owner(owner, audit):
    if (owner.get('experiment') != 'E002-574' or
            owner.get('evidence_tier') != 'SELECTION_PLAN_ONLY' or
            owner.get('window_count') != 330):
        raise ValueError('WRONG_FROZEN_OWNER_PLAN')
    mapping = owner.get('owner_mapping')
    if not isinstance(mapping, list) or len(mapping) != 330:
        raise ValueError('WRONG_WINDOW_COUNT')
    if (audit.get('experiment') != 'E002-575' or
            audit.get('evidence_tier') != 'SOURCE_BOUND_NATIVE_FRAME_PACKET_ONLY'):
        raise ValueError('WRONG_SOURCE_AUDIT')
    video_info = {}
    for v in audit.get('videos', []):
        key = (v.get('participant_id'), v.get('video_id'))
        if key in video_info or not all(type(v.get(k)) is int and v[k] > 0
                                         for k in ('native_width', 'native_height')):
            raise ValueError('INVALID_VIDEO_GEOMETRY')
        if not isinstance(v.get('video_sha256'), str) or not HEX.fullmatch(v['video_sha256']):
            raise ValueError('INVALID_VIDEO_HASH')
        video_info[key] = v
    if len(video_info) != 33:
        raise ValueError('EXPECTED_33_HELDOUT_VIDEOS')
    mapping_by_clip, native_seen, by_video = {}, set(), Counter()
    for m in mapping:
        clip = m.get('blind_clip')
        key = (m.get('participant_id'), m.get('video_id'))
        start = m.get('start_native_frame')
        if (not isinstance(clip, str) or not CLIP.fullmatch(clip) or
                clip in mapping_by_clip or key not in video_info or
                type(start) is not int or start < 0 or start % WINDOW != 0 or
                m.get('native_frames') != list(range(start, start + WINDOW)) or
                m.get('video_sha256') != video_info[key]['video_sha256'] or
                type(m.get('candidate_windows')) is not int or m['candidate_windows'] < 10):
            raise ValueError('INVALID_FROZEN_MAPPING')
        for idx in m['native_frames']:
            if (key, idx) in native_seen:
                raise ValueError('OVERLAPPING_SOURCE_WINDOWS')
            native_seen.add((key, idx))
        mapping_by_clip[clip] = m
        by_video[key] += 1
    if (set(mapping_by_clip) != {f'clip_{i:04d}' for i in range(330)} or
            set(by_video) != set(video_info) or set(by_video.values()) != {10} or
            len({key[0] for key in video_info}) != 11):
        raise ValueError('PARTICIPANT_OR_WINDOW_SPLIT_FAILURE')
    frame_audit = {}
    for row in audit.get('frames', []):
        k = (row.get('blind_clip'), row.get('frame_in_clip'))
        if (k in frame_audit or k[0] not in mapping_by_clip or
                type(k[1]) is not int or not 0 <= k[1] < WINDOW):
            raise ValueError('DUPLICATE_OR_UNKNOWN_AUDIT_FRAME')
        m = mapping_by_clip[k[0]]
        if (row.get('participant_id') != m['participant_id'] or
                row.get('video_id') != m['video_id'] or
                row.get('native_frame_index') != m['native_frames'][k[1]] or
                not isinstance(row.get('decoded_png_sha256'), str) or
                not HEX.fullmatch(row['decoded_png_sha256'])):
            raise ValueError('SOURCE_FRAME_BINDING_MISMATCH')
        frame_audit[k] = row
    if len(frame_audit) != 330 * WINDOW:
        raise ValueError('MISSING_AUDITED_FRAMES')
    return mapping_by_clip, video_info


def check_calibration(cal, videos):
    if cal.get('experiment') != 'E002-576' or cal.get('threshold') != THRESHOLD:
        raise ValueError('WRONG_CALIBRATION_PROTOCOL')
    if cal.get('independently_validated') is not True or cal.get('frozen_before_holdout') is not True:
        raise ValueError('UNVERIFIED_SCALE_CALIBRATION')
    ref = cal.get('external_reference_id')
    if not isinstance(ref, str) or not 8 <= len(ref) <= 160:
        raise ValueError('MISSING_EXTERNAL_REFERENCE')
    rows = cal.get('videos')
    if not isinstance(rows, list):
        raise ValueError('MISSING_SCALE_BUDGETS')
    budgets = {}
    for row in rows:
        key = (row.get('participant_id'), row.get('video_id'))
        e = row.get('iris_diameter_error_px')
        if key not in videos or key in budgets or not number(e) or not 0 < e <= 30:
            raise ValueError('INVALID_INDEPENDENT_SCALE_BUDGET')
        budgets[key] = e
    if set(budgets) != set(videos):
        raise ValueError('INCOMPLETE_INDEPENDENT_SCALE_BUDGETS')
    return budgets


def check_rater(r, identity, clips):
    if (r.get('experiment') != 'E002-574' or r.get('rater') != identity or
            not isinstance(r.get('clips'), dict) or set(r['clips']) != set(clips)):
        raise ValueError('INVALID_BLINDED_RATER_EXPORT')
    for clip, frames in r['clips'].items():
        if not isinstance(frames, list) or len(frames) != WINDOW:
            raise ValueError('WRONG_RATER_FRAME_COUNT')
        for j, f in enumerate(frames):
            if (not isinstance(f, dict) or set(f) != {'frame', 'upper_y', 'lower_y',
                   'iris_diameter', 'uncertainty_px', 'flags'} or f['frame'] != j or
                    not isinstance(f['flags'], list) or len(f['flags']) != len(set(f['flags'])) or
                    any(flag not in FLAGS for flag in f['flags'])):
                raise ValueError('INVALID_RATER_FRAME_SCHEMA')
            if f['flags']:
                if any(f[x] is not None for x in ('upper_y', 'lower_y',
                                                 'iris_diameter', 'uncertainty_px')):
                    raise ValueError('NUISANCE_FRAME_WITH_MEASUREMENTS')
            elif any(not number(f[x]) for x in ('upper_y', 'lower_y',
                                                'iris_diameter', 'uncertainty_px')):
                raise ValueError('UNFLAGGED_INCOMPLETE_FRAME')


def interval(f, height, diameter_error):
    if f['flags']:
        return None
    u, l, d, e = (f[k] for k in ('upper_y', 'lower_y', 'iris_diameter', 'uncertainty_px'))
    if (not 0 <= u <= l <= height or not 0 < d <= height or
            not 0.5 <= e <= 30 or d <= diameter_error):
        return None
    return (max(0.0, l-u-2*e)/(d+diameter_error),
            max(0.0, l-u+2*e)/(d-diameter_error))


def classify(fa, fb, height, diameter_error):
    a, b = interval(fa, height, diameter_error), interval(fb, height, diameter_error)
    if a is None or b is None:
        return 'UNCERTAIN'
    if max(a[0], b[0]) > min(a[1], b[1]):
        return 'DISAGREEMENT'
    if a[1] <= THRESHOLD and b[1] <= THRESHOLD:
        return 'CLOSED'
    if a[0] > THRESHOLD and b[0] > THRESHOLD:
        return 'OPEN'
    return 'UNCERTAIN'


def analyze(owner, audit, rater_a, rater_b, calibration):
    mapping, videos = check_owner(owner, audit)
    budgets = check_calibration(calibration, videos)
    check_rater(rater_a, 'A', mapping)
    check_rater(rater_b, 'B', mapping)
    counts = Counter()
    phase_witnesses = [0, 0, 0]
    phase_eligible_pairs = [0, 0, 0]
    windows_positive = 0
    participants_positive = set()
    for clip in sorted(mapping):
        m = mapping[clip]
        key = (m['participant_id'], m['video_id'])
        height = videos[key]['native_height']
        states = []
        for a, b in zip(rater_a['clips'][clip], rater_b['clips'][clip]):
            state = classify(a, b, height, budgets[key])
            states.append(state)
            counts[state] += 1
        any_positive = False
        for phase in range(3):
            retained = list(range(phase, WINDOW, 3))
            for left, right in zip(retained, retained[1:]):
                if states[left] != 'OPEN' or states[right] != 'OPEN':
                    continue
                phase_eligible_pairs[phase] += 1
                if 'CLOSED' in states[left+1:right]:
                    phase_witnesses[phase] += 1
                    any_positive = True
        if any_positive:
            windows_positive += 1
            participants_positive.add(m['participant_id'])
    return {'experiment': 'E002-576',
            'evidence_tier': 'CONDITIONAL_NATIVE_FRAME_ALIAS_ONLY_OWNER_ASSERTED_CALIBRATION',
            'source_authenticity_independently_verified_by_tool': False,
            'rater_identity_independently_verified_by_tool': False,
            'physical_shutter_validated': False,
            'camera_clock_authenticated': False,
            'continuous_time_velocity_ceiling_certified': False,
            'frames': 330*WINDOW, 'windows': 330, 'heldout_participants': 11,
            'frame_states': {s: counts[s] for s in
                             ('OPEN', 'CLOSED', 'UNCERTAIN', 'DISAGREEMENT')},
            'phase_eligible_open_endpoint_pairs': phase_eligible_pairs,
            'phase_positive_alias_pairs': phase_witnesses,
            'windows_with_any_positive_alias': windows_positive,
            'participants_with_any_positive_alias': len(participants_positive),
            'zero_witness_excludes_hidden_closure': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for flag in ('owner', 'audit', 'rater-a', 'rater-b', 'calibration'):
        ap.add_argument('--'+flag, required=True)
    args = ap.parse_args()
    try:
        result = analyze(*(read_private(getattr(args, k)) for k in
                           ('owner', 'audit', 'rater_a', 'rater_b', 'calibration')))
        print(json.dumps(result, sort_keys=True))
    except Exception as exc:
        print(json.dumps({'experiment': 'E002-576', 'status': 'ABSTAIN',
                          'error_type': type(exc).__name__,
                          'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}))
        raise SystemExit(2)


if __name__ == '__main__':
    main()
