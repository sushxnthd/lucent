#!/usr/bin/env python3
"""E002-472 frozen design experiment regressions; no human evidence."""
import math
import unittest

from e002_472_design_feasibility import design_case, frozen_matrix
from e002_456_prospective_gate import evaluate_interval


def case(**changes):
    args = dict(fps=60.0, exposure_ms=4.0, aperture_margin_mm=1.0,
                aperture_uncertainty_mm=0.1, clock_error_ms=0.1,
                reference_exposure_ms=0.2, reference_clock_error_ms=0.1,
                hypothetical_velocity_mm_s=100.0)
    args.update(changes)
    return design_case(**args)


class TestE002472(unittest.TestCase):
    def test_frozen_matrix_exact_counts(self):
        r = frozen_matrix()
        self.assertEqual(r["n_rows"], 44)
        self.assertEqual(r["counts"], {
            "EXCLUSION_FEASIBLE_CONDITIONALLY": 13,
            "EXCLUSION_NOT_SUPPORTED": 23,
            "ABSTAIN_DESIGN": 8})
        self.assertFalse(r["physical_release_authorized"])
        self.assertEqual(r["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_30_fps_100mm_s_is_not_excludable_for_frozen_margin(self):
        r = case(fps=30, hypothetical_velocity_mm_s=100)
        self.assertEqual(r["decision"], "EXCLUSION_NOT_SUPPORTED")
        self.assertLess(r["critical_hypothetical_velocity_mm_s"], 53)

    def test_240_fps_200mm_s_with_1ms_exposure_is_conditionally_feasible(self):
        r = case(fps=240, exposure_ms=1, hypothetical_velocity_mm_s=200)
        self.assertEqual(r["decision"], "EXCLUSION_FEASIBLE_CONDITIONALLY")
        self.assertFalse(r["hard_human_velocity_bound_established"])

    def test_shutter_timing_can_make_reference_unobservable(self):
        for fps, exposure in ((120, 8), (240, 4)):
            with self.subTest(fps=fps):
                r = case(fps=fps, exposure_ms=exposure,
                         hypothetical_velocity_mm_s=50)
                self.assertEqual(r["decision"], "ABSTAIN_DESIGN")
                self.assertEqual(r["reason"], "REFERENCE_SUPPORT_CANNOT_FIT")

    def test_strict_critical_velocity_equality(self):
        threshold = case()["critical_hypothetical_velocity_mm_s"]
        self.assertEqual(case(hypothetical_velocity_mm_s=threshold)["decision"],
                         "EXCLUSION_NOT_SUPPORTED")
        self.assertEqual(case(hypothetical_velocity_mm_s=threshold * 0.99)["decision"],
                         "EXCLUSION_FEASIBLE_CONDITIONALLY")
        self.assertEqual(case(hypothetical_velocity_mm_s=threshold * 1.01)["decision"],
                         "EXCLUSION_NOT_SUPPORTED")

    def test_nuisance_precision_monotonicity(self):
        base = case(hypothetical_velocity_mm_s=80)
        self.assertEqual(base["decision"], "EXCLUSION_FEASIBLE_CONDITIONALLY")
        for changes in (
            dict(exposure_ms=8), dict(clock_error_ms=0.8),
            dict(aperture_uncertainty_mm=0.4),
            dict(aperture_margin_mm=0.6),
            dict(hypothetical_velocity_mm_s=160)):
            r = case(hypothetical_velocity_mm_s=80, **changes) if (
                "hypothetical_velocity_mm_s" not in changes) else case(**changes)
            self.assertLessEqual(
                r["critical_hypothetical_velocity_mm_s"],
                base["critical_hypothetical_velocity_mm_s"] + 1e-10
            ) if "hypothetical_velocity_mm_s" not in changes else None
            self.assertNotEqual(r["decision"], "ABSTAIN_UNCALIBRATED")

    def test_unknown_shutter_abstains(self):
        r = case(shutter_kernel="unspecified")
        self.assertEqual(r["reason"], "UNSUPPORTED_SHUTTER")
        self.assertFalse(r["physical_release_authorized"])

    def test_support_only_shutter_is_more_conservative(self):
        a = case(hypothetical_velocity_mm_s=80)
        b = case(hypothetical_velocity_mm_s=80,
                 shutter_kernel="support_symmetric")
        self.assertLess(b["critical_hypothetical_velocity_mm_s"],
                        a["critical_hypothetical_velocity_mm_s"])

    def test_no_dark_gap_abstains(self):
        r = case(fps=240, exposure_ms=4.0, clock_error_ms=0.2)
        self.assertEqual(r["reason"], "NO_GUARANTEED_DARK_GAP")

    def test_overlapping_exposures_abstain(self):
        r = case(fps=240, exposure_ms=8)
        self.assertEqual(r["reason"], "OVERLAPPING_EXPOSURES")

    def test_nonfinite_negative_bool_and_zero_velocity_rejected(self):
        for field, val in (
            ("fps", 0), ("exposure_ms", -1), ("clock_error_ms", float("nan")),
            ("hypothetical_velocity_mm_s", 0), ("aperture_margin_mm", True),
            ("reference_exposure_ms", float("inf"))):
            with self.subTest(field=field):
                args = dict(fps=60, exposure_ms=4, aperture_margin_mm=1,
                            aperture_uncertainty_mm=.1, clock_error_ms=.1,
                            reference_exposure_ms=.2, reference_clock_error_ms=.1,
                            hypothetical_velocity_mm_s=100)
                args[field] = val
                with self.assertRaises(ValueError):
                    design_case(**args)

    def test_reference_evaluator_crosscheck_all_feasible_grid_rows(self):
        for row in frozen_matrix()["rows"]:
            if row["decision"] == "ABSTAIN_DESIGN":
                continue
            T = 1000 / row["fps_nominal"]
            V = row["hypothetical_velocity_mm_s"]
            w = row["exposure_ms"]
            inp = {
                "closure_threshold_mm": 2.0,
                "endpoint_aperture_mm": [3.0, 3.0],
                "endpoint_uncertainty_mm": [0.1, 0.1],
                "endpoint_time_ms": [0.0, T],
                "shutter": {"kernel": "uniform_symmetric", "exposure_ms": w,
                            "clock_error_ms": 0.1, "reference_exposure_ms": 0.2,
                            "reference_clock_error_ms": 0.1},
                "velocity": {"limit_mm_s": V, "provenance": "ILLUSTRATIVE"},
                "instrument": {
                    "geometry_calibration_id": "synthetic",
                    "clock_calibration_id": "synthetic",
                    "exposure_calibration_id": "synthetic",
                    "reference_annotation_id": "synthetic",
                    "independent_reference": True},
                "nuisance": {k: "PASS" for k in (
                    "geometry", "brightness", "missingness", "blur",
                    "gaze", "glasses", "sampling", "clock", "rolling_shutter")},
                "reference": [],
            }
            actual = evaluate_interval(inp)
            expected = ("EXCLUDED_CONDITIONALLY" if
                        row["decision"] == "EXCLUSION_FEASIBLE_CONDITIONALLY"
                        else "NOT_EXCLUDED")
            self.assertEqual(actual["decision"], expected,
                             (row["fps_nominal"], w, V, actual))


if __name__ == "__main__":
    unittest.main()
