#!/usr/bin/env python3
"""E002-755: exact finite-phase coverage certificate for short closure injections.

T1 synthetic. No detector/human measurements. Run: python3 research/observability/e002_755_phase_coverage.py
"""
from fractions import Fraction
from math import gcd

PERIOD = 100
WIDTH = 25

def phases(start, step, trials):
    return [(start + step * k) % PERIOD for k in range(trials)]

def detects(phase, width=WIDTH):
    return phase < width

def coverage(step, trials=10000):
    outcomes = []
    for start in range(PERIOD):
        seq = phases(start, step, trials)
        outcomes.append((start, sum(map(detects, seq)), len(set(seq))))
    return outcomes

def worst_case_missed_width(observed_phases):
    """Longest cyclic run of phases not sampled, in integer ticks."""
    occupied = set(observed_phases)
    if not occupied:
        return PERIOD
    return max(((b-a-1) % PERIOD) for a,b in zip(sorted(occupied), sorted(occupied)[1:] + [min(occupied)+PERIOD]))

def run():
    # A long experiment does not imply broad phase coverage.
    for step, orbit in [(100,1),(50,2),(25,4),(20,5),(37,100)]:
        results = coverage(step)
        assert all(n == orbit for _,_,n in results)
        print("step",step,"orbit",orbit,"minimum_detected",min(x[1] for x in results),
              "maximum_detected",max(x[1] for x in results))
    assert min(x[1] for x in coverage(100)) == 0
    assert min(x[1] for x in coverage(37)) == 2500
    # Phase uncertainty must be included in any guaranteed phase-coverage claim.
    # A closure can be positioned in an untested interval; count alone is insufficient.
    for step in (100,50,25,20,37):
        seq = phases(0,step,10000)
        gap = worst_case_missed_width(seq)
        print("step",step,"maximum_unsampled_phase_run",gap)
    assert worst_case_missed_width(phases(0,37,10000)) == 0
    assert worst_case_missed_width(phases(0,100,10000)) == 99
    print("PASS: all exact phase-coverage assertions")
if __name__ == "__main__":
    run()
