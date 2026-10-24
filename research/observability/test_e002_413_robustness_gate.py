#!/usr/bin/env python3
"""Independent denominator checks and adversarial regression for E002-413."""
import copy
import json
import math
import unittest
from pathlib import Path
import e002_413_robustness_gate as gate

HERE = Path(__file__).resolve().parent


class DenominatorAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((HERE / "E002_413_AGGREGATE.json").read_text())

    def test_real_human_aggregate_rejects_transfer(self):
        r = gate.audit(self.data)
        self.assertEqual(r["total_frames"], 632)
        self.assertEqual(r["clean_valid_frames"], 623)
        self.assertEqual(r["rejected_variants"], ["gain_070", "translation_8_6"])
        self.assertEqual(r["product"], "ABSTAIN_UNCALIBRATED")
        self.assertTrue(r["glare_fail_closed"])
        self.assertAlmostEqual(r["variants"]["gain_070"]["clean_coverage"], 474/623, places=5)
        self.assertAlmostEqual(r["variants"]["gain_070"]["conservative_all_frame_stability"], 474/632, places=5)
        self.assertAlmostEqual(r["variants"]["translation_8_6"]["conservative_all_frame_stability"],
                               621/632 * .454106, places=5)

    def test_conditional_stability_cannot_hide_missingness(self):
        d = copy.deepcopy(self.data)
        d["nuisance"]["gain_070"].update(joint_valid_frames=60, rejected_frames=40,
                                            fraction_abs_change_le_008=1.0)
        d["total_frames"] = 100
        d["clean_valid_frames"] = 100
        # Keep other variants internally consistent with a 100-frame synthetic sample.
        for v in ("gain_130", "blur_sigma2", "translation_8_6"):
            d["nuisance"][v].update(joint_valid_frames=100, rejected_frames=0,
                                     fraction_abs_change_le_008=1.0)
        d["nuisance"]["glare"]["rejected_frames"] = 100
        r = gate.audit(d)
        self.assertEqual(r["variants"]["gain_070"]["conditional_stability"], 1.0)
        self.assertEqual(r["variants"]["gain_070"]["conservative_all_frame_stability"], 0.6)
        self.assertIn("gain_070", r["rejected_variants"])

    def test_perfect_synthetic_controls_never_authorize_physical_claim(self):
        d = copy.deepcopy(self.data)
        for v in gate.TRANSFER:
            d["nuisance"][v].update(joint_valid_frames=623, rejected_frames=9,
                                     fraction_abs_change_le_008=1.0)
        r = gate.audit(d)
        self.assertFalse(r["transfer_rejected"])
        self.assertEqual(r["hidden_closure_certification"], "NOT_AUTHORIZED")
        self.assertEqual(r["product"], "ABSTAIN_UNCALIBRATED")

    def test_malformed_counts_and_nonfinite_fraction_fail_closed(self):
        for field, value in [("joint_valid_frames", 999), ("joint_valid_frames", -1),
                             ("fraction_abs_change_le_008", float("nan")),
                             ("fraction_abs_change_le_008", float("inf")),
                             ("fraction_abs_change_le_008", 1.01)]:
            d = copy.deepcopy(self.data)
            d["nuisance"]["gain_070"][field] = value
            with self.assertRaises(ValueError):
                gate.audit(d)

    def test_alias_counts_independent_integer_check(self):
        d = self.data["point_decimation"]
        self.assertEqual(d["15"]["valid_clip_phases"], 128)
        self.assertEqual(d["30"]["valid_clip_phases"], 128)
        self.assertEqual(d["60"]["valid_clip_phases"], 128)
        self.assertEqual([round(d[str(rate)]["fraction_loss_gt_010"]*128)
                          for rate in (15,30,60)], [80,48,26])
        self.assertAlmostEqual(1-d["30"]["min_capture_ratio"], .303248, places=6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
