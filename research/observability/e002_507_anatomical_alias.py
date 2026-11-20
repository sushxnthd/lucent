#!/usr/bin/env python3
"""E002-507: frame-index-only dual-rater anatomical alias witness.

No source video is read, no timing is inferred, no product clearance is possible.
A positive is an observed *native-frame* closure missed by two sparse endpoints,
not a continuous-time or shutter-integrated physical closure certificate.
"""
import argparse
import json
import math
from pathlib import Path
from e002_492_anatomical_review import build_manifest

THRESHOLD = 0.10
STRIDE = 5
FROZEN_START = 3


def frozen_start(clip):
    if not isinstance(clip, str) or not clip.startswith('clip_') or len(clip) != 7:
        raise ValueError('INVALID_CLIP_ID')
    return FROZEN_START


def _finite(v):
    return type(v) in (float, int) and math.isfinite(v)


def classify(a, b, delta, threshold=THRESHOLD):
    """Agreement-only interval classification; disagreement/flags => UNKNOWN."""
    if not _finite(delta) or delta <= 0:
        raise ValueError('INVALID_IRIS_SCALE_DELTA')
    if not _finite(threshold) or not 0 < threshold < 1:
        raise ValueError('INVALID_THRESHOLD')
    intervals = []
    for f in (a, b):
        if not isinstance(f, dict) or not isinstance(f.get('flags'), list):
            return 'UNKNOWN'
        if f['flags']:
            return 'UNKNOWN'
        vals = [f.get(k) for k in ('upper_y', 'lower_y', 'iris_diameter', 'uncertainty_px')]
        if not all(_finite(v) for v in vals):
            return 'UNKNOWN'
        u, l, d, e = vals
        if not (0 <= u <= l <= 288 and 0 < d <= 288 and 0 <= e <= 30 and delta < d):
            return 'UNKNOWN'
        gap = l-u
        lo = max(0, gap-2*e)/(d+delta)
        hi = (gap+2*e)/(d-delta)
        intervals.append((lo, hi))
    # Both raters must independently certify the same side; shared bias still possible.
    if all(lo > threshold for lo, _ in intervals):
        return 'OPEN'
    if all(hi <= threshold for _, hi in intervals):
        return 'CLOSED'
    return 'UNKNOWN'


def evaluate(manifest, a, b, calibration):
    if manifest.get('experiment') != 'E002-492' or manifest.get('subject') != 'S01_CALIBRATION_ONLY':
        raise ValueError('WRONG_FROZEN_MANIFEST')
    if {a.get('rater'), b.get('rater')} != {'A', 'B'}:
        raise ValueError('WRONG_RATERS')
    if a.get('experiment') != 'E002-492' or b.get('experiment') != 'E002-492':
        raise ValueError('WRONG_RATER_EXPERIMENT')
    # E002-508: bind ratings to the exact previously frozen owner-only source map.
    # This is provenance validation, NOT proof of image-byte or human identity.
    if manifest != build_manifest():
        raise ValueError('NONCANONICAL_FROZEN_SOURCE_MANIFEST')
    clips = manifest.get('review_clips')
    if not isinstance(clips, list) or len(clips) != 20:
        raise ValueError('WRONG_CLIP_COUNT')
    ids = [c.get('clip') for c in clips]
    if len(set(ids)) != 20 or set(a.get('clips', {})) != set(ids) or set(b.get('clips', {})) != set(ids):
        raise ValueError('CLIP_SET_MISMATCH')
    if not isinstance(calibration, dict) or set(calibration) != set(ids):
        raise ValueError('IRIS_SCALE_CALIBRATION_REQUIRED_FOR_ALL_CLIPS')
    counts = {'windows': 0, 'endpoint_not_both_open': 0, 'eligible_open_endpoints': 0,
              'observed_interior_closed_witness': 0, 'no_observed_interior_closure': 0,
              'interior_unresolved': 0}
    for clip in sorted(ids):
        fa, fb = a['clips'][clip], b['clips'][clip]
        if not isinstance(fa, list) or not isinstance(fb, list) or len(fa) != 13 or len(fb) != 13:
            raise ValueError('FRAME_SET_MISMATCH')
        for j in range(13):
            if fa[j].get('frame') != j or fb[j].get('frame') != j:
                raise ValueError('FRAME_ORDER_MISMATCH')
        delta = calibration[clip]
        if not _finite(delta) or delta <= 0:
            raise ValueError('INVALID_IRIS_SCALE_DELTA')
        start = frozen_start(clip)
        states = [classify(fa[j], fb[j], delta) for j in range(start, start+STRIDE+1)]
        counts['windows'] += 1
        if states[0] != 'OPEN' or states[-1] != 'OPEN':
            counts['endpoint_not_both_open'] += 1
        else:
            counts['eligible_open_endpoints'] += 1
            interior = states[1:-1]
            if 'CLOSED' in interior:
                counts['observed_interior_closed_witness'] += 1
            elif 'UNKNOWN' in interior:
                counts['interior_unresolved'] += 1
            else:
                counts['no_observed_interior_closure'] += 1
    assert counts['windows'] == counts['endpoint_not_both_open'] + counts['eligible_open_endpoints']
    assert counts['eligible_open_endpoints'] == (counts['observed_interior_closed_witness']
              + counts['interior_unresolved'] + counts['no_observed_interior_closure'])
    return {'experiment': 'E002-507', 'evidence_tier': 'FRAME_INDEX_ANATOMY_ONLY_IF_INDEPENDENT_REAL_RATINGS',
            'sampling': 'one fixed native-frame window 3..8 per E002-492 clip; 20 windows; no FPS conversion',
            'threshold': THRESHOLD, **counts,
            'continuous_time_speed_certified': False, 'camera_timing_authenticated': False,
            'human_rater_independence_authenticated_by_code': False,
            'iris_scale_calibration_authenticated_by_code': False,
            'physical_hidden_closure_certified': False, 'product': 'ABSTAIN_UNCALIBRATED',
            'release': 'BLOCKED'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for flag in ('manifest', 'rater-a', 'rater-b', 'iris-scale-calibration', 'aggregate'):
        ap.add_argument('--'+flag, required=True)
    x = ap.parse_args()
    load = lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
    out = evaluate(load(x.manifest), load(x.rater_a), load(x.rater_b),
                   load(x.iris_scale_calibration))
    dest = Path(x.aggregate)
    if dest.exists():
        raise ValueError('REFUSE_OVERWRITE_PRIVATE_AGGREGATE')
    dest.write_text(json.dumps(out, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(out, sort_keys=True))


if __name__ == '__main__':
    main()
