#!/usr/bin/env python3
"""E002-624: exact sampling-design feasibility law. No physiological calibration implied."""
from fractions import Fraction as F
from math import isqrt

def penalty(h, eps, accel):
    """Velocity uncertainty from endpoint errors and bounded acceleration."""
    h, eps, accel = F(h), F(eps), F(accel)
    if h <= 0 or eps < 0 or accel < 0:
        raise ValueError("h>0, eps>=0, accel>=0 required")
    return 2*eps/h + accel*h/2

def feasible(h, eps, accel, budget):
    """Strict budget; equality is not a valid no-hidden-closure certificate."""
    return penalty(h,eps,accel) < F(budget)

def optimal_interval(eps, accel):
    """Exact squared optimum h^2 = 4 eps/A; avoid floating certification."""
    eps, accel = F(eps), F(accel)
    if eps <= 0 or accel <= 0:
        raise ValueError("Interior optimum requires eps>0 and A>0")
    return 4*eps/accel

def impossible_at_any_rate(eps, accel, budget):
    """True if minimum penalty >= budget, by AM-GM; exact comparison."""
    eps, accel, budget = F(eps), F(accel), F(budget)
    if min(eps,accel,budget) < 0: raise ValueError("nonnegative inputs")
    return budget*budget <= 4*eps*accel

def test():
    assert penalty(F(1,200),F(1,20),10000)==F(45,1)
    assert optimal_interval(F(1,20),10000)==F(1,50000)
    assert impossible_at_any_rate(F(1,20),10000,40)
    assert not impossible_at_any_rate(F(1,20),10000,45)
    assert feasible(F(1,200),F(1,20),10000,46)
    assert not feasible(F(1,200),F(1,20),10000,45)
    assert penalty(F(1,100),F(1,20),10000)>penalty(F(1,200),F(1,20),10000)
    for h in [F(1,1000),F(1,500),F(1,240),F(1,200),F(1,120),F(1,60)]:
        assert penalty(h,F(1,20),10000)**2 >= 4*F(1,20)*10000
    try: penalty(0,0,1)
    except ValueError: pass
    else: raise AssertionError("zero interval accepted")
    print("E002-624: 9 exact-rational assertions passed; synthetic design only")

if __name__=="__main__": test()
