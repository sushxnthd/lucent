#!/usr/bin/env python3
"""Adversarial tests for the post-hoc E002-474 cohort-tail design gate."""
import copy
import json
import math
import tempfile
import unittest
from pathlib import Path

from e002_474_cohort_tail_design import (
    ABSTAIN, DESIGNS, cohort_tail, evaluate, rational_design
)


class CohortTailDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = evaluate()

    def test_frozen_scenario_count(self):
        self.assertEqual(len(self.result["rows"]), len(DESIGNS) * 2)

    def test_240_tail_rejects_conservative_exclusion(self):
        rows = [r for r in self.result["rows"] if r["fps_nominal"] == 240]
        self.assertEqual([r["conservative_design_decision"] for r in rows],
                         ["EXCLUSION_FEASIBLE_CONDITIONALLY", "EXCLUSION_NOT_SUPPORTED"])

    def test_300_tail_rejects_conservative_exclusion(self):
        rows = [r for r in self.result["rows"] if r["fps_nominal"] == 300]
        self.assertEqual([r["conservative_design_decision"] for r in rows],
                         ["EXCLUSION_FEASIBLE_CONDITIONALLY", "EXCLUSION_NOT_SUPPORTED"])

    def test_480_is_only_conditional_under_tail_stress(self):
        rows = [r for r in self.result["rows"] if r["fps_nominal"] == 480]
        self.assertEqual([r["conservative_design_decision"] for r in rows],
                         ["EXCLUSION_FEASIBLE_CONDITIONALLY"] * 2)
        self.assertTrue(all(not r["physical_release_authorized"] for r in rows))

    def test_exact_boundary_never_certifies(self):
        crit, margin, ratio, decision = rational_design(240, 1, 369.86301369863014)
        self.assertGreater(crit, 0)
        self.assertGreater(margin, 0)
        self.assertGreater(ratio, 0)
        self.assertIn(decision, {"EXCLUSION_FEASIBLE_CONDITIONALLY",
                                 "EXCLUSION_NOT_SUPPORTED"})
        _, _, exact_ratio, exact_decision = rational_design(240, 1, crit)
        self.assertEqual(exact_ratio, 1)
        self.assertEqual(exact_decision, "EXCLUSION_NOT_SUPPORTED")

    def test_increasing_speed_cannot_restore_exclusion(self):
        for fps, shutter in DESIGNS:
            a = rational_design(fps, shutter, 243)
            b = rational_design(fps, shutter, 567.1039281430776)
            self.assertGreater(b[1], a[1])
            self.assertGreater(b[2], a[2])
            if a[3] == "EXCLUSION_NOT_SUPPORTED":
                self.assertNotEqual(b[3], "EXCLUSION_FEASIBLE_CONDITIONALLY")

    def test_invalid_or_tampered_aggregate_rejected(self):
        source = Path(__file__).with_name("E002_459_HUMAN_AGGREGATE.json")
        original = json.loads(source.read_text())
        for field, replacement in (
            ("source_sha256", "not-the-source"),
            ("physical_release_authorized", True),
            ("participants", {"calibration": 649, "holdout": 5}),
            ("pooled_training_caps", {"closing_mm_s": float("nan"),
                                      "opening_mm_s": 274.6}),
        ):
            mutated = copy.deepcopy(original)
            mutated[field] = replacement
            with tempfile.TemporaryDirectory() as tmp:
                file = Path(tmp) / "aggregate.json"
                file.write_text(json.dumps(mutated))
                with self.assertRaises(ValueError):
                    cohort_tail(file)

    def test_model_scope_does_not_flip_physical_release(self):
        self.assertTrue(self.result["ideal_linear_aperture_directional_240fps_conditional_exclusion"])
        self.assertTrue(self.result["ideal_linear_model_is_not_authenticated_rgb"])
        self.assertFalse(self.result["physical_release_authorized"])
        self.assertEqual(self.result["product_claim"], ABSTAIN)

    def test_source_is_not_a_hard_cap(self):
        self.assertTrue(self.result["sample_max_is_not_hard_cap"])
        self.assertEqual(self.result["physical_validation"], "NOT_ESTABLISHED")
        self.assertEqual(self.result["calibration_participants"], 12)

    def test_no_nonfinite_or_released_rows(self):
        for row in self.result["rows"]:
            for field in ("critical_speed_mm_s", "strict_min_margin_mm",
                          "dimensionless_speed_ratio"):
                self.assertTrue(math.isfinite(row[field]))
            self.assertFalse(row["physical_release_authorized"])
            self.assertFalse(row["is_hard_physiological_cap"])
            self.assertEqual(row["product_claim"], ABSTAIN)


if __name__ == "__main__":
    unittest.main()
