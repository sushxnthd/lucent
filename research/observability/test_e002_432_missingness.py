"""Independent numerical and adversarial checks for E002-432."""
import math
import unittest

from e002_432_missingness import (
    APERTURE_ERROR, CLOCK_ERROR, D, DEPTH, EXPOSURE, OPEN, THETA, V,
    aperture, boxcar_mean, conditional_lower, evaluate_trial, experiment,
    stress, study_decision,
)


def independent_midpoint_boxcar(center, depth, subdivisions=20000):
    left = center - EXPOSURE / 2
    return sum(aperture(left + (j + 0.5) * EXPOSURE / subdivisions, depth)
               for j in range(subdivisions)) / subdivisions


class MissingnessScience(unittest.TestCase):
    def test_exact_exposure_and_independent_quadrature(self):
        for depth in (0.0, 0.08, 0.10, 0.12, 0.125):
            for center in (0, D, 2 * D):
                self.assertAlmostEqual(boxcar_mean(center, depth),
                                       independent_midpoint_boxcar(center, depth),
                                       delta=2e-8)
            self.assertAlmostEqual(boxcar_mean(0, depth), OPEN, places=12)
            self.assertAlmostEqual(boxcar_mean(2 * D, depth), OPEN, places=12)

    def test_continuous_witness_speed_and_alias(self):
        self.assertLess(DEPTH / (D - EXPOSURE / 2), V)
        grid = [i * 2 * D / 20000 for i in range(20001)]
        values = [aperture(t, DEPTH) for t in grid]
        self.assertAlmostEqual(min(values), OPEN - DEPTH, places=12)
        self.assertTrue(any(v <= THETA for v in values))
        self.assertTrue(all(abs(b - a) / (2 * D / 20000) <= V + 1e-8
                            for a, b in zip(values, values[1:])))
        self.assertEqual([boxcar_mean(0, DEPTH), boxcar_mean(2 * D, DEPTH)],
                         [boxcar_mean(0, 0), boxcar_mean(2 * D, 0)])

    def test_frozen_prediction_and_uncertainty(self):
        self.assertAlmostEqual(conditional_lower(OPEN, OPEN, 0, D),
                               2.033333333333333, places=11)
        self.assertAlmostEqual(conditional_lower(OPEN, OPEN, 0, 2 * D),
                               1.9666666666666668, places=11)
        self.assertGreater(conditional_lower(OPEN, OPEN, 0, D), THETA)
        self.assertLess(conditional_lower(OPEN, OPEN, 0, 2 * D,
                          aperture_error=APERTURE_ERROR,
                          clock_error=CLOCK_ERROR), THETA)
        self.assertLess(boxcar_mean(D, DEPTH), THETA)

    def test_dropout_falsification_and_retained_control(self):
        hidden = evaluate_trial(DEPTH, True)
        self.assertTrue(hidden["truth_closed"])
        self.assertTrue(hidden["naive"])
        self.assertFalse(hidden["timestamp_aware"])
        self.assertFalse(evaluate_trial(DEPTH, False)["naive"])
        self.assertFalse(evaluate_trial(DEPTH, False)["timestamp_aware"])
        self.assertTrue(evaluate_trial(0, False)["timestamp_aware"])
        self.assertFalse(evaluate_trial(0, True)["timestamp_aware"])

    def test_frozen_holdout_and_negative_result(self):
        r = stress()
        self.assertEqual(r, stress())
        for regime in ("MCAR", "MNAR"):
            self.assertEqual(r[regime]["n"], 1200)
            self.assertGreater(r[regime]["true_closures"], 0)
            self.assertEqual(r[regime]["aware_false"], 0)
            self.assertGreater(r[regime]["aware_candidates"], 0)
            self.assertLess(r[regime]["aware_candidates"],
                            r[regime]["naive_candidates"])
            self.assertGreater(r[regime]["witnessed_when_retained"], 0)
        self.assertGreater(r["MNAR"]["naive_false"], 0)
        self.assertGreater(r["MNAR"]["naive_false"], r["MCAR"]["naive_false"])

    def test_invalid_metadata_and_product_gate(self):
        with self.assertRaises(ValueError):
            study_decision([0, 2], [None, 2 * D], [OPEN, OPEN])
        with self.assertRaises(ValueError):
            study_decision([0, 2], [0, D], [OPEN, OPEN])
        with self.assertRaises(ValueError):
            study_decision([0, 2, 2], [0, D, 2 * D], [OPEN] * 3)
        with self.assertRaises(ValueError):
            study_decision([0, 2], [0, 2 * D], [OPEN, float("nan")])
        with self.assertRaises(ValueError):
            conditional_lower(OPEN, OPEN, 0, 0)
        with self.assertRaises(ValueError):
            conditional_lower(OPEN, OPEN, 0, 2 * D, clock_error=-0.1)
        with self.assertRaises(ValueError):
            conditional_lower(OPEN, OPEN, 0, 2 * D, exposure=0.5)
        with self.assertRaises(ValueError):
            aperture(D, depth=1.0)
        with self.assertRaises(ValueError):
            stress(n=20)
        self.assertFalse(study_decision([0, 2], [0, 2 * D],
                          [OPEN, OPEN])["physical_certificate_authorized"])
        self.assertFalse(experiment()["physical_certificate_authorized"])
        self.assertEqual(experiment()["product"], "ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    unittest.main()
