"""Synthetic/adversarial checks for E002-453 external human velocity transfer audit."""
import csv
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from e002_453_external_human_velocity import (
    HOLDOUT_SUBJECTS, analyze_file, nearest_rank, parse_csv, transfer_audit,
)

def fixture(train_values=None, test_values=None, unseen_gaze=False):
    train_values = train_values or [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210]
    test_values = test_values or [80, 90, 100, 110, 120]
    train_ids = [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17]
    rows = [{"subject": s, "gaze": ("top" if unseen_gaze else ("bottom", "center", "top")[i % 3]),
             "v": float(v)} for i, (s, v) in enumerate(zip(train_ids, train_values))]
    rows += [{"subject": s, "gaze": ("bottom" if unseen_gaze else ("bottom", "center", "top")[i % 3]),
              "v": float(v)} for i, (s, v) in enumerate(zip(sorted(HOLDOUT_SUBJECTS), test_values))]
    return rows


class TestExternalHumanVelocity(unittest.TestCase):
    def test_participant_disjoint_frozen_split(self):
        r = transfer_audit(fixture())
        self.assertEqual((r["rows"]["train_subjects"], r["rows"]["holdout_subjects"]), (12, 5))
        self.assertEqual(r["rows"]["train"], 12)
        self.assertEqual(r["rows"]["holdout"], 5)

    def test_holdout_exceedance_falsifies_training_max(self):
        r = transfer_audit(fixture(test_values=[80, 90, 220, 110, 120]))
        self.assertEqual(r["tests"]["pooled_train_max"]["count"], 1)
        self.assertEqual(r["tests"]["pooled_train_max"]["holdout_subjects_with_exceedance"], 1)
        self.assertGreater(r["tests"]["pooled_train_max"]["max_exceedance_ratio"], 1)

    def test_q99_nearest_rank(self):
        self.assertEqual(nearest_rank(list(range(1, 101)), .99), 99)
        self.assertEqual(nearest_rank(list(range(1, 13)), .99), 12)

    def test_missing_training_gaze_abstains(self):
        r = transfer_audit(fixture(unseen_gaze=True))
        self.assertEqual(r["tests"]["gaze_train_max"]["abstained"], 5)
        self.assertEqual(r["tests"]["gaze_train_max"]["denominator"], 0)

    def test_zero_exceedances_not_authorization(self):
        r = transfer_audit(fixture())
        self.assertEqual(r["tests"]["pooled_train_max"]["count"], 0)
        self.assertEqual(r["product_claim"], "ABSTAIN_UNCALIBRATED")
        self.assertFalse(r["physical_release_authorized"])

    def test_gap_is_illustrative_only(self):
        r = transfer_audit(fixture())
        self.assertAlmostEqual(r["illustrative"]["critical_gap_ms"], 2000/210)
        self.assertFalse(r["illustrative"]["nominal_gap_shorter_than_illustrative_threshold"]["30"])

    def test_missing_holdout_rejected(self):
        with self.assertRaises(ValueError):
            transfer_audit([r for r in fixture() if r["subject"] != 15])

    def test_nonfinite_velocity_rejected(self):
        rows = fixture()
        rows[0]["v"] = float("nan")
        with self.assertRaises(ValueError):
            transfer_audit(rows)

    def test_csv_schema_and_missingness(self):
        header = "subject,target_pos,peak_closing_velocity,peak_opening_velocity,closing_amplitude,duration\n"
        rows, exclusions = parse_csv((header + "1,top,200,100,8,200\n2,bottom,nan,100,8,200\n").encode())
        self.assertEqual((len(rows), exclusions), (1, 1))

    def test_hash_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "Blinks.csv"
            path.write_text("not source", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
                analyze_file(path)

    def test_no_participant_ids_in_output(self):
        r = transfer_audit(fixture())
        self.assertNotIn("subject_ids", r["rows"])
        self.assertNotIn("by_subject", r["tests"]["pooled_train_max"])


if __name__ == "__main__":
    unittest.main()
