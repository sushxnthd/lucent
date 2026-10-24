#!/usr/bin/env python3
"""Independent checks for E002-425; no physical or human evidence is inferred."""
import math
import unittest

import numpy as np

try:
    from . import e002_425_shutter_identification as m
except ImportError:
    import e002_425_shutter_identification as m


def independent_midpoint_pulse(start, width, masses, dt=0.0001):
    """Direct time-domain quadrature, not the production overlap matrix."""
    total = 0.0
    n = round(2.4 / dt)
    for i in range(n):
        t = (i + 0.5) * dt
        if start <= t < start + width:
            cell = min(47, int(t / 0.05))
            total += masses[cell] * dt / 0.05
    return total


class E002425Tests(unittest.TestCase):
    def test_frozen_predictions_and_product_boundary(self):
        result = m.experiment()
        self.assertEqual(result["bins"], 48)
        self.assertEqual(result["calibration_observations"], 256)
        self.assertEqual(result["heldout_observations"], 128)
        self.assertTrue(all(result["frozen_tests"].values()), result)
        self.assertFalse(result["policy"]["camera_hardware_authenticated"])
        self.assertFalse(result["policy"]["product_claim_authorized"])
        self.assertEqual(result["policy"]["product"], "ABSTAIN_UNCALIBRATED")

    def test_independent_time_quadrature(self):
        _, A, starts, widths = m.designs()
        uniform, alternating = m.kernels()
        for masses in (uniform, alternating):
            for k in (0, 7, 25, 55, 127, 256, 283, 383):
                with self.subTest(kernel=masses[0], sample=k):
                    predicted = float(A[k] @ masses)
                    independently_integrated = independent_midpoint_pulse(
                        float(starts[k]), float(widths[k]), masses)
                    self.assertAlmostEqual(predicted, independently_integrated, delta=0.00011)

    def test_legacy_nullspace_and_holdout_conservation(self):
        legacy, A, starts, widths = m.designs()
        uniform, alternating = m.kernels()
        delta = uniform - alternating
        self.assertAlmostEqual(float(np.linalg.norm(delta, ord=1)), 0.99, places=12)
        self.assertEqual(np.linalg.matrix_rank(legacy), 24)
        self.assertLess(float(np.max(np.abs(legacy @ delta))), 1e-12)
        self.assertEqual(A.shape, (384, 48))
        self.assertTrue(np.all(A >= 0))
        self.assertTrue(np.all(A <= 1 + 1e-12))
        self.assertTrue(np.all((widths == 0.37) | (widths == 0.43) | (widths == 0.51)))
        self.assertGreater(float(np.max(np.abs(A[256:] @ delta))), 0.01)
        self.assertEqual(len(np.unique(starts)), 384)

    def test_invalid_inputs_and_bounded_fit(self):
        for s, w in (([], []), ([0], []), ([float("nan")], [0.5]),
                     ([0], [-0.2]), ([0], [float("inf")]), ([[0]], [[0.5]])):
            with self.subTest(s=s, w=w), self.assertRaises(ValueError):
                m.pulse_matrix(np.array(s), np.array(w))
        with self.assertRaises(ValueError):
            m.recover(np.ones((2, 47)), np.ones(2))
        with self.assertRaises(ValueError):
            m.recover(np.ones((2, 48)), np.array([0, float("nan")]))
        with self.assertRaises(ValueError):
            m.recover(np.ones((2, 48)), np.ones(3))


if __name__ == "__main__":
    unittest.main()
