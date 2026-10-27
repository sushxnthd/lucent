#!/usr/bin/env python3
"""E002-484 independent rational replay; stdlib only. Synthetic evidence."""
from fractions import Fraction as F
from math import pi, cos, isclose

def limits(mean, delta, q):
    return ((1-delta)*mean-q, (1+delta)*mean+q)

def overlap(a, b):
    return max(a[0],b[0]) <= min(a[1],b[1])

def run():
    delta, q, eps = F(1,10), F(3,100), F(7,20)
    closure = (F(3,2),F(1,2))
    nonclosure = (closure[0]-eps/2,closure[1]+eps/2)
    assert closure == (F(3,2),F(1,2))
    assert nonclosure == (F(53,40),F(27,40))
    ranges = [(limits(a,delta,q),limits(b,delta,q)) for a,b in zip(closure,nonclosure)]
    assert all(overlap(a,b) for a,b in ranges)
    witness = (F(7,5),F(289,500))
    assert all(all(lo<=v<=hi for lo,hi in pair) for v,pair in zip(witness,ranges))
    t1=(6*delta+4*q)/(1+delta)
    t2=(2*delta+4*q)/(1-delta)
    assert t1==F(36,55) and t2==F(16,45)
    assert eps < min(t1,t2) < F(9,25)
    # Independently falsify a stronger claim: with no endpoint measurements,
    # a smooth nonclosing cosine gives the same exact two gate integrals.
    assert 1-pi/4>0 and pi*pi/80 < F(1,5)
    n=200000
    for a,target in [(0,1.5),(10,.5)]:
        h=10/n
        avg=sum(1+pi/4*cos(pi*(a+(i+.5)*h)/20) for i in range(n))/n
        assert isclose(avg,target,abs_tol=1e-10)
    assert not all(overlap(limits(a,F(0),F(0)),limits(b,F(0),F(0))) for a,b in zip(closure,nonclosure))
    assert all(overlap(limits(a,F(0),q),limits(b,F(0),q)) for a,b in zip(closure,(F(29,20),F(11,20))))
    assert not all(overlap(limits(a,F(0),q),limits(b,F(0),q)) for a,b in zip(closure,(F(287,200),F(113,200))))
    print('PASS independent rational replay: 0.35 mm nonclosure common observation; threshold 16/45 mm; cosine control')

if __name__=='__main__': run()
