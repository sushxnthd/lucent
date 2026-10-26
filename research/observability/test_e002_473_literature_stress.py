#!/usr/bin/env python3
"""E002-473 independent human-literature stress tests; not a physical validation."""
import math
import unittest
from fractions import Fraction

from e002_473_literature_stress import (
    SOURCES, independent_rational_envelope, run)
from e002_472_design_feasibility import design_case
from e002_456_prospective_gate import evaluate_interval


def evaluator_case(fps, exposure_ms, v):
    T = 1000 / fps
    return evaluate_interval({
        "closure_threshold_mm": 2.0,
        "endpoint_aperture_mm": [3.0, 3.0],
        "endpoint_uncertainty_mm": [0.1, 0.1],
        "endpoint_time_ms": [0.0, T],
        "shutter": {"kernel": "uniform_symmetric", "exposure_ms": exposure_ms,
                    "clock_error_ms": 0.1, "reference_exposure_ms": 0.2,
                    "reference_clock_error_ms": 0.1},
        "velocity": {"limit_mm_s": v, "provenance": "LITERATURE_STRESS_NOT_HARD_CAP"},
        "instrument": {
            "geometry_calibration_id": "synthetic",
            "clock_calibration_id": "synthetic",
            "exposure_calibration_id": "synthetic",
            "reference_annotation_id": "synthetic",
            "independent_reference": True},
        "nuisance": {k: "PASS" for k in (
            "geometry", "brightness", "missingness", "blur", "gaze",
            "glasses", "sampling", "clock", "rolling_shutter")},
        "reference": [],
    })


class TestE002473(unittest.TestCase):
    def test_frozen_designs_and_counts(self):
        r = run()
        self.assertEqual(r["n_rows"], 12)
        self.assertEqual(r["counts"], {
            "EXCLUSION_FEASIBLE_CONDITIONALLY": 7,
            "EXCLUSION_NOT_SUPPORTED": 5, "ABSTAIN_DESIGN": 0})
        self.assertFalse(r["physical_release_authorized"])

    def test_frozen_four_decisions(self):
        d = {(r["fps_nominal"], r["velocity_mm_s"]): r["design_decision"]
             for r in run()["rows"]}
        self.assertEqual(d[(30, 243)], "EXCLUSION_NOT_SUPPORTED")
        self.assertEqual(d[(240, 243)], "EXCLUSION_FEASIBLE_CONDITIONALLY")
        self.assertEqual(d[(240, 427)], "EXCLUSION_NOT_SUPPORTED")
        self.assertEqual(d[(300, 427)], "EXCLUSION_FEASIBLE_CONDITIONALLY")

    def test_independent_rational_thresholds(self):
        for fps, w, expected in ((30, 4, 50.656660412758),
                                 (240, 1, 369.863013698630),
                                 (300, 1, 446.280991735537)):
            v, _, valid = independent_rational_envelope(fps, w, 243)
            self.assertTrue(valid)
            self.assertAlmostEqual(float(v), expected, places=9)

    def test_minimum_margin_for_243_at_30fps(self):
        _, margin, _ = independent_rational_envelope(30, 4, 243)
        self.assertEqual(margin, Fraction(44173, 10000))
        self.assertGreater(float(margin), 4.4)

    def test_minimum_margin_for_coil_stress_at_240fps(self):
        _, margin, _ = independent_rational_envelope(240, 1, 427)
        self.assertEqual(margin, Fraction(34171, 30000))
        self.assertGreater(float(margin), 1.0)

    def test_no_literature_statistic_becomes_hard_bound(self):
        r = run()
        self.assertTrue(r["not_hard_physiological_velocity_caps"])
        self.assertTrue(r["not_new_raw_human_measurements"])
        self.assertTrue(all(not x["published_statistic_is_hard_cap"]
                            and not x["physical_release_authorized"]
                            and x["product_claim"] == "ABSTAIN_UNCALIBRATED"
                            for x in r["rows"]))

    def test_source_modality_mismatch_explicit(self):
        self.assertTrue(SOURCES["2013_voluntary_optical_mean_peak"]
                        ["directly_comparable_to_optical_peak"])
        for k in ("2019_spontaneous_mean", "2019_spontaneous_reported_max",
                  "1997_coil_secondary_table_mean_peak"):
            self.assertFalse(SOURCES[k]["directly_comparable_to_optical_peak"])

    def test_actual_evaluator_crosscheck_all_twelve_rows(self):
        for r in run()["rows"]:
            actual = evaluator_case(r["fps_nominal"], r["exposure_ms"],
                                    r["velocity_mm_s"])
            expected = ("EXCLUDED_CONDITIONALLY" if
                        r["design_decision"] == "EXCLUSION_FEASIBLE_CONDITIONALLY"
                        else "NOT_EXCLUDED")
            self.assertEqual(actual["decision"], expected, r)
            self.assertFalse(actual.get("physical_release_authorized", False))

    def test_reference_support_can_kill_numerically_feasible_design(self):
        r = design_case(fps=240, exposure_ms=4,
                        aperture_margin_mm=1, aperture_uncertainty_mm=.1,
                        clock_error_ms=.1, reference_exposure_ms=.2,
                        reference_clock_error_ms=.1,
                        hypothetical_velocity_mm_s=93)
        self.assertEqual(r["decision"], "ABSTAIN_DESIGN")
        self.assertFalse(r["physical_release_authorized"])

    def test_dimensionless_ratio_boundary(self):
        for row in run()["rows"]:
            ratio = row["velocity_to_critical_ratio"]
            self.assertEqual(row["design_decision"] ==
                             "EXCLUSION_FEASIBLE_CONDITIONALLY", ratio < 1)
            self.assertTrue(math.isfinite(ratio))


if __name__ == "__main__":
    unittest.main()
