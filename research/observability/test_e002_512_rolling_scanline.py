#!/usr/bin/env python3
"""E002-512 frozen synthetic scanline adversaries; no human data."""
import unittest
from decimal import Decimal
from e002_512_rolling_scanline import fixture

class FrozenRollingShutterTests(unittest.TestCase):
    def test_zero_row_drift_conditional_only(self):
        x = fixture()
        self.assertEqual(x['conditional_scalar_result'], 'CONDITIONAL_EXCLUSION')
        self.assertAlmostEqual(float(x['risk_upper']), .74898979485566, places=11)

    def test_ten_rows_conditional_only(self):
        self.assertEqual(fixture(110)['conditional_scalar_result'], 'CONDITIONAL_EXCLUSION')
        self.assertAlmostEqual(float(fixture(110)['risk_upper']), .77898979485566, places=11)

    def test_twenty_rows_reverses(self):
        self.assertEqual(fixture(120)['conditional_scalar_result'], 'NOT_EXCLUDED_OR_BOUNDARY')
        self.assertAlmostEqual(float(fixture(120)['risk_upper']), .80898979485566, places=11)

    def test_row_localization_uncertainty_reverses(self):
        self.assertEqual(fixture(110, row_uncertainty=5)['conditional_scalar_result'], 'NOT_EXCLUDED_OR_BOUNDARY')

    def test_reversed_readout_changes_direction(self):
        self.assertLess(Decimal(fixture(120, readout_direction='BOTTOM_TO_TOP')['risk_upper']),
                        Decimal(fixture(100)['risk_upper']))

    def test_row_drift_monotonic_top_down(self):
        values = [Decimal(fixture(x)['risk_upper']) for x in (80, 100, 110, 120)]
        self.assertEqual(values, sorted(values))

    def test_uncertainty_monotonic(self):
        values = [Decimal(fixture(110, row_uncertainty=x)['risk_upper']) for x in (0, 1, 5, 10)]
        self.assertEqual(values, sorted(values))

    def test_line_delay_monotonic_for_positive_drift(self):
        values = [Decimal(fixture(120, line_delay=x)['risk_upper']) for x in ('0', '.00005', '.0001')]
        self.assertEqual(values, sorted(values))

    def test_boundary_never_certifies_equality(self):
        j = Decimal(fixture()['critical_extra_gap_seconds'])
        self.assertEqual(fixture(clock_gap_error=j)['conditional_scalar_result'], 'NOT_EXCLUDED_OR_BOUNDARY')

    def test_unknown_readout_and_geometry_abstain(self):
        for key, value in [('readout_direction', 'UNKNOWN'),
                           ('observation_model', 'MULTIROW_RGB'),
                           ('same_aperture_assumed', False)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                fixture(**{key: value})

    def test_out_of_sensor_and_invalid_row_errors(self):
        for key, value in [('row_1', -1), ('row_2', 288),
                           ('row_uncertainty', -1), ('row_uncertainty', 101),
                           ('sensor_height', 0), ('row_1', 100.1)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                fixture(**{key: value})

    def test_nonfinite_or_missing_physics_abstain(self):
        for key, value in [('speed', None), ('speed', 'NaN'), ('speed', 'Infinity'),
                           ('line_delay', None), ('line_delay', '-.001'),
                           ('clock_gap_error', '-.001'), ('exposure', '.05'),
                           ('mean_error', '-.01')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                fixture(**{key: value})

    def test_overlap_abstains(self):
        with self.assertRaisesRegex(ValueError, 'POSSIBLY_OVERLAPPING_EXPOSURES'):
            fixture(0, line_delay='.0003')

    def test_no_numeric_result_grants_product_release(self):
        for result in (fixture(), fixture(110), fixture(120), fixture(80)):
            self.assertEqual(result['product'], 'ABSTAIN_UNCALIBRATED')
            self.assertEqual(result['release'], 'BLOCKED')
            self.assertFalse(result['camera_line_timing_authenticated'])
            self.assertFalse(result['eyelid_velocity_certified'])
            self.assertFalse(result['full_rgb_claim_supported'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
