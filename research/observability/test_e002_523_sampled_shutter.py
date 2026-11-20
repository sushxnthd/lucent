"""Adversarial exact tests for E002-523; no real camera data."""
import importlib.util
from pathlib import Path
from fractions import Fraction as F
import unittest

spec = importlib.util.spec_from_file_location('e002_523_sampled_shutter', Path(__file__).with_name('e002_523_sampled_shutter.py'))
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


class SampledShutterFalsification(unittest.TestCase):
    def test_sampled_equality_at_all_11_times(self):
        for w in (F(1, 100), F(1, 10000)):
            self.assertEqual([s.q0(t) for t in s.SAMPLE_TIMES], [s.q1(t, w) for t in s.SAMPLE_TIMES])

    def test_exact_normalization(self):
        self.assertEqual(s.T / s.T + s.ALPHA - s.ALPHA, 1)

    def test_nonnegative_dip(self):
        self.assertGreaterEqual(s.q1(s.B_CENTER, F(1, 100)), 0)
        self.assertEqual(s.q1(s.B_CENTER, F(1, 100)), F(1, 20))

    def test_peak_and_true_cap(self):
        for w in (F(1, 100), F(1, 10000)):
            peak = s.q1(s.A_CENTER, w)
            self.assertEqual(s.T * peak, 1 + 2 * s.ALPHA * s.T / w)

    def test_means_match_and_mean_is_below_threshold(self):
        for w in (F(1, 100), F(1, 10000)):
            mean = s.closure_mean(w)
            self.assertEqual(mean, s.OPEN * (1 - w / s.T - s.ALPHA))
            self.assertLess(mean, s.THETA)

    def test_naive_cap_falsifies_lower_bound(self):
        for w in (F(1, 100), F(1, 10000)):
            mean = s.closure_mean(w)
            self.assertGreater(s.lower_duration(mean, F(1)), w)

    def test_true_cap_restores_soundness(self):
        for w in (F(1, 100), F(1, 10000)):
            mean = s.closure_mean(w)
            true_cap = 1 + 2 * s.ALPHA * s.T / w
            self.assertLessEqual(s.lower_duration(mean, true_cap), w)

    def test_uncalibrated_abstains(self):
        samples = [(t, s.q0(t)) for t in s.SAMPLE_TIMES]
        self.assertIsNone(s.sampled_response_cap(samples))
        self.assertIsNone(s.sampled_response_cap(samples, F(0), F(0), False))
        self.assertIsNone(s.lower_duration(F(19, 100), None))

    def test_independent_lipschitz_cap(self):
        samples = [(t, s.q0(t)) for t in s.SAMPLE_TIMES]
        cap = s.sampled_response_cap(samples, F(1, 200), F(1, 50), True)
        self.assertEqual(cap, F(23, 20))

    def test_true_lipschitz_envelope_is_conservative(self):
        w = F(1, 100)
        samples = [(t, s.q1(t, w)) for t in s.SAMPLE_TIMES]
        L = max(4 * s.ALPHA / (w*w), 4 * s.ALPHA / (s.DIP_WIDTH*s.DIP_WIDTH))
        cap = s.sampled_response_cap(samples, F(0), L, True)
        self.assertGreaterEqual(cap, 1 + 2*s.ALPHA*s.T/w)

    def test_reject_unordered_samples(self):
        with self.assertRaises(ValueError):
            s.sampled_response_cap([(F(1), F(1, 10)), (F(1), F(1, 10))], F(0), F(0), True)

    def test_reject_inconsistent_normalization(self):
        with self.assertRaises(ValueError):
            s.sampled_response_cap([(F(0), F(0)), (s.T, F(0))], F(0), F(0), True)

    def test_reject_invalid_width(self):
        for w in (F(0), F(1), F(-1)):
            with self.assertRaises(ValueError):
                s.closure_mean(w)

    def test_reject_invalid_cap(self):
        for cap in (F(0), F(1, 2)):
            with self.assertRaises(ValueError):
                s.lower_duration(F(19, 100), cap)

    def test_frozen_results_are_deterministic(self):
        self.assertEqual(s.evaluate(F(1, 100)), s.evaluate(F(1, 100)))
        self.assertEqual(s.evaluate(F(1, 10000))['sampled_peak_R_hat']['fraction'], '1')


if __name__ == '__main__':
    unittest.main()
