"""E002-742: deterministic held-out shutter timing and velocity stress test.
Synthetic point-aperture trajectories only; no human inference.
"""
import random

def run(seed=742, n=10000):
    rng=random.Random(seed)
    out={'n':n,'hidden':0,'naive_false_exclusions':0,'robust_false_exclusions':0,'robust_exclusions':0,'robust_abstentions':0}
    for _ in range(n):
        gap=rng.uniform(.010,.050)
        a=rng.uniform(.2,1.)
        speed=rng.uniform(12.,55.)
        # Symmetric V-shaped aperture path, sampled at its endpoints.
        # A full closure exists if the unconstrained midpoint reaches zero.
        hidden=a-speed*gap/2 <= 0
        out['hidden']+=hidden
        nominal=max(0.,gap-rng.uniform(0.,.008))
        naive=(2*a>25*nominal)
        # Synthetic certified bound: speed <=55; gap <=nominal+8 ms.
        robust=(2*a>55*(nominal+.008))
        out['naive_false_exclusions']+=bool(naive and hidden)
        out['robust_false_exclusions']+=bool(robust and hidden)
        out['robust_exclusions']+=bool(robust)
        out['robust_abstentions']+=not robust
    assert out['robust_false_exclusions']==0, out
    assert out['robust_exclusions']+out['robust_abstentions']==n
    return out

if __name__=='__main__':
    for seed in (742,743,744): print(seed,run(seed))
