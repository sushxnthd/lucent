#!/usr/bin/env python3
"""E002-540: exact idealized global-shutter exposure-average counterexample.

Synthetic scalar model only. This does not measure eyelids, shutters or hard
human velocity ceilings. The linear frame-mean/aperture model is hypothetical.
"""
from fractions import Fraction as F
import json
from math import sqrt


def edge_min_from_average(b: float, V: float, E: float) -> float:
    """Sharp minimum aperture at exposure end, assuming mean b and V-Lipschitz a."""
    if not (0 <= b <= 1 and V >= 0 and E >= 0):
        raise ValueError("invalid calibrated average, speed ceiling, or exposure")
    if V == 0 or E == 0:
        return b
    z = V * E
    mean_max_at_zero = z / 2 if z <= 1 else 1 - 1 / (2 * z)
    if b <= mean_max_at_zero:
        return 0.0
    if z <= 1 and b <= 1 - z / 2:
        return b - z / 2
    return 1 - sqrt(2 * z * (1 - b))


def symmetric_hidden_floor(b: float, c: float, V: float, E: float, T: float) -> dict:
    """Conditional idealized speed-only bound for two equal exposure averages."""
    if not (0 <= c < b <= 1 and T > E >= 0 and V >= 0):
        raise ValueError("invalid geometry/threshold/velocity")
    x = edge_min_from_average(b, V, E)
    floor = max(0.0, x - V * (T - E) / 2)
    return {
        "edge_min": x,
        "hidden_floor": floor,
        "threshold": c,
        "conditional_exclusion": floor > c,
        "evidence": "IDEALIZED_EXPOSURE_AVERAGE_ONLY_NOT_HUMAN_CERTIFIED",
    }


def frozen_witness() -> dict:
    """Construct the preregistered seven-vertex exact rational witness."""
    V, E, T, b, c = F(45), F(1,100), F(1,30), F(9,10), F(1,5)
    D = T - E
    x = F(7,10)
    ramp = (1-x)/V
    plateau = E-ramp
    midpoint = (E+T)/2
    m = x - V*D/2
    vertices = [
        (F(0),F(1)), (plateau,F(1)), (E,x),
        (midpoint,m), (T,x), (T+ramp,F(1)), (T+E,F(1))
    ]
    assert all(F(0) <= a <= F(1) for _,a in vertices)
    assert all(vertices[i][0] < vertices[i+1][0] for i in range(len(vertices)-1))
    slopes = [(vertices[i+1][1]-vertices[i][1])/(vertices[i+1][0]-vertices[i][0])
              for i in range(len(vertices)-1)]
    assert all(abs(s) <= V for s in slopes)

    def integrate(left: F, right: F) -> F:
        area=F(0)
        for (t0,a0),(t1,a1) in zip(vertices,vertices[1:]):
            lo,hi=max(left,t0),min(right,t1)
            if lo >= hi: continue
            v=(a1-a0)/(t1-t0)
            ylo=a0+v*(lo-t0)
            yhi=a0+v*(hi-t0)
            area+=(ylo+yhi)*(hi-lo)/2
        return area

    mean1=integrate(F(0),E)/E
    mean2=integrate(T,T+E)/E
    dwell=2*(c-m)/V
    assert mean1 == mean2 == b
    assert m == F(7,40) and dwell == F(1,900)
    invalid_point_floor = b - V*D/2
    assert invalid_point_floor == F(3,8)
    assert invalid_point_floor > c > m
    return {
        "T": str(T), "E": str(E), "blind_gap": str(D), "V": str(V),
        "mean_first": str(mean1), "mean_second": str(mean2),
        "exposure_edge_aperture": str(x), "hidden_minimum": str(m),
        "closed_dwell_seconds": str(dwell),
        "invalid_pointwise_floor": str(invalid_point_floor),
        "vertex_times_apertures": [[str(t),str(a)] for t,a in vertices],
        "slopes": [str(s) for s in slopes],
        "model_only": True,
    }


def main() -> None:
    print(json.dumps({
        "frozen": frozen_witness(),
        "unseen_speed_40": symmetric_hidden_floor(.9,.2,40,.01,1/30),
        "unseen_speed_45": symmetric_hidden_floor(.9,.2,45,.01,1/30),
    },indent=2,sort_keys=True))

if __name__ == "__main__": main()
