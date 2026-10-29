"""E002-527 frozen adversarial tests; entirely artificial observations."""
import copy
import unittest

from e002_526_locked_transport import commitment as old_commitment, verify_and_evaluate as old_verify
from e002_527_calibration_lock import commitment, verify_and_evaluate


def fixture(scale=1.2):
    m = {
        "version": "E002-527-v1", "evaluator": "E002-520-v1",
        "nonce_hex": "0123456789abcdef" * 4,
        "gaps": [{
            "id": "g1", "participant": "synthetic_p1", "session": "synthetic_s1",
            "prediction": "EXCLUDE", "left_end_max_ms": 10,
            "right_start_min_ms": 30, "ordinary_closure_threshold": 0.20,
            "calibration_id": "prelabel_cal_01", "transport_scale_upper": scale,
            "transport_offset_upper": 0.0,
        }, {
            "id": "g2", "participant": "synthetic_p2", "session": "synthetic_s2",
            "prediction": "ABSTAIN", "left_end_max_ms": 40,
            "right_start_min_ms": 60, "ordinary_closure_threshold": 0.20,
            "calibration_id": "prelabel_cal_02", "transport_scale_upper": scale,
            "transport_offset_upper": 0.0,
        }],
    }
    ref = {
        "id": "r1", "start_min_ms": 12, "end_max_ms": 20,
        "anatomy": "CLOSED_WITNESS", "two_independent_raters": True,
        "radiometry_linear_valid": True, "clock_valid": True,
        "native_provenance_valid": True, "geometry_transport_valid": True,
        "nuisance_clear": True, "reference_mean_aperture_upper": 0.19,
        "transport_scale_upper": scale, "transport_offset_upper": 0.0,
        "calibration_id": "prelabel_cal_01",
    }
    e = {"version": "E002-520-v1",
         "gaps": [dict(g, references=[copy.deepcopy(ref)] if i == 0 else [])
                  for i, g in enumerate(m["gaps"])]}
    return m, e


def to_old(m, e):
    old_m = copy.deepcopy(m)
    old_m["version"] = "E002-526-v1"
    for g in old_m["gaps"]:
        for key in ("calibration_id", "transport_scale_upper", "transport_offset_upper"):
            del g[key]
    old_e = copy.deepcopy(e)
    for g in old_e["gaps"]:
        for key in ("calibration_id", "transport_scale_upper", "transport_offset_upper"):
            del g[key]
        for r in g["references"]:
            del r["calibration_id"]
    return old_m, old_e


