"""E002-437 independent analytic and adversarial reference tests."""
import copy
import math
import unittest

from e002_437_velocity_bridge import (NUISANCES, VelocityBridgeError, adjudicate, demo,
                                        optimal_spacing, penalty, segment_upper)


def valid_record():
    return {'trace_id': 'synthetic-demo', 'frames': [
        {'frame_id': i, 'time_s': i / 400, 'aperture_mm': 2.1 + .03 * math.sin(i / 8),
         'valid': True, 'nuisances': {k: False for k in NUISANCES}} for i in range(8)],
        'acceleration_upper_mm_s2': 3600.0, 'aperture_error_mm': .005,
        'clock_error_s': .00005, 'max_step_s': .003,
        'physical_scale_attested': True, 'sensor_timing_attested': True,
        'acceleration_bound_attested': True, 'nuisance_calibration_attested': True,
        'external_calibration_reference': 'SYNTHETIC_PREMISES_NOT_AUTHENTICATED'}


class BridgeTests(unittest.TestCase):
    def test_quadratic_sharpness_with_endpoint_errors(self):
        # Independent x(t)=c+30t-1800t², |x''|=3600, h=2.5ms.
        h, e, A, v0 = .0025, .005, 3600, 30
        x0 = 2.0
        x1 = 2.0 + v0*h - A*h*h/2
        y0, y1 = x0+e, x1-e
        observed = (y1-y0)/h
        self.assertAlmostEqual(observed, 21.5, places=9)
        self.assertAlmostEqual(segment_upper(y0, y1, h, e, A), v0, places=9)
        self.assertGreater(v0, observed)

    def test_rate_noise_acceleration_nonmonotonic(self):
        expected = {200: 11.0, 400: 8.5, 1000: 11.8}
        for hz, v in expected.items():
            self.assertAlmostEqual(penalty(1/hz, .005, 3600), v)
        opt = optimal_spacing(.005, 3600)
        self.assertAlmostEqual(opt['optimal_spacing_s'], 2*math.sqrt(.005/3600))
        self.assertAlmostEqual(opt['minimum_penalty_mm_s'], 2*math.sqrt(18))
        self.assertLess(opt['minimum_penalty_mm_s'], 8.5)

    def test_500_unseen_smooth_synthetic_oracle(self):
        result = demo(seed=437, traces=500)
        self.assertEqual(result['violations_under_true_premises'], 0)
        self.assertLessEqual(result['maximum_truth_minus_bound_mm_s'], 0)
        self.assertEqual(result['human_participants'], 0)
        self.assertFalse(result['physical_certificate_authorized'])

    def test_misspecified_acceleration_falsifies_bridge(self):
        h, v0, A = .0025, 30, 3600
        y0, y1 = 2.0, 2.0+v0*h-A*h*h/2
        bad = segment_upper(y0, y1, h, 0, 0)
        good = segment_upper(y0, y1, h, 0, A)
        self.assertAlmostEqual(bad, 25.5)
        self.assertAlmostEqual(good, 30.0)
        self.assertLess(bad, v0)

    def test_misspecified_error_falsifies_bridge(self):
        h, e, v0, A = .0025, .005, 30, 3600
        y0 = 2+e
        y1 = 2+v0*h-A*h*h/2-e
        bad = segment_upper(y0, y1, h, 0, A)
        self.assertAlmostEqual(bad, 26)
        self.assertLess(bad, v0)

    def test_clock_uncertainty_monotonic(self):
        values = [segment_upper(2.1, 2.13, .0025, .005, 3600, d)
                  for d in (0, .00005, .0002)]
        self.assertLess(values[0], values[1])
        self.assertLess(values[1], values[2])
        with self.assertRaises(VelocityBridgeError):
            segment_upper(2.1, 2.13, .0025, .005, 3600, .00125)

    def test_study_only_output_never_authorizes(self):
        r = adjudicate(valid_record())
        self.assertEqual(r['status'], 'CONDITIONAL_REFERENCE_BOUND')
        self.assertGreater(r['reference_velocity_upper_mm_s'], 0)
        self.assertFalse(r['external_provenance_authenticated_by_code'])
        self.assertFalse(r['physical_certificate_authorized'])
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')

    def test_missing_acceleration_abstains(self):
        d = valid_record()
        d['acceleration_upper_mm_s2'] = None
        self.assertEqual(adjudicate(d)['reason'], 'acceleration_bound_unavailable')
        self.assertIsNone(adjudicate(d)['reference_velocity_upper_mm_s'])

    def test_unattested_calibration_abstains(self):
        for key in ('physical_scale_attested','sensor_timing_attested',
                    'acceleration_bound_attested','nuisance_calibration_attested'):
            d = valid_record()
            d[key] = False
            self.assertEqual(adjudicate(d)['status'], 'ABSTAIN')

    def test_missing_frame_and_nuisance_abstain(self):
        d = valid_record()
        d['frames'][2]['frame_id'] += 2
        with self.assertRaises(VelocityBridgeError):
            adjudicate(d)  # makes ID nonmonotone with following ID
        d = valid_record()
        for i in range(2, len(d['frames'])):
            d['frames'][i]['frame_id'] += 1
        self.assertEqual(adjudicate(d)['reason'], 'missing_reference_frame_id')
        d = valid_record()
        d['frames'][2]['nuisances']['glasses'] = True
        self.assertEqual(adjudicate(d)['reason'], 'missing_or_nuisance_affected_reference')

    def test_explicit_nuisance_controls(self):
        for nuisance in NUISANCES:
            d = valid_record()
            d['frames'][2]['nuisances'][nuisance] = True
            self.assertEqual(adjudicate(d)['reason'], 'missing_or_nuisance_affected_reference')
        d = valid_record()
        del d['frames'][2]['nuisances']['geometry']
        with self.assertRaises(VelocityBridgeError):
            adjudicate(d)

    def test_invalid_timing_and_gap(self):
        d = valid_record()
        d['clock_error_s'] = .0013
        self.assertEqual(adjudicate(d)['reason'], 'clock_uncertainty_overlaps_samples')
        d = valid_record()
        d['max_step_s'] = .002
        self.assertEqual(adjudicate(d)['reason'], 'reference_gap_exceeds_protocol')
        d = valid_record()
        d['frames'][3]['time_s'] = d['frames'][2]['time_s']
        with self.assertRaises(VelocityBridgeError):
            adjudicate(d)

    def test_malformed_and_boolean_numeric_rejection(self):
        for field, val in [('aperture_error_mm',True),('clock_error_s',float('nan')),
                           ('acceleration_upper_mm_s2',-1),('max_step_s',0)]:
            d = valid_record()
            d[field] = val
            with self.assertRaises(VelocityBridgeError):
                adjudicate(d)
        d = valid_record()
        d['frames'][1]['aperture_mm'] = float('inf')
        with self.assertRaises(VelocityBridgeError):
            adjudicate(d)


if __name__ == '__main__':
    unittest.main()
