"""E002-446 independent synthetic adversarial tests; no human imagery."""
import unittest
import numpy as np
from e002_446_edge_triage import WIDTH, HEIGHT, edge_span, summarize


def eye(top=95, bottom=185, brightness=0):
    f = np.full((HEIGHT, WIDTH), 175+brightness, dtype=np.uint8)
    f[top:bottom, 80:240] = 55+brightness
    return f


class EdgeTriageTests(unittest.TestCase):
    def test_synthetic_eye_candidate(self):
        v = edge_span(eye())
        self.assertIsNotNone(v)
        self.assertAlmostEqual(v[1]-v[0], 90, delta=3)

    def test_additive_brightness_invariant(self):
        self.assertEqual(edge_span(eye()), edge_span(eye(brightness=30)))

    def test_pupil_only_rejected_by_width(self):
        y, x = np.ogrid[:HEIGHT, :WIDTH]
        f = np.full((HEIGHT, WIDTH), 175, dtype=np.uint8)
        f[(x-160)**2+(y-140)**2 < 30**2] = 55
        self.assertIsNone(edge_span(f))

    def test_horizontal_dark_stripe_is_false_anatomy(self):
        # Not an eyelid: glasses/overlay shadow; identical pixel geometry.
        stripe = np.full((HEIGHT, WIDTH), 175, dtype=np.uint8)
        stripe[95:185, 80:240] = 55
        self.assertIsNotNone(edge_span(stripe))
        self.assertEqual(edge_span(stripe), edge_span(eye()))

    def test_flat_image_abstains(self):
        self.assertIsNone(edge_span(np.full((HEIGHT, WIDTH), 150, dtype=np.uint8)))

    def test_wrong_shape_rejected(self):
        with self.assertRaisesRegex(ValueError, "shape"):
            edge_span(np.zeros((20, 20), dtype=np.uint8))

    def test_wrong_dtype_rejected(self):
        with self.assertRaisesRegex(ValueError, "dtype"):
            edge_span(np.zeros((HEIGHT, WIDTH), dtype=float))

    def test_summary_fails_closed(self):
        s = summarize([eye() for _ in range(5)], limit=5)
        self.assertEqual(s["edge_span_candidate_frames"], 5)
        self.assertEqual(s["triage_screen"], "ANNOTATION_TRIAGE_ONLY_NOT_ANATOMY")
        self.assertFalse(s["anatomical_aperture_measured"])
        self.assertFalse(s["physical_release_authorized"])
        self.assertEqual(s["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_insufficient_frames_rejected(self):
        with self.assertRaisesRegex(ValueError, "fewer"):
            summarize([eye() for _ in range(2)], limit=3)

    def test_no_candidate_summary_is_null_not_zero_aperture(self):
        s = summarize([np.full((HEIGHT, WIDTH), 150, dtype=np.uint8) for _ in range(5)], limit=5)
        self.assertEqual(s["edge_span_candidate_frames"], 0)
        self.assertIsNone(s["candidate_span_px_median"])
        self.assertIsNone(s["candidate_edge_jump_ge_20_fraction"])
        self.assertEqual(s["triage_screen"], "REJECT_UNSTABLE_OR_INSUFFICIENT_EDGE_PROXY")

    def test_large_jumps_reject_triage(self):
        seq = [eye(80, 170), eye(110, 200), eye(80, 170), eye(110, 200), eye(80, 170)]
        s = summarize(seq, limit=5)
        self.assertGreater(s["candidate_edge_jump_ge_20_fraction"], .1)
        self.assertEqual(s["triage_screen"], "REJECT_UNSTABLE_OR_INSUFFICIENT_EDGE_PROXY")


if __name__ == "__main__":
    unittest.main()
