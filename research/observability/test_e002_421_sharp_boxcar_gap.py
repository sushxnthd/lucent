"""Independent LP and quadrature oracle for E002-421."""
import math
import random
import unittest
import numpy as np
from scipy.optimize import linprog
from e002_421_sharp_boxcar_gap import GapCase, evaluate, trajectory, exposure_average, robust_gap_lower


def independent_lp(c):
    m, v, d, e = c.mean, c.velocity_per_s, c.center_separation_s, c.exposure_s
    # Piecewise linear grid contains both exact shutter boundaries and gap midpoint.
    anchors = [-e/2, e/2, d/2, d-e/2, d+e/2]
    nodes = []
    for a, b in zip(anchors[:-1], anchors[1:]):
        if b <= a + 1e-15:
            continue
        nodes.extend(a+(b-a)*i/8 for i in range(8))
    nodes.append(anchors[-1])
    nodes = np.array(nodes)
    n = len(nodes)
    W = np.zeros((2,n))
    for k,(left,right) in enumerate(((-e/2,e/2),(d-e/2,d+e/2))):
        for j in range(n-1):
            if nodes[j] >= left-1e-13 and nodes[j+1] <= right+1e-13:
                h=nodes[j+1]-nodes[j]
                W[k,j]+=h/(2*e)
                W[k,j+1]+=h/(2*e)
    assert np.max(np.abs(W.sum(axis=1)-1)) < 1e-11
    A=np.zeros((2*(n-1),n))
    b=np.zeros(2*(n-1))
    for j in range(n-1):
        A[2*j,j+1]=1
        A[2*j,j]=-1
        A[2*j+1,j+1]=-1
        A[2*j+1,j]=1
        b[2*j:2*j+2]=v*(nodes[j+1]-nodes[j])
    objective=np.zeros(n)
    objective[np.argmin(abs(nodes-d/2))]=1
    res=linprog(objective,A_ub=A,b_ub=b,A_eq=W,b_eq=np.array([m,m]),bounds=(0,1),method='highs',
                options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    assert res.success, res.message
    assert np.max(A@res.x-b) < 1e-7
    assert np.max(abs(W@res.x-m)) < 1e-7
    return float(res.fun), nodes, res.x


def independent_integral(c, world, center, bins=20000):
    m,v,d,e=c.mean,c.velocity_per_s,c.center_separation_s,c.exposure_s
    left=center-e/2
    if world=='open':
        return m
    # Explicit V-valley independent of candidate trajectory implementation.
    return math.fsum(m-v*d/2+v*abs(left+(j+.5)*e/bins-d/2) for j in range(bins))/bins


class TestSharpBoxcarGap(unittest.TestCase):
    def test_frozen_false_safe_ratio(self):
        c=GapCase(.315,.20,60.,1/240,.002)
        r=evaluate(c)
        self.assertAlmostEqual(r['sharp_gap_lower'],.190,delta=1e-12)
        self.assertLess(r['construction_specific_E002_420_ratio'],1)
        self.assertTrue(r['ratio_less_than_one_does_not_certify'])
        self.assertEqual(r['conditional_research_gap_decision'],'AMBIGUOUS')
        for world in ('open','valley'):
            for center in (0.,c.center_separation_s):
                self.assertAlmostEqual(independent_integral(c,world,center),.315,delta=1e-10)
                self.assertAlmostEqual(exposure_average(c,center,world,200),.315,delta=1e-10)
        self.assertAlmostEqual(trajectory(c,c.center_separation_s/2,'valley'),.190,delta=1e-12)
        self.assertFalse(r['product_claim_authorized'])
        self.assertEqual(r['product'],'ABSTAIN_UNCALIBRATED')

    def test_24_independent_linear_programs(self):
        rng=random.Random(4212026)
        ambiguous=certified=0
        for _ in range(24):
            d=rng.uniform(.002,.008)
            v=rng.uniform(12,75)
            e=d*rng.uniform(.12,.7)
            m=rng.uniform(v*d/2+.08,min(.75,1-v*e/2-.02))
            theta=rng.uniform(.03,m-.01)
            c=GapCase(m,theta,v,d,e)
            expected=m-v*d/2
            actual,nodes,x=independent_lp(c)
            self.assertAlmostEqual(actual,expected,delta=1e-7)
            self.assertGreaterEqual(x.min(),-1e-9)
            self.assertLessEqual(x.max(),1+1e-9)
            self.assertAlmostEqual(independent_integral(c,'valley',0,4096),m,delta=1e-10)
            self.assertAlmostEqual(independent_integral(c,'valley',d,4096),m,delta=1e-10)
            decision=evaluate(c)['conditional_research_gap_decision']
            self.assertEqual(decision,'CERTIFY_NO_CROSSING' if expected>theta else 'AMBIGUOUS')
            if decision=='AMBIGUOUS': ambiguous+=1
            else: certified+=1
        self.assertGreater(ambiguous,0)
        self.assertGreater(certified,0)

    def test_adversarial_random_lipschitz_paths(self):
        rng=random.Random(42)
        c=GapCase(.315,.2,60.,1/240,.002)
        # 1000 V-Lipschitz paths sharing exposure means via convex combinations.
        for _ in range(1000):
            lam=rng.random()
            t=rng.uniform(c.exposure_s/2,c.center_separation_s-c.exposure_s/2)
            value=(1-lam)*c.mean+lam*(c.mean-c.velocity_per_s*c.center_separation_s/2+
                                     c.velocity_per_s*abs(t-c.center_separation_s/2))
            self.assertGreaterEqual(value,c.mean-c.velocity_per_s*c.center_separation_s/2-1e-12)

    def test_robust_uncertainty_and_fail_closed(self):
        self.assertAlmostEqual(robust_gap_lower(.315,60,1/240),.190,places=12)
        self.assertLessEqual(robust_gap_lower(.305,65,1/225),.2)
        self.assertGreater(robust_gap_lower(.65,60,1/240),.2)
        for c in (GapCase(.315,.2,60,.002,.003),GapCase(.315,.2,60,.004,0),
                  GapCase(.315,.2,float('nan'),.004,.002),GapCase(.1,.2,60,.004,.002),
                  GapCase(.98,.2,60,.004,.002)):
            with self.assertRaises(ValueError): evaluate(c)
        for args in ((float('nan'),60,.01),(.3,-1,.01),(.3,60,-1)):
            with self.assertRaises(ValueError): robust_gap_lower(*args)


if __name__=='__main__':
    unittest.main()
