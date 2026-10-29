"""E002-526 adversarial regression. All fixtures synthetic, no real participants."""
import copy
import unittest

from e002_519_reference_censoring import evaluate as legacy_evaluate
from e002_520_cross_camera import evaluate as quantitative_evaluate
from e002_526_locked_transport import commitment, verify_and_evaluate

NONCE = "0123456789abcdef" * 4


def manifest():
    return {"version": "E002-526-v1", "evaluator": "E002-520-v1",
            "nonce_hex": NONCE, "gaps": [
                {"id": "g1", "participant": "synthetic_p1", "session": "synthetic_s1",
                 "prediction": "EXCLUDE", "left_end_max_ms": 10,
                 "right_start_min_ms": 30, "ordinary_closure_threshold": 0.20},
                {"id": "g2", "participant": "synthetic_p2", "session": "synthetic_s2",
                 "prediction": "ABSTAIN", "left_end_max_ms": 40,
                 "right_start_min_ms": 60, "ordinary_closure_threshold": 0.20}
            ]}


def reference():
    return {"id": "r1", "start_min_ms": 12, "end_max_ms": 20,
            "anatomy": "CLOSED_WITNESS", "two_independent_raters": True,
            "radiometry_linear_valid": True, "clock_valid": True,
            "native_provenance_valid": True, "geometry_transport_valid": True,
            "nuisance_clear": True, "reference_mean_aperture_upper": 0.19,
            "transport_scale_upper": 1.2, "transport_offset_upper": 0.0}


def evidence(m=None):
    m = m or manifest()
    gaps = [dict(g, references=[]) for g in m["gaps"]]
    gaps[0]["references"] = [reference()]
    return {"version": "E002-520-v1", "gaps": gaps}


