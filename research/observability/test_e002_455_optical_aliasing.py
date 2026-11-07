#!/usr/bin/env python3
"""Independent synthetic and adversarial tests for E002-455 (no human labels)."""
import unittest
import numpy as np

from e002_455_optical_aliasing import (
    C, HEIGHT, WIDTH, evaluate, frame_observables, read_series
)


class OpticalAliasingTests(unittest.TestCase):
    def setUp(self):
        self.z = np.zeros(80, dtype=float)
        self.w = np.zeros(80, dtype=float)

    def test_hidden_pulse_both_strides(self):
        self.z[20] = .1
        r = evaluate(self.z, self.w, start=10, strides=(8, 17))
        self.assertEqual(r["optical_decision"], "PRIMARY_OPTICAL_ALIASING_OBSERVED_CONTROL_LOWER")
        self.assertGreater(r["stride_results"]["8"]["primary"]["hidden_excursions"], 0)
        self.assertGreater(r["stride_results"]["17"]["primary"]["hidden_excursions"], 0)
        self.assertFalse(r["physical_release_authorized"])

    def test_monotone_linear_is_not_excursion(self):
        z = np.linspace(0, 1, 80)
        r = evaluate(z, self.w, start=10, strides=(8, 17))
        self.assertEqual(r["optical_decision"], "NOT_OBSERVED")

    def test_nuisance_control_equal_prevents_specificity(self):
        self.z[20] = .1
        r = evaluate(self.z, self.z, start=10, strides=(8, 17))
        self.assertEqual(r["optical_decision"], "SPATIAL_SPECIFICITY_NOT_ESTABLISHED")

    def test_additive_uniform_brightness_invariance(self):
        a = np.full((HEIGHT, WIDTH), 40, dtype=np.uint8)
        a[C] = 100
        b = a + np.uint8(12)
        z1, w1 = frame_observables(a)
        z2, w2 = frame_observables(b)
        self.assertAlmostEqual(z1, z2)
        self.assertAlmostEqual(w1, w2)

    def test_nonanatomical_spatial_gradient_can_trigger(self):
        # Illumination confined to central ROI mimics optical excursion.
        a = np.full((HEIGHT, WIDTH), 30, dtype=np.uint8)
        b = a.copy()
        b[C] = 90
        z0, w0 = frame_observables(a)
        z1, w1 = frame_observables(b)
        z = np.full(80, z0)
        z[20] = z1
        r = evaluate(z, np.full(80, w0), start=10, strides=(8, 17))
        self.assertGreater(r["stride_results"]["8"]["primary"]["hidden_excursions"], 0)
        self.assertFalse(r["independent_anatomical_labels"])
        self.assertEqual(r["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_missing_frames_fail_closed(self):
        frame = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
        with self.assertRaisesRegex(ValueError, "missing"):
            read_series(iter([frame, frame]), limit=3)

    def test_invalid_frame_shape_rejected(self):
        with self.assertRaises(ValueError):
            frame_observables(np.zeros((3, 3), dtype=np.uint8))

    def test_invalid_dtype_rejected(self):
        with self.assertRaises(ValueError):
            frame_observables(np.zeros((HEIGHT, WIDTH), dtype=float))

    def test_nan_series_rejected(self):
        self.z[19] = np.nan
        with self.assertRaises(ValueError):
            evaluate(self.z, self.w, start=10, strides=(8, 17))

    def test_phase_count_exact(self):
        r = evaluate(self.z, self.w, start=10, strides=(8, 17))
        for k in (8, 17):
            s = r["stride_results"][str(k)]["primary"]
            self.assertEqual(s["intervals"], len(self.z) - 10 - k)
            self.assertEqual(sum(p["intervals"] for p in s["per_phase"]), s["intervals"])
            self.assertEqual(len(s["per_phase"]), k)

    def test_insufficient_window_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(self.z[:20], self.w[:20], start=10, strides=(8, 17))

    def test_duplicate_stride_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(self.z, self.w, start=10, strides=(8, 8))

    def test_fixed_threshold_floor(self):
        r = evaluate(self.z, self.w, start=10, strides=(8, 17))
        self.assertAlmostEqual(r["threshold_contrast_normalized"], 4 / 255)

    def test_unsupported_physical_claim_rejected(self):
        self.z[20] = .1
        r = evaluate(self.z, self.w, start=10, strides=(8, 17))
        self.assertEqual(r["e002_371_physical_validation"], "NOT_ESTABLISHED")
        self.assertFalse(r["physical_shutter_calibration"])
        self.assertFalse(r["physiological_velocity_upper_bound_validated"])
        self.assertFalse(r["participant_holdouts_inspected"])


if __name__ == "__main__":
    unittest.main()
