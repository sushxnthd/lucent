#!/usr/bin/env python3
"""Independent synthetic E002-412 integrity, aliasing and fail-closed tests."""
import math
import unittest

import numpy as np

import e002_412_human_proxy_aliasing as exp


class E002412(unittest.TestCase):
    def test_independent_nearest_oracle(self):
        self.assertEqual(exp.self_test()["independent_decimation_trials"], 500)

    def test_unobserved_fast_transient_lost_by_phase(self):
        # This is a synthetic optical score, not a blink/aperture trajectory.
        times = [i / 240 for i in range(121)]
        values = [0.1] * len(times)
        values[18] = 0.9
        # At 30Hz, phase zero samples frame indices 0,8,16,24,...;
        # the one-frame transient at index 18 is never observed.
        self.assertEqual(exp.captured_range(times, values, 30, 0.0), 0.0)
        # A phase aligned to frame 18 observes the transient.
        self.assertAlmostEqual(exp.captured_range(times, values, 30, 2/240), 1.0)

    def test_no_missing_frame_imputation(self):
        times = [i / 240 for i in range(121)]
        idx = exp.nearest_indices(times, 60, 0, tolerance=0.001)
        self.assertTrue(all(i is not None for i in idx))
        jittered = [t + (0.003 * math.sin(i / 5)) for i, t in enumerate(times)]
        self.assertGreaterEqual(len(exp.nearest_indices(jittered, 30, 0)), 14)\n        self.assertLessEqual(len(exp.nearest_indices(jittered, 30, 0)), 16)

    def test_zero_variation_not_certified(self):
        times = [i / 240 for i in range(121)]
        self.assertIsNone(exp.captured_range(times, [0.2]*121, 30, 0))
        self.assertIsNone(exp.captured_range(times, [None]*121, 30, 0))

    def test_image_glare_and_shape(self):
        im = np.full((130, 190), 170, dtype=np.uint8)
        im[45:85, 60:125] = 45
        self.assertIsNotNone(exp.score(im))
        self.assertIsNone(exp.score(exp.transform(im, "glare")))
        with self.assertRaises(ValueError):
            exp.score(im[:, :150])

    def test_aggregate_fail_closed_even_when_all_pass(self):
        t = [i/240 for i in range(121)]
        score = [0.1 + .3*math.sin(i / 15) for i in range(121)]
        samples = [(t, {v: score[:] for v in ("clean",) + exp.VARIANTS})
                   for _ in range(8)]
        result = exp.summarize(samples)
        self.assertEqual(result["product"], "ABSTAIN_UNCALIBRATED")
        self.assertFalse(result["physical_aperture_validated"])
        self.assertFalse(result["camera_exposure_calibrated"])
        self.assertEqual(result["clips"], 8)
        self.assertNotIn("event", result)
        self.assertNotIn("source_timestamps", result)

    def test_translation_is_not_silently_claimed_invariant(self):
        t = [i/240 for i in range(100)]
        vals = [0.1 + .2*math.sin(i/10) for i in range(100)]
        d = {v: vals[:] for v in ("clean",) + exp.VARIANTS}
        d["translation_8_6"] = [min(1.0, x + .3) for x in vals]
        result = exp.summarize([(t,d)]*8)
        self.assertTrue(result["translation_transfer_rejected"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
