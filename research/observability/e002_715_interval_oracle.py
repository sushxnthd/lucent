"""E002-715: interval-robust closure exclusion, synthetic instrument oracle.
Run: python research/observability/e002_715_interval_oracle.py. Not human or physical validation.
"""
from itertools import product
from math import isfinite

def decision(a0_interval, a1_interval, dt_interval, v_interval):
    """Certificate only if every admissible parameter combination excludes closure."""
    a0l,a0u=a0_interval; a1l,a1u=a1_interval
    dtl,dtu=dt_interval; vl,vu=v_interval
    if not all(isfinite(x) for x in [a0l,a0u,a1l,a1u,dtl,dtu,vl,vu]):
        return 'ABSTAIN_INVALID_BOUNDS'
    if not (0 <= a0l <= a0u and 0 <= a1l <= a1u and 0 <= dtl <= dtu and 0 <= vl <= vu):
        return 'ABSTAIN_INVALID_BOUNDS'
    return 'EXCLUDE_HIDDEN_CLOSURE' if vu*dtu < a0l+a1l else 'POSSIBLE_HIDDEN_CLOSURE'

def triangular_witness(a0,a1,dt,v):
    """Construct continuous piecewise-linear closure trajectory if feasible."""
    if v == 0 and a0 == a1 == 0 and dt >= 0:
        return ((0.,0.),(dt,0.))
    if v <= 0 or dt < 0 or a0 < 0 or a1 < 0 or v*dt < a0+a1:
        return None
    tclose=a0/v
    topen=dt-a1/v
    return ((0.,a0),(tclose,0.),(topen,0.),(dt,a1))

def check():
    from fractions import Fraction as F
    vals=[F(0),F(1,4),F(1,2),F(1),F(2)]
    intervals=[(a,b) for a in vals for b in vals if a<=b]
    n=0; certificates=0; possible=0
    for a0,a1,dt,v in product(intervals,repeat=4):
        result=decision(a0,a1,dt,v)
        feasible=any(triangular_witness(x,y,t,s) is not None for x,y,t,s in product(a0,a1,dt,v))
        assert (result=='EXCLUDE_HIDDEN_CLOSURE') == (not feasible), (a0,a1,dt,v,result,feasible)
        n+=1; certificates+=result=='EXCLUDE_HIDDEN_CLOSURE'; possible+=feasible
    assert decision((1,1),(1,1),(1,1),(2,2))=='POSSIBLE_HIDDEN_CLOSURE'
    assert decision((1,1),(1,1),(1,1),(F(7,4),F(7,4)))=='EXCLUDE_HIDDEN_CLOSURE'
    assert decision((1,1),(1,1),(1,1),(float('nan'),2))=='ABSTAIN_INVALID_BOUNDS'
    print(f'PASS {n} exhaustive interval cells; {certificates} exclusions; {possible} feasible closure witnesses')

if __name__=='__main__':
    check()
