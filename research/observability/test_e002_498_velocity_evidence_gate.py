#!/usr/bin/env python3
"""Adversarial tests for E002-498; synthetic aggregate attestations only."""
import copy
import math
import unittest
from e002_498_velocity_evidence_gate import (
    NUISANCES, assess, minimum_participants,
)


def synthetic(n=59, p=.95, confidence=.95):
    return {
        "target_population_coverage": p,
        "target_confidence": confidence,
        "distinct_participants": n,
        "sampling_unit": "independent_participants",
        "target_population": "synthetic_pop_A",
        "calibration_population": "synthetic_pop_A",
        "holdout_population": "synthetic_pop_A",
        "camera_clock_authenticated": True,
        "shutter_calibrated": True,
        "geometry_calibrated": True,
        "independent_anatomical_review": True,
        "continuous_upper_bound_certified": True,
        "independent_participant_sampling": True,
        "participant_disjoint_holdout": True,
        "independent_replay": True,
        "nuisance_controls": {k: True for k in NUISANCES},
        "certified_max_normalized_speed_per_second": 12.0,
    }


class TestVelocityEvidenceGate(unittest.TestCase):
    def test_exact_pilot_threshold(self):
        self.assertEqual(minimum_participants(.95, .95), 59)
        self.assertEqual(assess(synthetic(58))["decision"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(assess(synthetic(59))["decision"],
                         "STATISTICAL_ENVELOPE_RESEARCH_ONLY")

    def test_exact_stronger_threshold(self):
        self.assertEqual(minimum_participants(.99, .95), 299)
        self.assertEqual(assess(synthetic(298, .99))["decision"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(assess(synthetic(299, .99))["decision"],
                         "STATISTICAL_ENVELOPE_RESEARCH_ONLY")

    def test_passing_record_never_releases(self):
        x = assess(synthetic())
        self.assertEqual(x["release"], "BLOCKED")
        self.assertFalse(x["physical_hidden_closure_certified"])
        self.assertFalse(x["universal_human_velocity_bound"])
        self.assertFalse(x["fatigue_or_medical_claims"])
        self.assertGreaterEqual(x["distribution_free_confidence_lower_bound"], .95)

    def test_frames_are_not_participants(self):
        x = synthetic(299, .99)
        x["sampling_unit"] = "blink_events"
        self.assertEqual(assess(x)["decision"], "ABSTAIN_UNCALIBRATED")

    def test_repeated_subjects_not_independent(self):
        x = synthetic(299, .99)
        x["independent_participant_sampling"] = False
        self.assertIn("MISSING_INDEPENDENT_PARTICIPANT_SAMPLING", assess(x)["reasons"])

    def test_no_between_sample_upper_bound(self):
        x = synthetic()
        x["continuous_upper_bound_certified"] = False
        self.assertEqual(assess(x)["decision"], "ABSTAIN_UNCALIBRATED")

    def test_nominal_camera_rate_not_enough(self):
        x = synthetic()
        x["camera_clock_authenticated"] = False
        self.assertEqual(assess(x)["decision"], "ABSTAIN_UNCALIBRATED")

    def test_no_shutter_calibration(self):
        x = synthetic()
        x["shutter_calibrated"] = False
        self.assertEqual(assess(x)["decision"], "ABSTAIN_UNCALIBRATED")

    def test_nuisance_inventory_missing(self):
        x = synthetic()
        del x["nuisance_controls"]["gaze"]
        self.assertIn("INCOMPLETE_NUISANCE_INVENTORY", assess(x)["reasons"])

    def test_nuisance_failed(self):
        x = synthetic()
        x["nuisance_controls"]["glasses"] = False
        self.assertEqual(assess(x)["decision"], "ABSTAIN_UNCALIBRATED")

    def test_holdout_population_mismatch(self):
        x = synthetic()
        x["holdout_population"] = "synthetic_pop_B"
        self.assertEqual(assess(x)["decision"], "ABSTAIN_UNCALIBRATED")

    def test_non_disjoint_holdout(self):
        x = synthetic()
        x["participant_disjoint_holdout"] = False
        self.assertEqual(assess(x)["decision"], "ABSTAIN_UNCALIBRATED")

    def test_individual_data_rejected(self):
        x = synthetic()
        x["individual_velocities"] = [1, 2, 3]
        result = assess(x)
        self.assertEqual(result["decision"], "ABSTAIN_UNCALIBRATED")
        self.assertNotIn("max_certified_normalized_speed_per_second", result)

    def test_invalid_values_rejected(self):
        for v in (float("nan"), float("inf"), -1, 0, True, "12"):
            x = synthetic()
            x["certified_max_normalized_speed_per_second"] = v
            self.assertEqual(assess(x)["decision"], "ABSTAIN_UNCALIBRATED")

    def test_bad_probabilities(self):
        for v in (0, 1, -1, float("nan"), float("inf"), True, "0.95"):
            x = synthetic()
            x["target_population_coverage"] = v
            self.assertEqual(assess(x)["reasons"], ["INVALID_TARGET"])

    def test_count_boolean_and_negative(self):
        for n in (True, -1, 2.5, "299"):
            x = synthetic()
            x["distinct_participants"] = n
            self.assertIn("INVALID_PARTICIPANT_COUNT", assess(x)["reasons"])

    def test_absent_input(self):
        self.assertEqual(assess(None)["reasons"], ["INVALID_INPUT"])

    def test_no_independent_review(self):
        x = synthetic()
        x["independent_anatomical_review"] = False
        self.assertEqual(assess(x)["decision"], "ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    unittest.main()
