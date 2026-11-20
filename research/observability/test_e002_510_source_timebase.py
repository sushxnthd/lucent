#!/usr/bin/env python3
"""Frozen E002-510 adversarial tests. Synthetic clock rows only."""
import unittest
from e002_510_source_timebase import validate_frame_clock, safe_member
from zipfile import ZipInfo

HEAD = ["phantom_frame_idx", "phantom_timestamp_ms"]

def rows(period=1000/150, count=150):
    return [[str(i), format(i*period, ".12f")] for i in range(count)]

class SourceClockTests(unittest.TestCase):
    def test_150hz_consistent_is_not_authenticated(self):
        x = validate_frame_clock(rows(), HEAD)
        self.assertEqual(x["status"], "SOURCE_TIMEBASE_CONSISTENT_UNAUTHENTICATED")
        self.assertFalse(x["hardware_authenticated"])
        self.assertEqual(x["paired_frames"], 150)

    def test_500hz_contradicts_150(self):
        x = validate_frame_clock(rows(2), HEAD)
        self.assertEqual(x["status"], "SOURCE_TIMEBASE_CONTRADICTS_CLEAN_150HZ")

    def test_missing_phantom_specific_columns(self):
        x = validate_frame_clock(rows(), ["eeg_frame", "eeg_timestamp_ms"])
        self.assertEqual(x["status"], "NO_VALID_PHANTOM_FRAME_TIME_MAP")

    def test_ambiguous_duplicate_time_columns(self):
        x = validate_frame_clock([[a,b,b] for a,b in rows()],
                                 HEAD + ["phantom_time_ms"])
        self.assertEqual(x["status"], "NO_VALID_PHANTOM_FRAME_TIME_MAP")

    def test_unknown_time_units_abstain(self):
        x = validate_frame_clock(rows(), ["phantom_frame_idx", "phantom_timestamp"])
        self.assertEqual(x["status"], "NO_VALID_PHANTOM_FRAME_TIME_MAP")

    def test_noncontiguous_frame_indices_abstain(self):
        r = rows()
        r[100][0] = "102"
        x = validate_frame_clock(r, HEAD)
        self.assertEqual(x["reason"], "NONCONTIGUOUS_OR_NONMONOTONIC")

    def test_duplicate_timestamps_abstain(self):
        r = rows()
        r[30][1] = r[29][1]
        x = validate_frame_clock(r, HEAD)
        self.assertEqual(x["reason"], "NONCONTIGUOUS_OR_NONMONOTONIC")

    def test_less_than_100_frames_abstain(self):
        x = validate_frame_clock(rows(count=99), HEAD)
        self.assertEqual(x["reason"], "INSUFFICIENT_PAIRED_FRAMES")

    def test_single_large_gap_contradicts(self):
        r = rows()
        for i in range(101, len(r)):
            r[i][1] = str(float(r[i][1]) + 20)
        x = validate_frame_clock(r, HEAD)
        self.assertEqual(x["status"], "SOURCE_TIMEBASE_CONSISTENT_UNAUTHENTICATED")
        self.assertEqual(x["large_gaps_gt_1_5x_median"], 1)

    def test_two_large_gaps_exceed_one_percent(self):
        r = rows()
        for i in range(51, len(r)):
            r[i][1] = str(float(r[i][1]) + 20)
        for i in range(101, len(r)):
            r[i][1] = str(float(r[i][1]) + 20)
        x = validate_frame_clock(r, HEAD)
        self.assertEqual(x["status"], "SOURCE_TIMEBASE_CONTRADICTS_CLEAN_150HZ")
        self.assertEqual(x["large_gaps_gt_1_5x_median"], 2)

    def test_zip_path_traversal_rejected(self):
        self.assertFalse(safe_member(ZipInfo("../secret")))
        self.assertTrue(safe_member(ZipInfo("S01/record_phantom.xml")))

    def test_invalid_numeric_abstains(self):
        r = rows()
        r[1][1] = "NaN"
        x = validate_frame_clock(r, HEAD)
        self.assertEqual(x["reason"], "INVALID_FRAME_OR_TIME")

if __name__ == "__main__":
    unittest.main()
