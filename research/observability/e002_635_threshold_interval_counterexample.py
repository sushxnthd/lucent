#!/usr/bin/env python3
"""E002-635: exact-rational counterexample to point-valued closure thresholds.
Synthetic only. Run: python e002_635_threshold_interval_counterexample.py
"""
from fractions import Fraction as Q

def excluded(gap_hi, aperture0_lo, aperture1_lo, closure_hi, vc_hi, vo_hi):
    """Sound scalar exclusion only when all interval inputs are independently bounded."""
    a = aperture0_lo - closure_hi
    b = aperture1_lo - closure_hi
    if min(gap_hi, a, b, vc_hi, vo_hi) <= 0:
        return None  # abstain; includes endpoint at/below closure
    return a / vc_hi + b / vo_hi > gap_hi

def run():
    gap, x0, x1, vc, vo = Q(1,50), Q(2), Q(2), Q(100), Q(100)
    # Legacy point threshold zero gives 40ms minimum, hence EXCLUDE.
    legacy = excluded(gap,x0,x1,Q(0),vc,vo)
    # Actual closure definition could be 1.5mm: only 10ms travel needed.
    robust = excluded(gap,x0,x1,Q(3,2),vc,vo)
    assert legacy is True and robust is False
    # Construct a 20ms V-Lipschitz closure and reopening:
    # x(0)=2, x(5ms)=1.5, x(10ms)=1, x(15ms)=1.5, x(20ms)=2.
    points=[(Q(0),Q(2)),(Q(1,200),Q(3,2)),
            (Q(1,100),Q(1)),(Q(3,200),Q(3,2)),(Q(1,50),Q(2))]
    for (t,a),(u,b) in zip(points,points[1:]):
        assert abs((b-a)/(u-t)) <= vc
    assert min(a for _,a in points) <= Q(3,2)
    assert excluded(gap,x0,x1,Q(2),vc,vo) is None
    assert excluded(gap,x0,x1,Q(0),vc,vo) is True
    print("PASS: legacy false-exclusion witness; interval-threshold guard abstains")
if __name__=="__main__": run()
