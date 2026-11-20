"""E002-491 synthetic nuisance controls, not human-anatomical validation."""
import unittest
import e002_491_calibration_motion as m


def synthetic(patch=None, brightness=0, low_contrast=False):
    raw = bytearray(100 if low_contrast else (60 if (x + y) % 2 else 190)
                    for y in range(64) for x in range(64))
    if patch is not None:
        x0, y0, x1, y1 = patch
        for y in range(y0, y1):
            for x in range(x0, x1):
                raw[y * 64 + x] = 25
    return bytes(min(255, max(0, v + brightness)) for v in raw)


class TestCalibrationScreen(unittest.TestCase):
    def setUp(self):
        self.base = synthetic()
        self.a = synthetic((20, 20, 28, 28))
        self.b = synthetic((30, 20, 38, 28))

    def test_exact_duplicate(self):
        self.assertEqual(m.motion_pair(self.base, self.base)["status"], "DUPLICATE")

    def test_global_brightness_invariant(self):
        r = m.motion_pair(self.base, synthetic(brightness=10))
        self.assertEqual(r["status"], "ELIGIBLE")
        self.assertLess(r["center"], 1e-12)
        self.assertFalse(r["candidate"])

    def test_large_brightness_change_abstains(self):
        self.assertEqual(m.motion_pair(self.base, synthetic(brightness=40))["status"], "NUISANCE")

    def test_center_localized_change_is_candidate_not_closure(self):
        r = m.motion_pair(self.a, self.b)
        self.assertTrue(r["candidate"])
        self.assertGreater(r["center"], 0.035)
        self.assertGreater(r["ratio"], 1.7)

    def test_border_only_motion_not_candidate(self):
        edge = synthetic((0, 0, 8, 8))
        self.assertFalse(m.motion_pair(self.base, edge)["candidate"])

    def test_low_contrast_rejected(self):
        r = m.motion_pair(synthetic(low_contrast=True),
                          synthetic(low_contrast=True, brightness=1))
        self.assertEqual(r["status"], "NUISANCE")

    def test_gaze_like_translation_is_not_anatomical_label(self):
        report = m.analyze([self.a, self.b, self.a])
        self.assertGreater(report["localized_motion_candidate_pairs"], 0)
        self.assertEqual(report["anatomical_closure_labels"], 0)
        self.assertFalse(report["physical_hidden_closure_certified"])
        self.assertEqual(report["product"], "ABSTAIN_UNCALIBRATED")

    def test_duplicate_count_and_blocked_release(self):
        r = m.analyze([self.base, self.base, self.a, self.b])
        self.assertEqual(r["decoded_native_frames"], 4)
        self.assertEqual(r["exact_duplicate_pairs"], 1)
        self.assertEqual(r["release"], "BLOCKED")
        self.assertFalse(r["acquisition_fps_authenticated"])

    def test_invalid_frame_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_FRAME_SIZE"):
            m.motion_pair(b"short", self.base)

    def test_insufficient_frames_rejected(self):
        with self.assertRaisesRegex(ValueError, "INSUFFICIENT_DECODED_FRAMES"):
            m.analyze([self.base, self.a])


if __name__ == "__main__":
    unittest.main()
