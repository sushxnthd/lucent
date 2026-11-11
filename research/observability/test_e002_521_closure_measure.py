import copy
from decimal import Decimal as D
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("e002_521_closure_measure", Path(__file__).with_name("e002_521_closure_measure.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def record():
    return {
        "version": m.VERSION,
        "gaps": [{
            "id": "g1", "prediction": "EXCLUDE", "left_end_max_ms": 10,
            "right_start_min_ms": 30, "ordinary_closure_threshold": D("0.20"),
            "references": [{
                "id": "r1", "start_min_ms": 12, "end_max_ms": 22,
                "exposure_duration_lower_ms": 8,
                "anatomy": "CLOSED_WITNESS",
                "reference_mean_aperture_upper": D("0.19"),
                "transport_scale_upper": 1,
                "transport_offset_upper": 0,
                **{f: True for f in m.FLAGS},
            }],
        }],
    }


class ClosureMeasureTests(unittest.TestCase):
    def evaluate(self, p=None):
        return m.evaluate(record() if p is None else p)

    def decision(self, p=None):
        return self.evaluate(p)["decisions"][0]

    def test_strict_margin_exact_rational(self):
        d = self.decision()
        self.assertEqual(d["decision"], m.POSITIVE)
        self.assertEqual(d["total_closure_fraction_lower_bound_exact"], "1/20")
        self.assertEqual(d["total_closure_time_ms_lower_bound_exact"], "2/5")
        self.assertFalse(d["contiguous_blink_duration_certified"])

    def test_scale_reversal(self):
        p = record(); p["gaps"][0]["references"][0]["transport_scale_upper"] = D("1.2")
        self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_equality_no_positive_duration(self):
        p = record(); p["gaps"][0]["references"][0]["reference_mean_aperture_upper"] = D("0.20")
        d = self.decision(p)
        self.assertEqual(d["decision"], m.CONTACT)
        self.assertIsNone(d["total_closure_time_ms_lower_bound_exact"])

    def test_near_equality_exact_no_float_rounding(self):
        p = record(); p["gaps"][0]["references"][0]["reference_mean_aperture_upper"] = D("0.200000000000000001")
        self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_tiny_strict_margin_remains_exact(self):
        p = record(); p["gaps"][0]["references"][0]["reference_mean_aperture_upper"] = D("0.199999999999999999")
        self.assertEqual(self.decision(p)["total_closure_time_ms_lower_bound_exact"], "1/25000000000000000")

    def test_nonuniform_shutter_abstains(self):
        p = record(); p["gaps"][0]["references"][0]["integration_uniform_valid"] = False
        self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_each_missing_evidence_flag_abstains(self):
        for flag in m.FLAGS:
            with self.subTest(flag=flag):
                p = record(); p["gaps"][0]["references"][0][flag] = False
                self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_uncertain_clock_containment(self):
        p = record(); p["gaps"][0]["references"][0]["start_min_ms"] = 10
        self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_reference_duration_lower_missing(self):
        p = record(); p["gaps"][0]["references"][0]["exposure_duration_lower_ms"] = None
        self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_duration_inconsistent_rejected(self):
        p = record(); p["gaps"][0]["references"][0]["exposure_duration_lower_ms"] = 11
        with self.assertRaisesRegex(ValueError, "IMPOSSIBLE_EXPOSURE"):
            self.evaluate(p)

    def test_open_is_censored_not_certified(self):
        p = record(); p["gaps"][0]["references"][0]["anatomy"] = "OPEN_OBSERVED"
        self.assertEqual(self.decision(p)["decision"], m.CENSORED)
        self.assertFalse(self.evaluate(p)["verified_no_hidden_closure"])

    def test_abstain_not_falsified(self):
        p = record(); p["gaps"][0]["prediction"] = "ABSTAIN"
        self.assertEqual(self.decision(p)["decision"], m.NOT_TESTABLE)

    def test_multiple_refs_do_not_sum_overlapping_durations(self):
        p = record(); r = copy.deepcopy(p["gaps"][0]["references"][0]); r["id"] = "r2"
        p["gaps"][0]["references"].append(r)
        self.assertEqual(self.decision(p)["total_closure_time_ms_lower_bound_exact"], "2/5")

    def test_duplicate_reference_rejected(self):
        p = record(); p["gaps"][0]["references"].append(copy.deepcopy(p["gaps"][0]["references"][0]))
        with self.assertRaisesRegex(ValueError, "INVALID_REFERENCE_ID"):
            self.evaluate(p)

    def test_duplicate_gap_rejected(self):
        p = record(); p["gaps"].append(copy.deepcopy(p["gaps"][0]))
        with self.assertRaisesRegex(ValueError, "INVALID_GAP_ID"):
            self.evaluate(p)

    def test_degenerate_theta_one_rejected(self):
        p = record(); p["gaps"][0]["ordinary_closure_threshold"] = 1
        with self.assertRaisesRegex(ValueError, "INVALID_THRESHOLD"):
            self.evaluate(p)

    def test_invalid_nonfinite_rejected(self):
        p = record(); p["gaps"][0]["references"][0]["reference_mean_aperture_upper"] = float("nan")
        with self.assertRaisesRegex(ValueError, "INVALID_"):
            self.evaluate(p)

    def test_negative_offset_rejected(self):
        p = record(); p["gaps"][0]["references"][0]["transport_offset_upper"] = -1
        with self.assertRaisesRegex(ValueError, "NEGATIVE_"):
            self.evaluate(p)

    def test_empty_gap_rejected(self):
        p = record(); p["gaps"][0]["right_start_min_ms"] = 9
        with self.assertRaisesRegex(ValueError, "EMPTY_OR_NEGATIVE_GAP"):
            self.evaluate(p)

    def test_no_external_authentication_claim(self):
        o = self.evaluate()
        self.assertFalse(o["calibration_or_human_provenance_authenticated_by_code"])
        self.assertFalse(o["contiguous_blink_certified"])
        self.assertEqual((o["product"], o["release"]), ("ABSTAIN_UNCALIBRATED", "BLOCKED"))


if __name__ == "__main__":
    unittest.main()
