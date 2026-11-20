"""E002-529 preregistered adversarial tests. Synthetic only."""
import importlib.util
from fractions import Fraction as F
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "e529", Path(__file__).with_name("e002_529_dwell_counterexample.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SpeedDwellCounterexampleTests(unittest.TestCase):
    def setUp(self):
        self.b, self.c, self.v, self.H = F(1), F(1, 5), F(60), F(1, 30)
        self.eps = F(1, 10000)
        self.model = m.construct(self.b, self.c, self.v, self.H, self.eps)

    def test_frozen_exact_excursion(self):
        self.assertEqual(self.model["minimum_excursion"], F(2, 75))
        self.assertEqual(self.model["total_excursion"], F(803, 30000))

    def test_endpoints_and_continuity(self):
        self.assertEqual(self.model["knots"][0], (0, self.b))
        self.assertEqual(self.model["knots"][-1], (self.H, self.b))
        self.assertTrue(m.validate_trajectory(self.model))

    def test_strict_dwell_independent_oracle(self):
        self.assertEqual(m.integrate_below_threshold(self.model["knots"], self.c), self.eps)

    def test_velocity_and_range(self):
        for (t0, a0), (t1, a1) in zip(self.model["knots"], self.model["knots"][1:]):
            self.assertTrue(0 <= a0 <= 1 and 0 <= a1 <= 1)
            self.assertLessEqual(abs(a1-a0), self.v*(t1-t0))

    def test_frozen_240hz(self):
        p = m.phase_opportunity(F(1,240), F(1,1000), self.eps, F(1,10000))
        self.assertEqual(p, {"strict_full": F(0), "ideal_overlap": F(33,125)})

    def test_frozen_1000hz(self):
        p = m.phase_opportunity(F(1,1000), F(1,2000), self.eps)
        self.assertEqual(p, {"strict_full": F(0), "ideal_overlap": F(3,5)})

    def test_false_excursion_substitution(self):
        p = m.phase_opportunity(F(1,240), F(1,1000),
                                self.model["minimum_excursion"], F(1,10000))
        self.assertEqual(p["strict_full"], F(1))
        self.assertEqual(m.phase_opportunity(F(1,240), F(1,1000),
                                             self.eps, F(1,10000))["strict_full"], F(0))

    def test_frozen_grid(self):
        self.assertEqual(m.phase_grid_full(F(1,240), F(1,1000),
                                            self.eps, F(1,10000)), F(0))

    def test_heldout_smaller_dwell(self):
        eps = F(1,100000)
        model = m.construct(self.b, self.c, self.v, self.H, eps)
        self.assertTrue(m.validate_trajectory(model))
        self.assertEqual(m.integrate_below_threshold(model["knots"], self.c), eps)

    def test_heldout_10000hz(self):
        eps = F(1,100000)
        p = m.phase_opportunity(F(1,10000), F(1,100000), eps)
        self.assertEqual(p, {"strict_full": F(0), "ideal_overlap": F(1,5)})

    def test_near_critical_gap_refused(self):
        critical = F(2,75)
        for H in (critical, critical-F(1,10000), critical+F(1,100000)):
            with self.subTest(H=H), self.assertRaises(ValueError):
                m.construct(self.b, self.c, self.v, H, self.eps)

    def test_large_gap_allowed(self):
        model = m.construct(self.b, self.c, self.v, F(1), self.eps)
        self.assertTrue(m.validate_trajectory(model))

    def test_unphysical_dip_rejected(self):
        with self.assertRaises(ValueError):
            m.construct(self.b, self.c, self.v, self.H, F(1,10))

    def test_invalid_inputs(self):
        for args in ((1,0,60,F(1,30),self.eps),
                     (1,1,60,F(1,30),self.eps),
                     (1,F(1,5),0,F(1,30),self.eps),
                     (1,F(1,5),60,F(1,30),0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                m.construct(*args)

    def test_floats_and_bool_refused(self):
        for bad in (0.1, True, float("nan"), float("inf")):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                m.construct(1,F(1,5),60,F(1,30),bad)

    def test_modified_slope_refused(self):
        corrupted = dict(self.model)
        knots = list(corrupted["knots"])
        knots[2] = (knots[2][0], F(0))
        corrupted["knots"] = tuple(knots)
        self.assertFalse(m.validate_trajectory(corrupted))

    def test_invalid_camera_refused(self):
        for args in ((0,1,1,0),(1,1,1,0),(1,2,1,0),(2,1,-1,0),(2,1,1,-1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                m.phase_opportunity(*args)

    def test_evidence_tier_fail_closed(self):
        r = m.run_examples()
        self.assertEqual(r["product"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(r["release"], "BLOCKED")
        self.assertFalse(r["authenticated_camera"])
        self.assertFalse(r["certified_human_speed_bound"])
        self.assertEqual(r["human_anatomical_raters"], 0)


if __name__ == "__main__":
    unittest.main()