class CalibrationLockTest(unittest.TestCase):
    def setUp(self):
        self.m, self.e = fixture()
        self.digest = commitment(self.m)

    def evaluate(self, m=None, e=None, digest=None):
        return verify_and_evaluate(m if m is not None else self.m,
                                   digest if digest is not None else self.digest,
                                   e if e is not None else self.e)

    def test_old_digest_allows_postlabel_scale_selection(self):
        old_m, old_e = to_old(self.m, self.e)
        digest = old_commitment(old_m)
        self.assertEqual(old_verify(old_m, digest, old_e)["counts"]["UNKNOWN"], 1)
        old_e["gaps"][0]["references"][0]["transport_scale_upper"] = 1.0
        self.assertEqual(old_verify(old_m, digest, old_e)["counts"]["FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS"], 1)
        self.assertEqual(old_commitment(old_m), digest)

    def test_new_lock_rejects_scale_shrink_and_inflation(self):
        for scale in (1.0, 1.5):
            e = copy.deepcopy(self.e)
            e["gaps"][0]["references"][0]["transport_scale_upper"] = scale
            with self.assertRaisesRegex(ValueError, "POSTHOC_REFERENCE_CALIBRATION_BOUND"):
                self.evaluate(e=e)

    def test_locked_12_is_unknown(self):
        r = self.evaluate()
        self.assertEqual(r["counts"]["UNKNOWN"], 1)
        self.assertEqual(r["counts"]["NOT_TESTABLE"], 1)
        self.assertFalse(r["physical_calibration_authenticated_by_code"])
        self.assertEqual(r["release"], "BLOCKED")

    def test_legitimate_precommitted_10_falsifies_conditionally(self):
        m, e = fixture(1.0)
        r = self.evaluate(m=m, e=e, digest=commitment(m))
        self.assertEqual(r["counts"]["FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS"], 1)
        self.assertFalse(r["human_anatomy_authenticated_by_code"])

    def test_posthoc_gap_bound_change_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["transport_scale_upper"] = 1.0
        with self.assertRaisesRegex(ValueError, "POSTHOC_TIMING_PREDICATE_OR_CALIBRATION"):
            self.evaluate(e=e)

    def test_posthoc_calibration_id_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"][0]["calibration_id"] = "other"
        with self.assertRaisesRegex(ValueError, "POSTHOC_REFERENCE_CALIBRATION_ID"):
            self.evaluate(e=e)

    def test_offset_switch_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"][0]["transport_offset_upper"] = 0.1
        with self.assertRaisesRegex(ValueError, "POSTHOC_REFERENCE_CALIBRATION_BOUND"):
            self.evaluate(e=e)

    def test_invalid_calibration_values(self):
        for val in (True, -1, float("nan"), float("inf"), "1", None):
            m = copy.deepcopy(self.m)
            m["gaps"][0]["transport_scale_upper"] = val
            with self.assertRaises(ValueError):
                commitment(m)

    def test_invalid_calibration_ids(self):
        for val in ("", " ", None, 5):
            m = copy.deepcopy(self.m)
            m["gaps"][0]["calibration_id"] = val
            with self.assertRaises(ValueError):
                commitment(m)

    def test_false_nuisance_flags_censor(self):
        for flag in ("clock_valid", "two_independent_raters", "geometry_transport_valid",
                     "native_provenance_valid", "radiometry_linear_valid", "nuisance_clear"):
            e = copy.deepcopy(self.e)
            e["gaps"][0]["references"][0][flag] = False
            self.assertEqual(self.evaluate(e=e)["counts"]["UNKNOWN"], 1)

    def test_missing_reference_is_unknown(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"] = []
        self.assertEqual(self.evaluate(e=e)["counts"]["UNKNOWN"], 1)

    def test_open_reference_cannot_verify_no_closure(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"][0]["anatomy"] = "OPEN_OBSERVED"
        self.assertFalse(self.evaluate(e=e)["verified_no_hidden_closure"])

    def test_changed_gap_denominator_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"].pop()
        with self.assertRaisesRegex(ValueError, "CHANGED_DENOMINATOR"):
            self.evaluate(e=e)

    def test_changed_prediction_or_threshold_rejected(self):
        for key, value in (("prediction", "ABSTAIN"), ("ordinary_closure_threshold", 0.23)):
            e = copy.deepcopy(self.e)
            e["gaps"][0][key] = value
            with self.assertRaises(ValueError):
                self.evaluate(e=e)

    def test_digest_mismatch(self):
        with self.assertRaisesRegex(ValueError, "COMMITMENT_MISMATCH"):
            self.evaluate(digest="a" * 64)

    def test_reference_extra_fields_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"][0]["unregistered"] = 1
        with self.assertRaisesRegex(ValueError, "INVALID_REFERENCE_SCHEMA"):
            self.evaluate(e=e)

    def test_reference_boolean_calibration_rejected(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"][0]["transport_scale_upper"] = True
        with self.assertRaisesRegex(ValueError, "INVALID_NUMBER"):
            self.evaluate(e=e)

    def test_key_order_stable(self):
        m = dict(reversed(list(self.m.items())))
        self.assertEqual(commitment(m), self.digest)


if __name__ == "__main__":
    unittest.main()
