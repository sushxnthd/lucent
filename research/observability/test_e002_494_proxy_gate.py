"""Adversarial E002-494 claim-gate tests. No external data or dependencies."""
import copy
import json
import unittest
from pathlib import Path
from e002_494_proxy_gate import assess

DATA = Path(__file__).with_name("E002_493_HOSTED_AGGREGATE.json")

class GateTests(unittest.TestCase):
    def fixture(self):
        return json.loads(DATA.read_text())

    def test_authentic_failure_is_preserved(self):
        d = assess(self.fixture())
        self.assertEqual(d["reason"], "AUTHENTIC_NUISANCE_FALSIFICATION")
        self.assertEqual(d["failed_conditions"],
                         ["alternating_jitter_1px", "stride2"])
        self.assertEqual(d["proxy_for_robust_event_selection"], "REJECT")
        self.assertEqual(d["release"], "BLOCKED")

    def test_invalid_evidence_abstains(self):
        self.assertEqual(assess({})["reason"], "INVALID_OR_INCOMPLETE_EVIDENCE")

    def test_missing_condition_abstains(self):
        r = self.fixture()
        del r["conditions"]["stride2"]
        self.assertEqual(assess(r)["reason"], "INVALID_OR_INCOMPLETE_EVIDENCE")

    def test_forged_pass_abstains(self):
        r = self.fixture()
        r["conditions"]["stride2"]["verdict"] = "SURVIVES_THIS_FIXTURE_ONLY"
        self.assertEqual(assess(r)["reason"], "INVALID_OR_INCOMPLETE_EVIDENCE")

    def test_inconsistent_counts_abstain(self):
        r = self.fixture()
        r["conditions"]["baseline"]["eligible_pairs"] += 1
        self.assertEqual(assess(r)["reason"], "INVALID_OR_INCOMPLETE_EVIDENCE")

    def test_anatomical_overclaim_abstains(self):
        r = self.fixture()
        r["physical_hidden_closure_certified"] = True
        self.assertEqual(assess(r)["reason"], "INVALID_OR_INCOMPLETE_EVIDENCE")

    def test_even_all_survival_cannot_authorize_product(self):
        r = self.fixture()
        for name in ("stride2", "alternating_jitter_1px"):
            c = r["conditions"][name]
            c["candidate_clip_candidates"] = 1
            c["proxy_candidates"] = 1
            c["candidate_clip_positive"] = True
            c["verdict"] = "SURVIVES_THIS_FIXTURE_ONLY"
        c = r["conditions"]["stride2"]
        c["eligible_pairs"] = 100
        c["nuisance_abstentions"] = 20
        c["eligible_fraction"] = round(100 / 120, 6)
        d = assess(r)
        self.assertEqual(d["reason"], "UNVALIDATED_SINGLE_SUBJECT_PROXY")
        self.assertEqual(d["anatomical_closure"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(d["release"], "BLOCKED")

if __name__ == "__main__":
    unittest.main()
