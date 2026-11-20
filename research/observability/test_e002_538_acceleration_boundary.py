#!/usr/bin/env python3
"""Adversarial, non-physiology tests for E002-538."""
import math
import unittest
from fractions import Fraction as Q
from e002_538_acceleration_boundary import (
    ATTESTATIONS, evaluate, exact_minimum, frozen_case, lower, run_frozen
)

class AccelerationBoundaryTests(unittest.TestCase):
    def test_exact_frozen_predictions(self):
        r=run_frozen()
        self.assertEqual([r[k]['equal_endpoint_dimensionless_Q'] for k in
                         ('30fps_A3000','30fps_A5040','30fps_A6000','240fps_A6000')],
                         ['25/42','1','25/21','25/1344'])

    def test_strict_touch_is_not_excluded(self):
        r=evaluate(frozen_case(5040,30))
        self.assertEqual(r['minimum_lower_envelope'],'1/5')
        self.assertEqual(r['conditional_geometry'],'HIDDEN_CROSSING_FEASIBLE')
        self.assertFalse(r['threshold_touch_is_excluded'])

    def test_asymmetric_minimizer(self):
        r=evaluate(frozen_case(6000,30,'4/5','9/10'))
        self.assertEqual(r['minimizer_time_s'],'97/6000')
        self.assertEqual(r['minimum_lower_envelope'],'191/12000')
        self.assertEqual(r['conditional_geometry'],'HIDDEN_CROSSING_FEASIBLE')

    def test_sharp_witness_in_physical_range(self):
        for b0,b1 in ((Q(9,10),Q(9,10)),(Q(4,5),Q(9,10))):
            d=Q(1,30); a=Q(6000)
            t,m=exact_minimum(b0,b1,d,a)
            self.assertEqual(lower(t,b0,b1,d,a),m)
            self.assertTrue(0<m<Q(1,5))
            vals=[lower(d*i/200,b0,b1,d,a) for i in range(201)]
            self.assertTrue(all(Q(0)<=v<=Q(1) for v in vals))
            h=d/100
            self.assertEqual((lower(t+h,b0,b1,d,a)-2*lower(t,b0,b1,d,a)
                              +lower(t-h,b0,b1,d,a))/(h*h),a)

    def test_safe_bound_all_times(self):
        b=Q(9,10);d=Q(1,30);a=Q(3000);c=Q(1,5)
        self.assertTrue(all(lower(d*i/1000,b,b,d,a)>c for i in range(1001)))

    def test_clock_gap_nuisance_can_reverse_decision(self):
        base=frozen_case(3000,30)
        self.assertEqual(evaluate(base)['conditional_geometry'],'NO_HIDDEN_CROSSING')
        base['max_unobserved_gap_s']='1/20'
        self.assertEqual(evaluate(base)['conditional_geometry'],'HIDDEN_CROSSING_FEASIBLE')

    def test_missing_frame_can_reverse_decision(self):
        base=frozen_case(3000,30)
        base['max_unobserved_gap_s']='1/15'
        self.assertEqual(evaluate(base)['conditional_geometry'],'HIDDEN_CROSSING_FEASIBLE')

    def test_sampled_velocity_alias(self):
        b=.9;c=.2;d=1/30
        def a(t): return b-(b-c)*math.sin(math.pi*t/d)**2
        def v(t): return -(b-c)*math.pi/d*math.sin(2*math.pi*t/d)
        self.assertAlmostEqual(a(0),b)
        self.assertAlmostEqual(a(d),b)
        self.assertAlmostEqual(v(0),0)
        self.assertAlmostEqual(v(d),0,places=12)
        self.assertAlmostEqual(a(d/2),c)
        peak_a=2*(b-c)*(math.pi/d)**2
        self.assertGreater(peak_a,5040)

    def test_raw_pixel_or_exposure_average_abstains(self):
        for obs in ('raw_pixel_brightness','exposure_average'):
            case=frozen_case(3000,30)
            case['endpoint_observable']=obs
            case['attestations']={k:True for k in ATTESTATIONS}
            case['acceleration_source']='independent_continuous_envelope'
            r=evaluate(case)
            self.assertEqual(r['evidence_decision'],'ILLUSTRATIVE_NOT_CERTIFIED')
            self.assertIn('EXPOSURE_AVERAGE_NOT_POINTWISE_ANATOMY',r['blockers'])

    def test_sampled_acceleration_not_hard(self):
        case=frozen_case(3000,30)
        case['attestations']={k:True for k in ATTESTATIONS}
        self.assertEqual(evaluate(case)['evidence_decision'],'ILLUSTRATIVE_NOT_CERTIFIED')

    def test_even_all_attested_stays_conditional(self):
        case=frozen_case(3000,30)
        case['attestations']={k:True for k in ATTESTATIONS}
        case['acceleration_source']='independent_continuous_envelope'
        r=evaluate(case)
        self.assertEqual(r['evidence_decision'],'CONDITIONAL_BOUND_ONLY')
        self.assertEqual(r['product'],'ABSTAIN_UNCALIBRATED')
        self.assertFalse(r['physical_validated'])
        self.assertEqual(r['release'],'BLOCKED')

    def test_attestations_are_strict_boolean(self):
        for x in (None,1,'true'):
            case=frozen_case(3000,30)
            case['attestations']['authenticated_clock_and_gap']=x
            with self.assertRaises(ValueError): evaluate(case)

    def test_invalid_physical_geometry(self):
        for field,value in [('b0','1/10'),('b1','2'),('threshold','-1/10'),
                            ('max_unobserved_gap_s','0'),('max_abs_aperture_accel_s2','-1')]:
            case=frozen_case(3000,30);case[field]=value
            with self.assertRaises(ValueError): evaluate(case)

    def test_invalid_observable_or_source(self):
        for field,value in [('endpoint_observable','segmentation_confidence'),
                            ('acceleration_source','group_average')]:
            case=frozen_case(3000,30);case[field]=value
            with self.assertRaises(ValueError): evaluate(case)

    def test_zero_acceleration_reduces_to_linear(self):
        case=frozen_case(0,30,'4/5','9/10')
        r=evaluate(case)
        self.assertEqual(r['minimum_lower_envelope'],'4/5')
        self.assertEqual(r['minimizer_time_s'],'0')

    def test_strictly_out_of_bounds_inputs(self):
        for value in (True,False,None,'nan','inf','1/0'):
            case=frozen_case(3000,30);case['max_abs_aperture_accel_s2']=value
            with self.assertRaises((ValueError,OverflowError)): evaluate(case)

    def test_monotonic_acceleration_risk(self):
        minima=[Q(evaluate(frozen_case(a,30))['minimum_lower_envelope'])
                for a in (0,1000,3000,5040,6000,10000)]
        self.assertEqual(minima,sorted(minima,reverse=True))

if __name__=='__main__':
    unittest.main()
