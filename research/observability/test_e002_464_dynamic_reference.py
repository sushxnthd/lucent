#!/usr/bin/env python3
"""E002-464 adversarial tests. All traces are synthetic, never physical."""
import copy
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e002_463_encoder_reference import evaluate_encoder
from e002_464_dynamic_reference import (
    dynamic_fixture, evaluate_dynamic_encoder, synthetic_run,
)


class DynamicReferenceTests(unittest.TestCase):
    def test_delayed_report_is_legacy_false_witness(self):
        case, encoder = dynamic_fixture(past=1.4)
        old = evaluate_encoder(case, encoder)
        new = evaluate_dynamic_encoder(case, encoder)
        self.assertTrue(old["joint_falsification"])
        self.assertEqual(old["reference"], "WITNESSED_CROSSING")
        self.assertEqual(new["reference"], "REFERENCE_UNRESOLVED")
        self.assertFalse(new["joint_falsification"])
        self.assertFalse(new["physical_release_authorized"])

    def test_declared_bounded_positive_remains_usable(self):
        case, encoder = dynamic_fixture(past=0.1)
        r = evaluate_dynamic_encoder(case, encoder)
        self.assertEqual(r["reference"], "WITNESSED_CROSSING")
        self.assertTrue(r["joint_falsification"])
        self.assertEqual(r["positive_witness_semantics"],
                         "EXISTENTIAL_IN_INFLUENCE_SUPPORT")
        self.assertFalse(r["dynamic_response_independently_verified"])

    def test_signed_kernel_false_reading(self):
        # Signed weights 2,-1: 2*2.20 - 2.45 = 1.95 < 2.0,
        # although BOTH actual physical apertures remain above threshold.
        self.assertAlmostEqual(2 * 2.2 - 2.45, 1.95)
        case, encoder = dynamic_fixture(signed=True)
        self.assertTrue(evaluate_encoder(case, encoder)["joint_falsification"])
        r = evaluate_dynamic_encoder(case, encoder)
        self.assertEqual(r["decision"], "ABSTAIN")
        self.assertEqual(r["reference"], "REFERENCE_UNRESOLVED")
        self.assertFalse(r["joint_falsification"])

    def test_no_response_kernel_declaration(self):
        case, encoder = dynamic_fixture()
        del encoder["provenance"]["response_nonnegative_unit_mass_declared"]
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_no_dynamic_support_calibration(self):
        case, encoder = dynamic_fixture()
        encoder["provenance"]["dynamic_support_calibration_id"] = ""
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_no_kernel_calibration(self):
        case, encoder = dynamic_fixture()
        encoder["provenance"]["response_kernel_calibration_id"] = ""
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_missing_memory_bound(self):
        case, encoder = dynamic_fixture()
        del encoder["provenance"]["max_past_memory_ms"]
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_missing_future_lead_bound(self):
        case, encoder = dynamic_fixture()
        del encoder["provenance"]["max_future_lead_ms"]
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["decision"], "ABSTAIN")

    def test_past_boundary_strict(self):
        case, encoder = dynamic_fixture(past=0.83)
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")
        case, encoder = dynamic_fixture(past=0.82)
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["reference"],
                         "WITNESSED_CROSSING")

    def test_future_boundary_strict(self):
        case, encoder = dynamic_fixture(future=1.33)
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")
        case, encoder = dynamic_fixture(future=1.32)
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["reference"],
                         "WITNESSED_CROSSING")

    def test_acquisition_support_expands_influence(self):
        case, encoder = dynamic_fixture(past=0.82)
        encoder["provenance"]["sample_support_ms"] = 0.1
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")

    def test_clock_error_expands_influence(self):
        case, encoder = dynamic_fixture(past=0.82)
        encoder["provenance"]["max_time_error_ms"] = 0.04
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")

    def test_bad_numeric_bounds_fail_closed(self):
        for bad in (float("nan"), float("inf"), -1, True, "0.1"):
            case, encoder = dynamic_fixture()
            encoder["provenance"]["max_past_memory_ms"] = bad
            self.assertEqual(evaluate_dynamic_encoder(case, encoder)["decision"],
                             "ABSTAIN")

    def test_missing_samples_not_negative_truth(self):
        case, encoder = dynamic_fixture()
        encoder["samples"] = []
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["reference"],
                         "REFERENCE_UNRESOLVED")

    def test_open_world_never_certifies_negative(self):
        case, encoder = dynamic_fixture(closed=False)
        r = evaluate_dynamic_encoder(case, encoder)
        self.assertEqual(r["reference"], "REFERENCE_UNRESOLVED")
        self.assertFalse(r["joint_falsification"])

    def test_bad_nuisance_blocks_witness(self):
        case, encoder = dynamic_fixture()
        case["nuisance"]["blur"] = "UNKNOWN"
        self.assertEqual(evaluate_dynamic_encoder(case, encoder)["decision"],
                         "ABSTAIN")

    def test_monotone_witness_coverage_sweep(self):
        case, encoder = dynamic_fixture()
        admitted = 0
        for i in range(201):
            for j in range(201):
                encoder["provenance"]["max_past_memory_ms"] = i / 100.0
                encoder["provenance"]["max_future_lead_ms"] = j / 100.0
                r = evaluate_dynamic_encoder(case, encoder)
                admitted += (r["reference"] == "WITNESSED_CROSSING")
                self.assertFalse(r["physical_release_authorized"])
        self.assertEqual(admitted, 11039)

    def test_synthetic_aggregate(self):
        r = synthetic_run()
        self.assertEqual(r["real_human_measurements"], 0)
        self.assertEqual(r["real_physical_encoder_measurements"], 0)
        self.assertEqual(r["product_claim"], "ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    unittest.main()
