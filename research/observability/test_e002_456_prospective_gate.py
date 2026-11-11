#!/usr/bin/env python3
"""E002-456 independent synthetic/adversarial regression suite; NO human labels."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e002_456_prospective_gate import evaluate_interval, evaluate_dataset


def fixture():
    return {
        "interval_id": "synthetic-1", "participant_id": "opaque-A",
        "split": "development", "closure_threshold_mm": 2.0,
        "endpoint_aperture_mm": [3.0, 3.0],
        "endpoint_uncertainty_mm": [0.0, 0.0],
        "endpoint_time_ms": [0.0, 10.0],
        "shutter": {"kernel": "uniform_symmetric",
                    "exposure_ms": 0.0, "clock_error_ms": 0.0,
                    "reference_exposure_ms": 0.2, "reference_clock_error_ms": 0.1},
        "velocity": {"limit_mm_s": 100.0, "provenance": "ILLUSTRATIVE"},
        "instrument": {
            "geometry_calibration_id": "synthetic-geometry",
            "clock_calibration_id": "synthetic-clock",
            "exposure_calibration_id": "synthetic-exposure",
            "reference_annotation_id": "synthetic-reference",
            "independent_reference": True,
        },
        "nuisance": {k: "PASS" for k in (
            "geometry", "brightness", "missingness", "blur", "gaze",
            "glasses", "sampling", "clock", "rolling_shutter")},
        "reference": [{"time_ms": 5.0, "aperture_mm": 2.8,
                       "uncertainty_mm": 0.0, "quality": "PASS"}],
    }


class ProspectiveGateTests(unittest.TestCase):
    def test_sharp_instantaneous_conditional_exclusion(self):
        r = evaluate_interval(fixture())
        self.assertEqual(r["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertAlmostEqual(r["lower_envelope_mm"], 2.5)
        self.assertEqual(r["reference"], "NO_WITNESSED_CROSSING")

    def test_witness_falsifies_joint_assumptions(self):
        c = fixture()
        c["reference"][0]["aperture_mm"] = 1.8
        r = evaluate_interval(c)
        self.assertTrue(r["joint_falsification"])
        self.assertEqual(r["reference"], "WITNESSED_CROSSING")

    def test_large_velocity_makes_closure_not_excluded(self):
        c = fixture()
        c["velocity"]["limit_mm_s"] = 300
        self.assertEqual(evaluate_interval(c)["decision"], "NOT_EXCLUDED")

    def test_equality_does_not_exclude(self):
        c = fixture()
        c["velocity"]["limit_mm_s"] = 200
        self.assertEqual(evaluate_interval(c)["decision"], "NOT_EXCLUDED")

    def test_uniform_shutter_penalty(self):
        c = fixture()
        c["shutter"]["exposure_ms"] = 2
        self.assertAlmostEqual(evaluate_interval(c)["lower_envelope_mm"], 2.45)

    def test_unknown_kernel_support_more_conservative(self):
        c = fixture()
        c["shutter"]["exposure_ms"] = 2
        c["shutter"]["kernel"] = "support_symmetric"
        self.assertAlmostEqual(evaluate_interval(c)["lower_envelope_mm"], 2.4)

    def test_clock_uncertainty_monotonic(self):
        c = fixture()
        c["shutter"]["clock_error_ms"] = 1
        self.assertAlmostEqual(evaluate_interval(c)["lower_envelope_mm"], 2.4)

    def test_exposure_overlap_abstains(self):
        c = fixture()
        c["shutter"]["exposure_ms"] = 11
        self.assertEqual(evaluate_interval(c)["reason"], "OVERLAPPING_EXPOSURES")

    def test_nuisance_fail_closed(self):
        for key in fixture()["nuisance"]:
            c = fixture()
            c["nuisance"][key] = "UNKNOWN"
            self.assertEqual(evaluate_interval(c)["reason"], "NUISANCE_NOT_CLEARED")

    def test_empirical_max_not_a_hard_bound(self):
        c = fixture()
        c["velocity"]["provenance"] = "EMPIRICAL_SAMPLE_MAX"
        self.assertEqual(evaluate_interval(c)["reason"],
                         "VELOCITY_CAP_PROVENANCE_INVALID")

    def test_missing_reference_not_counted_as_open(self):
        c = fixture()
        c["reference"] = []
        r = evaluate_interval(c)
        self.assertEqual(r["reference"], "REFERENCE_INCOMPLETE")
        self.assertFalse(r["joint_falsification"])

    def test_uncertain_reference_not_a_witness(self):
        c = fixture()
        c["reference"][0].update(aperture_mm=2.0, uncertainty_mm=0.2)
        r = evaluate_interval(c)
        self.assertEqual(r["reference"], "REFERENCE_INDETERMINATE")
        self.assertFalse(r["joint_falsification"])

    def test_bad_reference_not_silently_used(self):
        c = fixture()
        c["reference"][0]["time_ms"] = 10
        self.assertEqual(evaluate_interval(c)["reason"], "REFERENCE_NOT_INTERIOR")
        c = fixture()
        c["reference"][0]["quality"] = "BLURRED"
        self.assertEqual(evaluate_interval(c)["reference"], "REFERENCE_INCOMPLETE")

    def test_inconsistent_endpoints_abstain(self):
        c = fixture()
        c["endpoint_aperture_mm"] = [3, 5]
        self.assertEqual(evaluate_interval(c)["reason"],
                         "MODEL_INCONSISTENT_ENDPOINTS")

    def test_no_self_attested_calibration_promotes_release(self):
        c = fixture()
        c["velocity"]["provenance"] = "EXTERNAL_HARD_BOUND_DECLARED"
        r = evaluate_dataset({"schema_version": "E002-456-v1", "intervals": [c]})
        self.assertFalse(r["physical_release_authorized"])
        self.assertFalse(r["external_hard_bound_verified_by_this_program"])
        self.assertEqual(r["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_participant_leakage_rejected(self):
        c = fixture()
        h = copy.deepcopy(c)
        h["interval_id"] = "synthetic-2"
        h["split"] = "holdout"
        with self.assertRaises(ValueError):
            evaluate_dataset({"schema_version": "E002-456-v1",
                              "intervals": [c, h]})

    def test_aggregate_has_no_private_identifiers(self):
        c = fixture()
        h = copy.deepcopy(c)
        h.update(interval_id="synthetic-2", participant_id="opaque-B",
                 split="holdout")
        h["reference"][0]["aperture_mm"] = 1.0
        r = evaluate_dataset({"schema_version": "E002-456-v1",
                              "intervals": [c, h]})
        self.assertEqual(r["counts"]["holdout"]["FALSIFIED_JOINT_ASSUMPTIONS"], 1)
        text = json.dumps(r)
        self.assertNotIn("opaque-", text)
        self.assertNotIn("synthetic-", text)

    def test_nonfinite_or_boolean_inputs_abstain(self):
        for invalid in (float("nan"), float("inf"), True, -1):
            c = fixture()
            c["endpoint_uncertainty_mm"][0] = invalid
            self.assertEqual(evaluate_interval(c)["decision"], "ABSTAIN")

    def test_reference_shutter_must_be_robustly_interior(self):
        c = fixture()
        c["reference"][0].update(time_ms=0.1, aperture_mm=1.0)
        self.assertEqual(evaluate_interval(c)["reference"], "REFERENCE_INCOMPLETE")
        self.assertFalse(evaluate_interval(c)["joint_falsification"])

    def test_reference_clock_support_too_wide_abstains(self):
        c = fixture()
        c["shutter"]["reference_exposure_ms"] = 10
        self.assertEqual(evaluate_interval(c)["reason"], "REFERENCE_TIME_SUPPORT_TOO_WIDE")

    def test_unknown_shutter_abstains(self):
        c = fixture()
        c["shutter"]["kernel"] = "rolling_unknown"
        self.assertEqual(evaluate_interval(c)["reason"], "UNKNOWN_SHUTTER")


if __name__ == "__main__":
    unittest.main()
