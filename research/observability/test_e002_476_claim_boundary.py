#!/usr/bin/env python3
"""E002-476: adversarial tests for interval-level physical claim boundary."""
import copy
import unittest

from e002_456_prospective_gate import evaluate_interval, evaluate_dataset
from e002_476_claim_boundary import (
    ABSTAIN, _synthetic_case, render_public, run_frozen,
)


class ClaimBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.case = _synthetic_case()

    def assert_blocked(self, raw):
        self.assertIs(raw["physical_release_authorized"], False)
        self.assertEqual(raw["product_claim"], ABSTAIN)
        self.assertIs(raw["external_hard_bound_verified_by_this_program"], False)
        display = render_public(raw)
        self.assertIs(display["physical_release_authorized"], False)
        self.assertEqual(display["physical_claim"], ABSTAIN)
        return display

    def test_illustrative_conditional_remains_research_only(self):
        raw = evaluate_interval(self.case)
        self.assertEqual(raw["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertEqual(self.assert_blocked(raw)["research_label"],
                         "CONDITIONAL_MODEL_EXCLUSION_ONLY")

    def test_declared_external_provenance_cannot_authenticate_hard_bound(self):
        self.case["velocity"]["provenance"] = "EXTERNAL_HARD_BOUND_DECLARED"
        raw = evaluate_interval(self.case)
        self.assertEqual(raw["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertEqual(self.assert_blocked(raw)["research_label"],
                         "CONDITIONAL_MODEL_EXCLUSION_ONLY")

    def test_no_reference_not_anatomical_negative(self):
        self.case["reference"] = []
        raw = evaluate_interval(self.case)
        self.assertEqual(raw["reference"], "REFERENCE_INCOMPLETE")
        self.assertEqual(raw["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertEqual(self.assert_blocked(raw)["research_label"],
                         "CONDITIONAL_MODEL_EXCLUSION_ONLY")

    def test_witnessed_contradiction_takes_precedence(self):
        self.case["reference"][0]["aperture_mm"] = 1.8
        raw = evaluate_interval(self.case)
        self.assertTrue(raw["joint_falsification"])
        self.assertEqual(self.assert_blocked(raw)["research_label"],
                         "JOINT_MODEL_ASSUMPTIONS_FALSIFIED")

    def test_empirical_max_rejected(self):
        self.case["velocity"]["provenance"] = "EMPIRICAL_SAMPLE_MAX"
        raw = evaluate_interval(self.case)
        self.assertEqual(raw["decision"], "ABSTAIN")
        self.assertEqual(self.assert_blocked(raw)["research_label"], "RESEARCH_ABSTAIN")

    def test_nuisance_unknown_rejected(self):
        for nuisance in self.case["nuisance"]:
            case = copy.deepcopy(self.case)
            case["nuisance"][nuisance] = "UNKNOWN"
            self.assertEqual(self.assert_blocked(evaluate_interval(case))["research_label"],
                             "RESEARCH_ABSTAIN")

    def test_missing_instrument_rejected(self):
        self.case.pop("instrument")
        self.assertEqual(self.assert_blocked(evaluate_interval(self.case))["research_label"],
                         "RESEARCH_ABSTAIN")

    def test_not_excluded_still_no_physical_claim(self):
        self.case["velocity"]["limit_mm_s"] = 300
        raw = evaluate_interval(self.case)
        self.assertEqual(raw["decision"], "NOT_EXCLUDED")
        self.assertEqual(self.assert_blocked(raw)["research_label"], "CLOSURE_NOT_EXCLUDED")

    def test_invalid_schema_abstains_with_product_fields(self):
        for bad in (None, [], {}, {"nuisance": []}, {"nuisance": "PASS"}):
            self.assertEqual(self.assert_blocked(evaluate_interval(bad))["research_label"],
                             "RESEARCH_ABSTAIN")

    def test_forged_release_flag_rejected(self):
        raw = evaluate_interval(self.case)
        raw["physical_release_authorized"] = True
        self.assertEqual(render_public(raw)["research_label"], "NOT_DISPLAYED")

    def test_forged_bound_verification_rejected(self):
        raw = evaluate_interval(self.case)
        raw["external_hard_bound_verified_by_this_program"] = True
        self.assertEqual(render_public(raw)["research_label"], "NOT_DISPLAYED")

    def test_forged_product_claim_rejected(self):
        raw = evaluate_interval(self.case)
        raw["product_claim"] = "NO_HIDDEN_CLOSURE"
        self.assertEqual(render_public(raw)["research_label"], "NOT_DISPLAYED")

    def test_missing_and_wrong_typed_authorization_rejected(self):
        for key in ("physical_release_authorized", "product_claim",
                    "external_hard_bound_verified_by_this_program"):
            for value in (None, 0, "false", [], {}):
                raw = evaluate_interval(self.case)
                raw[key] = value
                self.assertEqual(render_public(raw)["research_label"], "NOT_DISPLAYED")
            raw = evaluate_interval(self.case)
            raw.pop(key)
            self.assertEqual(render_public(raw)["research_label"], "NOT_DISPLAYED")

    def test_inconsistent_reference_falsification_rejected(self):
        raw = evaluate_interval(self.case)
        raw["joint_falsification"] = True
        self.assertEqual(render_public(raw)["research_label"], "NOT_DISPLAYED")
        raw = evaluate_interval(self.case)
        raw["reference"] = "WITNESSED_CROSSING"
        self.assertEqual(render_public(raw)["research_label"], "NOT_DISPLAYED")

    def test_nonfinite_and_missing_envelope_rejected(self):
        for bad in (float("nan"), float("inf"), -1, True, None):
            raw = evaluate_interval(self.case)
            raw["lower_envelope_mm"] = bad
            self.assertEqual(render_public(raw)["research_label"], "NOT_DISPLAYED")
        raw = evaluate_interval(self.case)
        raw.pop("lower_envelope_mm")
        self.assertEqual(render_public(raw)["research_label"], "NOT_DISPLAYED")

    def test_dataset_remains_blocked_and_split_safe(self):
        a = dict(self.case, interval_id="one", participant_id="A", split="development")
        b = dict(copy.deepcopy(self.case), interval_id="two", participant_id="B", split="holdout")
        aggregate = evaluate_dataset({"schema_version": "E002-456-v1", "intervals": [a, b]})
        self.assertIs(aggregate["physical_release_authorized"], False)
        self.assertEqual(aggregate["product_claim"], ABSTAIN)
        self.assertEqual(aggregate["counts"]["development"]["participants"], 1)
        self.assertEqual(aggregate["counts"]["holdout"]["participants"], 1)

    def test_frozen_experiment_reproducible(self):
        result = run_frozen()
        self.assertEqual(len(result["cases"]), 6)
        self.assertFalse(result["physical_release_authorized"])
        self.assertEqual(result["product_claim"], ABSTAIN)
        self.assertTrue(all(v["physical_claim"] == ABSTAIN for v in result["cases"].values()))


if __name__ == "__main__":
    unittest.main()
