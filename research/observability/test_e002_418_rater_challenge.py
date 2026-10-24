#!/usr/bin/env python3
"""E002-418 independent synthetic integrity and adversarial qualification tests."""
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import e002_407_full_event_pilot as base
import e002_418_rater_challenge as qc


class ChallengeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        root = Path(cls.temp.name)
        cls.pack, cls.private = root / "blinded", root / "PRIVATE"
        cls.result = qc.generate(cls.pack, cls.private)
        cls.truth_file = cls.private / "PRIVATE_DO_NOT_SHARE_truth.json"

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_integrity_and_privacy(self):
        self.assertEqual(self.result["synthetic_frames"], 144)
        self.assertEqual(self.result["human_ratings"], 0)
        manifest = json.loads((self.pack / "blinded_manifest.json").read_text())
        entries = base.validate_manifest(manifest)
        self.assertEqual(len(entries), 144)
        self.assertEqual([len(c["frames"]) for c in manifest["clips"]], [36]*4)
        self.assertNotIn("condition", json.dumps(manifest))
        self.assertNotIn("geometry", json.dumps(manifest))
        self.assertFalse((self.pack / "PRIVATE_DO_NOT_SHARE_truth.json").exists())
        self.assertTrue((self.pack / "annotate_offline.html").exists())
        self.assertEqual(set(self.result["conditions"].values()), {16})
        for _, _, filename, digest in entries:
            raw = (self.pack / "images" / filename).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
            self.assertEqual(base.png_dimensions(self.pack / "images" / filename), (190, 130))

    def test_oracle_and_adversaries(self):
        root = Path(self.temp.name)
        a, b = root / "oracle_a.csv", root / "oracle_b.csv"
        qc.make_oracle(self.pack, self.truth_file, a, "oracle_A")
        qc.make_oracle(self.pack, self.truth_file, b, "oracle_B")
        good = qc.score(self.pack, self.truth_file, a, b)
        self.assertTrue(good["joint_synthetic_qualification"])
        self.assertEqual(good["raters"][0]["synthetic_visible_pass"], 96)
        self.assertEqual(good["raters"][0]["obscured_abstain"], 48)
        self.assertFalse(good["physical_reference_validated"])
        self.assertFalse(good["actual_independent_human_raters_authenticated"])
        self.assertEqual(good["product"], "ABSTAIN_UNCALIBRATED")
        shifted = root / "shifted.csv"
        qc.make_oracle(self.pack, self.truth_file, shifted, "shifted", "shifted")
        failed = qc.score(self.pack, self.truth_file, shifted, b)
        self.assertFalse(failed["joint_synthetic_qualification"])
        self.assertEqual(failed["raters"][0]["synthetic_visible_pass"], 0)
        over = root / "over.csv"
        qc.make_oracle(self.pack, self.truth_file, over, "overconfident", "overconfident")
        failed = qc.score(self.pack, self.truth_file, over, b)
        self.assertFalse(failed["joint_synthetic_qualification"])
        self.assertEqual(failed["raters"][0]["obscured_abstain"], 0)
        self.assertEqual(sum(v["false_confident"] for v in
                             failed["raters"][0]["by_condition"].values()), 48)
        # A malicious/buggy UI must not conceal coordinates behind an
        # unresolved flag; the denominator still includes the frame.
        masked = root / "masked.csv"
        with a.open(newline="") as inp:
            original = list(csv.DictReader(inp))
        for row in original:
            if row["unresolved"] == "1":
                row["center_upper_x"] = "95"
                row["center_upper_y"] = "45"
                break
        with masked.open("w", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=base.COLUMNS)
            writer.writeheader()
            writer.writerows(original)
        masked_result = qc.score(self.pack, self.truth_file, masked, b)
        self.assertEqual(masked_result["raters"][0]["obscured_abstain"], 47)
        self.assertEqual(sum(v["false_confident"] for v in
                             masked_result["raters"][0]["by_condition"].values()), 1)
        with self.assertRaisesRegex(ValueError, "distinct"):
            qc.score(self.pack, self.truth_file, a, a)

    def test_manifest_tamper_rejected(self):
        root = Path(self.temp.name)
        clone = root / "tampered"
        clone.mkdir(exist_ok=True)
        raw = (self.pack / "blinded_manifest.json").read_text()
        (clone / "blinded_manifest.json").write_text(raw + " ")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            qc.read_truth(clone, self.truth_file)


if __name__ == "__main__":
    unittest.main(verbosity=2)
