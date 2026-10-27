#!/usr/bin/env python3
import unittest
from decimal import Decimal
from fractions import Fraction
from e002_475_tail_calibration import (
    CALIBRATION_BLINKS, PRODUCT, evaluate, exact_joint_rank,
    exhaustive_rank_check, minimum_joint_n, minimum_tolerance_n,
    synthetic_joint_coverage, tolerance_confidence,
)


class ParticipantTailTests(unittest.TestCase):
    def test_exact_rank_one(self):
        self.assertEqual(exact_joint_rank(12, 1), Fraction(12, 13))

    def test_exact_rank_eight(self):
        self.assertEqual(exact_joint_rank(12, 8), Fraction(3, 5))

    def test_permutation_independence(self):
        self.assertEqual(exhaustive_rank_check(3, 2), Fraction(3, 5))

    def test_tolerance_n12(self):
        self.assertAlmostEqual(float(tolerance_confidence(12, Decimal('0.95'))), 1 - 0.95**12)

    def test_tolerance_boundary(self):
        self.assertEqual(minimum_tolerance_n(Decimal('0.95'), Decimal('0.95')), 59)
        self.assertLess(tolerance_confidence(58, Decimal('0.95')), Decimal('0.95'))

    def test_joint_boundary(self):
        self.assertEqual(minimum_joint_n(8, Fraction(95, 100)), 152)
        self.assertLess(exact_joint_rank(151, 8), Fraction(95, 100))

    def test_shift_counterexample(self):
        self.assertEqual(synthetic_joint_coverage(12, 8, shift=True), 0)

    def test_seeded_baseline(self):
        self.assertLess(abs(synthetic_joint_coverage(12, 8) - 0.6), 0.02)

    def test_no_blink_pseudoreplication(self):
        with self.assertRaises(ValueError):
            evaluate(CALIBRATION_BLINKS)

    def test_no_boolean_sample_counts(self):
        with self.assertRaises(ValueError):
            exact_joint_rank(True, 8)

    def test_invalid_probability(self):
        with self.assertRaises(ValueError):
            tolerance_confidence(12, Decimal('1'))

    def test_no_physical_release(self):
        result = evaluate()
        self.assertFalse(result['physical_release_authorized'])
        self.assertEqual(result['product_claim'], PRODUCT)
        self.assertTrue(result['sample_max_is_not_hard_cap'])
        self.assertTrue(result['recorded_peak_proxy_is_not_instantaneous_anatomical_speed'])


if __name__ == '__main__':
    unittest.main()
