#!/usr/bin/env python3
"""Independent synthetic/adversarial tests for the E002-459 frozen gaze shift."""
import math
import unittest

from e002_459_gaze_shift_transfer import GAZES, HOLDOUT, evaluate


def fixture():
    """Twelve training participants, five held-out; 3 gaze conditions each."""
    rows = []
    for sid in range(1, 18):
        holdout = sid in HOLDOUT
        for gaze, (closing, opening) in {
            "center": (190, 90) if holdout else (200, 100),
            "bottom": (210, 120) if holdout else (250, 125),
            "top": (230, 105) if holdout else (300, 150),
        }.items():
            rows.append({"subject": sid, "gaze": gaze,
                         "closing": float(closing), "opening": float(opening)})
    return rows


class TestGazeShift(unittest.TestCase):
    def test_out_of_gaze_falsification(self):
        a = evaluate(fixture(), expected_count=51)
        self.assertTrue(a["center_only_noncenter_falsified_in_sample"])
        self.assertEqual(a["primary_noncenter_center_trained"]["exceed_either_blinks"], 10)
        self.assertEqual(a["primary_noncenter_center_trained"]["exceed_either_participants"], 5)
        self.assertEqual(a["heldout_gaze_transfer"]["center"]["center_only_transfer"]["exceed_either_blinks"], 0)
        self.assertEqual(a["heldout_gaze_transfer"]["top"]["center_only_transfer"]["exceed_either_blinks"], 5)
        self.assertEqual(a["heldout_gaze_transfer"]["bottom"]["center_only_transfer"]["exceed_either_blinks"], 5)

    def test_matched_and_pooled_controls(self):
        a = evaluate(fixture())
        for gaze in GAZES:
            self.assertEqual(a["heldout_gaze_transfer"][gaze]["pooled_transfer"]["exceed_either_blinks"], 0)
            self.assertEqual(a["heldout_gaze_transfer"][gaze]["gaze_matched_transfer"]["exceed_either_blinks"], 0)
        self.assertEqual(a["blinks"], {"calibration": 36, "holdout": 15})

    def test_no_person_identifiers_or_rows_in_output(self):
        a = evaluate(fixture())
        self.assertNotIn("rows", a)
        self.assertNotIn("subject", a)
        self.assertFalse(a["physical_release_authorized"])
        self.assertEqual(a["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_nonindependence_of_blinks(self):
        rows = fixture()
        heldout = next(r for r in rows if r["subject"] == 3 and r["gaze"] == "top")
        rows.extend([dict(heldout) for _ in range(50)])
        a = evaluate(rows)
        self.assertEqual(a["primary_noncenter_center_trained"]["exceed_either_participants"], 5)
        self.assertEqual(a["primary_noncenter_center_trained"]["exceed_either_blinks"], 60)

    def test_strict_equality_does_not_exceed(self):
        rows = fixture()
        for r in rows:
            if r["subject"] in HOLDOUT and r["gaze"] != "center":
                r["closing"], r["opening"] = 200.0, 100.0
        a = evaluate(rows)
        self.assertEqual(a["primary_noncenter_center_trained"]["exceed_either_blinks"], 0)
        self.assertFalse(a["center_only_noncenter_falsified_in_sample"])

    def test_reject_missing_stratum(self):
        rows = [r for r in fixture() if not (r["subject"] in HOLDOUT and r["gaze"] == "bottom")]
        with self.assertRaises(ValueError):
            evaluate(rows)

    def test_reject_missing_participant(self):
        with self.assertRaises(ValueError):
            evaluate([r for r in fixture() if r["subject"] != 15])

    def test_reject_bad_source_and_speeds(self):
        with self.assertRaises(ValueError):
            evaluate([], expected_count=0)
        with self.assertRaises(ValueError):
            evaluate(fixture(), expected_count=2306)
        for bad in (math.nan, math.inf, -1, 0, True):
            rows = fixture()
            rows[0]["closing"] = bad
            with self.assertRaises(ValueError):
                evaluate(rows)

    def test_reject_unknown_gaze_and_schema(self):
        rows = fixture()
        rows[0]["gaze"] = "side"
        with self.assertRaises(ValueError):
            evaluate(rows)
        rows = fixture()
        rows[0]["identifying_field"] = "do not export"
        with self.assertRaises(ValueError):
            evaluate(rows)

    def test_directional_math_and_no_release(self):
        a = evaluate(fixture())
        c = a["center_only_training_caps"]
        self.assertAlmostEqual(c["closing_mm_s"], 200)
        self.assertAlmostEqual(c["opening_mm_s"], 100)
        self.assertAlmostEqual(
            a["hypothetical_1mm_ideal_camera"]["center_only"]["critical_gap_ms_for_hypothetical_1mm_endpoints"], 15)
        self.assertFalse(a["physical_release_authorized"])
        self.assertEqual(a["human_anatomical_trajectory_validation"], "NOT_ESTABLISHED")


if __name__ == "__main__":
    unittest.main()
