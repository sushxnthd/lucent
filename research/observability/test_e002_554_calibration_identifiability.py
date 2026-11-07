"""Frozen E002-554 synthetic adversarial controls."""
import unittest
from fractions import Fraction as F
from e002_554_calibration_identifiability import (
    kernel, moments, integral, measured_quadratic, exclusion_bound, experiment,
    THETA, HALF, ONE,
)


class CalibrationIdentifiabilityTests(unittest.TestCase):
    def setUp(self):
        self.high = kernel(1)
        self.low = kernel(-1)

    def test_normalization(self):
        self.assertEqual(moments(self.high)[0], ONE)
        self.assertEqual(moments(self.low)[0], ONE)

    def test_full_support(self):
        self.assertTrue(all(w > 0 for _, _, w in self.high + self.low))
        self.assertEqual(self.high[0][0], F(0))
        self.assertEqual(self.high[-1][1], ONE)

    def test_same_center(self):
        self.assertEqual(moments(self.high)[1], moments(self.low)[1])
        self.assertEqual(moments(self.high)[1], HALF)

    def test_variance_difference(self):
        self.assertEqual(moments(self.high)[2] - moments(self.low)[2], F(2, 125))

    def test_calibration_pulse_interior(self):
        for lo, hi in ((F(1, 4), F(3, 10)), (F(9, 20), F(11, 20)), (F(7, 10), F(3, 4))):
            self.assertEqual(integral(self.high, lo=lo, hi=hi), integral(self.low, lo=lo, hi=hi))

    def test_all_central_pulses_indistinguishable(self):
        for i in range(20, 79):
            self.assertEqual(integral(self.high, lo=F(i, 100), hi=F(i+1, 100)),
                             integral(self.low, lo=F(i, 100), hi=F(i+1, 100)))

    def test_edge_pulse_distinguishes(self):
        self.assertNotEqual(integral(self.high, lo=F(1, 20), hi=F(1, 10)),
                            integral(self.low, lo=F(1, 20), hi=F(1, 10)))

    def test_both_measured_means_equal(self):
        self.assertEqual(measured_quadratic(self.high, -HALF, HALF),
                         measured_quadratic(self.high, ONE, HALF))

    def test_wrong_kernel_false_exclusion(self):
        m = measured_quadratic(self.high, -HALF, HALF)
        self.assertEqual(exclusion_bound(m, m, self.low), F(1, 250))
        self.assertGreater(exclusion_bound(m, m, self.low), THETA)

    def test_correct_kernel_abstains(self):
        m = measured_quadratic(self.high, -HALF, HALF)
        self.assertEqual(exclusion_bound(m, m, self.high), 0)
        self.assertLess(exclusion_bound(m, m, self.high), THETA)

    def test_invalid_pulse_rejected(self):
        with self.assertRaises(ValueError):
            integral(self.high, lo=F(-1, 10), hi=F(1, 10))

    def test_invalid_sign_rejected(self):
        with self.assertRaises(ValueError):
            kernel(0)

    def test_experiment_never_claims_human(self):
        self.assertEqual(experiment()["evidence_tier"], "EXACT_SYNTHETIC_ONLY")
        self.assertEqual(experiment()["human_rater_count"], 0)


if __name__ == '__main__':
    unittest.main()
