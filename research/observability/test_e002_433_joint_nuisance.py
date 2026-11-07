"""Independent adversarial regression for preregistered E002-433."""
import math
import random
import unittest

from e002_433_joint_nuisance import (
    D, E, THETA, V, Y, G_RANGE, ANGLE_RANGE, ENDPOINT_B, MIN_B,
    conditional_lower, cosd, experiment, exposure_mean, optical,
    stress, world_a, world_b, world_b_aperture,
)


def independent_trapezoid(world, center, intervals=20000):
    step = E / intervals
    start = center - E / 2
    total = (optical(world, start) + optical(world, start + E)) / 2
    for j in range(1, intervals):
        total += optical(world, start + j * step)
    return total / intervals


class JointNuisanceScience(unittest.TestCase):
    def test_independent_quadrature_and_alias(self):
        for center in (0.0, D):
            for world in (world_a, world_b):
                self.assertAlmostEqual(exposure_mean(world, center),
                                       independent_trapezoid(world, center),
                                       delta=1e-9)
                self.assertAlmostEqual(exposure_mean(world, center), Y, delta=1e-10)
        self.assertLess(experiment()["max_observation_discrepancy"], 1e-10)

    def test_physical_velocity_and_hidden_closure(self):
        slope = (ENDPOINT_B - MIN_B) / (D / 2 - E / 2)
        self.assertLessEqual(slope, V)
        dt = D / 20000
        values = [world_b_aperture(j * dt) for j in range(20001)]
        self.assertAlmostEqual(min(values), MIN_B, delta=1e-12)
        self.assertTrue(any(x < THETA for x in values))
        self.assertTrue(all(abs(b - a) / dt <= V + 1e-8
                            for a, b in zip(values, values[1:])))
        self.assertGreater(world_a(0)[0], THETA)

    def test_both_nuisances_are_admissible(self):
        a, gain, phi = world_b(D / 2)
        self.assertAlmostEqual(a, MIN_B)
        self.assertGreaterEqual(gain, G_RANGE[0])
        self.assertLessEqual(gain, G_RANGE[1])
        self.assertGreaterEqual(phi, ANGLE_RANGE[0])
        self.assertLessEqual(phi, ANGLE_RANGE[1])
        for t in (0, D / 2, D):
            self.assertAlmostEqual(world_b(t)[1], gain)
            self.assertAlmostEqual(world_b(t)[2], phi)

    def test_incomplete_independent_checks_are_unsound(self):
        naive = conditional_lower(Y, Y, 1.0, 20.0)
        geometry_only = conditional_lower(Y, Y, 1.0, 15.0)
        gain_only = conditional_lower(Y, Y, 1.03, 20.0)
        joint = conditional_lower(Y, Y, 1.03, 15.0)
        self.assertGreater(naive, THETA)
        self.assertGreater(geometry_only, THETA)
        self.assertGreater(gain_only, THETA)
        self.assertLess(joint, THETA)
        self.assertLess(MIN_B, THETA)
        self.assertAlmostEqual(joint, 1.985245010505016, places=10)
        self.assertTrue(experiment()["incomplete_checks_false_candidates"])
        self.assertTrue(experiment()["joint_abstains"])

    def test_holdout_and_independent_lipschitz_oracle(self):
        r = stress()
        self.assertEqual(r, stress())
        self.assertEqual(r["n"], 2000)
        self.assertGreater(r["candidates"], 0)
        self.assertGreater(r["true_closures"], 0)
        self.assertEqual(r["false_certificates"], 0)
        self.assertGreaterEqual(r["min_truth_minus_bound_mm"], -1e-9)
        # Independent pointwise adversarial oracle: for a nonnegative
        # V-Lipschitz path, a(t) >= a(s)-V|t-s|. Verify the claimed
        # lower formula never exceeds a dense-grid min for random
        # piecewise-linear paths with fixed nuisance bounds.
        rng = random.Random(9433)
        for _ in range(300):
            x0 = rng.uniform(1.85, 2.25)
            xmid = x0 + rng.uniform(-V, V) * D / 2
            x1 = xmid + rng.uniform(-V, V) * D / 2
            # Instantaneous shutter surrogate is a limiting oracle;
            # exact finite-exposure holdout is separately checked.
            y0 = x0 * rng.uniform(*G_RANGE) * cosd(rng.uniform(*ANGLE_RANGE))
            y1 = x1 * rng.uniform(*G_RANGE) * cosd(rng.uniform(*ANGLE_RANGE))
            lower = conditional_lower(y0, y1, G_RANGE[1], ANGLE_RANGE[0])
            self.assertLessEqual(lower, min(x0, xmid, x1) + 1e-9)

    def test_invalid_metadata_and_physical_abstention(self):
        bad = [
            (float("nan"), Y, 1.03, 15.0),
            (Y, None, 1.03, 15.0),
            (Y, Y, 0.0, 15.0),
            (Y, Y, -1.0, 15.0),
            (Y, Y, 1.03, -0.1),
            (Y, Y, 1.03, 90.0),
            (-1.0, Y, 1.03, 15.0),
        ]
        for args in bad:
            with self.subTest(args=args), self.assertRaises(ValueError):
                conditional_lower(*args)
        for kwargs in (
            {"speed_cap": -1.0}, {"center_spacing": 0.0},
            {"exposure_s": 0.0}, {"exposure_s": D + 0.1},
            {"center_spacing": float("inf")},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                conditional_lower(Y, Y, 1.03, 15.0, **kwargs)
        with self.assertRaises(ValueError):
            world_b_aperture(None)
        with self.assertRaises(ValueError):
            exposure_mean(world_b, 0, subdivisions=0)
        with self.assertRaises(ValueError):
            stress(n=100)
        self.assertFalse(experiment()["physical_certificate_authorized"])
        self.assertEqual(experiment()["product"], "ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    unittest.main()
