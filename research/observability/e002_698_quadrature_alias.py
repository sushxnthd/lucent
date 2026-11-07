#!/usr/bin/env python3
"""E002-698: exact-rational adversarial exposure quadrature test. stdlib only."""
from fractions import Fraction as F

def integrate_piecewise(points):
    return sum((y0+y1)*(x1-x0)/2 for (x0,y0),(x1,y1) in zip(points,points[1:]))

def check(points, velocity):
    assert all(x1>x0 and abs(y1-y0)<=velocity*(x1-x0)
               for (x0,y0),(x1,y1) in zip(points,points[1:]))
    assert all(F(0)<=y<=1 for _,y in points)

def run():
    # A valid continuous-time tent hidden between sample nodes.
    # Both sample endpoints are 0.9; true exposure mean is 0.95.
    points=[(F(0),F(9,10)),(F(1,10),F(1)),(F(1,5),F(9,10))]
    check(points,F(1))
    actual=integrate_piecewise(points)/F(1,5)
    trapezoid=(points[0][1]+points[-1][1])/2
    assert actual==F(19,20) and trapezoid==F(9,10)
    # Worst-case quadrature error for an L-Lipschitz function on a
    # cell of width d is <= L*d/4 in its cell mean.
    # Saturation uses a symmetric tent without aperture clipping.
    for d in (F(1,10),F(1,5),F(1,2)):
        base=F(1,2)
        witness=[(F(0),base),(d/2,base+d/2),(d,base)]
        check(witness,F(1))
        error=integrate_piecewise(witness)/d-base
        assert error==d/4
    # For N cells, mean error <= L*sum(d_i^2)/(4*sum(d_i)).
    # Equal grid spacing d gives L*d/4, not zero.
    print("PASS: exact exposure alias 0.95 vs trapezoid 0.90")
    print("PASS: Lipschitz trapezoid mean-error envelope saturated on three grids")
    print("Interpretation: uncorrected discrete LP exposure equality is not a continuous-time certificate")

if __name__=="__main__":
    run()
