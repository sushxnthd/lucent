import copy
import json
import tempfile
import unittest
from pathlib import Path

from e002_543_optical_edge_intake import evaluate, load_private


def trial(name, frame, *, start=(0, .1), end=(.9, 1), shutter_start=(3, 3.1), shutter_end=(5, 5.1), flash=.8, control=.2, noise=.05):
    return {'trial_id': name, 'frame_id': frame, 'row_id': 0, 'partition': 'heldout',
            'pulse_onset_ms': list(start), 'pulse_offset_ms': list(end),
            'shutter_start_ms': list(shutter_start), 'shutter_end_ms': list(shutter_end),
            'control_roi': control, 'flash_roi': flash, 'noise_upper': noise,
            'quality': {k: True for k in (
                'native_identity', 'independent_photodiode', 'paired_control',
                'fixed_camera_settings', 'no_clipping', 'no_motion', 'no_occlusion',
                'stable_illumination', 'blur_characterized', 'no_missing_frames')}}


def manifest():
    return {'schema': 'E002-543-v1', 'session_id': 'private-synthetic',
            'calibration_id': 'synthetic-calibration', 'prelabel_commitment': 'a' * 64,
            'optical_trace_sha256': 'b' * 64, 'native_capture_sha256': 'c' * 64,
            'photodiode_sample_rate_hz': 10000, 'sync_error_ms': .2,
            'trials': [trial('before', 'frame1'),
                       trial('after', 'frame2', start=(7, 7.1), end=(8, 8.1), flash=.23),
                       trial('overlap', 'frame3', start=(4, 4.1), end=(4.5, 4.6))]}


class OpticalEdgeIntakeTests(unittest.TestCase):
    def setUp(self):
        self.p = manifest()

    def test_frozen_three_outcomes(self):
        r = evaluate(self.p)
        self.assertEqual(r['decision'], 'AGGREGATE_NONCERTIFYING')
        self.assertEqual(r['total_trials'], 3)
        self.assertEqual(r['counts']['TRANSFER_FALSIFICATION_CANDIDATE'], 1)
        self.assertEqual(r['counts']['NO_FALSIFICATION_CENSORED'], 1)
        self.assertEqual(r['counts']['ABSTAIN_NOT_OUTSIDE'], 1)
        self.assertEqual(r['counts']['ABSTAIN_QUALITY'], 0)

    def test_clock_uncertainty_reverses_candidate(self):
        self.p['sync_error_ms'] = 2.1
        self.assertEqual(evaluate(self.p)['counts']['TRANSFER_FALSIFICATION_CANDIDATE'], 0)
        self.assertEqual(evaluate(self.p)['counts']['ABSTAIN_NOT_OUTSIDE'], 3)

    def test_equal_boundary_abstains(self):
        self.p['sync_error_ms'] = 0
        self.p['trials'][0]['pulse_offset_ms'] = [2.9, 3]
        self.assertEqual(evaluate(self.p)['counts']['ABSTAIN_NOT_OUTSIDE'], 2)

    def test_quality_flags_abstain(self):
        for key in self.p['trials'][0]['quality']:
            p = copy.deepcopy(self.p)
            p['trials'][0]['quality'][key] = False
            self.assertEqual(evaluate(p)['counts']['ABSTAIN_QUALITY'], 1, key)

    def test_duplicate_ids_reject_session(self):
        self.p['trials'][1]['trial_id'] = 'before'
        self.assertEqual(evaluate(self.p)['decision'], 'ABSTAIN_INVALID_SESSION')

    def test_duplicate_frame_row_reject_session(self):
        self.p['trials'][1]['frame_id'] = 'frame1'
        self.assertEqual(evaluate(self.p)['decision'], 'ABSTAIN_INVALID_SESSION')

    def test_wrong_partition_rejects_session(self):
        self.p['trials'][0]['partition'] = 'training'
        self.assertEqual(evaluate(self.p)['decision'], 'ABSTAIN_INVALID_SESSION')

    def test_unexpected_field_rejects_session(self):
        self.p['trials'][0]['source_url'] = 'example'
        self.assertEqual(evaluate(self.p)['decision'], 'ABSTAIN_INVALID_SESSION')

    def test_missing_quality_field_rejects_session(self):
        del self.p['trials'][0]['quality']['native_identity']
        self.assertEqual(evaluate(self.p)['decision'], 'ABSTAIN_INVALID_SESSION')

    def test_bad_hash_rejects_session(self):
        self.p['optical_trace_sha256'] = 'unverified'
        self.assertEqual(evaluate(self.p)['decision'], 'ABSTAIN_INVALID_SESSION')

    def test_invalid_intervals_abstain(self):
        self.p['trials'][0]['pulse_onset_ms'] = [1, 0]
        self.assertEqual(evaluate(self.p)['counts']['ABSTAIN_QUALITY'], 1)

    def test_nan_and_bool_numeric_abstain(self):
        for bad in (float('nan'), float('inf'), True):
            p = copy.deepcopy(self.p)
            p['trials'][0]['flash_roi'] = bad
            self.assertEqual(evaluate(p)['counts']['ABSTAIN_QUALITY'], 1)

    def test_bad_sync_rejects_session(self):
        self.p['sync_error_ms'] = -0.1
        self.assertEqual(evaluate(self.p)['decision'], 'ABSTAIN_INVALID_SESSION')

    def test_duplicate_json_keys_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'fixture.json'
            path.write_text('{"schema":"E002-543-v1","schema":"wrong"}')
            with self.assertRaises(ValueError):
                load_private(path)

    def test_no_private_ids_in_aggregate(self):
        result = json.dumps(evaluate(self.p))
        for marker in ('private-synthetic', 'synthetic-calibration', 'frame1', 'before', 'a' * 64):
            self.assertNotIn(marker, result)

    def test_never_certifies_product_or_physiology(self):
        r = evaluate(self.p)
        self.assertEqual(r['release'], 'BLOCKED')
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertFalse(r['physical_source_authenticated'])
        self.assertFalse(r['human_anatomical_validation'])
        self.assertFalse(r['shutter_support_certified'])
        self.assertNotIn('SHUTTER_CERTIFIED', json.dumps(r))


if __name__ == '__main__':
    unittest.main()
