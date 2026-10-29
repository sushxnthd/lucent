import unittest
from fractions import Fraction as F
from e002_531_native_missingness import (
    C, HZ, MISSING, dwell_samples, experiment, fill_linear, max_slope,
    observed, reference_decision, sample_25fps, worlds,
)


class NativeMissingness(unittest.TestCase):
    def test_frozen_exact_predictions(self):
        d = experiment()
        self.assertEqual(d['complete_world_b_piecewise_linear_dwell_s'], '1/160')
        self.assertEqual(d['complete_world_b_closed_native_frames'], 3)
        self.assertEqual(d['complete_world_b_max_slope_per_s'], '80')

    def test_identical_observed_two_worlds(self):
        a, b = worlds()
        self.assertNotEqual(a, b)
        self.assertEqual(observed(a), observed(b))

    def test_identical_imputed_two_worlds(self):
        a, b = worlds()
        self.assertEqual(fill_linear(observed(a)), fill_linear(observed(b)))
        self.assertEqual(fill_linear(observed(b)), tuple(a))

    def test_dwell_and_native_witness(self):
        a, b = worlds()
        self.assertEqual(dwell_samples(a), F(0))
        self.assertEqual(dwell_samples(b), F(1, 160))
        self.assertEqual([i for i, x in enumerate(b) if x <= C], [33, 34, 35])

    def test_phase_aliasing(self):
        _, b = worlds()
        self.assertEqual(sum(x <= C for x in sample_25fps(b, 0)), 0)
        self.assertEqual(sum(x <= C for x in sample_25fps(b, 1)), 1)
        self.assertEqual(sum(x <= C for x in sample_25fps(fill_linear(observed(b)), 1)), 0)

    def test_missingness_abstention(self):
        a, b = worlds()
        self.assertEqual(reference_decision(observed(b)), 'UNKNOWN_MISSING_NATIVE')
        self.assertEqual(reference_decision(observed(a)), 'UNKNOWN_MISSING_NATIVE')
        self.assertEqual(reference_decision(b), 'POSITIVE_NATIVE_WITNESS')
        self.assertEqual(reference_decision(a), 'NO_SAMPLED_WITNESS_NOT_CERTIFIED_NEGATIVE')

    def test_80_per_second_is_hypothetical(self):
        _, b = worlds()
        self.assertEqual(max_slope(b), F(80))
        self.assertEqual(HZ, 400)
        self.assertEqual(len(MISSING), 9)

    def test_negative_control_unmasked_center(self):
        a, b = worlds()
        missing = MISSING - {34}
        self.assertNotEqual(observed(a, missing), observed(b, missing))
        self.assertEqual(reference_decision(observed(b, missing)), 'POSITIVE_NATIVE_WITNESS')

    def test_missing_at_boundary_is_not_fillable(self):
        a, _ = worlds()
        with self.assertRaises(ValueError):
            fill_linear(observed(a, {0}))
        with self.assertRaises(ValueError):
            fill_linear(observed(a, {len(a)-1}))

    def test_phase_validation(self):
        a, _ = worlds()
        with self.assertRaises(ValueError):
            sample_25fps(a, 16)
        with self.assertRaises(ValueError):
            sample_25fps(a, -1)

    def test_postprocess_cannot_distinguish(self):
        a, b = worlds()
        x, y = fill_linear(observed(a)), fill_linear(observed(b))
        # Any deterministic downstream transform has identical inputs.
        filt = lambda s: tuple(sum(s[max(0, i-2):i+3], F(0))/len(s[max(0, i-2):i+3]) for i in range(len(s)))
        self.assertEqual(filt(x), filt(y))


if __name__ == '__main__':
    unittest.main()
