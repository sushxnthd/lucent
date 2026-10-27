import unittest
from e002_495_exposure_mean_boundary import evaluate, independent_midpoint, sweep


class ExactMeanBoundaryTests(unittest.TestCase):
    def test_frozen_false_exclusion(self):
        a = evaluate(15, 5, '.1', '.7', '.1', 1)
        self.assertEqual(a['R_endpoint'], '5/6')
        self.assertEqual(a['R_average'], '5/4')
        self.assertEqual(a['tent_slope'], '2/25')
        self.assertEqual(a['tent_peak'], '9/10')
        self.assertEqual(a['endpoint_aperture'], '1/2')
        self.assertEqual(a['left_exposure_mean'], '7/10')
        self.assertTrue(a['naive_endpoint_substitution_false_exclusion'])
        self.assertTrue(a['closing_tent_admissible_by_velocity'])

    def test_strict_exclusion(self):
        a = evaluate(15, 5, '.1', '.9', '.1')
        self.assertTrue(a['hidden_closure_excluded_by_mean_bound'])
        self.assertFalse(a['closing_tent_admissible_by_velocity'])

    def test_sharp_equality(self):
        a = evaluate(15, 5, '.1', '.85', '.1')
        self.assertEqual(a['R_average'], '1')
        self.assertTrue(a['closing_tent_admissible_by_velocity'])

    def test_zero_gap(self):
        a = evaluate(15, 15, '.1', '.7', '.1')
        self.assertEqual(a['g'], '0')
        self.assertTrue(a['closing_tent_admissible_by_velocity'])
        self.assertEqual(a['R_endpoint'], '0')

    def test_short_exposure(self):
        a = evaluate('15', '0.000001', '.1', '.7', '.1')
        self.assertTrue(a['closing_tent_admissible_by_velocity'])
        # As e tends to zero, exposure means approach instantaneous endpoints.
        self.assertFalse(a['naive_endpoint_substitution_false_exclusion'])

    def test_cap_does_not_imply_global_impossibility(self):
        a = evaluate(15, 5, '.1', '.7', '.1', '.8')
        self.assertFalse(a['constructed_witness_respects_cap'])
        self.assertFalse(a['hidden_closure_excluded_by_mean_bound'])

    def test_independent_quadrature(self):
        for x in independent_midpoint(15, 5, .7, .1, n=10001):
            self.assertAlmostEqual(x, .7, places=10)

    def test_exact_sweep(self):
        a = sweep(n=1000)
        self.assertEqual(a['feasible'] + a['excluded'], 1000)
        self.assertGreater(a['naive_endpoint_false_exclusions'], 0)

    def test_invalid_models(self):
        for args in [(0, 1, 1, 1, 0), (1, 2, 1, 1, 0), (1, 1, 0, 1, 0),
                     (1, 1, 1, 0, 0), (1, 1, 1, 1, -1), (True, 1, 1, 1, 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                evaluate(*args)

    def test_release_remains_blocked(self):
        a = evaluate(15, 5, '.1', '.7', '.1')
        self.assertEqual(a['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertEqual(a['release'], 'BLOCKED')
        self.assertFalse(a['physical_camera_calibrated'])


if __name__ == '__main__':
    unittest.main()
