import unittest, random
from fractions import Fraction as F
from e002_553_kernel_curvature import *

class KernelTests(unittest.TestCase):
    def setUp(self):
        self.k0=two_pulse("-1/2","0","1/20")
        self.k1=two_pulse("1","3/2","1/20")
        self.f=(F(1),F(-1),F(1,4))
        self.m=self.k0.quadratic_mean(*self.f)
    def test_frozen_means(self): self.assertEqual(self.m,F(46,75))
    def test_frozen_right(self): self.assertEqual(self.k1.quadratic_mean(*self.f),F(46,75))
    def test_frozen_variance(self): self.assertEqual(self.k0.moments()[1],F(61,1200))
    def test_boxcar_variance(self): self.assertEqual(boxcar("-1/2",0).moments()[1],F(1,48))
    def test_correct_min(self): self.assertEqual(minimum_gap(self.k0,self.k1,self.m,self.m,F(2),F(0),F(1)),(F(0),F(1,2)))
    def test_wrong_false_exclusion(self):
        low,_=minimum_gap(boxcar("-1/2",0),boxcar("1","3/2"),self.m,self.m,F(2),F(0),F(1))
        self.assertEqual(low,F(3,100));self.assertGreater(low,F(1,50))
    def test_negative_weights(self):
        with self.assertRaises(ValueError): Pulse(F(0),F(1),F(-1))
    def test_unnormalized(self):
        with self.assertRaises(ValueError): Kernel(F(0),F(1),(Pulse(F(0),F(1),F(1,2)),))
    def test_overlap(self):
        with self.assertRaises(ValueError): Kernel(F(0),F(1),(Pulse(F(0),F(3,4),F(1,2)),Pulse(F(1,2),F(1),F(1,2))))
    def test_outside(self):
        with self.assertRaises(ValueError): Kernel(F(0),F(1),(Pulse(F(-1),F(0),F(1)),))
    def test_float_rejected(self):
        with self.assertRaises(ValueError): Q(0.1)
    def test_gap_rejected(self):
        with self.assertRaises(ValueError): minimum_gap(self.k0,self.k1,self.m,self.m,F(2),F(-1),F(1))
    def test_missing_gate_abstains(self):
        self.assertEqual(adjudicate(self.k0,self.k1,self.m,self.m,F(2),F(0),F(1),F(1,50),{})["decision"],"ABSTAIN_UNCALIBRATED")
    def test_all_gates_only_conditional(self):
        gates={x:True for x in REQUIRED_GATES}
        self.assertEqual(adjudicate(self.k0,self.k1,self.m,self.m,F(2),F(0),F(1),F(1,50),gates)["decision"],"HIDDEN_CLOSURE_NOT_EXCLUDED")
    def test_error_widens_lower(self):
        base,_=minimum_gap(self.k0,self.k1,self.m,self.m,F(2),F(0),F(1))
        err,_=minimum_gap(self.k0,self.k1,self.m,self.m,F(2),F(0),F(1),F(1,10),F(1,10))
        self.assertEqual(err,base-F(1,10))
    def test_quadratic_equality_random(self):
        rng=random.Random(553)
        for _ in range(1000):
            h=F(rng.randint(2,8),10);d=F(rng.randint(10,30),10)
            w=h/F(rng.randint(3,10))
            k0=two_pulse(-h,F(0),w);k1=two_pulse(d,d+h,w)
            a=F(rng.randint(0,10),100);b=F(rng.randint(-10,10),100)
            c=F(rng.randint(20,50),100);A=2*a
            m0=k0.quadratic_mean(a,b,c);m1=k1.quadratic_mean(a,b,c)
            for t in (F(0),d/4,d/2,3*d/4,d):
                self.assertEqual(lower_at(t,k0,k1,m0,m1,A),a*t*t+b*t+c)
    def test_loose_A_is_conservative(self):
        for A in (F(2),F(3),F(10)):
            for t in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
                self.assertLessEqual(lower_at(t,self.k0,self.k1,self.m,self.m,A),(t-F(1,2))**2)
    def test_asymmetric_kernel_and_error(self):
        k0=Kernel(F(-1),F(0),(Pulse(F(-1),F(-3,4),F(3,4)),Pulse(F(-1,4),F(0),F(1,4))))
        k1=boxcar("1","3");a,b,c=F(1,8),F(-1,4),F(1,2)
        m0=k0.quadratic_mean(a,b,c);m1=k1.quadratic_mean(a,b,c)
        for t in (F(0),F(1,2),F(1)):
            self.assertEqual(lower_at(t,k0,k1,m0,m1,F(1,4)),a*t*t+b*t+c)
            self.assertLessEqual(lower_at(t,k0,k1,m0,m1,F(1,4),F(1,100),F(1,50)),a*t*t+b*t+c)

if __name__=="__main__": unittest.main()
