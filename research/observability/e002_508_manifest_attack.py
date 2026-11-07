#!/usr/bin/env python3
"""E002-508: frozen synthetic manifest-substitution attack; never human evidence."""
import argparse
import copy
import json
from e002_492_anatomical_review import build_manifest, template
from e002_507_anatomical_alias import evaluate

def _frame(j, closed=False):
    return {'frame': j, 'upper_y': 100, 'lower_y': 100 if closed else 120,
            'iris_diameter': 100, 'uncertainty_px': 0, 'flags': []}

def fixture():
    m = build_manifest()
    a, b = template(m, 'A'), template(m, 'B')
    for x in (a, b):
        for clip in x['clips']:
            x['clips'][clip] = [_frame(j, clip == 'clip_00' and j == 5)
                                for j in range(13)]
    d = {c['clip']: 1 for c in m['review_clips']}
    return m, a, b, d

def mutations(m):
    variants = {}
    x = copy.deepcopy(m)
    x['review_clips'][0]['native_frames'][5] += 1000
    variants['source_frame_substitution'] = x
    x = copy.deepcopy(m)
    x['review_clips'][0]['center_native_frame'] += 1
    variants['center_shift'] = x
    x = copy.deepcopy(m)
    x['review_clips'][0]['candidate'] = not x['review_clips'][0]['candidate']
    variants['candidate_bit_flip'] = x
    x = copy.deepcopy(m)
    x['untrusted_annotation_mapping'] = True
    variants['unauthorized_owner_key'] = x
    return variants

def run(expect):
    m, a, b, d = fixture()
    baseline = evaluate(m, a, b, d)
    assert baseline['observed_interior_closed_witness'] == 1
    assert baseline['product'] == 'ABSTAIN_UNCALIBRATED' and baseline['release'] == 'BLOCKED'
    assert evaluate(copy.deepcopy(m), a, b, d)['observed_interior_closed_witness'] == 1
    accepted, rejected = [], []
    for name, tampered in mutations(m).items():
        try:
            got = evaluate(tampered, a, b, d)
            assert got['observed_interior_closed_witness'] == 1
            assert got['release'] == 'BLOCKED'
            accepted.append(name)
        except ValueError as e:
            if str(e) != 'NONCANONICAL_FROZEN_SOURCE_MANIFEST':
                raise
            rejected.append(name)
    if expect == 'vulnerable':
        assert len(accepted) == 4 and not rejected, (accepted, rejected)
    elif expect == 'fixed':
        assert not accepted and len(rejected) == 4, (accepted, rejected)
    else:
        raise ValueError('UNKNOWN_EXPECTATION')
    result = {'experiment': 'E002-508', 'evidence': 'SYNTHETIC_MANIFEST_PROVENANCE_ONLY',
              'expectation': expect, 'canonical_fixture_witnesses': 1,
              'substitutions_accepted': accepted, 'substitutions_rejected': rejected,
              'human_ratings': 0, 'physical_validation': False,
              'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}
    print(json.dumps(result, sort_keys=True))
    return result

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--expect', choices=['vulnerable', 'fixed'], required=True)
    run(ap.parse_args().expect)
