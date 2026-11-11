#!/usr/bin/env python3
"""E002-754: phase-lock falsifier for reference-detector validation.
Exact integer ticks. No random sampling or empirical data. Python standard library only.
"""
from math import gcd

def hits(period, duration, phase, count, stride):
    assert 0 < duration < period and count > 0
    return sum(((phase + k * stride) % period) < duration for k in range(count))

def phase_coverage(period, duration, count, stride):
    return [hits(period, duration, phase, count, stride) for phase in range(period)]

def main():
    period, duration, count = 100, 25, 10000
    locked = phase_coverage(period, duration, count, 100)
    assert locked.count(0) == 75 and locked.count(count) == 25
    # Coprime phase progression exhausts all discrete phases.
    swept = phase_coverage(period, duration, count, 37)
    assert gcd(period, 37) == 1
    assert set(swept) == {2500}
    # A 2-phase cycle can miss the pulse entirely for some initial phases.
    short = phase_coverage(period, duration, count, 50)
    assert min(short) == 0 and max(short) == 5000
    print("E002-754 exact synthetic point-sampler results")
    print("locked: 75/100 starting phases miss ALL 10000 events; 25/100 detect ALL")
    print("coprime sweep: all 100 starting phases detect exactly 2500/10000")
    print("2-phase sweep: min 0, max 5000 detections across initial phases")
    print("NOTE: not human data; no detector bandwidth/exposure/noise model")

if __name__ == "__main__":
    main()
