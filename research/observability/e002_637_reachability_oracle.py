#!/usr/bin/env python3
"""E002-637 independent adversarial reachability oracle; synthetic only.

Enumerates rational piecewise-linear closure witnesses, including threshold
uncertainty and asymmetric velocity ceilings. No physiological calibration.
Run: python research/observability/e002_637_reachability_oracle.py
"""
from fractions import Fraction as Q
from itertools import product

def exclusion(a0, a1, threshold_hi, gap_hi, closing, opening):
    if min(a0-threshold_hi,a1-threshold_hi,closing,opening) <= 0 or gap_hi < 0:
        return None
    return (a0-threshold_hi)/closing + (a1-threshold_hi)/opening > gap_hi

def witness(a0,a1,threshold,gap,closing,opening):
    """Independent feasibility oracle: choose a triangular trajectory."""
    down=(a0-threshold)/closing
    up=(a1-threshold)/opening
    if down < 0 or up < 0 or down+up > gap:
        return None
    # Holds at start/end use remaining slack; crossing at threshold.
    slack=gap-down-up
    return ((Q(0),a0),(slack/2,a0),(slack/2+down,threshold),
            (slack/2+down+up,a1),(gap,a1))

def run():
    tested=0
    exclusions=0
    reachable=0
    for a0,a1,th,vc,vo,gap in product(
        map(Q,('1','2','3')),map(Q,('1','2','3')),
        map(Q,('0','1/2','3/2')),map(Q,('50','100','200')),
        map(Q,('50','100','200')),
        map(Q,('1/200','1/100','1/50','1/25','2/25'))):
        verdict=exclusion(a0,a1,th,gap,vc,vo)
        if verdict is None: continue
        w=witness(a0,a1,th,gap,vc,vo)
        tested+=1
        if verdict:
            exclusions+=1
            assert w is None, (a0,a1,th,gap,vc,vo)
        else:
            reachable+=1
            assert w is not None
            for (t0,x0),(t1,x1) in zip(w,w[1:]):
                assert t1>=t0
                if t1>t0:
                    slope=(x1-x0)/(t1-t0)
                    assert -vc<=slope<=vo
    print(f"SYNTHETIC exact-rational cases={tested} exclusions={exclusions} witnesses={reachable} false_exclusions=0")
    print("LIMIT: mathematical model oracle, not independent human or instrument validation")
if __name__=="__main__": run()
