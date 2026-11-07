"""E002-552 adversarial tests: conditional boxcar envelope only."""
import unittest
from fractions import Fraction as F
from e002_552_boxcar_curvature import (GATES, exclude, quadratic_mean,
    quadratic_minmax, simulation)

G={k:True for k in GATES}

class BoxcarTests(unittest.TestCase):
    def test_exact_naive_false_exclusion(self):
        m=quadratic_mean(F(1,4),-1,2,F(-1,5),0)
        self.assertEqual(m,F(109,300))
        self.assertEqual(m-F(2,8),F(17,150))
        self.assertGreater(m-F(2,8),F(1,10))
        r=exclude(m,m,1,F(1,5),F(1,5),2,F(1,10),gates=G)
        self.assertEqual((r.minimum,r.argmin),(F(0),F(1,2)))
        self.assertEqual(r.label,'POSSIBLE_CLOSURE_OR_UNRESOLVED')

    def test_equal_boxcar_dimensionless_formula(self):
        d,h,A,m=F(1),F(1,5),F(2),F(109,300)
        correction=A*(d*d/8+d*h/4+h*h/6)
        self.assertEqual(correction,m)
        self.assertEqual(exclude(m,m,d,h,h,A,F(1,10),gates=G).minimum,m-correction)

    def test_constant_positive_control(self):
        r=exclude('0.5','0.5','1','0.2','0.2',0,'0.1',gates=G)
        self.assertEqual(r.label,'CONDITIONAL_INSTRUMENT_EXCLUSION_ONLY')
        self.assertEqual(r.minimum,F(1,2))

    def test_unequal_exposures_quadratic_sharpness(self):
        d,h0,h1=F(1),F(1,10),F(3,10)
        a,b,A=F(1,4),F(-1),F(2)
        m0=quadratic_mean(a,b,A,-h0,0)
        m1=quadratic_mean(a,b,A,d,d+h1)
        r=exclude(m0,m1,d,h0,h1,A,F(1,10),gates=G)
        self.assertEqual(r.minimum,F(0))
        self.assertEqual(r.argmin,F(1,2))

    def test_narrow_exposure_limit(self):
        for den in [10,100,1000,10000]:
            h=F(1,den)
            m=F(1,2)
            r=exclude(m,m,1,h,h,2,F(1,10),gates=G)
            expected=m-2*(F(1,8)+h/4+h*h/6)
            self.assertEqual(r.minimum,expected)
        self.assertEqual(exclude(F(1,2),F(1,2),1,F(1,10000),F(1,10000),2,F(1,10),gates=G).label,'CONDITIONAL_INSTRUMENT_EXCLUSION_ONLY')

    def test_more_acceleration_cannot_improve_lower(self):
        vals=[exclude(F(1,2),F(1,2),1,F(1,5),F(1,5),A,F(1,10),gates=G).minimum for A in (0,1,2,3)]
        self.assertEqual(vals,sorted(vals,reverse=True))

    def test_more_mean_error_cannot_improve_lower(self):
        vals=[exclude(F(1,2),F(1,2),1,F(1,5),F(1,5),1,F(1,10),e0=e,e1=e,gates=G).minimum for e in (F(0),F(1,100),F(1,10))]
        self.assertEqual(vals,sorted(vals,reverse=True))

    def test_clock_uncertainty_forces_abstention(self):
        r=exclude(F(1,2),F(1,2),1,F(1,5),F(1,5),2,F(1,10),clock_error=F(1,10000),gates=G)
        self.assertEqual(r.label,'ABSTAIN_UNCALIBRATED')

    def test_every_nuisance_gate_fails_closed(self):
        for key in GATES:
            g=G.copy();g[key]=False
            self.assertEqual(exclude(F(1,2),F(1,2),1,F(1,5),F(1,5),0,F(1,10),gates=g).label,'ABSTAIN_UNCALIBRATED',key)

    def test_missing_or_forged_certificates(self):
        for g in (None,{}, {'boxcar_aperture_response':True}):
            self.assertEqual(exclude(F(1,2),F(1,2),1,F(1,5),F(1,5),0,F(1,10),gates=g).label,'ABSTAIN_UNCALIBRATED')

    def test_inexact_float_rejected(self):
        self.assertEqual(exclude(.5,.5,1,F(1,5),F(1,5),0,F(1,10),gates=G).label,'ABSTAIN_UNCALIBRATED')

    def test_invalid_range_and_nan(self):
        for kw in [dict(d=0),dict(h0=0),dict(h1=-1),dict(A=-1),dict(theta=2),dict(e0=-1),dict(m0='nan')]:
            args=dict(m0=F(1,2),m1=F(1,2),d=1,h0=F(1,5),h1=F(1,5),A=0,theta=F(1,10),gates=G)
            args.update(kw)
            self.assertEqual(exclude(**args).label,'ABSTAIN_UNCALIBRATED')

    def test_boundary_equality_does_not_exclude(self):
        A=F(2);d=F(1);h=F(1,5);theta=F(1,10)
        m=theta+A*(d*d/8+d*h/4+h*h/6)
        r=exclude(m,m,d,h,h,A,theta,gates=G)
        self.assertEqual(r.minimum,theta)
        self.assertEqual(r.label,'POSSIBLE_CLOSURE_OR_UNRESOLVED')

    def test_quadratic_extrema(self):
        self.assertEqual(quadratic_minmax(F(1,4),-1,2,0,1),(0,F(1,4)))

    def test_seeded_adversarial_simulation(self):
        r=simulation()
        self.assertEqual(r['generated'],10000)
        self.assertGreaterEqual(r['accepted'],5000)
        self.assertEqual(r['false_exclusions'],0)
        self.assertEqual(r['envelope_violations'],0)
        self.assertGreater(r['true_closures'],0)

if __name__=='__main__':
    unittest.main()
