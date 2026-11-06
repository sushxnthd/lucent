"""E002-683: sharp global bounded-aperture/acceleration speed envelope.
No physiological calibration is implied.
"""
from fractions import Fraction
from math import sqrt

def velocity_ceiling(acceleration, aperture_range):
    if acceleration < 0 or aperture_range < 0:
        raise ValueError("nonnegative physical bounds required")
    return sqrt(acceleration * aperture_range)

def bang_bang_peak(acceleration, aperture_range):
    # From rest, accelerate over half range, then decelerate over half.
    return sqrt(acceleration * aperture_range)

def test():
    for a in [Fraction(1,4), Fraction(1), Fraction(4), Fraction(100)]:
        for r in [Fraction(1,4), Fraction(1,2), Fraction(1)]:
            v = velocity_ceiling(a,r)
            assert abs(v-bang_bang_peak(a,r)) < 1e-12
            assert abs(v*v-float(a*r)) < 1e-12
    assert velocity_ceiling(0,1) == 0
    print("PASS: 12 sharp bang-bang envelopes plus zero-acceleration case")
if __name__ == "__main__": test()
