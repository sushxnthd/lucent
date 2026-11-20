#!/usr/bin/env python3
"""E002-371 independent synthetic shutter-gap witness generator.

This is mathematical/instrument-protocol validation ONLY, not human evidence.
Units: aperture mm, time seconds, speed mm/s. Python standard library.
Run: python3 research/observability/e002_371_gap_witness.py
"""
from dataclasses import dataclass
from math import isfinite
import json

@dataclass(frozen=True)
class Case:
    name: str
    left: float
    right: float
    gap_s: float
    speed_mm_s: float
    closure_mm: float = 0.0

def feasible(c):
    vals = (c.left,c.right,c.gap_s,c.speed_mm_s,c.closure_mm)
    if not all(isfinite(v) for v in vals) or c.gap_s <= 0 or c.speed_mm_s <= 0:
        raise ValueError("nonfinite, nonpositive gap/speed")
    if c.left < c.closure_mm or c.right < c.closure_mm:
        raise ValueError("endpoints already at/below closure threshold")
    if abs(c.left-c.right) > c.speed_mm_s*c.gap_s:
        return None  # endpoints themselves incompatible with assumed bound
    needed = (c.left+c.right-2*c.closure_mm)/c.speed_mm_s
    return c.gap_s >= needed - 1e-12

def witness(c):
    f=feasible(c)
    if not f: return None
    t1=(c.left-c.closure_mm)/c.speed_mm_s
    t2=c.gap_s-(c.right-c.closure_mm)/c.speed_mm_s
    return [(0.,c.left),(t1,c.closure_mm),(t2,c.closure_mm),(c.gap_s,c.right)]

def aperture_at(points,t):
    for (ta,a),(tb,b) in zip(points,points[1:]):
        if ta <= t <= tb:
            return b if tb==ta else a+(b-a)*(t-ta)/(tb-ta)
    raise ValueError("outside gap")

def run():
    cases=[
        Case("30fps_3mm_100mms",3,3,1/30,100),
        Case("30fps_3mm_200mms",3,3,1/30,200),
        Case("60fps_3mm_200mms",3,3,1/60,200),
        Case("30fps_asymmetric_1_3mm_150mms",1,3,1/30,150),
        Case("inconsistent_endpoints",1,4,.01,100),
        Case("threshold_equality",2,2,.04,100),
    ]
    expected=[False,True,False,True,None,True]
    out=[]
    for c,e in zip(cases,expected):
        f=feasible(c)
        assert f is e,(c.name,f,e)
        p=witness(c)
        if p:
            assert p[0][1]==c.left and p[-1][1]==c.right
            assert min(a for _,a in p)<=c.closure_mm
            for (ta,a),(tb,b) in zip(p,p[1:]):
                assert abs(b-a) <= c.speed_mm_s*(tb-ta)+1e-9
            for i in range(101):
                assert aperture_at(p,c.gap_s*i/100)>=c.closure_mm-1e-9
        out.append(dict(case=c.name,feasible=f,required_gap_s=(c.left+c.right-2*c.closure_mm)/c.speed_mm_s, witness=p))
    print(json.dumps({"evidence_tier":"synthetic mathematical witness only","results":out},indent=2))

if __name__=="__main__":
    run()
