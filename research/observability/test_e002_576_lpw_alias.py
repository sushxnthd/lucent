#!/usr/bin/env python3
"""Synthetic adversarial controls for E002-576. No human footage or ratings."""
import copy
import hashlib
import json
import unittest

from e002_576_lpw_alias import analyze


def digest(s):
    return hashlib.sha256(s.encode()).hexdigest()


def measured(gap, uncertainty=0.5):
    return {'frame': 0, 'upper_y': 10., 'lower_y': 10.+gap,
            'iris_diameter': 100., 'uncertainty_px': uncertainty, 'flags': []}


def blank(j):
    return {'frame': j, 'upper_y': None, 'lower_y': None,
            'iris_diameter': None, 'uncertainty_px': None, 'flags': ['BLUR']}


def fixture():
    videos, mapping, frames, ra, rb, calibrations = [], [], [], {}, {}, []
    for vi in range(33):
        participant = f'p{vi//3:02d}'
        video = f'v{vi:02d}'
        sha = digest(f'video-{vi}')
        videos.append({'participant_id': participant, 'video_id': video,
                       'video_sha256': sha, 'native_width': 320,
                       'native_height': 240})
        calibrations.append({'participant_id': participant, 'video_id': video,
                             'iris_diameter_error_px': 1.})
        for wi in range(10):
            i = vi*10+wi
            clip = f'clip_{i:04d}'
            start = wi*19
            mapping.append({'blind_clip': clip, 'participant_id': participant,
                            'video_id': video, 'video_sha256': sha,
                            'start_native_frame': start,
                            'native_frames': list(range(start, start+19)),
                            'candidate_windows': 10})
            ra[clip] = [blank(j) for j in range(19)]
            rb[clip] = [blank(j) for j in range(19)]
            for j in range(19):
                frames.append({'blind_clip': clip, 'participant_id': participant,
                               'video_id': video, 'native_frame_index': start+j,
                               'frame_in_clip': j,
                               'decoded_png_sha256': digest(f'{clip}-{j}')})
    owner = {'experiment': 'E002-574', 'evidence_tier': 'SELECTION_PLAN_ONLY',
             'window_count': 330, 'owner_mapping': mapping}
    audit = {'experiment': 'E002-575',
             'evidence_tier': 'SOURCE_BOUND_NATIVE_FRAME_PACKET_ONLY',
             'videos': videos, 'frames': frames}
    a = {'experiment': 'E002-574', 'rater': 'A', 'clips': ra}
    b = {'experiment': 'E002-574', 'rater': 'B', 'clips': rb}
    cal = {'experiment': 'E002-576', 'threshold': 0.20,
           'independently_validated': True, 'frozen_before_holdout': True,
           'external_reference_id': 'synthetic-test-only',
           'videos': calibrations}
    return owner, audit, a, b, cal


def set_measurement(r, clip, j, gap, uncertainty=0.5):
    f = measured(gap, uncertainty)
    f['frame'] = j
    r['clips'][clip][j] = f


class FrozenTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()

    def evaluate(self):
        return analyze(*self.data)

    def test_all_nuisance_abstains(self):
        r = self.evaluate()
        self.assertEqual(r['frame_states']['UNCERTAIN'], 6270)
        self.assertEqual(r['phase_positive_alias_pairs'], [0, 0, 0])
        self.assertFalse(r['zero_witness_excludes_hidden_closure'])

    def test_positive_alias_one_phase(self):
        _, _, a, b, _ = self.data
        for r in (a, b):
            for j, gap in [(0, 30), (1, 1), (3, 30)]:
                set_measurement(r, 'clip_0000', j, gap)
        result = self.evaluate()
        self.assertEqual(result['phase_positive_alias_pairs'], [1, 0, 0])
        self.assertEqual(result['windows_with_any_positive_alias'], 1)
        self.assertEqual(result['participants_with_any_positive_alias'], 1)
        self.assertFalse(result['physical_shutter_validated'])

    def test_open_endpoints_without_closed_interior_not_positive(self):
        _, _, a, b, _ = self.data
        for r in (a, b):
            for j in (0, 1, 3):
                set_measurement(r, 'clip_0000', j, 30)
        self.assertEqual(self.evaluate()['phase_positive_alias_pairs'], [0, 0, 0])

    def test_unmeasured_interior_not_imputed_closed(self):
        _, _, a, b, _ = self.data
        for r in (a, b):
            for j in (0, 3):
                set_measurement(r, 'clip_0000', j, 30)
        self.assertEqual(self.evaluate()['phase_positive_alias_pairs'], [0, 0, 0])

    def test_rater_disagreement_is_not_closed(self):
        _, _, a, b, _ = self.data
        set_measurement(a, 'clip_0000', 1, 30)
        set_measurement(b, 'clip_0000', 1, 1)
        self.assertEqual(self.evaluate()['frame_states']['DISAGREEMENT'], 1)

    def test_scale_uncertainty_kills_threshold_shortcut(self):
        _, _, a, b, cal = self.data
        cal['videos'][0]['iris_diameter_error_px'] = 10.
        for r in (a, b):
            set_measurement(r, 'clip_0000', 0, 20)
        self.assertEqual(self.evaluate()['frame_states']['OPEN'], 0)
        self.assertEqual(self.evaluate()['frame_states']['UNCERTAIN'], 6270)

    def test_zero_pixel_uncertainty_abstains(self):
        _, _, a, b, _ = self.data
        for r in (a, b):
            set_measurement(r, 'clip_0000', 0, 30, uncertainty=0)
        self.assertEqual(self.evaluate()['frame_states']['UNCERTAIN'], 6270)

    def test_missing_calibration_rejected(self):
        self.data[4]['videos'].pop()
        with self.assertRaisesRegex(ValueError, 'INCOMPLETE'):
            self.evaluate()

    def test_fake_calibration_flag_rejected(self):
        self.data[4]['independently_validated'] = False
        with self.assertRaisesRegex(ValueError, 'UNVERIFIED'):
            self.evaluate()

    def test_duplicate_source_frame_rejected(self):
        self.data[1]['frames'][1] = copy.deepcopy(self.data[1]['frames'][0])
        with self.assertRaisesRegex(ValueError, 'DUPLICATE'):
            self.evaluate()

    def test_wrong_native_frame_rejected(self):
        self.data[1]['frames'][0]['native_frame_index'] += 1
        with self.assertRaisesRegex(ValueError, 'SOURCE_FRAME_BINDING'):
            self.evaluate()

    def test_wrong_rater_identity_rejected(self):
        self.data[3]['rater'] = 'A'
        with self.assertRaisesRegex(ValueError, 'INVALID_BLINDED'):
            self.evaluate()

    def test_missing_clip_rejected(self):
        self.data[2]['clips'].pop('clip_0000')
        with self.assertRaisesRegex(ValueError, 'INVALID_BLINDED'):
            self.evaluate()

    def test_partial_unreviewed_is_not_human_measurement(self):
        self.data[2]['clips']['clip_0000'][0]['flags'] = ['UNREVIEWED']
        self.assertEqual(self.evaluate()['frame_states']['UNCERTAIN'], 6270)

    def test_no_private_identity_in_aggregate(self):
        r = self.evaluate()
        s = json.dumps(r)
        self.assertNotIn('clip_0000', s)
        self.assertNotIn('p00', s)
        self.assertNotIn('video_sha256', s)
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')

    def test_order_independent(self):
        before = self.evaluate()
        self.data[0]['owner_mapping'].reverse()
        self.data[1]['frames'].reverse()
        self.data[2]['clips'] = dict(reversed(list(self.data[2]['clips'].items())))
        self.assertEqual(self.evaluate(), before)


if __name__ == '__main__':
    unittest.main()
