#!/usr/bin/env python3
"""E002-410 regression tests: eligibility is research-only and always fail-closed for product."""
import unittest

from e002_410_cluster_risk import exact_batch_exceedance, research_risk_gate


class RankAndGateTests(unittest.TestCase):
    def setUp(self):
        self.base = dict(
            participant_maxima=[1 + i * 0.01 for i in range(20)],
            future_participants=1,
            alpha=0.05,
            calibration_unit="independent_participant_session_maximum",
            exchangeability_reviewed=True,
            physical_aperture_reviewed=True,
            same_device_domain=True,
        )

    def gate(self, **kwargs):
        x = dict(self.base)
        x.update(kwargs)
        return research_risk_gate(**x)

    def test_exact_batch_risk(self):
        self.assertAlmostEqual(exact_batch_exceedance(20, 1), 1 / 21)
        self.assertAlmostEqual(exact_batch_exceedance(190, 10), 0.05)

    def test_bad_counts_rejected(self):
        for n, m in ((0, 1), (1, 0), (True, 1), (1.2, 1), (1, False)):
            with self.assertRaises(ValueError):
                exact_batch_exceedance(n, m)

    def test_eligible_research_still_product_abstains(self):
        r = self.gate()
        self.assertEqual(r["research_rank_eligibility"], "CONDITIONAL_ONLY")
        self.assertEqual(r["product"], "ABSTAIN_UNCALIBRATED")
        self.assertAlmostEqual(r["marginal_exceedance_risk_if_exchangeable"], 1 / 21)

    def test_frames_are_not_independent_participants(self):
        r = self.gate(calibration_unit="independent_frames")
        self.assertIn("frame_pseudoreplication", r["reasons"])
        self.assertEqual(r["product"], "ABSTAIN_UNCALIBRATED")

    def test_18_participants_insufficient_for_5pct(self):
        r = self.gate(participant_maxima=self.base["participant_maxima"][:18])
        self.assertIn("insufficient_independent_participants", r["reasons"])

    def test_batch_requires_190_participants(self):
        r = self.gate(future_participants=10)
        self.assertIn("insufficient_independent_participants", r["reasons"])

    def test_device_shift_rejected(self):
        self.assertIn("device_domain_shift", self.gate(same_device_domain=False)["reasons"])

    def test_no_physical_reference_rejected(self):
        self.assertIn("physical_aperture_not_reviewed",
                      self.gate(physical_aperture_reviewed=False)["reasons"])

    def test_exchangeability_not_reviewed_rejected(self):
        self.assertIn("participant_exchangeability_not_reviewed",
                      self.gate(exchangeability_reviewed=False)["reasons"])

    def test_missing_and_nonfinite_rejected(self):
        for values in ([], [float("nan")], [-1], [float("inf")], None):
            self.assertIn("invalid_or_missing_participant_maxima",
                          self.gate(participant_maxima=values)["reasons"])

    def test_ties_do_not_invalidate_conservative_rank_bound(self):
        r = self.gate(participant_maxima=[1.0] * 20)
        self.assertTrue(r["ties_present"])
        self.assertEqual(r["research_rank_eligibility"], "CONDITIONAL_ONLY")

    def test_invalid_alpha_and_future_count_rejected(self):
        self.assertIn("invalid_alpha", self.gate(alpha=0.0)["reasons"])
        self.assertIn("invalid_future_participant_count",
                      self.gate(future_participants=True)["reasons"])


if __name__ == "__main__":
    unittest.main()
