"""Independent checks and adversarial cases for E002-440."""
import copy
import unittest
from e002_440_cluster_risk import (cp_upper, binomial_cdf, min_zero_failure_participants,
                                   run_cluster_countermodel, adjudicate_ledger)


def example():
    return {"evidence_tier": "synthetic", "random_sampling_verified": False,
            "external_review_verified": False, "velocity_cap_verified": False,
            "nuisance_transport_verified": False,
            "participants": [{"participant_id": "p0", "predictions_locked": True,
                              "reference_authenticated": True, "physical_calibration_authenticated": True,
                              "nuisance_complete": True,
                              "observations": [{"decision": "NO_CLOSURE_CANDIDATE",
                                                "reference": "NEGATIVE_CONDITIONAL"} for _ in range(40)]}]}


class ClusterRiskTests(unittest.TestCase):
    def test_zero_error_exact(self):
        self.assertAlmostEqual(cp_upper(0, 30), 1 - .05 ** (1 / 30), places=13)
        self.assertAlmostEqual(cp_upper(0, 1200), 1 - .05 ** (1 / 1200), places=13)
        self.assertGreater(cp_upper(0, 30), .09)
        self.assertLess(cp_upper(0, 1200), .003)

    def test_exact_sample_size(self):
        self.assertEqual(min_zero_failure_participants(.05, .01), 299)
        self.assertGreaterEqual(cp_upper(0, 298), .01)
        self.assertLess(cp_upper(0, 299), .01)

    def test_general_cp_root(self):
        for n, k in ((30, 1), (30, 10), (100, 3), (1200, 40)):
            u = cp_upper(k, n)
            self.assertAlmostEqual(binomial_cdf(k, n, u), .05, places=9)
            self.assertGreaterEqual(u, k / n)

    def test_cp_monotonic(self):
        self.assertTrue(all(cp_upper(k, 30) < cp_upper(k + 1, 30) for k in range(30)))
        self.assertEqual(cp_upper(30, 30), 1.0)

    def test_invalid_cp(self):
        for args in ((0, 0), (-1, 30), (31, 30)):
            with self.assertRaises(ValueError): cp_upper(*args)
        with self.assertRaises(ValueError): cp_upper(0, 30, 0)

    def test_simulation_prediction(self):
        r = run_cluster_countermodel()
        self.assertLess(abs(r["observed_zero_error_frequency"] - r["exact_zero_error_probability"]), .012)
        self.assertEqual(r["minimum_independent_zero_error_participants_for_upper_below_1pct"], 299)
        self.assertFalse(r["physical_release_authorized"])

    def test_deterministic_seed(self):
        self.assertEqual(run_cluster_countermodel(trials=30), run_cluster_countermodel(trials=30))

    def test_eligible_synthetic_never_release(self):
        r = adjudicate_ledger(example())
        self.assertEqual(r["evaluable_participants"], 1)
        self.assertEqual(r["candidate_intervals_total"], 40)
        self.assertFalse(r["physical_release_authorized"])
        self.assertFalse(r["eligible_for_external_release_review_ONLY"])

    def test_incomplete_challenge_not_eligible(self):
        s = example()
        s["participants"][0]["observations"].pop()
        self.assertEqual(adjudicate_ledger(s)["unresolved_participants"], 1)

    def test_unresolved_blocks_denominator(self):
        s = example()
        s["participants"][0]["observations"].append({"decision": "NO_CLOSURE_CANDIDATE", "reference": "UNRESOLVED"})
        r = adjudicate_ledger(s)
        self.assertEqual((r["evaluable_participants"], r["unresolved_participants"]), (0, 1))
        self.assertIsNone(r["one_sided_95pct_upper_conditional_on_iid_and_complete_reference"])

    def test_witnessed_false_counts_participant_once(self):
        s = example()
        s["participants"][0]["observations"][0]["reference"] = "WITNESSED_FALSE"
        self.assertEqual(adjudicate_ledger(s)["participant_any_false"], 1)

    def test_abstention_not_success(self):
        s = example()
        s["participants"][0]["observations"] = [{"decision": "ABSTAIN", "reference": None}]
        r = adjudicate_ledger(s)
        self.assertEqual(r["abstain_only_participants"], 1)
        self.assertEqual(r["evaluable_participants"], 0)

    def test_duplicate_participants_rejected(self):
        s = example()
        s["participants"].append(copy.deepcopy(s["participants"][0]))
        with self.assertRaises(ValueError): adjudicate_ledger(s)

    def test_unlocked_or_unauthenticated_not_success(self):
        for key in ("predictions_locked", "reference_authenticated", "physical_calibration_authenticated", "nuisance_complete"):
            s = example()
            s["participants"][0][key] = False
            self.assertEqual(adjudicate_ledger(s)["unresolved_participants"], 1)

    def test_missing_attestation_rejected(self):
        s = example()
        del s["participants"][0]["reference_authenticated"]
        with self.assertRaises(ValueError): adjudicate_ledger(s)

    def test_invalid_reference_rejected(self):
        s = example()
        s["participants"][0]["observations"][0]["reference"] = "POSITIVE_UNVERIFIED"
        with self.assertRaises(ValueError): adjudicate_ledger(s)

    def test_review_only_with_299_human_units(self):
        s = example()
        s["evidence_tier"] = "human_prospective"
        for key in ("random_sampling_verified", "external_review_verified", "velocity_cap_verified", "nuisance_transport_verified"):
            s[key] = True
        s["participants"] = []
        for i in range(299):
            row = copy.deepcopy(example()["participants"][0])
            row["participant_id"] = str(i)
            s["participants"].append(row)
        r = adjudicate_ledger(s)
        self.assertTrue(r["eligible_for_external_release_review_ONLY"])
        self.assertFalse(r["physical_release_authorized"])
        s["participants"].pop()
        self.assertFalse(adjudicate_ledger(s)["eligible_for_external_release_review_ONLY"])


if __name__ == "__main__":
    unittest.main()