class PredicateLockedStudy(unittest.TestCase):
    def setUp(self):
        self.m = manifest()
        self.digest = commitment(self.m)
        self.e = evidence(self.m)

    def run_locked(self, m=None, e=None, digest=None):
        return verify_and_evaluate(m if m is not None else self.m,
                                   digest if digest is not None else self.digest,
                                   e if e is not None else self.e)

    def test_qualitative_legacy_false_falsification(self):
        legacy = copy.deepcopy(self.e)
        legacy["version"] = "E002-519-v1"
        for g in legacy["gaps"]:
            del g["ordinary_closure_threshold"]
            for r in g["references"]:
                r["photometry_valid"] = r.pop("radiometry_linear_valid")
        self.assertEqual(legacy_evaluate(legacy)["counts"]["FALSIFIED_BY_REFERENCE_WITNESS"], 1)
        self.assertEqual(quantitative_evaluate(self.e)["counts"]["UNKNOWN"], 1)

    def test_locked_original_predicate_is_unknown(self):
        out = self.run_locked()
        self.assertEqual(out["counts"]["UNKNOWN"], 1)
        self.assertEqual(out["counts"]["NOT_TESTABLE"], 1)
        self.assertEqual(out["counts"]["FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS"], 0)
        self.assertFalse(out["human_or_camera_provenance_authenticated_by_code"])
        self.assertEqual(out["release"], "BLOCKED")

    def test_posthoc_threshold_switch_reverses_unlocked_outcome(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["ordinary_closure_threshold"] = 0.23
        self.assertEqual(quantitative_evaluate(e)["counts"]["FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS"], 1)
        with self.assertRaisesRegex(ValueError, "POSTHOC_TIMING_OR_THRESHOLD"):
            self.run_locked(e=e)

    def test_genuine_frozen_threshold_023_is_conditionally_falsified(self):
        m = manifest()
        m["gaps"][0]["ordinary_closure_threshold"] = 0.23
        e = evidence(m)
        out = self.run_locked(m=m, e=e, digest=commitment(m))
        self.assertEqual(out["counts"]["FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS"], 1)
        self.assertFalse(out["human_or_camera_provenance_authenticated_by_code"])

    def test_missing_transport_remains_unknown(self):
        e = copy.deepcopy(self.e)
        del e["gaps"][0]["references"][0]["transport_scale_upper"]
        self.assertEqual(self.run_locked(e=e)["counts"]["UNKNOWN"], 1)

    def test_false_clock_or_geometry_flag_remains_unknown(self):
        for flag in ("clock_valid", "geometry_transport_valid", "native_provenance_valid",
                     "radiometry_linear_valid", "nuisance_clear", "two_independent_raters"):
            e = copy.deepcopy(self.e)
            e["gaps"][0]["references"][0][flag] = False
            self.assertEqual(self.run_locked(e=e)["counts"]["UNKNOWN"], 1)

    def test_open_observed_never_validates_absence(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"][0]["anatomy"] = "OPEN_OBSERVED"
        out = self.run_locked(e=e)
        self.assertEqual(out["counts"]["REFERENCE_CENSORED_NOT_FALSIFIED"], 1)
        self.assertFalse(out["verified_no_hidden_closure"])

    def test_missing_reference_is_unknown(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"] = []
        self.assertEqual(self.run_locked(e=e)["counts"]["UNKNOWN"], 1)

    def test_prediction_switch_is_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["prediction"] = "ABSTAIN"
        with self.assertRaisesRegex(ValueError, "POSTHOC"):
            self.run_locked(e=e)

    def test_participant_and_session_switch_are_rejected(self):
        for field in ("participant", "session"):
            e = copy.deepcopy(self.e)
            e["gaps"][0][field] = "other"
            with self.assertRaisesRegex(ValueError, "POSTHOC"):
                self.run_locked(e=e)

    def test_timing_change_is_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["right_start_min_ms"] = 31
        with self.assertRaisesRegex(ValueError, "POSTHOC"):
            self.run_locked(e=e)

    def test_missing_or_added_gap_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"].pop()
        with self.assertRaisesRegex(ValueError, "DENOMINATOR"):
            self.run_locked(e=e)
        e = copy.deepcopy(self.e)
        e["gaps"].append(dict(e["gaps"][0], id="g3"))
        with self.assertRaisesRegex(ValueError, "DENOMINATOR"):
            self.run_locked(e=e)

    def test_duplicate_gap_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"][1]["id"] = "g1"
        with self.assertRaisesRegex(ValueError, "DUPLICATE"):
            self.run_locked(e=e)

    def test_commitment_mismatch_and_invalid_digest(self):
        with self.assertRaisesRegex(ValueError, "COMMITMENT_MISMATCH"):
            self.run_locked(digest="a" * 64)
        with self.assertRaisesRegex(ValueError, "INVALID_PUBLISHED"):
            self.run_locked(digest="invalid")

    def test_nonce_and_evaluator_binding(self):
        m = copy.deepcopy(self.m)
        m["nonce_hex"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "COMMITMENT_MISMATCH"):
            self.run_locked(m=m)
        m = copy.deepcopy(self.m)
        m["evaluator"] = "E002-519-v1"
        with self.assertRaisesRegex(ValueError, "INVALID_EVALUATOR_VERSION"):
            commitment(m)

    def test_invalid_threshold_or_numeric_bool_rejected(self):
        for val in (0, 1, True, float("nan"), float("inf"), -0.1):
            m = copy.deepcopy(self.m)
            m["gaps"][0]["ordinary_closure_threshold"] = val
            with self.assertRaises(ValueError):
                commitment(m)

    def test_manifest_duplicate_ids_rejected(self):
        m = copy.deepcopy(self.m)
        m["gaps"][1]["id"] = "g1"
        with self.assertRaisesRegex(ValueError, "DUPLICATE"):
            commitment(m)

    def test_extra_evidence_fields_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["extra"] = True
        with self.assertRaisesRegex(ValueError, "SCHEMA"):
            self.run_locked(e=e)

    def test_key_order_independent(self):
        m = copy.deepcopy(self.m)
        m["gaps"] = [dict(reversed(list(g.items()))) for g in m["gaps"]]
        self.assertEqual(commitment(dict(reversed(list(m.items())))), self.digest)

    def test_no_human_data_in_fixture(self):
        self.assertTrue(all(g["participant"].startswith("synthetic_") for g in self.m["gaps"]))


if __name__ == "__main__":
    unittest.main()
