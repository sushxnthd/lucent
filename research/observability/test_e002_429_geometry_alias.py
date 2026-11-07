"""Independent tests for E002-429; no private images or external packages."""
import math
import unittest
from e002_429_geometry_alias import (
    ALIased_ENDPOINT_MM, ALIased_MIN_MM, EXPOSURE_S, FRAME_PERIOD_S,
    OPEN_MM, REFERENCE_ANGLE_DEG, THRESHOLD_MM, VELOCITY_CAP_MM_S,
    boxcar_average, effective_angle_deg, experiment, hidden_aperture,
    pixel_observable, projected_lower_bound,
)


class GeometryAlias(unittest.TestCase):
    def test_independent_physical_velocity_and_crossing(self):
        # Finite-difference oracle on a grid including the V cusp.
        n = 2000
        ts = [i * FRAME_PERIOD_S / n for i in range(n + 1)]
        hs = [hidden_aperture(t) for t in ts]
        self.assertAlmostEqual(min(hs), ALIased_MIN_MM, places=12)
        self.assertGreater(hs[0], THRESHOLD_MM)
        self.assertGreater(hs[-1], THRESHOLD_MM)
        self.assertLess(min(hs), THRESHOLD_MM)
        slopes = [abs(b-a) / (FRAME_PERIOD_S/n) for a, b in zip(hs, hs[1:])]
        self.assertLessEqual(max(slopes), VELOCITY_CAP_MM_S + 1e-9)

    def test_full_continuous_projection_alias(self):
        target = OPEN_MM * math.cos(math.radians(REFERENCE_ANGLE_DEG))
        for i in range(-100, 1101):
            t = i * FRAME_PERIOD_S / 1000
            h = hidden_aperture(t)
            # Distinct geometric angle restores the same projected signal.
            self.assertAlmostEqual(h * math.cos(math.radians(effective_angle_deg(h))), target, places=12)
        self.assertNotAlmostEqual(effective_angle_deg(ALIased_MIN_MM), REFERENCE_ANGLE_DEG, places=3)

    def test_shutter_and_rate_independence(self):
        # Independent quadrature across rates and exposures: alias exists even at 500 fps.
        target = pixel_observable(OPEN_MM, REFERENCE_ANGLE_DEG)
        for rate in (24, 30, 60, 120, 500):
            for exposure in (0.0005, 0.002, 0.004):
                for j in range(3):
                    center = j / rate
                    got = boxcar_average(lambda t: pixel_observable(hidden_aperture(t), effective_angle_deg(hidden_aperture(t))), center, exposure, n=200)
                    self.assertAlmostEqual(got, target, places=10)

    def test_false_fixed_geometry_certificate_and_guard(self):
        r = experiment()
        self.assertTrue(r['naive_would_claim_no_closure'])
        self.assertGreater(r['naive_fixed_angle_sharp_lower_mm'], THRESHOLD_MM)
        self.assertLess(r['world_b_physical_min_mm'], THRESHOLD_MM)
        self.assertTrue(r['interval_guard_rejects'])
        self.assertFalse(r['physical_certificate_authorized'])
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')

    def test_geometry_interval_monotonicity_and_invalid(self):
        y = pixel_observable(OPEN_MM, REFERENCE_ANGLE_DEG)
        self.assertLess(projected_lower_bound(y, 15, 20), THRESHOLD_MM)
        self.assertGreater(projected_lower_bound(y, 18, 20), THRESHOLD_MM)
        for args in ((-1, 15, 20), (y, -1, 20), (y, 25, 20),
                     (y, 15, 90), (float('nan'), 15, 20)):
            with self.assertRaises(ValueError):
                projected_lower_bound(*args)


if __name__ == '__main__':
    unittest.main()
