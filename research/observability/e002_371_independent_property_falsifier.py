"""Independent exact-rational property test of exposure-aware closure exclusion.

Synthetic only. The oracle uses piecewise-linear trajectories and exact
integrals; it does not call the implementation under test for its prediction.
"""
from fractions import Fraction as F
from random import Random

SEED = 37120261118
N = 10000

def interp(knots, t):
    for (x,a),(y,b) in zip(knots,knots[1:]):
        if x <= t <= y:
            return a+(b-a)*(t-x)/(y-x)
    raise AssertionError('outside trajectory')

def integrate(knots, lo, hi):
    cuts=[lo]+[t for t,_ in knots if lo<t<hi]+[hi]
    return sum((interp(knots,a)+interp(knots,b))*(b-a)/2 for a,b in zip(cuts,cuts[1:]))/(hi-lo)

def oracle(knots, gap_lo, gap_hi, threshold):
    cuts=[gap_lo]+[t for t,_ in knots if gap_lo<t<gap_hi]+[gap_hi]
    return min(interp(knots,t) for t in cuts) <= threshold

def run():
    rng=Random(SEED)
    violations=0; exclusions=0; closures=0
    for i in range(N):
        e0=F(rng.randint(1,20),1000)
        e1=F(rng.randint(1,20),1000)
        g=F(rng.randint(1,60),1000)
        t0=F(0);t1=e0;t2=t1+g;t3=t2+e1
        ts=[t0,t0+e0/2,t1,t1+g/2,t2,t2+e1/2,t3]
        vals=[F(rng.randint(0,40),10) for _ in ts]
        knots=list(zip(ts,vals))
        v=max(abs((b-a)/(y-x)) for (x,a),(y,b) in zip(knots,knots[1:]))
        m0=integrate(knots,t0,t1);m1=integrate(knots,t2,t3)
        threshold=F(rng.randint(0,5),10)
        low0=max(F(0),m0-F(rng.randint(0,2),100))
        low1=max(F(0),m1-F(rng.randint(0,2),100))
        upper_v=v+F(rng.randint(0,10),10)
        upper_e0=e0+F(rng.randint(0,2),1000)
        upper_e1=e1+F(rng.randint(0,2),1000)
        upper_g=g+F(rng.randint(0,2),1000)
        a0=low0-upper_v*upper_e0/2
        a1=low1-upper_v*upper_e1/2
        excluded=(a0>threshold and a1>threshold and a0+a1-2*threshold>upper_v*upper_g)
        hidden=oracle(knots,t1,t2,threshold)
        closures+=hidden
        exclusions+=excluded
        violations+=excluded and hidden
    assert violations==0, f'UNSOUND: {violations} false exclusions'
    print(f'PASS seed={SEED} trajectories={N} closure_feasible={closures} exclusions={exclusions} false_exclusions={violations}')
    print('LIMIT: random synthetic testing is not a proof, human evidence, or a calibration certificate.')

if __name__=='__main__': run()
