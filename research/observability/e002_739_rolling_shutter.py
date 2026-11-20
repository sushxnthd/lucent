#!/usr/bin/env python3
"""E002-739: rolling-shutter row-time counterexample, exact rational arithmetic.

Synthetic instrument falsification, not a human measurement. Run:
    python research/observability/e002_739_rolling_shutter.py
"""
from fractions import Fraction as F

def aperture(t, t0, t1, a, speed):
    """Piecewise linear closure/reopening with exact slope <= speed."""
    mid = (t0 + t1) / 2
    return max(F(0), a - speed * abs(t - t0)) if t <= mid else max(F(0), a - speed * abs(t1 - t))

def hidden_possible(a0, a1, gap, speed):
    return speed * gap >= a0 + a1

def test():
    cases = 0
    # Each observation is stamped with the same frame timestamp 0,
    # but distinct sensor rows are exposed at different physical times.
    for rows in (100, 200, 400, 800):
        for readout in (F(1,100), F(1,50), F(1,25)):
            for speed in (F(50), F(100), F(200), F(400)):
                for aperture_value in (F(1,4), F(1,2), F(3,4)):
                    row0, row1 = 0, rows - 1
                    t0 = F(row0, rows-1) * readout
                    t1 = F(row1, rows-1) * readout
                    nominal_gap = F(0)
                    physical_gap = t1 - t0
                    assert not hidden_possible(aperture_value, aperture_value, nominal_gap, speed)
                    possible = hidden_possible(aperture_value, aperture_value, physical_gap, speed)
                    if possible:
                        # For symmetric endpoints the tent construction reaches zero at midpoint
                        # when the velocity budget is sufficient.
                        mid = (t0+t1)/2
                        assert aperture(t0,t0,t1,aperture_value,speed) == aperture_value
                        assert aperture(t1,t0,t1,aperture_value,speed) == aperture_value
                        assert aperture(mid,t0,t1,aperture_value,speed) == 0
                    cases += 1
    assert cases == 144
    # Explicit reversal: nominal gap zero says excluded, physical row gap permits closure.
    a, speed, gap = F(1,2), F(100), F(1,100)
    assert not hidden_possible(a,a,F(0),speed)
    assert hidden_possible(a,a,gap,speed)
    print(f"PASS {cases} exact-rational synthetic row-time configurations; explicit nominal/physical reversal")

if __name__ == "__main__":
    test()
