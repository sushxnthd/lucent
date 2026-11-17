#!/usr/bin/env python3
"""E002-371 independent discrete reachability adversary; synthetic only.

Tests the exact continuous-time Lipschitz gap condition against a separately
implemented sampled dynamic-programming reachability search. Does not use the
original witness generator. Units: mm, seconds, mm/s. No external dependencies.
"""
from math import ceil
from random import Random

def analytical(left,right,threshold,gap,speed):
    if abs(left-right)>speed*gap: return None
    return left+right-2*threshold <= speed*gap

def grid_reachable(left,right,threshold,gap,speed,steps=80,scale=100):
    # Integer aperture positions; integer edge budget rounded DOWN. This
    # conservative lattice can yield false negatives near the sharp boundary.
    unit=1/scale
    dt=gap/steps
    jump=int(speed*dt*scale+1e-10)
    L=round(left*scale); R=round(right*scale); T=round(threshold*scale)
    if abs(L/scale-left)>1e-9 or abs(R/scale-right)>1e-9: raise ValueError("off grid")
    # Instead of enumerating paths, propagate intervals reachable after a
    # threshold visit; exact for the integer-grid dynamics.
    unvisited={L}; visited=set()
    for _ in range(steps):
        next_u=set(); next_v=set()
        for x in unvisited:
            for y in range(max(T,x-jump),x+jump+1):
                (next_v if y==T else next_u).add(y)
        for x in visited:
            next_v.update(range(max(T,x-jump),x+jump+1))
        unvisited,visited=next_u,next_v
    return R in visited

def run():
    # Exact lattice-compatible trials: each time step has a 1-grid-unit speed
    # budget, so the dynamic program and continuous boundary must agree.
    rng=Random(371)
    n=0
    for _ in range(200):
        steps=40
        left=rng.randrange(1,18)/10
        right=rng.randrange(1,18)/10
        threshold=0.
        gap=steps/100.
        speed=1.0 # per-step max 0.01 mm
        # Most pairs cannot close; deliberately include feasible near threshold
        a=analytical(left,right,threshold,gap,speed)
        b=grid_reachable(left,right,threshold,gap,speed,steps,100)
        assert a==b,(left,right,a,b)
        n+=1
    # Construct a sharp equality case and a one-step-below case.
    assert analytical(.2,.2,0,.4,1) is True
    assert grid_reachable(.2,.2,0,.4,1,40,100) is True
    assert analytical(.2,.2,0,.39,1) is False
    assert grid_reachable(.2,.2,0,.39,1,39,100) is False
    # Uncertainty envelope: if all compatible endpoint and speed values
    # forbid closure, a safe rejection is possible; otherwise abstain.
    def conservative_no_closure(l_lo,r_lo,gap_hi,speed_hi,threshold=0):
        return l_lo+r_lo-2*threshold > speed_hi*gap_hi
    assert conservative_no_closure(2.8,2.8,1/30+.001,100)
    assert not conservative_no_closure(2.8,2.8,1/30+.001,200)
    print("PASS: 200 seeded lattice comparisons, 2 sharp-edge tests, 2 uncertainty abstention tests")
    print("EVIDENCE: discrete synthetic verification only; no human/physical validation")
if __name__=="__main__": run()
