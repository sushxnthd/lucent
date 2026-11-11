#!/usr/bin/env python3
"""Independent midpoint-quadrature checks for E002-424's exact synthetic alias."""
import math
import unittest

try:
    from . import e002_424_subphase_shutter_alias as m
except ImportError:
    import e002_424_subphase_shutter_alias as m


def midpoint_integral(row, mode, phase=None, width=None, minimum=None):
    """Separate numerical forward model; does not use m.segments or m.pulse_response."""
    c = (0.0, 3.2)[row]
    e = 2.4
    step = 0.0005
    n = 4800
    left = c - e / 2
    result = 0.0
    for i in range(n):
        t = left + (i + 0.5) * step
        if mode == 'boxcar':
            h = 1 / e
        else:
            u = (t - left) / 0.1
            frac = u - math.floor(u)
            sign = 1 if row == 0 else -1
            h = (1 + sign * 0.99 * (1 if frac < 0.5 else -1)) / e
        if phase is not None:
            y = 1.0 if phase <= t < phase + width else 0.0
        else:
            y = minimum + 0.05 * abs(t - 1.6)
        result += step * h * y
    return result


class E002424Tests(unittest.TestCase):
    def test_frozen_predictions(self):
        x = m.experiment()
        self.assertEqual(x['phase_count'], 101)
        self.assertTrue(all(x['frozen_tests'].values()), x)
        self.assertLess(max(x['max_original_grid_response_difference_per_row']), 1e-11)
        self.assertGreater(min(x['max_changed_width_response_difference_per_row']), 0.015)
        self.assertAlmostEqual(x['minimum_aperture_boxcar_world'], 0.201, places=12)
        self.assertAlmostEqual(x['minimum_aperture_subphase_world'], 0.1997625, places=12)
        self.assertEqual(x['policy']['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertFalse(x['policy']['product_claim_authorized'])

    def test_independent_midpoint_quadrature(self):
        for row in (0, 1):
            for mode in ('boxcar', 'subphase'):
                for s, width in [(-2.1, 0.5), (-1.2, 0.5), (-1.0, 0.45),
                                 (-0.75, 0.45), (0.0, 0.5), (1.1, 0.45),
                                 (2.0, 0.5), (3.15, 0.45), (4.3, 0.45), (5.3, 0.5)]:
                    with self.subTest(row=row, mode=mode, s=s, width=width):
                        exact = m.pulse_response(row, mode, s, width)
                        numerical = midpoint_integral(row, mode, phase=s, width=width)
                        self.assertAlmostEqual(exact, numerical, delta=1e-10)
                minimum = 0.201 if mode == 'boxcar' else 0.1997625
                self.assertAlmostEqual(m.aperture_response(row, mode, minimum),
                                       midpoint_integral(row, mode, minimum=minimum),
                                       delta=1e-9)

    def test_kernel_is_genuinely_different_and_nonnegative(self):
        for row in (0, 1):
            seg = m.segments(row, 'subphase')
            self.assertEqual(len(seg), 48)
            self.assertGreater(min(w for _, _, w in seg), 0)
            self.assertAlmostEqual(sum((b-a)*w for a,b,w in seg), 1, places=12)
            l1 = sum((b-a)*abs(w-1/2.4) for a,b,w in seg)
            self.assertAlmostEqual(l1, 0.99, places=12)

    def test_invalid_and_physical_abstention(self):
        for args in [(-1, 'boxcar', 0.0, 0.5), (2, 'subphase', 0.0, 0.5),
                     (0, 'unknown', 0.0, 0.5), (0, 'boxcar', float('nan'), 0.5),
                     (0, 'boxcar', 0.0, -1), (0, 'boxcar', 0.0, float('inf'))]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                m.pulse_response(*args)
        with self.assertRaises(ValueError):
            m.aperture_response(0, 'subphase', float('nan'))
        self.assertFalse(m.policy()['physical_camera_authenticated'])
        self.assertFalse(m.policy()['human_velocity_authenticated'])


if __name__ == '__main__':
    unittest.main()
