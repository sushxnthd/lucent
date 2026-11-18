"""Executable synthetic regression for the E002-371 prospective evaluator.

All records are fabricated unit-test fixtures, NOT human observations.
Run from repository root:
python -m unittest discover -s research/observability -p 'test_e002_371_reference_evaluator.py' -v
"""
import unittest
from e002_371_reference_evaluator import evaluate

BASE = dict(
    participant_id="synthetic-A", split="holdout",
    mean0_lower_mm="2", mean1_lower_mm="2",
    exposure0_upper_s="0.01", exposure1_upper_s="0.01",
    gap_upper_s="0.01", velocity_upper_mm_s="100",
    threshold_mm="0", reference_min_aperture_upper_mm="1",
    reference_adjudicable="1", calibration_authenticated="1",
    linear_exposure_verified="1", timing_verified="1",
    geometry_verified="1",
)

def fixture(**changes):
    return {**BASE, **changes}

class ProspectiveEvaluatorTests(unittest.TestCase):
    def test_valid_synthetic_exclusion(self):
        result = evaluate([fixture()])
        self.assertEqual(result["mathematical_exclusions"], 1)
        self.assertEqual(result.get("false_exclusions", 0), 0)

    def test_adversarial_reference_closure_triggers_safety_failure(self):
        # Deliberately inconsistent synthetic record: ensures false
        # exclusions are COUNTED rather than silently suppressed.
        result = evaluate([fixture(reference_min_aperture_upper_mm="0")])
        self.assertEqual(result["reference_closures"], 1)
        self.assertEqual(result["false_exclusions"], 1)

    def test_provenance_missing_abstains(self):
        result = evaluate([fixture(calibration_authenticated="0")])
        self.assertEqual(result["abstain_provenance"], 1)
        self.assertEqual(result.get("mathematical_exclusions", 0), 0)

    def test_timing_uncertainty_reverses_exclusion(self):
        result = evaluate([fixture(gap_upper_s="0.04")])
        self.assertEqual(result["not_excluded"], 1)

    def test_uncertain_reference_not_safety_denominator(self):
        result = evaluate([fixture(reference_adjudicable="0")])
        self.assertEqual(result["reference_uncertain"], 1)
        self.assertEqual(result.get("reference_closures", 0), 0)

    def test_nonholdout_not_evaluated(self):
        result = evaluate([fixture(split="development")])
        self.assertEqual(result["non_holdout"], 1)
        self.assertEqual(result.get("mathematical_exclusions", 0), 0)

    def test_invalid_numeric_abstains(self):
        result = evaluate([fixture(velocity_upper_mm_s="NaN")])
        self.assertEqual(result["invalid"], 1)

if __name__ == "__main__":
    unittest.main()
