#!/usr/bin/env python3
"""Independent input invariants for E002-489's physical-claim guard."""
import unittest
from e002_489_rate_provenance import evaluate


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.header = {
            'main_header_nominal_fps': 1.0,
            'stream_header_nominal_fps': 1.0,
            'avi_main_header': {'declared_frames': 50932},
            'independent_hardware_clock_authenticated': False,
            'physical_shutter_calibrations': 0,
        }

    def test_authentic_observation_implied_durations(self):
        x = evaluate(self.header)
        self.assertEqual(x['avi_implied_duration_seconds'], 50932.0)
        self.assertEqual(x['paper_150fps_implied_duration_seconds'], round(50932 / 150, 6))
        self.assertEqual(x['rehost_500fps_implied_duration_seconds'], round(50932 / 500, 6))

    def test_rate_hypotheses_flip_illustrative_boundary(self):
        s = evaluate(self.header)['hypothetical_scenarios_not_anatomical_predictions']
        self.assertEqual([x['hypothetical_hidden_closure_kinematically_possible'] for x in s], [True, False, False])
        self.assertEqual([x['hypothetical_R'] for x in s], [100.0, round(2 / 3, 9), 0.2])

    def test_all_physical_claims_abstain(self):
        x = evaluate(self.header)
        self.assertEqual(x['product_release'], 'BLOCKED')
        for k in ('timing_certificate', 'eyelid_velocity_certificate', 'hidden_closure_exclusion',
                  'blink_duration', 'perclos', 'fatigue', 'medical'):
            self.assertTrue(x[k].startswith('ABSTAIN_'), k)

    def test_metadata_spoofing_cannot_authorize(self):
        self.header.update({'main_header_nominal_fps': 150, 'stream_header_nominal_fps': 150,
                            'independent_hardware_clock_authenticated': True,
                            'physical_shutter_calibrations': 100})
        self.assertEqual(evaluate(self.header)['hidden_closure_exclusion'], 'ABSTAIN_UNCALIBRATED')

    def test_reject_mismatched_headers(self):
        self.header['stream_header_nominal_fps'] = 150
        with self.assertRaisesRegex(ValueError, 'INCONSISTENT_AVI_HEADERS'):
            evaluate(self.header)

    def test_reject_zero_or_nonfinite_rate(self):
        for bad in (0, -1, float('nan'), float('inf'), True, None):
            with self.subTest(bad=bad):
                self.header['stream_header_nominal_fps'] = bad
                with self.assertRaisesRegex(ValueError, 'INVALID_NOMINAL_RATE'):
                    evaluate(self.header)

    def test_reject_invalid_frame_count(self):
        for bad in (0, -1, 1.5, True, None):
            with self.subTest(bad=bad):
                self.header['avi_main_header']['declared_frames'] = bad
                with self.assertRaisesRegex(ValueError, 'INVALID_FRAME_COUNT'):
                    evaluate(self.header)


if __name__ == '__main__':
    unittest.main(verbosity=2)
