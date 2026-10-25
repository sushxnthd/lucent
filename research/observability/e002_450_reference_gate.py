#!/usr/bin/env python3
"""E002-450: conservative human-reference quality gate; never physical certification.

Consumes the PRIVATE E002-448 master and two private, independent rater exports.
Produces counts only, with no frame indices, view IDs, private key or coordinates.
"""
import argparse
import json
import math
from pathlib import Path

from e002_448_blind_annotation import aperture, FLAGS

THRESHOLD = 0.03  # Frozen E002-448 threshold, not retuned on S19.


def _base(n_views, n_unique, n_medium, n_control):
    return {
        'experiment': 'E002-450', 'source_experiment': 'E002-448',
        'pilot': 'S19', 'total_blinded_views': n_views,
        'total_unique_frames': n_unique, 'candidate_medium_pairs': n_medium,
        'candidate_short_pairs': n_control,
        'rater1_submitted_views': 0, 'rater2_submitted_views': 0,
        'rater1_explicit_abstentions': 0, 'rater2_explicit_abstentions': 0,
        'rater1_invalid_geometry': 0, 'rater2_invalid_geometry': 0,
        'rater_repeat_failure_frames': 0, 'between_rater_failure_frames': 0,
        'eligible_consensus_frames': 0, 'eligible_medium_pairs': 0,
        'eligible_short_pairs': 0, 'annotation_status': 'NOT_EVALUABLE',
        'physical_timing_authenticated': False,
        'anatomical_scale_authenticated': False,
        'physiological_velocity_cap_established': False,
        'e002_371_physical_validation': 'NOT_ESTABLISHED',
        'product_claim': 'ABSTAIN_UNCALIBRATED',
        'physical_release_authorized': False,
    }


def _parse_rater(doc, expected_ids):
    if not isinstance(doc, dict) or not isinstance(doc.get('rater_id'), str) or not doc['rater_id'].strip():
        raise ValueError('nonempty rater identity required')
    rows = doc.get('annotations')
    if not isinstance(rows, list):
        raise ValueError('annotation list required')
    parsed = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('view_id'), str):
            raise ValueError('malformed annotation')
        vid = row['view_id']
        if vid not in expected_ids or vid in parsed:
            raise ValueError('unknown or duplicate view ID')
        status = row.get('status')
        flags = row.get('flags', [])
        if status not in ('valid', 'abstain') or not isinstance(flags, list) or any(f not in FLAGS for f in flags):
            raise ValueError('invalid annotation status or nuisance flags')
        if status == 'abstain' and not flags:
            raise ValueError('abstention requires an explicit reason')
        if status == 'valid' and flags:
            raise ValueError('valid annotation cannot have nuisance flags')
        parsed[vid] = row
    return parsed


def assess(master, r1, r2):
    if not isinstance(master, dict) or master.get('experiment') != 'E002-448' or master.get('pilot') != 'S19':
        raise ValueError('expected private frozen S19 master')
    views = master.get('views')
    if not isinstance(views, list) or not views:
        raise ValueError('nonempty private master views required')
    ids = set()
    by_frame = {}
    for view in views:
        if not isinstance(view, dict) or not isinstance(view.get('view_id'), str) or not view['view_id']:
            raise ValueError('invalid master view')
        vid, idx = view['view_id'], view.get('frame_index')
        if vid in ids or type(idx) is not int or idx < 0:
            raise ValueError('duplicate view or invalid frame index')
        ids.add(vid)
        by_frame.setdefault(idx, []).append(vid)
    medium = master.get('medium_intervals')
    control = master.get('control_intervals')
    if not isinstance(medium, list) or not isinstance(control, list) or not medium or not control:
        raise ValueError('missing candidate strata')
    if (any(type(i) is not int or i <= 0 for i in medium + control)
            or len(set(medium + control)) != len(medium + control)
            or any(i - 1 not in by_frame or i not in by_frame for i in medium + control)):
        raise ValueError('invalid candidate intervals or missing frame mapping')
    out = _base(len(views), len(by_frame), len(medium), len(control))
    if r1 is None or r2 is None:
        out['annotation_status'] = 'NOT_EVALUABLE_NO_INDEPENDENT_RATERS'
        return out
    if not isinstance(r1, dict) or not isinstance(r2, dict):
        raise ValueError('rater documents required')
    a = _parse_rater(r1, ids)
    b = _parse_rater(r2, ids)
    if r1['rater_id'].strip() == r2['rater_id'].strip():
        raise ValueError('distinct rater identities required')
    out['rater1_submitted_views'] = len(a)
    out['rater2_submitted_views'] = len(b)
    if set(a) != ids or set(b) != ids:
        out['annotation_status'] = 'NOT_EVALUABLE_INCOMPLETE'
        return out
    measures = []
    for n, rows in enumerate((a, b), 1):
        vals = {}
        for vid, row in rows.items():
            if row['status'] == 'abstain':
                out[f'rater{n}_explicit_abstentions'] += 1
                vals[vid] = None
            else:
                val = aperture(row)
                if val is None or not math.isfinite(val):
                    out[f'rater{n}_invalid_geometry'] += 1
                    vals[vid] = None
                else:
                    vals[vid] = val
        measures.append(vals)
    good_frames = set()
    for idx, frame_views in by_frame.items():
        repeat_bad = False
        for vals in measures:
            z = [vals[v] for v in frame_views]
            if any(x is None for x in z) or max(z) - min(z) > THRESHOLD + 1e-12:
                repeat_bad = True
        if repeat_bad:
            if len(frame_views) > 1:
                out['rater_repeat_failure_frames'] += 1
            continue
        if any(abs(measures[0][v] - measures[1][v]) > THRESHOLD + 1e-12 for v in frame_views):
            out['between_rater_failure_frames'] += 1
            continue
        good_frames.add(idx)
    out['eligible_consensus_frames'] = len(good_frames)
    out['eligible_medium_pairs'] = sum(i - 1 in good_frames and i in good_frames for i in medium)
    out['eligible_short_pairs'] = sum(i - 1 in good_frames and i in good_frames for i in control)
    out['annotation_status'] = ('PILOT_IMAGE_SPACE_REFERENCE_ONLY' if good_frames
                                else 'ABSTAIN_REFERENCE_UNRESOLVED')
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--master', type=Path, required=True)
    p.add_argument('--rater1', type=Path, required=True)
    p.add_argument('--rater2', type=Path, required=True)
    p.add_argument('--summary', type=Path, required=True)
    a = p.parse_args()
    master, r1, r2 = [json.loads(f.read_text()) for f in (a.master, a.rater1, a.rater2)]
    result = assess(master, r1, r2)
    a.summary.parent.mkdir(parents=True, exist_ok=True)
    a.summary.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
