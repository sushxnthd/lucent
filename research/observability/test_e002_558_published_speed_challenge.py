#!/usr/bin/env python3
"""E002-558 deterministic scientific falsification tests (no human data copied)."""
import unittest
from fractions import Fraction
from e002_558_published_speed_challenge import lower_constraint, decision

class PublishedSpeedChallenge(unittest.TestCase):
    def test_exact_reported_constraint(self):
        self.assertEqual(lower_constraint(), Fraction(1215, 64))
    def test_nominal_low_caps_contradicted(self):
        for cap in (0, 10, 15):
            self.assertEqual(decision(Fraction(cap), lower_constraint()),
                             "INCOMPATIBLE_WITH_REPORTED_POINT_ESTIMATES")
    def test_no_cap_is_certified(self):
        for cap in (19, 20, 40, 1000):
            self.assertEqual(decision(Fraction(cap), lower_constraint()),
                             "NOT_FALSIFIED_NOT_CERTIFIED")
    def test_error_budget_not_invented(self):
        self.assertLess(lower_constraint(Fraction(10), Fraction(1, 2)), lower_constraint())
        self.assertLess(lower_constraint(Fraction(50), Fraction(1)), Fraction(15))
    def test_bias_monotonicity(self):
        for b in (0, 1, 5, 10, 50, 200, 243, 300):
            for e in (0, 1, 10):
                self.assertLessEqual(lower_constraint(Fraction(b), Fraction(e)), lower_constraint())
    def test_invalid_assumptions_rejected(self):
        for b,e in ((-1,0),(0,-1)):
            with self.assertRaises(ValueError): lower_constraint(Fraction(b),Fraction(e))
    def test_zero_speed_under_very_large_bias(self):
        self.assertEqual(lower_constraint(Fraction(300),Fraction(0)), 0)
    def test_no_cross_behavior_extrapolation(self):
        # No inference about reflexive/spontaneous blinks or camera transfer
        self.assertEqual(decision(Fraction(20), lower_constraint()), "NOT_FALSIFIED_NOT_CERTIFIED")

if __name__ == "__main__":
    unittest.main()
