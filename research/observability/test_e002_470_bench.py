#!/usr/bin/env python3
"""E002-470 adversarial instrument-surrogate checks."""
import unittest
from e002_470_bench import (avg_abs, shutter_mean, dark_gap_min,
                            make_case, nuisance_challenge, clean_sweep,
                            integration_control)
from e002_456_prospective_gate import evaluate_interval


class TestBench(unittest.TestCase):
    def test_abs_integral_crossing(self):
        self.assertAlmostEqual(avg_abs(-1, 1, 0), 0.5)

    def test_abs_integral_offset(self):
        self.assertAlmostEqual(avg_abs(0, 2, -1), 2.0)

    def test_exact_camera_mean(self):
        self.assertAlmostEqual(shutter_mean(2, 0.25, 0, 0, 2), 2.125)

    def test_hidden_closure_truth(self):
        self.assertLess(dark_gap_min(1.99, 0.25, 2, 4, 1), 2)

    def test_no_hidden_closure_truth(self):
        self.assertGreater(dark_gap_min(2.01, 0.25, 2, 4, 1), 2)

    def test_invalid_shutter(self):
        with self.assertRaises(ValueError):
            avg_abs(1, 1, 0)

    def test_invalid_gap(self):
        with self.assertRaises(ValueError):
            dark_gap_min(1, 0.1, 1, 1, 1)

    def test_declared_nuisance_failure_abstains(self):
        case = make_case(4, 1, 3, 3, bad_nuisance="brightness")
        self.assertEqual(evaluate_interval(case)["decision"], "ABSTAIN")

    def test_clean_open_exclusion(self):
        case = make_case(4, 1, 4, 4)
        self.assertEqual(evaluate_interval(case)["decision"],
                         "EXCLUDED_CONDITIONALLY")

    def test_clean_sweep_no_false_exclusion(self):
        out = clean_sweep()
        self.assertEqual(out["total"].get("false_exclusions", 0), 0)
        self.assertEqual(out["total"].get("unexpected_abstentions", 0), 0)

    def test_fault_controls(self):
        out = nuisance_challenge()
        self.assertEqual(out["total_fault_strata"], 9)
        self.assertEqual(out["abstentions_if_fail_declared"], 9)

    def test_quadrature(self):
        self.assertTrue(integration_control()["within_1e_minus_6_mm"])


if __name__ == "__main__":
    unittest.main()
