#!/usr/bin/env python3
"""E002-667: phase-grid coverage, exact rational and exhaustive adversarial checks."""
from fractions import Fraction as F

def guaranteed_grid(n, closed_width, timing_error):
    """Sufficient universal phase-offset hit for arbitrary per-probe bounded timing error."""
    robust_width=max(F(0), closed_width-2*timing_error)
    return robust_width>F(1,n)

def independent_random_lower(n, closed_width, timing_error):
    q=max(F(0),closed_width-2*timing_error)
    return 1-(1-q)**n

def grid_hits_for_offset(n, q, offset):
    # Robust core is [offset,offset+q] modulo 1; strict interior.
    return any(F(0)<((F(k,n)-offset)%1)<q for k in range(n))

def test():
    c=F(3,10); e=F(1,20); q=c-2*e
    assert q==F(1,5)
    assert not guaranteed_grid(5,c,e)  # equality does not ensure strict hit
    assert guaranteed_grid(6,c,e)
    assert independent_random_lower(6,c,e)==1-F(4,5)**6
    # Exhaustive rational offset grid, including alignment with sample points.
    for offset_index in range(600):
        assert grid_hits_for_offset(6,q,F(offset_index,600))
    # At q<1/n an adversary can place the core between samples.
    assert not grid_hits_for_offset(6,F(1,10),F(1,120))
    # A shared unknown phase offset is allowed: coverage is deterministic,
    # unlike n perfectly correlated random draws.
    assert not guaranteed_grid(6,c,F(1,10))
    print("PASS: 600 offsets; 6-grid robust, 5-grid not certified; adversarial narrow core")

if __name__=="__main__":
    test()
