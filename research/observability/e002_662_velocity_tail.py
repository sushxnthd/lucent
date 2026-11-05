#!/usr/bin/env python3
"""E002-662: distribution-free velocity-tail audit; synthetic only, stdlib."""
from fractions import Fraction
from math import comb

def miss_probability(n, tail_fraction):
    """P(no tail event in n iid calibration transitions)."""
    return (1-tail_fraction)**n

def binomial_tail(n, k, p):
    """P(X <= k), X~Binomial(n,p); exact rational arithmetic."""
    return sum(Fraction(comb(n,j))*p**j*(1-p)**(n-j) for j in range(k+1))

def required_n(p, alpha):
    n=1
    while miss_probability(n,p)>alpha:
        n+=1
    return n

def triangle(t, midpoint, floor, speed):
    return min(Fraction(1), floor+speed*abs(t-midpoint))

def test():
    p=Fraction(1,100)
    assert required_n(p,Fraction(5,100))==299
    assert miss_probability(100,p)>Fraction(1,3)
    assert miss_probability(299,p)<=Fraction(5,100)
    # A held-out faster eyelid closure can defeat a velocity ceiling inferred
    # solely from calibration maxima. No deterministic bound follows.
    left=right=Fraction(1)
    dt=Fraction(1,30)
    midpoint=dt/2
    true_speed=Fraction(60)
    floor=Fraction(0)
    assert triangle(Fraction(0),midpoint,floor,true_speed)==left
    assert triangle(dt,midpoint,floor,true_speed)==right
    assert triangle(midpoint,midpoint,floor,true_speed)==floor
    assumed_speed=Fraction(12)
    naive_lower=min(left,right)-assumed_speed*dt/2
    assert naive_lower>Fraction(3,10) and floor<Fraction(3,10)
    # Conditional on an externally verified ceiling of 60 aperture/s,
    # the correct bound is nonpositive and abstains.
    robust_lower=min(left,right)-true_speed*dt/2
    assert robust_lower<=Fraction(3,10)
    print("E002-662 PASS: n=299 for 1% iid tail / 95% detection;")
    print("synthetic false-open certificate under unverified velocity ceiling")
if __name__=="__main__":
    test()
