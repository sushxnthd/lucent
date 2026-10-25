"""Independent numerical and adversarial tests for E002-430."""
import math
import unittest
from e002_430_reference_sampling import (THRESHOLD_MM, envelope_lower, synthetic_alias, experiment)


class ReferenceSamplingTests(unittest.TestCase):
    def test_four_rates_identical_samples_but_hidden_closure(self):
        for rate in (200, 400, 500, 600):
            x = synthetic_alias(rate)
            self.assertTrue(x['sampled_worlds_equal'])
            self.assertTrue(x['reference_samples_naively_no_closure'])
            self.assertTrue(x['continuous_hidden_world_crosses_threshold'])
            self.assertAlmostEqual(x['hidden_world_peak_speed_mm_s'], .4*rate)
            self.assertFalse(x['reference_negative_authorized'])

    def test_independent_midpoint_oracle_and_speed(self):
        for rate in (200,400,500,600):
            dt = 1/rate
            a, m = 2.15, 1.95
            # Independent two-line reference witness (not calling production trajectory).
            f = lambda t: a - 2*(a-m)*t/dt if t <= dt/2 else m + 2*(a-m)*(t-dt/2)/dt
            values = [f(i*dt/10000) for i in range(10001)]
            self.assertAlmostEqual(min(values), m, places=12)
            self.assertAlmostEqual(values[0], values[-1], places=12)
            vmax = max(abs(values[i+1]-values[i])/(dt/10000) for i in range(10000))
            self.assertAlmostEqual(vmax, .4*rate, places=7)

    def test_envelope_matches_bruteforce_two_cones(self):
        for left,right,dt,v in [(2.15,2.15,.0025,243),(3,4,.01,243),(4,3,.01,243),(2.15,2.15,.005,243)]:
            lower = envelope_lower(left,right,dt,v)
            grid = [max(left-v*t, right-v*(dt-t),0) for t in [dt*i/200000 for i in range(200001)]]
            self.assertAlmostEqual(lower, min(grid), delta=1e-4)

    def test_error_and_clock_uncertainty_never_increase_certificate(self):
        x = envelope_lower(2.15,2.15,1/600,243)
        self.assertLessEqual(envelope_lower(2.15,2.15,1/600,243,.05,.0001), x)
        self.assertLess(x, THRESHOLD_MM)
        self.assertAlmostEqual(x, 2.15-243/1200)

    def test_strict_threshold_and_robust_positive_control(self):
        self.assertEqual(envelope_lower(2.15,2.15,.0025,120),2.0)
        self.assertGreater(envelope_lower(3.0,3.0,.0025,120),THRESHOLD_MM)

    def test_invalid_inputs_and_no_physical_unlock(self):
        for bad in [0,-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError): synthetic_alias(bad)
        for kwargs in [dict(aperture_error_mm=-1),dict(clock_jitter_s=-1),dict(speed_cap_mm_s=float('nan'))]:
            args = dict(left_mm=2.15,right_mm=2.15,interval_s=.0025,speed_cap_mm_s=243)
            args.update(kwargs)
            with self.assertRaises(ValueError): envelope_lower(**args)
        self.assertFalse(experiment()['physical_certificate_authorized'])

if __name__ == '__main__': unittest.main()
