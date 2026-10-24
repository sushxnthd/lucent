"""Independent numerical oracle and negative controls for E002-420."""
import math
import random
import unittest

from e002_420_exposure_alias import Witness, evaluate, exposure_average


def independent_midpoint(w, center, closed, bins=4096):
    # Separate piecewise construction; no call to the primary aperture function.
    start = center-w.exposure_s/2
    dx = w.exposure_s/bins
    s = 0.
    for j in range(bins):
        t = start+(j+.5)*dx
        if closed:
            drop = min(t, w.frame_gap_s-t) if 0 <= t <= w.frame_gap_s else 0.
            s += w.aperture-w.velocity_per_s*drop
        else:
            s += w.aperture-w.velocity_per_s*w.exposure_s/8
    return s/bins


class TestExposureAlias(unittest.TestCase):
    def test_frozen_witness(self):
        w = Witness(.30, 60., 1/240, .002, .20)
        o = evaluate(w)
        self.assertAlmostEqual(o['predicted_both_exposure_averages'], .285, places=12)
        self.assertAlmostEqual(o['closure_world_minimum'], .175, places=12)
        self.assertTrue(o['conditional_observational_ambiguity'])
        for closed, name in ((False, 'open'), (True, 'closure')):
            for t in (0, w.frame_gap_s):
                self.assertAlmostEqual(independent_midpoint(w, t, closed, 20000), .285, delta=1e-9)
                self.assertAlmostEqual(exposure_average(w, t, name), .285, delta=1e-9)
        self.assertFalse(o['product_claim_authorized'])
        self.assertEqual(o['product'], 'ABSTAIN_UNCALIBRATED')

    def test_one_thousand_blinded_parameter_draws(self):
        rng = random.Random(4202026)
        for _ in range(1000):
            d = rng.uniform(.003, .014)
            v = rng.uniform(5, 55)
            e = d*rng.uniform(.05, 1)
            bottom = v*d/2
            a = rng.uniform(bottom+.03, .95)
            low = a-bottom
            high = a-v*e/8
            theta = (low+high)/2
            w = Witness(a, v, d, e, theta)
            o = evaluate(w)
            self.assertTrue(o['conditional_observational_ambiguity'])
            self.assertGreaterEqual(o['dimensionless_ambiguity_ratio'], 1)
            self.assertLessEqual(0, low)
            self.assertLessEqual(a, 1)
            for closed, name in ((False, 'open'), (True, 'closure')):
                for t in (0, d):
                    numerical = independent_midpoint(w, t, closed)
                    self.assertAlmostEqual(numerical, high, delta=1e-10)
                    self.assertAlmostEqual(exposure_average(w, t, name, 32), numerical, delta=1e-10)
            self.assertFalse(o['product_claim_authorized'])

    def test_negative_controls(self):
        for w in [
            Witness(.3, 60, 1/240, .01, .2),  # exposure exceeds frame separation
            Witness(.1, 60, 1/240, .002, .2),  # negative physical aperture
            Witness(.3, float('nan'), 1/240, .002, .2),
            Witness(.3, 60, 1/240, 0, .2),
        ]:
            with self.assertRaises(ValueError):
                evaluate(w)
        self.assertFalse(evaluate(Witness(.3, 60, 1/240, .002, .05))['conditional_observational_ambiguity'])
        self.assertFalse(evaluate(Witness(.3, 60, 1/240, .002, .29))['conditional_observational_ambiguity'])
        self.assertIsNone(evaluate(Witness(.3, 60, 1/240, .002, .29))['dimensionless_ambiguity_ratio'])
        with self.assertRaises(ValueError):
            exposure_average(Witness(.3, 60, 1/240, .002, .2), 0, 'closure', 5)


if __name__ == '__main__':
    unittest.main()
