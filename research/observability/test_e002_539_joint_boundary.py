#!/usr/bin/env python3
"""E002-539 adversarial exact-math and evidence-gate tests."""
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e002_539_joint_boundary as m


class JointBoundaryTests(unittest.TestCase):
    def case(self, speed=45, fps=30):
        return m.frozen_case(speed, fps)

    def test_frozen_cases(self):
        out = m.run_frozen()
        self.assertEqual(len(out), 5)

    def test_joint_rescue_not_individual_clearance(self):
        out = m.evaluate(self.case())
        self.assertEqual(out["joint_dip"], "93/160")
        self.assertEqual(out["joint_dimensionless_ratio"], "93/112")
        self.assertFalse(out["speed_only_excludes"])
        self.assertFalse(out["acceleration_only_excludes"])
        self.assertTrue(out["joint_excludes_if_hard_bounds"])
        self.assertEqual(out["sharp_lower_aperture"], "51/160")

    def test_equality_is_not_exclusion(self):
        out = m.evaluate(self.case(60))
        self.assertEqual(out["joint_dimensionless_ratio"], "1")
        self.assertFalse(out["joint_excludes_if_hard_bounds"])
        self.assertEqual(out["sharp_lower_aperture"], "1/5")

    def test_crossing_is_feasible(self):
        out = m.evaluate(self.case(65))
        self.assertEqual(out["joint_dip"], "117/160")
        self.assertEqual(out["sharp_lower_aperture"], "27/160")
        self.assertFalse(out["joint_excludes_if_hard_bounds"])

    def test_fast_camera_acceleration_regime(self):
        out = m.evaluate(self.case(45, 240))
        self.assertEqual(out["joint_dip"], "5/384")
        self.assertEqual(out["joint_dimensionless_ratio"], "25/1344")

    def test_gap_inflation_reverses(self):
        self.assertTrue(m.evaluate(self.case(45, 30))["joint_excludes_if_hard_bounds"])
        self.assertFalse(m.evaluate(self.case(45, 15))["joint_excludes_if_hard_bounds"])

    def test_speed_monotonic(self):
        d = F(1, 30)
        self.assertLessEqual(m.joint_dip(d, F(45), F(6000)),
                             m.joint_dip(d, F(65), F(6000)))

    def test_acceleration_monotonic(self):
        d = F(1, 30)
        self.assertLessEqual(m.joint_dip(d, F(45), F(4000)),
                             m.joint_dip(d, F(45), F(6000)))

    def test_zero_speed_or_acceleration(self):
        self.assertEqual(m.joint_dip(F(1, 30), F(0), F(6000)), 0)
        self.assertEqual(m.joint_dip(F(1, 30), F(45), F(0)), 0)

    def test_exact_witness_endpoints_and_midpoint(self):
        b, d, v, a = F(9, 10), F(1, 30), F(45), F(6000)
        self.assertEqual(m.witness_aperture(F(0), b, d, v, a), b)
        self.assertEqual(m.witness_aperture(d, b, d, v, a), b)
        self.assertEqual(m.witness_aperture(d/2, b, d, v, a), F(51, 160))

    def test_equality_witness_touches_threshold(self):
        b, d, v, a = F(9, 10), F(1, 30), F(60), F(6000)
        self.assertEqual(m.witness_aperture(d/2, b, d, v, a), F(1, 5))

    def test_long_gap_witness_can_be_scaled_into_physical_range(self):
        b, d, v, a = F(9, 10), F(1, 15), F(45), F(6000)
        scale = (b-F(1, 5))/m.joint_dip(d, v, a)
        values = [m.witness_aperture(d*F(i, 100), b, d, v, a, scale)
                  for i in range(101)]
        self.assertTrue(all(F(0) <= x <= 1 for x in values))
        self.assertEqual(values[50], F(1, 5))

    def test_extremal_sampled_velocity_and_acceleration(self):
        b, d, v, a, n = F(9, 10), F(1, 30), F(45), F(6000), 240
        dt = d/n
        samples = [m.witness_aperture(i*dt, b, d, v, a)
                   for i in range(n+1)]
        slopes = [(y-x)/dt for x, y in zip(samples, samples[1:])]
        self.assertLessEqual(max(map(abs, slopes)), v)
        self.assertLessEqual(max(abs((y-x)/dt)
                                 for x, y in zip(slopes, slopes[1:])), a)

    def test_exposure_average_not_anatomical_endpoint(self):
        case = self.case()
        case["endpoint_observable"] = "exposure_average"
        out = m.evaluate(case)
        self.assertIn("ENDPOINTS_NOT_POINTWISE_ANATOMY", out["blockers"])
        self.assertEqual(out["product"], "ABSTAIN_UNCALIBRATED")

    def test_cohort_mean_and_sampled_difference_rejected(self):
        out = m.evaluate(self.case())
        self.assertIn("SPEED_NOT_INDEPENDENT_HARD_CONTINUOUS_BOUND", out["blockers"])
        self.assertIn("ACCELERATION_NOT_INDEPENDENT_HARD_CONTINUOUS_BOUND", out["blockers"])

    def test_all_claimed_attestations_still_not_physical_certificate(self):
        case = self.case()
        case["speed_source"] = "independent_continuous_hard_bound"
        case["acceleration_source"] = "independent_continuous_hard_bound"
        case["attestations"] = {k: True for k in m.EVIDENCE}
        out = m.evaluate(case)
        self.assertEqual(out["evidence_decision"], "CONDITIONAL_ONLY_NOT_PHYSICALLY_VERIFIED")
        self.assertFalse(out["physical_validated"])
        self.assertEqual(out["release"], "BLOCKED")

    def test_native_missingness_fails_closed(self):
        case = self.case()
        case["attestations"]["native_frame_missingness_audited"] = False
        self.assertIn("MISSING_NATIVE_FRAME_MISSINGNESS_AUDITED",
                      m.evaluate(case)["blockers"])

    def test_geometry_nuisance_fails_closed(self):
        case = self.case()
        self.assertIn("MISSING_GEOMETRY_GAZE_GLASSES_BRIGHTNESS_BLUR_CONTROLS",
                      m.evaluate(case)["blockers"])

    def test_invalid_input_rejected(self):
        for field, value in (("max_unobserved_gap_s", None),
                             ("equal_endpoint_aperture", "NaN"),
                             ("closure_threshold", "1"),
                             ("hard_speed_s_inverse", "-1"),
                             ("hard_acceleration_s_inverse2", "-1")):
            case = self.case()
            case[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                m.evaluate(case)

    def test_missing_or_spoofed_attestations_rejected(self):
        case = self.case()
        del case["attestations"]["photodiode_authenticated_exposure"]
        with self.assertRaises(ValueError):
            m.evaluate(case)
        case["attestations"]["photodiode_authenticated_exposure"] = "true"
        with self.assertRaises(ValueError):
            m.evaluate(case)


if __name__ == "__main__":
    unittest.main()
