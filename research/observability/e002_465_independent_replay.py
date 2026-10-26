#!/usr/bin/env python3
"""Independent exact-rational E002-465 replay; no JS imports, no hardware data."""
from fractions import Fraction as F

def overlap(left, right, pulse, width):
    return max(F(0), min(right, pulse + width) - max(left, pulse))

def bracket(start, end):
    width, step = F(1, 10), F(1, 20)
    phases = [F(-6 + i, 20) for i in range(24)]
    positive = [i for i, phase in enumerate(phases)
                if overlap(start, end, phase, width) > 0]
    first, last = positive[0], positive[-1]
    assert first > 0 and last < len(phases) - 1
    return ((phases[first - 1] + width, phases[first] + width),
            (phases[last], phases[last + 1]))

def main():
    a, b = (F(0), F(2, 5)), (F(1, 5), F(3, 5))
    bounds_a, bounds_b = bracket(*a), bracket(*b)
    for bounds, (start, end) in ((bounds_a, a), (bounds_b, b)):
        assert bounds[0][0] <= start <= bounds[0][1]
        assert bounds[1][0] <= end <= bounds[1][1]
    assert a[1] < F(1, 2) < F(2)
    assert b[0] < F(1, 2) < b[1]
    assert bounds_a != bounds_b
    print("E002-465 independent rational phase-scan replay PASS")
    print("A shutter brackets:", bounds_a)
    print("B shutter brackets:", bounds_b)

if __name__ == "__main__":
    main()
