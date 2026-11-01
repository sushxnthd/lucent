#!/usr/bin/env python3
"""E002-594 exact synthetic reference-frame velocity gate. No human evidence."""
from fractions import Fraction as F
import json
import unittest

REQUIRED=('anatomy','geometry','clock','error','acceleration','coverage')

def velocity_bound(samples,h,epsilon,acceleration,provenance):
    """Conditional |a'| upper envelope under independently HARD |a''|<=A."""
    if not isinstance(provenance,dict) or any(provenance.get(k) is not True for k in REQUIRED):
        return {'decision':'ABSTAIN_UNCALIBRATED','reason':'MISSING_INDEPENDENT_PREMISE'}
    if len(samples)<2 or h<=0 or epsilon<0 or acceleration<0:
        return {'decision':'ABSTAIN_UNCALIBRATED','reason':'INVALID_INPUT'}
    if any(not 0<=v<=1 for v in samples):
        return {'decision':'ABSTAIN_UNCALIBRATED','reason':'INVALID_APERTURE'}
    upper=max((abs(y-x)+2*epsilon)/h+acceleration*h/2 for x,y in zip(samples,samples[1:]))
    return {'decision':'MODEL_CONDITIONAL_VELOCITY_BOUND','bound':upper}

def synthetic_report():
    h=F(1,100); c=F(1,2); A=F(200); eps=F(1,500)
    valid={k:True for k in REQUIRED}
    flat=velocity_bound([c,c],h,F(0),A,valid)
    noisy=velocity_bound([c,c],h,eps,A,valid)
    slope=2*eps/h+A*h/2
    a0=c-eps
    ah=a0+slope*h-A*h*h/2
    return {
      'sample_step_ms':'10',
      'acceleration_ceiling_per_s2':str(A),
      'endpoint_error':str(eps),
      'flat_exact_bound_per_s':str(flat['bound']),
      'noisy_bound_per_s':str(noisy['bound']),
      'quadratic_start_aperture':str(a0),
      'quadratic_end_aperture':str(ah),
      'quadratic_initial_speed_per_s':str(slope),
      'quadratic_attains_noisy_bound':slope==noisy['bound'] and ah==c+eps,
      'uncalibrated_decision':velocity_bound([c,c],h,eps,A,{})['decision'],
      'zero_acceleration_exact_bound_per_s':str(velocity_bound([c,c],h,F(0),F(0),valid)['bound']),
      'finite_difference_only_not_a_hard_speed_ceiling':True
    }

class Tests(unittest.TestCase):
    def setUp(self): self.p={k:True for k in REQUIRED}
    def test_flat(self):
        self.assertEqual(velocity_bound([F(1,2),F(1,2)],F(1,100),F(0),F(200),self.p)['bound'],F(1))
    def test_noisy(self):
        self.assertEqual(velocity_bound([F(1,2),F(1,2)],F(1,100),F(1,500),F(200),self.p)['bound'],F(7,5))
    def test_sharp_quadratic(self):
        self.assertTrue(synthetic_report()['quadratic_attains_noisy_bound'])
    def test_missing_premises(self):
        for k in self.p:
            q=self.p.copy();q[k]=False
            self.assertEqual(velocity_bound([F(1,2),F(1,2)],F(1,100),F(0),F(200),q)['decision'],'ABSTAIN_UNCALIBRATED')
    def test_invalid_inputs(self):
        for args in [
          ([F(1,2)],F(1,100),F(0),F(1)),
          ([F(1,2),F(1,2)],F(0),F(0),F(1)),
          ([F(1,2),F(1,2)],F(1,100),F(-1),F(1)),
          ([F(1,2),F(3,2)],F(1,100),F(0),F(1))
        ]:
            self.assertEqual(velocity_bound(*args,self.p)['decision'],'ABSTAIN_UNCALIBRATED')
    def test_nonflat(self):
        self.assertEqual(velocity_bound([F(2,5),F(1,2)],F(1,100),F(0),F(200),self.p)['bound'],F(11))
    def test_tightness_for_zero_A(self):
        self.assertEqual(velocity_bound([F(2,5),F(1,2)],F(1,100),F(0),F(0),self.p)['bound'],F(10))

if __name__=='__main__':
    unittest.main(exit=False,verbosity=2)
    print('E002594_AGGREGATE='+json.dumps(synthetic_report(),sort_keys=True))
