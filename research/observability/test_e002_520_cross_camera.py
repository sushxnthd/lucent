import math
import unittest
from copy import deepcopy

from e002_520_cross_camera import evaluate, VERSION


def fixture():
    return {
        "version": VERSION,
        "gaps": [{
            "id": "g1",
            "prediction": "EXCLUDE",
            "left_end_max_ms": 10,
            "right_start_min_ms": 30,
            "ordinary_closure_threshold": 0.20,
            "references": [{
                "id": "r1",
                "start_min_ms": 12,
                "end_max_ms": 20,
                "anatomy": "CLOSED_WITNESS",
                "two_independent_raters": True,
                "radiometry_linear_valid": True,
                "clock_valid": True,
                "native_provenance_valid": True,
                "geometry_transport_valid": True,
                "nuisance_clear": True,
                "reference_mean_aperture_upper": 0.19,
                "transport_scale_upper": 1.0,
                "transport_offset_upper": 0.0,
            }],
        }],
    }


class TestCrossCameraTransport(unittest.TestCase):
    def check(self, x, decision):
        out = evaluate(x)
        self.assertEqual(out["decisions"][0]["decision"], decision)
        self.assertFalse(out["verified_no_hidden_closure"])
        self.assertFalse(out["human_or_instrument_provenance_authenticated_by_code"])
        self.assertFalse(out["legacy_e002_519_witness_admissible_without_transport"])
        self.assertEqual(out["product"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(out["release"], "BLOCKED")
        return out

    def test_world_a_transport_certifies_conditional_witness(self):
        out = self.check(fixture(), "FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS")
        self.assertEqual(out["decisions"][0]["conditional_witness_reference_id"], "r1")

    def test_world_b_same_anatomical_label_not_a_witness(self):
        x = fixture()
        x["gaps"][0]["references"][0]["transport_scale_upper"] = 1.2
        self.check(x, "UNKNOWN")

    def test_threshold_equality_is_sufficient(self):
        x = fixture()
        x["gaps"][0]["references"][0]["reference_mean_aperture_upper"] = 0.20
        self.check(x, "FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS")

    def test_offset_uncertainty_blocks_witness(self):
        x = fixture()
        x["gaps"][0]["references"][0]["transport_offset_upper"] = 0.02
        self.check(x, "UNKNOWN")

    def test_missing_numeric_transport_blocks_witness(self):
        x = fixture()
        del x["gaps"][0]["references"][0]["transport_scale_upper"]
        self.check(x, "UNKNOWN")

    def test_unverified_geometry_blocks_witness(self):
        x = fixture()
        x["gaps"][0]["references"][0]["geometry_transport_valid"] = False
        self.check(x, "UNKNOWN")

    def test_non_linear_photometry_blocks_witness(self):
        x = fixture()
        x["gaps"][0]["references"][0]["radiometry_linear_valid"] = False
        self.check(x, "UNKNOWN")

    def test_no_independent_raters_blocks_witness(self):
        x = fixture()
        x["gaps"][0]["references"][0]["two_independent_raters"] = False
        self.check(x, "UNKNOWN")

    def test_clock_uncertainty_blocks_witness(self):
        x = fixture()
        x["gaps"][0]["references"][0]["clock_valid"] = False
        self.check(x, "UNKNOWN")

    def test_boundary_touch_blocks_witness(self):
        x = fixture()
        x["gaps"][0]["references"][0]["start_min_ms"] = 10
        self.check(x, "UNKNOWN")

    def test_open_frame_cannot_verify_negative(self):
        x = fixture()
        x["gaps"][0]["references"][0]["anatomy"] = "OPEN_OBSERVED"
        self.check(x, "REFERENCE_CENSORED_NOT_FALSIFIED")

    def test_empty_reference_is_unknown(self):
        x = fixture()
        x["gaps"][0]["references"] = []
        self.check(x, "UNKNOWN")

    def test_abstention_not_testable(self):
        x = fixture()
        x["gaps"][0]["prediction"] = "ABSTAIN"
        self.check(x, "NOT_TESTABLE")

    def test_zero_blind_gap_not_testable(self):
        x = fixture()
        x["gaps"][0]["right_start_min_ms"] = 10
        self.check(x, "NOT_TESTABLE")

    def test_qualified_witness_dominates_ambiguous_reference(self):
        x = fixture()
        r = deepcopy(x["gaps"][0]["references"][0])
        r["id"] = "r2"
        r["anatomy"] = "UNKNOWN"
        x["gaps"][0]["references"].append(r)
        self.check(x, "FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS")

    def test_duplicate_gap_fails_closed(self):
        x = fixture()
        x["gaps"].append(deepcopy(x["gaps"][0]))
        with self.assertRaisesRegex(ValueError, "INVALID_GAP_ID"):
            evaluate(x)

    def test_duplicate_reference_fails_closed(self):
        x = fixture()
        x["gaps"][0]["references"].append(deepcopy(x["gaps"][0]["references"][0]))
        with self.assertRaisesRegex(ValueError, "INVALID_REFERENCE_ID"):
            evaluate(x)

    def test_negative_scale_fails_closed(self):
        x = fixture()
        x["gaps"][0]["references"][0]["transport_scale_upper"] = -1
        with self.assertRaisesRegex(ValueError, "NEGATIVE_TRANSPORT_SCALE_UPPER"):
            evaluate(x)

    def test_nonfinite_bound_fails_closed(self):
        x = fixture()
        x["gaps"][0]["references"][0]["reference_mean_aperture_upper"] = math.nan
        with self.assertRaisesRegex(ValueError, "INVALID_REFERENCE_MEAN_APERTURE_UPPER"):
            evaluate(x)

    def test_boolean_threshold_fails_closed(self):
        x = fixture()
        x["gaps"][0]["ordinary_closure_threshold"] = True
        with self.assertRaisesRegex(ValueError, "INVALID_THRESHOLD"):
            evaluate(x)

    def test_missing_attestation_fails_closed(self):
        x = fixture()
        del x["gaps"][0]["references"][0]["native_provenance_valid"]
        with self.assertRaisesRegex(ValueError, "INVALID_REFERENCE_FLAGS"):
            evaluate(x)

    def test_no_numeric_false_clearance_with_legacy_category(self):
        x = fixture()
        ref = x["gaps"][0]["references"][0]
        del ref["reference_mean_aperture_upper"]
        del ref["transport_scale_upper"]
        del ref["transport_offset_upper"]
        self.check(x, "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
