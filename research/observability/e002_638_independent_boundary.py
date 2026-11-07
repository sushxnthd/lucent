#!/usr/bin/env python3
"""E002-638 independent exact-arithmetic cross-check of E002-637 (synthetic).
No physiological velocity certification, human video or physical measurements.
Run: python research/observability/e002_638_independent_boundary.py
"""
from fractions import Fraction as F
from itertools import product

def minimum_time(a,b,h,c,o):
    return (a-h)/c+(b-h)/o

def reach_by_interval(a,b,h,g,c,o):
    # Independently test intersection of reachable aperture intervals at time t.
    # At t, start permits x>=a-c*t; end permits x>=b-o*(g-t).
    # A closure is feasible iff some t in [0,g] has both lower bounds <=h.
    left=(a-h)/c
    right=g-(b-h)/o
    return left<=right

def run():
    n=excluded=reachable=equality=0
    for a,b,h,c,o,g in product(
        map(F,('1','2','3')),map(F,('1','2','3')),
        map(F,('0','1/2','3/2')),map(F,('50','100','200')),
        map(F,('50','100','200')),
        map(F,('1/200','1/100','1/50','1/25','2/25'))):
        if a<=h or b<=h: continue
        n+=1
        possible=reach_by_interval(a,b,h,g,c,o)
        excluded+=(not possible)
        reachable+=possible
        equality+=(minimum_time(a,b,h,c,o)==g)
        assert possible == (minimum_time(a,b,h,c,o)<=g)
        # Raising the uncertain closure threshold cannot turn reachable into excluded.
        h2=(h+min(a,b))/2
        assert not (possible and not reach_by_interval(a,b,h2,g,c,o))
    assert (n,excluded,reachable)==(990,595,395)
    print(f"exact synthetic n={n} excluded={excluded} reachable={reachable} equality={equality}")
    print("No empirical calibration or human closure validation.")
if __name__=="__main__": run()
