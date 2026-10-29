"""E002-522: frozen adversarial shutter-response tests; synthetic evidence only."""
import copy
from decimal import Decimal as D
from fractions import Fraction as F
import importlib.util
from pathlib import Path
import random
import unittest

spec = importlib.util.spec_from_file_location("e002_522_weight_cap", Path(__file__).with_name("e002_522_weight_cap.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def record():
    return {"version": m.VERSION, "gaps": [{
        "id": "g1", "prediction": "EXCLUDE",
        "left_end_max_ms": 10, "right_start_min_ms": 30,
        "ordinary_closure_threshold": D("0.2"),
        "references": [{
            "id": "r1", "start_min_ms": 12, "end_max_ms": 22,
            "exposure_duration_lower_ms": 8,
            "anatomy": "CLOSED_WITNESS",
            "reference_weighted_mean_aperture_upper": D("0.19"),
            "transport_scale_upper": 1, "transport_offset_upper": 0,
            "shutter_weight_concentration_upper": 2,
            **{f: True for f in m.FLAGS},
        }],
    }]}


class BoundedShutterTests(unittest.TestCase):
    def decision(self, payload=None):
        return m.evaluate(record() if payload is None else payload)["decisions"][0]

    def test_frozen_nonuniform_result(self):
        d = self.decision()
        self.assertEqual(d["decision"], m.POSITIVE)
        self.assertEqual(d["total_closure_fraction_lower_bound_exact"], "1/40")
        self.assertEqual(d["total_closure_time_ms_lower_bound_exact"], "1/5")
        self.assertFalse(d["contiguous_blink_certified"])

    def test_uniform_limit_recovers_e521(self):
        p = record(); p["gaps"][0]["references"][0]["shutter_weight_concentration_upper"] = 1
        self.assertEqual(self.decision(p)["total_closure_time_ms_lower_bound_exact"], "2/5")

    def test_high_concentration_weakens_claim(self):
        p = record(); p["gaps"][0]["references"][0]["shutter_weight_concentration_upper"] = 100
        self.assertEqual(self.decision(p)["total_closure_time_ms_lower_bound_exact"], "1/250")

    def test_no_strict_mean_margin_abstains(self):
        p = record(); p["gaps"][0]["references"][0]["reference_weighted_mean_aperture_upper"] = D("0.2")
        self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_no_calibrated_cap_abstains(self):
        p = record(); p["gaps"][0]["references"][0]["shutter_weight_concentration_upper"] = None
        self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_under_one_cap_rejected(self):
        p = record(); p["gaps"][0]["references"][0]["shutter_weight_concentration_upper"] = D("0.99")
        with self.assertRaisesRegex(ValueError, "INVALID_CONCENTRATION"):
            self.decision(p)

    def test_all_missing_attestations_fail_closed(self):
        for flag in m.FLAGS:
            with self.subTest(flag=flag):
                p = record(); p["gaps"][0]["references"][0][flag] = False
                self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_reference_uncertainty_containment(self):
        p = record(); p["gaps"][0]["references"][0]["start_min_ms"] = 10
        self.assertEqual(self.decision(p)["decision"], m.UNKNOWN)

    def test_reference_duration_impossible(self):
        p = record(); p["gaps"][0]["references"][0]["exposure_duration_lower_ms"] = 11
        with self.assertRaisesRegex(ValueError, "IMPOSSIBLE_DURATION"):
            self.decision(p)

    def test_reference_censoring(self):
        p = record(); p["gaps"][0]["references"][0]["anatomy"] = "OPEN_OBSERVED"
        self.assertEqual(self.decision(p)["decision"], m.CENSORED)

    def test_abstention_cannot_be_recast_as_falsification(self):
        p = record(); p["gaps"][0]["prediction"] = "ABSTAIN"
        self.assertEqual(self.decision(p)["decision"], m.NOT_TESTABLE)

    def test_no_product_release_claim(self):
        result = m.evaluate(record())
        self.assertEqual(result["product"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(result["release"], "BLOCKED")
        self.assertFalse(result["instrument_or_human_provenance_authenticated_by_code"])
        self.assertFalse(result["verified_no_hidden_closure"])

    def test_multiple_references_do_not_sum_overlaps(self):
        p = record()
        r = copy.deepcopy(p["gaps"][0]["references"][0]); r["id"] = "r2"
        p["gaps"][0]["references"].append(r)
        self.assertEqual(self.decision(p)["total_closure_time_ms_lower_bound_exact"], "1/5")

    def test_duplicate_reference_rejected(self):
        p = record(); p["gaps"][0]["references"].append(copy.deepcopy(p["gaps"][0]["references"][0]))
        with self.assertRaisesRegex(ValueError, "INVALID_REFERENCE_ID"):
            self.decision(p)

    def test_exact_near_threshold(self):
        p = record(); p["gaps"][0]["references"][0]["reference_weighted_mean_aperture_upper"] = D("0.199999999999999999")
        self.assertEqual(self.decision(p)["total_closure_time_ms_lower_bound_exact"], "1/50000000000000000")

    def test_exact_sharpness_construction(self):
        theta, M, R = F(1, 5), F(19, 100), F(2)
        target = (1 - M / theta) / R
        for exponent in (2, 3, 4, 5, 6):
            eps = F(1, 10 ** exponent)
            p = (1 - M / (theta + eps)) / R
            q_outside = (1 - R * p) / (1 - p)
            self.assertGreaterEqual(q_outside, 0)
            self.assertLessEqual(q_outside, R)
            self.assertEqual(R * p * 0 + q_outside * (1 - p) * (theta + eps), M)
            self.assertGreater(p, target)
        self.assertLess(p - target, F(1, 10000))

    def test_uncalibrated_uniform_assumption_is_false(self):
        # N=100 equal physical-time cells. A concentrated shutter weights only
        # the first cell, which is closed; all other cells are open.
        n = 100
        weights = [F(1)] + [F(0)] * (n - 1)
        apertures = [F(0)] + [F(21, 100)] * (n - 1)
        mean = sum(w * a for w, a in zip(weights, apertures))
        p_actual = F(sum(a <= F(1, 5) for a in apertures), n)
        self.assertEqual(mean, 0)
        self.assertEqual(p_actual, F(1, 100))
        self.assertLess(p_actual, 1 - mean / F(1, 5))  # false R=1
        self.assertEqual(p_actual, (1 - mean / F(1, 5)) / 100)  # true R=100

    def test_heldout_piecewise_instrument_response_5000(self):
        # Independently compute actual weighted means and closure fractions.
        # The evaluator is not used to generate these signals.
        rng = random.Random(20261029)
        tested = 0
        for _ in range(5000):
            n = rng.choice((8, 16, 32))
            raw = [rng.randint(0, 100) for _ in range(n)]
            if not any(raw):
                raw[0] = 1
            total = sum(raw)
            q = [F(x, total) for x in raw]
            a = [F(rng.randint(0, 30), 100) for _ in range(n)]
            theta = F(1, 5)
            M = sum(w * v for w, v in zip(q, a))
            if M >= theta:
                continue
            R = n * max(q)
            p_actual = F(sum(v <= theta for v in a), n)
            lower = (1 - M / theta) / R
            self.assertGreaterEqual(p_actual, lower)
            tested += 1
        self.assertGreater(tested, 1000)


if __name__ == "__main__":
    unittest.main()
