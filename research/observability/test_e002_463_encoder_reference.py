#!/usr/bin/env python3
"""E002-463 adversarial instrument-gate tests; synthetic fixtures only."""
import copy
import json
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e002_463_encoder_reference import (
    evaluate_encoder, synthetic_fixture, synthetic_run,
)


class EncoderWitnessTests(unittest.TestCase):
    def test_frozen_closed_world_falsifies_intentionally_wrong_cap(self):
        case, encoder = synthetic_fixture(True)
        r = evaluate_encoder(case, encoder)
        self.assertEqual(r["prediction"], "EXCLUDED_CONDITIONALLY")
        self.assertEqual(r["reference"], "WITNESSED_CROSSING")
        self.assertTrue(r["joint_falsification"])
        self.assertFalse(r["physical_release_authorized"])

    def test_frozen_open_world_is_unresolved_not_negative_truth(self):
        case, encoder = synthetic_fixture(False)
        r = evaluate_encoder(case, encoder)
        self.assertEqual(r["reference"], "REFERENCE_UNRESOLVED")
        self.assertFalse(r["joint_falsification"])
        self.assertEqual(r["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertEqual(r["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_frozen_shutter_indistinguishability(self):
        result = synthetic_run()
        self.assertTrue(result["shutter_camera_positive_negative_identical"])
        self.assertGreater(result["positive_subthreshold_duration_ms"], 0)
        self.assertEqual(result["real_human_measurements"], 0)

    def test_dark_gap_boundary_equality_is_unresolved(self):
        case, encoder = synthetic_fixture(True)
        encoder["samples"] = [{"time_ms": 0.17, "aperture_mm": 1.95,
                               "quality": "PASS"}]
        self.assertEqual(evaluate_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")

    def test_reference_in_ordinary_exposure_is_not_dark_gap_witness(self):
        case, encoder = synthetic_fixture(True)
        case["shutter"]["exposure_ms"] = 2.2
        self.assertEqual(evaluate_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")

    def test_clock_uncertainty_can_withdraw_witness(self):
        case, encoder = synthetic_fixture(True)
        case["shutter"]["clock_error_ms"] = 0.95
        self.assertEqual(evaluate_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")

    def test_encoder_temporal_support_can_withdraw_witness(self):
        case, encoder = synthetic_fixture(True)
        encoder["provenance"]["sample_support_ms"] = 1.8
        self.assertEqual(evaluate_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")

    def test_nonmonotone_encoder_times_fail_closed(self):
        case, encoder = synthetic_fixture(True)
        encoder["samples"].append(copy.deepcopy(encoder["samples"][0]))
        self.assertEqual(evaluate_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_missing_source_hash_fails_closed(self):
        case, encoder = synthetic_fixture(True)
        encoder["provenance"]["raw_trace_sha256"] = "synthetic"
        self.assertEqual(evaluate_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_missing_independence_fails_closed(self):
        case, encoder = synthetic_fixture(True)
        encoder["provenance"]["independent_position_instrument"] = False
        self.assertEqual(evaluate_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_unknown_encoder_bandwidth_fails_closed(self):
        case, encoder = synthetic_fixture(True)
        encoder["provenance"]["bandwidth_calibration_id"] = ""
        self.assertEqual(evaluate_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_quality_failure_fails_closed(self):
        case, encoder = synthetic_fixture(True)
        encoder["samples"][0]["quality"] = "OCCLUDED"
        self.assertEqual(evaluate_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_nonfinite_and_boolean_inputs_fail_closed(self):
        for invalid in (float("nan"), float("inf"), -1.0, True):
            case, encoder = synthetic_fixture(True)
            encoder["provenance"]["max_time_error_ms"] = invalid
            self.assertEqual(evaluate_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_preexisting_reference_rejected(self):
        case, encoder = synthetic_fixture(True)
        case["reference"] = [{"time_ms": 1.0, "aperture_mm": 1.0}]
        self.assertEqual(evaluate_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_inconsistent_ordinary_measurement_rejected(self):
        case, encoder = synthetic_fixture(True)
        case["endpoint_aperture_mm"][1] = 4.0
        self.assertEqual(evaluate_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_no_encoder_samples_not_negative_truth(self):
        case, encoder = synthetic_fixture(True)
        encoder["samples"] = []
        self.assertEqual(evaluate_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")

    def test_no_personal_identifiers_in_result(self):
        case, encoder = synthetic_fixture(True)
        case["participant_id"] = "PRIVATE_PARTICIPANT"
        case["interval_id"] = "PRIVATE_INTERVAL"
        output = json.dumps(evaluate_encoder(case, encoder))
        self.assertNotIn("PRIVATE_PARTICIPANT", output)
        self.assertNotIn("PRIVATE_INTERVAL", output)
        self.assertNotIn("synthetic-only", output)

    def test_nuisance_unknown_prevents_positive_claim(self):
        case, encoder = synthetic_fixture(True)
        case["nuisance"]["glasses"] = "UNKNOWN"
        self.assertEqual(evaluate_encoder(case, encoder)["decision"], "ABSTAIN")


if __name__ == "__main__":
    unittest.main()
