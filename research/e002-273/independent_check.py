#!/usr/bin/env python3
"""Independent fail-closed evidence checker; not a human physiology validator."""
import copy
import json
from pathlib import Path

def verify(r):
    assert r['run'] == 'E002-273'
    assert r['source'] == '10.5281/zenodo.19408373'
    assert r['decision'] == 'REJECT_FOR_RGB_WAVEFORM_CERTIFICATION_PENDING_RAW_RGB_PROOF'
    assert r['human_waveform_evaluated'] is False
    assert r['raw_rgb_eye_frames_verified'] is False
    assert r['archive_bytes_verified'] is False
    assert r['archive_member_listing_verified'] is False
    assert r['clock_alignment_verified'] is False
    assert r['source_only_excludes_rgb_archive_members'] is False
    assert r['wildcard_nonexclusion'] is True
    assert all(r['wildcard_probe'].values())
    assert r['documented_v2_repaired_sidecars'] == 91
    assert r['documented_v2_forced_surrogate_sidecars'] == 22
    assert r['documented_v2_affected_subjects'] == 24
    if r['upstream_source_bytes_verified']:
        assert r['source_provenance_status'] == 'PINNED_BLOBS_VERIFIED'
    else:
        assert r['source_provenance_status'] != 'PINNED_BLOBS_VERIFIED'
    return True

if __name__ == '__main__':
    r = json.loads(Path(__file__).with_name('RESULTS.json').read_text())
    verify(r)
    print('PASS: provenance classification and fail-closed gates')
    for field, mutation in [('raw_rgb_eye_frames_verified', True),
                            ('source_only_excludes_rgb_archive_members', True),
                            ('decision', 'ADMIT')]:
        bad = copy.deepcopy(r)
        bad[field] = mutation
        try:
            verify(bad)
        except AssertionError:
            print('PASS: mutation rejected:', field)
        else:
            raise AssertionError('MUTATION_ESCAPED:' + field)
