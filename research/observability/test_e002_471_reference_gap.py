#!/usr/bin/env python3
"""E002-471: shutter-gap reference localization regressions; synthetic only."""
import copy
import unittest

from e002_456_prospective_gate import evaluate_interval, evaluate_dataset


def fixture():
    return {
        "interval_id": "constructed-gap", "participant_id": "synthetic-only",
        "split": "development",
        "closure_threshold_mm": 2.0,
        "endpoint_aperture_mm": [3.0, 3.0],
        "endpoint_uncertainty_mm": [0.0, 0.0],
        "endpoint_time_ms": [0.0, 10.0],
        "shutter": {"kernel": "uniform_symmetric", "exposure_ms": 4.0,
                    "clock_error_ms": 0.1, "reference_exposure_ms": 0.2,
                    "reference_clock_error_ms": 0.1},
        "velocity": {"limit_mm_s": 100.0, "provenance": "ILLUSTRATIVE"},
        "instrument": {
            "geometry_calibration_id": "synthetic",
            "clock_calibration_id": "synthetic",
            "exposure_calibration_id": "synthetic",
            "reference_annotation_id": "synthetic",
            "independent_reference": True,
        },
        "nuisance": {k: "PASS" for k in (
            "geometry", "brightness", "missingness", "blur", "gaze",
            "glasses", "sampling", "clock", "rolling_shutter")},
        "reference": [{"time_ms": 1.0, "aperture_mm": 1.8,
                       "uncertainty_mm": 0.0, "quality": "PASS"}],
    }


class DarkGapWitnessTests(unittest.TestCase):
    def test_previously_misclassified_exposure_witness_is_incomplete(self):
        c = fixture()
        r = evaluate_interval(c)
        self.assertEqual(r["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertEqual(r["reference"], "REFERENCE_INCOMPLETE")
        self.assertFalse(r["joint_falsification"])

    def test_exploratory_realizable_exposure_only_crossing(self):
        # Independent continuous 1000-mm/s-Lipschitz aperture:
        # a(t) = 2.5 - max(0, 0.7 - |t-1|).
        # It reaches 1.8 mm at 1 ms, but remains 2.5 mm in the
        # entire unexposed gap [2,8] ms. Exact first shutter mean is
        # 2.5 - triangular_area(0.7*0.7)/4 = 2.3775 mm.
        c = fixture()
        c["velocity"]["limit_mm_s"] = 1000.0
        c["endpoint_aperture_mm"] = [2.3775, 2.5]
        c["reference"][0]["aperture_mm"] = 1.85  # 0.2-ms boxcar average
        r = evaluate_interval(c)
        self.assertEqual(r["decision"], "NOT_EXCLUDED")
        self.assertEqual(r["reference"], "REFERENCE_INCOMPLETE")
        self.assertFalse(r["joint_falsification"])

    def test_interior_gap_witness_still_falsifies_joint_assumptions(self):
        c = fixture()
        c["reference"][0]["time_ms"] = 5.0
        r = evaluate_interval(c)
        self.assertEqual(r["reference"], "WITNESSED_CROSSING")
        self.assertTrue(r["joint_falsification"])

    def test_strict_support_boundaries_are_not_witnesses(self):
        for t in (2.3, 7.7):
            with self.subTest(time_ms=t):
                c = fixture()
                c["reference"][0]["time_ms"] = t
                r = evaluate_interval(c)
                self.assertEqual(r["reference"], "REFERENCE_INCOMPLETE")
                self.assertFalse(r["joint_falsification"])

    def test_ordinary_shutter_width_cannot_improve_witness(self):
        c = fixture()
        c["reference"][0]["time_ms"] = 2.8
        self.assertEqual(evaluate_interval(c)["reference"], "WITNESSED_CROSSING")
        c["shutter"]["exposure_ms"] = 6.0
        self.assertEqual(evaluate_interval(c)["reference"], "REFERENCE_INCOMPLETE")

    def test_clock_uncertainty_cannot_improve_witness(self):
        c = fixture()
        c["reference"][0]["time_ms"] = 2.5
        self.assertEqual(evaluate_interval(c)["reference"], "WITNESSED_CROSSING")
        c["shutter"]["clock_error_ms"] = 0.6
        self.assertEqual(evaluate_interval(c)["reference"], "REFERENCE_INCOMPLETE")

    def test_zero_guaranteed_gap_abstains(self):
        c = fixture()
        c["shutter"]["exposure_ms"] = 9.8
        self.assertEqual(evaluate_interval(c)["reason"], "NO_GUARANTEED_DARK_GAP")

    def test_reference_cannot_fit_in_gap_abstains(self):
        c = fixture()
        c["shutter"]["exposure_ms"] = 9.5
        c["shutter"]["reference_exposure_ms"] = 0.5
        self.assertEqual(evaluate_interval(c)["reason"],
                         "REFERENCE_TIME_SUPPORT_TOO_WIDE")

    def test_invalid_nuisance_still_abstains(self):
        c = fixture()
        c["nuisance"]["blur"] = "UNKNOWN"
        self.assertEqual(evaluate_interval(c)["decision"], "ABSTAIN")

    def test_product_claim_remains_blocked_even_with_gap_witness(self):
        c = fixture()
        c["reference"][0]["time_ms"] = 5.0
        c["velocity"]["provenance"] = "EXTERNAL_HARD_BOUND_DECLARED"
        r = evaluate_dataset({"schema_version": "E002-456-v1", "intervals": [c]})
        self.assertEqual(r["product_claim"], "ABSTAIN_UNCALIBRATED")
        self.assertFalse(r["physical_release_authorized"])
        self.assertFalse(r["external_hard_bound_verified_by_this_program"])
        self.assertEqual(r["counts"]["development"]["FALSIFIED_JOINT_ASSUMPTIONS"], 1)


if __name__ == "__main__":
    unittest.main()
