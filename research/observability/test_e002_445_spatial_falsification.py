"""E002-445 independent synthetic and adversarial tests; no human pixels."""
import unittest

import numpy as np

from e002_445_spatial_falsification import (
    WIDTH, HEIGHT, CENTRAL, BORDER, pair_measurements, evaluate
)


def frames(a, b):
    return [a.copy(), b.copy(), a.copy()]


class SpatialFalsificationTests(unittest.TestCase):
    def setUp(self):
        self.blank = np.full((HEIGHT, WIDTH), 50, dtype=np.uint8)

    def test_uniform_brightness_rejected_by_adjustment(self):
        changed = np.full_like(self.blank, 70)
        rec, _ = pair_measurements(frames(self.blank, changed), [0, .007, .014], limit=3)
        self.assertGreater(rec["central_raw"][0], 0)
        self.assertGreater(rec["border_raw"][0], 0)
        self.assertEqual(rec["central_adjusted"][0], 0)
        self.assertEqual(rec["border_adjusted"][0], 0)

    def test_center_only_change_not_invented_in_border(self):
        changed = self.blank.copy()
        changed[CENTRAL] += 30
        rec, _ = pair_measurements(frames(self.blank, changed), [0, .007, .014], limit=3)
        self.assertGreater(rec["central_adjusted"][0], 0)
        self.assertEqual(rec["border_adjusted"][0], 0)

    def test_border_only_majority_change_does_not_invent_center(self):
        changed = self.blank.copy()
        changed[BORDER] += 30
        rec, _ = pair_measurements(frames(self.blank, changed), [0, .007, .014], limit=3)
        self.assertEqual(rec["central_raw"][0], 0)
        self.assertEqual(rec["central_adjusted"][0], 0)
        self.assertGreater(rec["border_raw"][0], 0)

    def test_missing_frames_rejected(self):
        with self.assertRaisesRegex(ValueError, "fewer"):
            pair_measurements([self.blank, self.blank], [0, .007, .014], limit=3)

    def test_wrong_shape_rejected(self):
        with self.assertRaisesRegex(ValueError, "shape or dtype"):
            pair_measurements([self.blank, np.zeros((2, 2), dtype=np.uint8), self.blank],
                              [0, .007, .014], limit=3)

    def test_wrong_dtype_rejected(self):
        with self.assertRaisesRegex(ValueError, "shape or dtype"):
            pair_measurements([self.blank, self.blank.astype(np.float32), self.blank],
                              [0, .007, .014], limit=3)

    def test_invalid_candidate_clock_rejected(self):
        with self.assertRaisesRegex(ValueError, "event times"):
            pair_measurements(frames(self.blank, self.blank), [0, .007, .006], limit=3)

    def test_nonfinite_candidate_clock_rejected(self):
        with self.assertRaisesRegex(ValueError, "event times"):
            pair_measurements(frames(self.blank, self.blank), [0, np.nan, .014], limit=3)

    def test_no_medium_gaps_abstains(self):
        n = 1200
        rec = {key: np.full(n, .01) for key in
               ("central_raw", "border_raw", "central_adjusted", "border_adjusted")}
        result = evaluate(rec, np.full(n, .007), n_shifts=32)
        self.assertEqual(result["spatial_screen"], "ABSTAIN_INSUFFICIENT_EVENTS_OR_CONTRAST")
        self.assertFalse(result["physical_release_authorized"])

    def test_synthetic_localized_signal_passes_screen_but_never_physical(self):
        n = 1200
        gaps = np.full(n, .007)
        gaps[np.arange(50, n, 70)] = .05
        rec = {"central_raw": np.full(n, .01), "border_raw": np.full(n, .01),
               "central_adjusted": np.full(n, .01), "border_adjusted": np.full(n, .01)}
        rec["central_adjusted"][gaps > .01] = .08
        rec["central_raw"][gaps > .01] = .08
        result = evaluate(rec, gaps, n_shifts=32)
        self.assertEqual(result["spatial_screen"], "SPATIALLY_LOCALIZED_OPTICAL_ASSOCIATION_UNVERIFIED")
        self.assertEqual(result["null_count"], 32)
        self.assertFalse(result["physical_release_authorized"])
        self.assertEqual(result["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_synthetic_border_signal_fails_specificity(self):
        n = 1200
        gaps = np.full(n, .007)
        gaps[np.arange(50, n, 70)] = .05
        rec = {key: np.full(n, .01) for key in
               ("central_raw", "border_raw", "central_adjusted", "border_adjusted")}
        rec["border_adjusted"][gaps > .01] = .08
        result = evaluate(rec, gaps, n_shifts=32)
        self.assertEqual(result["spatial_screen"], "SPATIAL_SPECIFICITY_NOT_SUPPORTED")

    def test_zero_adjusted_contrast_abstains(self):
        n = 1200
        gaps = np.full(n, .007)
        gaps[::70] = .05
        rec = {key: np.full(n, .01) for key in
               ("central_raw", "border_raw", "central_adjusted", "border_adjusted")}
        rec["central_adjusted"][:] = 0
        result = evaluate(rec, gaps, n_shifts=32)
        self.assertEqual(result["spatial_screen"], "ABSTAIN_INSUFFICIENT_EVENTS_OR_CONTRAST")

    def test_nonfinite_measurement_rejected(self):
        n = 1200
        rec = {key: np.full(n, .01) for key in
               ("central_raw", "border_raw", "central_adjusted", "border_adjusted")}
        rec["central_adjusted"][5] = np.nan
        with self.assertRaisesRegex(ValueError, "invalid normalized"):
            evaluate(rec, np.full(n, .007), n_shifts=32)


if __name__ == "__main__":
    unittest.main()
