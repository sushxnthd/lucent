#!/usr/bin/env python3
"""E002-738: exact shutter-gap high-rate reference censoring test.

No human data are included. A 200-Hz reference is NOT continuous ground truth.
Run: python research/e002_738_reference_censoring.py
"""
from fractions import Fraction as F

def min_possible_aperture(a, b, dt, L):
    """Sharp minimum reachable between two instantaneous samples, Lipschitz L."""
    assert 0 <= a <= 1 and 0 <= b <= 1 and dt > 0 and L > 0
    assert abs(a-b) <= L*dt, "physically inconsistent endpoints"
    return max(F(0), (a+b-L*dt)/2)

def v_path(a, b, dt, L):
    """Piecewise linear trajectory attaining the sharp minimum."""
    m = min_possible_aperture(a,b,dt,L)
    t = (a-m)/L
    assert t <= dt and (b-m) <= L*(dt-t)
    return [(F(0),a),(t,m),(dt,b)]

def aperture_at(path,t):
    for (t0,a),(t1,b) in zip(path,path[1:]):
        if t0 <= t <= t1:
            return a if t0==t1 else a+(b-a)*(t-t0)/(t1-t0)
    raise ValueError("time outside path")

def test():
    # Reference at 200 Hz: an entire closure can be invisible at both frames.
    dt=F(1,200); a=b=F(1,5); L=F(100) # normalized aperture/s; synthetic only
    p=v_path(a,b,dt,L)
    assert aperture_at(p,F(0))==a and aperture_at(p,dt)==b
    assert aperture_at(p,a/L)==0
    # A second trajectory with identical observations never closes.
    flat=[(F(0),a),(dt,a)]
    assert all(aperture_at(flat,t)==aperture_at(p,t) for t in (F(0),dt))
    # Boundary and nuisance-free exact enumeration: sharp min is attained.
    n=0
    for fps in (120,200,240,1000):
        dt=F(1,fps)
        for L in (F(10),F(50),F(100),F(200)):
            for ai in range(11):
                for bi in range(11):
                    a,b=F(ai,10),F(bi,10)
                    if abs(a-b)>L*dt: continue
                    p=v_path(a,b,dt,L)
                    m=min_possible_aperture(a,b,dt,L)
                    assert min(v for _,v in p)==m
                    assert aperture_at(p,F(0))==a
                    assert aperture_at(p,dt)==b
                    assert all(abs(y-x)<=L*(v-u) for (u,x),(v,y) in zip(p,p[1:]))
                    n+=1
    print("PASS exact reference-censoring cases:",n)
    print("Interpretation: reference labels require interval uncertainty, not binary ground truth.")
if __name__=="__main__": test()
