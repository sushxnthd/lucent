"""Deterministic shutter integration falsifier; synthetic only, no physiological calibration."""
from fractions import Fraction as F

def aperture(t, center=F(20,1000), halfwidth=F(10,1000), height=F(2)):
    # Triangular closure: aperture 2 mm outside excursion, 0 mm at center.
    return height * min(F(1), abs(t-center)/halfwidth)

def integrate_piecewise(start, end):
    assert end > start
    knots = sorted(set([start,end]+[x for x in (F(10,1000),F(20,1000),F(30,1000)) if start<x<end]))
    area = sum((aperture(a)+aperture(b))*(b-a)/2 for a,b in zip(knots,knots[1:]))
    return area/(end-start)

def main():
    # A 40-ms exposure hides a true zero-aperture instant at 20 ms.
    full = integrate_piecewise(F(0), F(40,1000))
    assert full == F(3,2), full
    narrow = integrate_piecewise(F(19,1000), F(21,1000))
    assert narrow == F(1,10), narrow
    assert aperture(F(0)) == aperture(F(40,1000)) == 2
    # V=200 mm/s and 2-mm endpoints: Tcrit=20 ms, so 40 ms cannot exclude.
    assert F(40,1000) > F(4,200)
    print("PASS: exact-rational integrated 40ms aperture =",full,
          "mm; 2ms =",narrow,"mm; constructed hidden closure")
if __name__ == "__main__":
    main()
