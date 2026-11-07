"""Independent adversarial tests for E002-444; no human frames or data used."""
import unittest
import numpy as np
from e002_444_human_optical_motion import (
    HEIGHT, WIDTH, SHIFT_CONTROL, evaluate_frames, summarize
)

class HumanOpticalMotionTests(unittest.TestCase):
    def test_frozen_frame_differences_and_duplicates(self):
        a = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
        b = np.full((HEIGHT, WIDTH), 32, dtype=np.uint8)
        times = [0., .007, .014, .021, .221]
        result = evaluate_frames([a, a.copy(), b, b.copy(), a], times, limit=5)
        self.assertEqual(result["pair_count"], 4)
        self.assertEqual(result["exact_duplicate_pairs"], 2)
        self.assertAlmostEqual(result["mean_absolute_gray_change_normalized"]["max"], 32/255)
        self.assertEqual(result["event_gap_binned_optical_change"]["gt_100ms"]["n"], 1)
        self.assertEqual(result["long_gap_evidence"], "INSUFFICIENT_LONG_GAPS")
        self.assertEqual(result["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_no_physical_authorization_even_strong_motion(self):
        a = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
        b = np.full((HEIGHT, WIDTH), 255, dtype=np.uint8)
        r = evaluate_frames([a, b, a], [0., .007, .014], limit=3)
        self.assertFalse(r["physical_shutter_timing_authenticated"])
        self.assertFalse(r["anatomical_aperture_measured"])
        self.assertEqual(r["e002_371_physical_validation"], "NOT_ESTABLISHED")

    def test_reject_short_frame_stream(self):
        a = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
        with self.assertRaisesRegex(ValueError, "below frozen window"):
            evaluate_frames([a, a], [0., .007, .014], limit=3)

    def test_reject_invalid_shape(self):
        with self.assertRaisesRegex(ValueError, "shape or dtype"):
            evaluate_frames([np.zeros((4, 4), dtype=np.uint8)] * 3, [0., .007, .014], limit=3)

    def test_reject_invalid_dtype(self):
        with self.assertRaisesRegex(ValueError, "shape or dtype"):
            evaluate_frames([np.zeros((HEIGHT, WIDTH), dtype=np.float32)] * 3, [0., .007, .014], limit=3)

    def test_reject_nonmonotone_gap(self):
        with self.assertRaisesRegex(ValueError, "nonpositive event gap"):
            summarize([0., .1], [0., .1], [True, False], [.007, -.001])

    def test_reject_nan(self):
        with self.assertRaisesRegex(ValueError, "nonfinite"):
            summarize([0., float("nan")], [0., .1], [True, False], [.007, .007])

    def test_reject_out_of_range(self):
        with self.assertRaisesRegex(ValueError, "outside normalized"):
            summarize([0., 1.01], [0., .1], [True, False], [.007, .007])

    def test_reject_mismatched_arrays(self):
        with self.assertRaisesRegex(ValueError, "mismatched"):
            summarize([.1, .2], [.1], [False, False], [.007, .007])

    def test_shift_control_not_equal_to_identity_for_ramp(self):
        n = SHIFT_CONTROL + 10
        changes = [i / (2*n) for i in range(n)]
        r = summarize(changes, changes, [False] * n, [.007]*(n-1)+[.2])
        self.assertNotEqual(
            r["event_gap_binned_optical_change"]["gt_100ms"]["median"],
            r["shift_137_control_event_gap_binned_change"]["gt_100ms"]["median"])

    def test_all_duplicates_reject_independent_info(self):
        r = summarize([0.]*5, [0.]*5, [True]*5, [.007]*5)
        self.assertTrue(r["duplicate_warning"])
        self.assertTrue(r["independent_frame_information_rejected"])
        self.assertFalse(r["event_frame_alignment_authenticated"])

    def test_no_long_gaps_abstains(self):
        r = summarize([.01]*10, [.1]*10, [False]*10, [.007]*10)
        self.assertEqual(r["long_gap_evidence"], "INSUFFICIENT_LONG_GAPS")
        self.assertIsNone(r["long_gap_fraction_above_short_gap_median"])

if __name__ == "__main__":
    unittest.main()
