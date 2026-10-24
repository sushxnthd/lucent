#!/usr/bin/env python3
"""E002-414 independent arithmetic and adversarial release-gate tests."""
import copy
import itertools
import math
import unittest

import e002_414_claim_power as gate


def synthetic_manifest(n=59):
    return {
        "experiment": "E002-414",
        "preregistered_challenges": True,
        "heldout_participants": True,
        "independent_reference_review": True,
        "hardware_clock_and_shutter_calibrated": True,
        "physical_aperture_calibrated": True,
        "physical_velocity_bound_verified": True,
        "target_device_domain_reviewed": True,
        "target_device_id": "SYNTHETIC-CAM",
        "participants": [
            {"participant_id": f"FAKE-{i:04d}", "device_id": "SYNTHETIC-CAM",
             "unseen_participant": True, "eligible_gaps": 4,
             "reference_resolved_gaps": 3, "issued_certificates": 1,
             "false_certificates": 0, "unresolved_abstentions": 1}
            for i in range(n)
        ],
    }


class ExactArithmetic(unittest.TestCase):
    def test_frozen_zero_failure_numbers(self):
        for n, expected in [(2, .7763932022500211), (20, .13910834066826516),
                            (632, .004728866248583152)]:
            self.assertAlmostEqual(gate.clopper_pearson_upper(n, 0), expected, places=12)
        self.assertGreater(gate.clopper_pearson_upper(58, 0), .05)
        self.assertLessEqual(gate.clopper_pearson_upper(59, 0), .05)
        self.assertGreater(gate.clopper_pearson_upper(118, 0), .025)
        self.assertLessEqual(gate.clopper_pearson_upper(119, 0), .025)
        self.assertEqual(gate.minimum_zero_failure_units(.05), 59)
        self.assertEqual(gate.minimum_zero_failure_units(.025), 119)
        self.assertEqual(gate.minimum_rank_calibrators(10, .025), 390)
        self.assertEqual(gate.plan(validation_risk=.025)["illustrative_disjoint_total"], 509)

    def test_independent_enumeration_oracle(self):
        # Direct enumeration of every binary sequence, not binomial_cdf().
        for n in (2, 4, 7):
            for p in (.03, .20, .51, .88):
                for k in range(n + 1):
                    exact = sum(p ** sum(bits) * (1-p) ** (n-sum(bits))
                                for bits in itertools.product((0, 1), repeat=n)
                                if sum(bits) <= k)
                    self.assertAlmostEqual(gate.binomial_cdf(k, n, p), exact, places=12)

    def test_exact_coverage_independent_enumeration(self):
        for n in (4, 10):
            for p in (.02, .15, .40, .80):
                coverage = sum(math.comb(n, k) * p**k * (1-p)**(n-k)
                               for k in range(n+1)
                               if gate.clopper_pearson_upper(n, k) + 1e-12 >= p)
                self.assertGreaterEqual(coverage + 1e-12, .95)

    def test_nonzero_failures_strictly_increase_upper(self):
        self.assertGreater(gate.clopper_pearson_upper(59, 1),
                           gate.clopper_pearson_upper(59, 0))

    def test_invalid_probability_and_count(self):
        for bad in (float("nan"), float("inf"), -1, 0, 1, True):
            with self.assertRaises(ValueError):
                gate.minimum_zero_failure_units(bad)
        for bad in (True, -1, 0):
            with self.assertRaises(ValueError):
                gate.clopper_pearson_upper(bad, 0)


class ParticipantGate(unittest.TestCase):
    def test_zero_error_synthetic_gate_never_certifies_physical(self):
        r = gate.audit(synthetic_manifest())
        self.assertEqual(r["independent_participants"], 59)
        self.assertEqual(r["total_certificates_not_independent"], 59)
        self.assertTrue(r["research_threshold_met_conditional_on_assumptions"])
        self.assertEqual(r["product"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(r["physical_certificate"], "NOT_AUTHORIZED")

    def test_two_participants_are_not_632_independent_frames(self):
        r = gate.audit(synthetic_manifest(2))
        self.assertAlmostEqual(r["participant_failure_upper"], .7763932022500211)
        self.assertFalse(r["research_threshold_met_conditional_on_assumptions"])

    def test_one_false_certificate_fails_threshold(self):
        m = synthetic_manifest()
        m["participants"][7]["false_certificates"] = 1
        r = gate.audit(m)
        self.assertEqual(r["participants_with_any_false_certificate"], 1)
        self.assertFalse(r["research_threshold_met_conditional_on_assumptions"])

    def test_duplicate_participant_rejected(self):
        m = synthetic_manifest()
        m["participants"][1]["participant_id"] = m["participants"][0]["participant_id"]
        with self.assertRaises(ValueError):
            gate.audit(m)

    def test_unseen_device_shift_rejected(self):
        m = synthetic_manifest()
        m["participants"][0]["device_id"] = "NEW-UNREVIEWED-DEVICE"
        with self.assertRaises(ValueError):
            gate.audit(m)

    def test_reference_missingness_not_hidden(self):
        m = synthetic_manifest()
        m["participants"][0]["unresolved_abstentions"] = 0
        with self.assertRaises(ValueError):
            gate.audit(m)

    def test_all_abstain_cannot_be_zero_error_success(self):
        m = synthetic_manifest()
        m["participants"][0]["issued_certificates"] = 0
        with self.assertRaises(ValueError):
            gate.audit(m)

    def test_unreviewed_calibration_rejected(self):
        for key in gate.REQUIRED_TRUE:
            m = synthetic_manifest()
            m[key] = False
            with self.assertRaises(ValueError):
                gate.audit(m)

    def test_inconsistent_counts_rejected(self):
        for field, bad in [("eligible_gaps", 0), ("reference_resolved_gaps", 5),
                           ("false_certificates", 2), ("issued_certificates", True),
                           ("unresolved_abstentions", -1)]:
            m = synthetic_manifest()
            m["participants"][0][field] = bad
            with self.assertRaises(ValueError):
                gate.audit(m)


if __name__ == "__main__":
    unittest.main(verbosity=2)
