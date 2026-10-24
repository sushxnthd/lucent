#!/usr/bin/env python3
"""Independent LP and adversarial tests for frozen E002-422 predictions."""
from __future__ import annotations
import math
import random
import unittest

import numpy as np
from scipy.optimize import linprog

from e002_422_unequal_boxcar import conditional_full_horizon, open_world, witness


def independently_optimize(a, b, V, d, E):
    """Independent piecewise-linear LP: exact shutter integrals, speed constraints.

    Optimize at every grid node; no candidate bound is imported or used by LP.
    A fine grid includes the possible cusp location so a V-shaped extremizer
    is representable. This is a finite-dimensional check, not a continuum proof.
    """
    cusp = d / 2 + (a - b) / (2 * V)
    ts = np.unique(np.concatenate((
        np.linspace(-E / 2, E / 2, 13),
        np.linspace(E / 2, d - E / 2, 21),
        np.linspace(d - E / 2, d + E / 2, 13),
        [cusp],
    )))
    n = len(ts)
    eq = np.zeros((2, n))
    for row, lo, hi in ((0, -E / 2, E / 2),
                        (1, d - E / 2, d + E / 2)):
        for j in range(n - 1):
            overlap = max(0., min(ts[j + 1], hi) - max(ts[j], lo))
            if overlap:
                if abs(overlap - (ts[j + 1] - ts[j])) > 1e-10:
                    raise AssertionError("Integration grid crosses shutter boundary")
                eq[row, j] += overlap / (2 * E)
                eq[row, j + 1] += overlap / (2 * E)
    inequalities = np.zeros((2 * (n - 1), n))
    rhs = np.zeros(2 * (n - 1))
    for j in range(n - 1):
        h = V * (ts[j + 1] - ts[j])
        inequalities[2 * j, j] = 1
        inequalities[2 * j, j + 1] = -1
        inequalities[2 * j + 1, j] = -1
        inequalities[2 * j + 1, j + 1] = 1
        rhs[2 * j:2 * j + 2] = h
    minima = []
    for k in range(n):
        objective = np.zeros(n)
        objective[k] = 1.
        solution = linprog(objective, A_ub=inequalities, b_ub=rhs,
                           A_eq=eq, b_eq=np.array([a, b]),
                           bounds=(0., 1.), method="highs")
        if not solution.success:
            raise AssertionError(f"LP infeasible: {solution.message}")
        minima.append(float(solution.fun))
    return min(minima)


class UnequalBoxcarIndependentTests(unittest.TestCase):
    def test_frozen_false_safety_shortcut(self):
        a, b, V, d, E, theta = .4, .3, 50., .006, .002, .2
        r = conditional_full_horizon(a, b, V, d, E, theta)
        self.assertAlmostEqual(r["sharp_lower_bound"], .2, places=12)
        self.assertAlmostEqual(r["valley_time"], .004, places=12)
        self.assertEqual(r["research_decision"], "AMBIGUOUS_OR_NUMERICALLY_BORDERLINE")
        self.assertEqual(r["product_decision"], "ABSTAIN_UNCALIBRATED")
        self.assertGreater(max(a, b) - V * d / 2, theta)  # unsafe shortcut
        self.assertAlmostEqual(independently_optimize(a, b, V, d, E), .2, places=8)
        for center, expected in ((0., a), (d, b)):
            for f in (witness,):
                ts = np.linspace(center - E / 2, center + E / 2, 1001)
                ys = np.array([f(t, a, b, V, d) for t in ts])
                mean = float(np.trapezoid(ys, ts) / E)
                self.assertAlmostEqual(mean, expected, places=9)
            ts = np.linspace(center - E / 2, center + E / 2, 1001)
            self.assertAlmostEqual(float(np.trapezoid(
                [open_world(t, a, b, d, E) for t in ts], ts) / E),
                expected, places=9)
        self.assertAlmostEqual(witness(.004, a, b, V, d), theta)
        self.assertGreater(min(open_world(t, a, b, d, E)
                               for t in np.linspace(-E / 2, d + E / 2, 1001)), theta)

    def test_40_independent_unequal_mean_linear_programs(self):
        rng = random.Random(422)
        classes = set()
        for i in range(40):
            for _ in range(10000):
                d = rng.uniform(.004, .012)
                E = rng.uniform(.0005, .65 * d)
                V = rng.uniform(10, 35)
                center = rng.uniform(.40, .72)
                delta = rng.uniform(-.75, .75) * V * (d - E)
                a, b = center + delta / 2, center - delta / 2
                L = (a + b - V * d) / 2
                if L > .07 and max(a, b) + V * E / 2 < .98:
                    break
            else:
                self.fail("Unable to sample valid frozen regime")
            theta = L - .025 if i % 2 == 0 else L + .2 * (min(a, b) - L)
            r = conditional_full_horizon(a, b, V, d, E, theta)
            self.assertAlmostEqual(r["sharp_lower_bound"], L, places=11)
            oracle = independently_optimize(a, b, V, d, E)
            self.assertLess(abs(oracle - L), 1e-7)
            self.assertEqual(r["product_decision"], "ABSTAIN_UNCALIBRATED")
            classes.add(r["research_decision"])
        self.assertEqual(classes, {"CONDITIONAL_NO_CLOSURE",
                                   "AMBIGUOUS_OR_NUMERICALLY_BORDERLINE"})

    def test_unqualified_and_malformed_inputs_fail_closed(self):
        invalid = ((float("nan"), .3, 50., .006, .002, .2),
                   (None, .3, 50., .006, .002, .2),
                   (True, .3, 50., .006, .002, .2),
                   (.4, .3, 0., .006, .002, .2),
                   (.4, .3, 50., .006, .007, .2),
                   (.4, .3, 50., .006, .002, .31))
        for params in invalid:
            with self.subTest(params=params), self.assertRaises(ValueError):
                conditional_full_horizon(*params)
        out_of_regime = ((.6, .2, 20., .006, .002, .1),
                         (.4, .3, 500., .006, .002, .1),
                         (.95, .9, 50., .006, .004, .2))
        for params in out_of_regime:
            with self.subTest(params=params):
                r = conditional_full_horizon(*params)
                self.assertEqual(r["research_decision"], "UNRESOLVED_MODEL")
                self.assertIsNone(r["sharp_lower_bound"])
                self.assertEqual(r["product_decision"], "ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    unittest.main()
