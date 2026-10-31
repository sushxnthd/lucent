"""E002-503 adversarial tests: independent ratio oracle and actual adjudicator."""
import math
from fractions import Fraction
import unittest

from e002_503_iris_scale_falsifier import (
    aperture_interval, threshold_decision, fill_synthetic, run,
)
from e002_492_anatomical_review import build_manifest, adjudicate


class IrisScaleTests(unittest.TestCase):
    def test_frozen_predictions_against_actual_adjudicator(self):
        result = run()
        self.assertEqual(len(result["cases"]), 2)
        for case in result["cases"]:
            self.assertEqual(case["actual_adjudicator_agreement_intervals"], 260)
            self.assertEqual(case["actual_adjudicator_disagreements"], 0)
            self.assertEqual(case["actual_adjudicator_abstentions"], 0)
            self.assertNotEqual(case["nominal_threshold_decision_not_from_adjudicator"],
                                case["stipulated_truth_threshold_decision"])
            self.assertEqual(case["scale_aware_threshold_decision"], "THRESHOLD_UNRESOLVED")
        self.assertEqual(result["product"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(result["release"], "BLOCKED")

    def test_independent_exact_fraction_oracle(self):
        for gap, e, d, delta in (("4.2", "0.05", "44", "4"),
                                 ("3.8", "0.05", "36", "4")):
            g, u, diameter, uncertainty = map(Fraction, (gap, e, d, delta))
            expected = ((g - 2*u)/(diameter+uncertainty),
                        (g + 2*u)/(diameter-uncertainty))
            actual = aperture_interval(float(g), float(u), float(diameter),
                                       float(uncertainty))
            for a, b in zip(actual, expected):
                self.assertAlmostEqual(a, float(b), places=13)

    def test_zero_scale_error_recovers_nominal_interval(self):
        self.assertEqual(aperture_interval(4.2, 0.05, 40, 0),
                         aperture_interval(4.2, 0.05, 40))

    def test_expansion_monotone(self):
        previous = aperture_interval(4.2, 0.05, 40, 0)
        for delta in (0.5, 1, 2, 4, 8):
            current = aperture_interval(4.2, 0.05, 40, delta)
            self.assertLessEqual(current[0], previous[0])
            self.assertGreaterEqual(current[1], previous[1])
            previous = current

    def test_threshold_equality_abstains(self):
        self.assertEqual(threshold_decision((0.1, 0.1)), "THRESHOLD_UNRESOLVED")
        self.assertEqual(threshold_decision((0.09, 0.1)), "THRESHOLD_UNRESOLVED")
        self.assertEqual(threshold_decision((0.1, 0.11)), "THRESHOLD_UNRESOLVED")

    def test_invalid_denominator_or_uncertainty_abstains(self):
        for args in ((4.2, .05, 40, 40), (4.2, .05, 40, 41),
                     (4.2, .05, 0, 0), (4.2, -.1, 40, 0),
                     (4.2, .05, 40, -1), (-1, 0, 40, 0),
                     (4.2, .05, float("nan"), 0),
                     (4.2, .05, 40, float("inf")),
                     (4.2, .05, True, 0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                aperture_interval(*args)

    def test_no_biological_or_physical_claim(self):
        report = run()
        self.assertEqual(report["real_human_anatomical_ratings"], 0)
        self.assertFalse(report["authenticated_camera_clock"])
        self.assertFalse(report["physical_hidden_closure_certified"])

    def test_independent_rater_disagreement_still_detected(self):
        manifest = build_manifest()
        a = fill_synthetic(manifest, "A", 4.2, 44.0, .05)
        b = fill_synthetic(manifest, "B", 8.0, 44.0, .05)
        report = adjudicate(manifest, a, b)
        self.assertEqual(report["interval_disagreement"], 260)
        self.assertEqual(report["agreement_intervals"], 0)


if __name__ == "__main__":
    unittest.main()
