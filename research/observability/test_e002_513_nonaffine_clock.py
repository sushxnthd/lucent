#!/usr/bin/env python3
"""Frozen adversarial tests for E002-513's non-affine two-world witness."""
import unittest
from fractions import Fraction
from decimal import Decimal, localcontext
from e002_513_nonaffine_clock import (N, TARGET, EXPOSURE, SPIKE, PERIOD,
                                      build_world, falsify, maximum_local_period,
                                      risk_at_local_gap)


class NonAffineTests(unittest.TestCase):
    def test_same_perfect_optical_anchors(self):
        a, b = build_world(spike=Fraction(0)), build_world()
        self.assertEqual((a[0], a[-1]), (b[0], b[-1]))
        self.assertEqual((a[0], a[-1]), (Fraction(0), Fraction(10)))

    def test_complete_native_frame_numbering(self):
        for a in (build_world(spike=Fraction(0)), build_world()):
            self.assertEqual(len(a), 301)
            self.assertTrue(all(a[i+1] > a[i] for i in range(300)))
            self.assertTrue(all(a[i+1]-a[i] >= EXPOSURE for i in range(300)))

    def test_frozen_local_gap_spike(self):
        a, b = build_world(spike=Fraction(0)), build_world()
        self.assertEqual(a[TARGET+1]-a[TARGET], PERIOD)
        self.assertEqual(b[TARGET+1]-b[TARGET], PERIOD+SPIKE)

    def test_all_other_intervals_compensate_exactly(self):
        b = build_world()
        self.assertEqual(b[1]-b[0], PERIOD-SPIKE/Fraction(299))
        self.assertEqual(sum((b[i+1]-b[i] for i in range(N)), Fraction(0)), Fraction(10))

    def test_strict_risk_classification_reverses(self):
        x = falsify()
        self.assertEqual(x['world_a']['conditional_scalar_result'], 'CONDITIONAL_EXCLUSION')
        self.assertEqual(x['world_b']['conditional_scalar_result'], 'NOT_EXCLUDED_OR_BOUNDARY')
        self.assertAlmostEqual(float(x['world_a']['risk_upper']), .7489897948556636, places=12)
        self.assertAlmostEqual(float(x['world_b']['risk_upper']), .8089897948556636, places=12)

    def test_exact_optical_target_pulse_disambiguates(self):
        a, b = build_world(spike=Fraction(0)), build_world()
        self.assertNotEqual(a[TARGET+1], b[TARGET+1])
        self.assertGreater(abs(a[TARGET+1]-b[TARGET+1]), Fraction(1, 10000))

    def test_no_clock_calibration_from_long_span(self):
        self.assertFalse(falsify()['long_span_anchors_certify_local_gap'])

    def test_exact_local_period_envelope(self):
        self.assertEqual(maximum_local_period(Fraction(10), 300, Fraction(1,100)), Fraction(701,100))
        self.assertEqual(maximum_local_period(Fraction(10), 300, Fraction(0)), Fraction(10))

    def test_envelope_attainable_with_positive_minimum(self):
        s = Fraction(10); m = Fraction(1,100)
        ints = [m]*299 + [maximum_local_period(s,300,m)]
        self.assertEqual(sum(ints), s)
        self.assertEqual(min(ints), m)

    def test_invalid_envelope(self):
        for args in ((Fraction(10),1,Fraction(0)),(Fraction(10),300,Fraction(-1)),
                     (Fraction(1),300,Fraction(1,100)), (Fraction(0),300,Fraction(0))):
            with self.subTest(args=args), self.assertRaises(ValueError):
                maximum_local_period(*args)

    def test_bad_target_and_spike(self):
        for kw in ({'target':300},{'target':-1},{'n':1},{'spike':Fraction(-1)},
                   {'spike':Fraction(10)}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                build_world(**kw)

    def test_risk_refuses_overlapping_exposure(self):
        with self.assertRaisesRegex(ValueError,'INVALID_LOCAL_GAP'):
            risk_at_local_gap(Fraction(1,1000))

    def test_exact_threshold_is_not_excluded(self):
        with localcontext() as ctx:
            ctx.prec = 70
            risk = Decimal(falsify()['world_a']['risk_upper'])
            threshold = str(Decimal(1)-risk)
        x = risk_at_local_gap(PERIOD, threshold=threshold)
        self.assertEqual(x['conditional_scalar_result'], 'NOT_EXCLUDED_OR_BOUNDARY')

    def test_product_and_physical_flags_blocked(self):
        x = falsify()
        self.assertEqual(x['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertEqual(x['release'], 'BLOCKED')
        for k in ('independent_physical_clock_authenticated','physical_shutter_calibrated',
                  'continuous_time_human_speed_certified','human_anatomical_ratings_obtained',
                  'physical_hidden_closure_certified','affine_model_falsified'):
            self.assertFalse(x[k])


if __name__ == '__main__':
    unittest.main()
