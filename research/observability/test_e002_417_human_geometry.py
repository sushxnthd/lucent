#!/usr/bin/env python3
"""E002-417 independent synthetic known-gap and denominator tests."""
import unittest
import numpy as np
from e002_417_human_geometry import (
    estimate, transform, measure, summarize, idealized_control,
    gradient_gap, threshold_gap,
)

def synthetic_gap(gap=24, background=180, interior=40):
    img = np.full((130, 190), background, dtype=np.uint8)
    if gap:
        img[50:50 + gap, :] = interior
    return img

class TestHumanGeometry(unittest.TestCase):
    def test_known_gap_and_equivariance(self):
        for gap in (16, 24, 35):
            img = synthetic_gap(gap)
            got = estimate(img)
            self.assertTrue(all(x is not None for x in got), got)
            for value in got:
                self.assertLessEqual(abs(value-gap), 3)
            for v in ("gain070", "gain130", "blur2", "translate8_6"):
                changed = estimate(transform(img, v))
                self.assertTrue(all(x is not None for x in changed), (gap, v, changed))
                for x, y in zip(got, changed):
                    self.assertLessEqual(abs(x-y), 3, (gap, v, got, changed))

    def test_glare_and_blank_abstain(self):
        img = synthetic_gap()
        self.assertEqual(estimate(transform(img, "white_glare")), (None, None))
        self.assertEqual(estimate(np.full((130, 190), 170, dtype=np.uint8)), (None, None))
        self.assertEqual(estimate(np.full((130, 190), 255, dtype=np.uint8)), (None, None))

    def test_invalid_input_and_transform(self):
        with self.assertRaises(ValueError):
            gradient_gap(np.zeros((130, 190), dtype=np.float32))
        with self.assertRaises(ValueError):
            threshold_gap(np.zeros((190, 130), dtype=np.uint8))
        with self.assertRaises(ValueError):
            transform(synthetic_gap(), "unrecognized")

    def test_all_frame_denominator_cannot_be_gamed(self):
        good = measure(synthetic_gap())
        bad = {k:(None, None) for k in good}
        s = summarize([good]*10 + [bad]*90, clips=8)
        self.assertEqual(s["clean_joint_valid"], 10)
        self.assertEqual(s["clean_joint_agree_all_frame_fraction"], .1)
        self.assertFalse(s["hypotheses"]["H2_joint_coverage_and_agreement"])
        self.assertFalse(s["joint_transfer_gate_pass"])
        self.assertEqual(s["product"], "ABSTAIN_UNCALIBRATED")
        self.assertFalse(s["product_claim_authorized"])

    def test_missing_under_nuisance_counts_failure(self):
        good = measure(synthetic_gap())
        dropped = {k:v for k,v in good.items()}
        dropped["gain070"] = (None, None)
        s = summarize([good]*19+[dropped], clips=8)
        self.assertEqual(s["nuisance"]["gain070"]["retained_and_stable_fraction"], .95)
        s = summarize([good]*18+[dropped]*2, clips=8)
        self.assertEqual(s["nuisance"]["gain070"]["retained_and_stable_fraction"], .9)
        self.assertFalse(s["hypotheses"]["H3_all_four_transfer_conditions"])

    def test_zero_clean_joint_valid_never_passes(self):
        empty = {k:(None, None) for k in measure(synthetic_gap())}
        s = summarize([empty]*600, clips=8)
        self.assertFalse(s["hypotheses"]["H2_joint_coverage_and_agreement"])
        self.assertFalse(s["hypotheses"]["H3_all_four_transfer_conditions"])

    def test_synthetic_control(self):
        self.assertTrue(idealized_control())

if __name__ == "__main__":
    unittest.main(verbosity=2)
