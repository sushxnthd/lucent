#!/usr/bin/env python3
"""E002-665: phase randomization versus phase-locked hidden closures.
Synthetic, exact rational arithmetic; no human validation.
Run: python3 research/observability/e002_665_phase_dither.py
"""
from fractions import Fraction as F
from math import comb

def aperture(phase):
    """Triangular trajectory, period 1, open at phase 0, closed at 1/2."""
    p = phase % 1
    return 1 - 2*p if p <= F(1, 2) else 2*p - 1

def detection_probability(n, width):
    """IID uniform phase samples, closure set measure width."""
    return 1 - (1 - width) ** n

def exact_grid_detection(n, k, threshold):
    """Probability of detection for n IID draws from k equiprobable phases."""
    hits = sum(aperture(F(j,k)) <= threshold for j in range(k))
    return 1 - F(k-hits,k)**n, hits

def run():
    threshold=F(3,10)
    # Aperture <= threshold occupies fraction threshold of each period.
    assert aperture(F(1,2)) == 0
    assert all(aperture(F(0)) == 1 for _ in range(300))
    assert detection_probability(10,threshold) == 1-F(7,10)**10
    assert detection_probability(10,threshold) > F(97,100)
    p,hits=exact_grid_detection(10,20,threshold)
    assert hits == 6 and p == 1-F(7,10)**10
    # Jitter restricted to +/- 1/10 period never reaches the hidden closure.
    assert all(aperture(F(j,100)) > threshold for j in list(range(0,11))+list(range(90,100)))
    # Identical shared phase across 10 observations: detection chance remains 0.3.
    assert F(hits,20) == threshold
    # Worst-case fixed phase sequence can miss regardless of n.
    assert all(aperture(F(0)) > threshold for _ in range(100000))
    # Confidence over 10 IID phase probes is not a deterministic certificate.
    print("E002-665 PASS; 10 independent uniform phases detection=",float(p),
          "; shared-phase detection=",float(threshold),
          "; bounded jitter can remain blind")
if __name__=="__main__": run()
