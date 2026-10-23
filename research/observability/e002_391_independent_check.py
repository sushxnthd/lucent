#!/usr/bin/env python3
"""Independent E002-391 analytic phase-geometry and quadrature check."""
import json
from pathlib import Path
import numpy as np

F=1/30
V=40.
THETA=.2
EXPOSURE=.005

def direct_mean(start,exposure=.005):
    t=np.linspace(start,start+exposure,10001)
    a=np.clip(V*np.abs(t),0.,1.)
    return float(np.trapezoid(a,t)/exposure)

def main():
    d=json.loads(Path(__file__).with_name("e002_391_results.json").read_text())
    # theta/V >= e/2 => mean-threshold crossing at |exposure-center|=theta/V.
    assert THETA/V>=EXPOSURE/2
    p_exact=2*THETA/(V*F)
    assert abs(d["single_cycle_phase_grid_capture_p"]-p_exact)<1e-4
    for center in (-.005,-.0025,0.,.0025,.005):
        value=direct_mean(center-EXPOSURE/2)
        if abs(center)==.005:
            assert abs(value-THETA)<1e-7,(center,value)
        else:
            assert value<THETA,(center,value)
    predicted=1-(1-p_exact)**12
    assert abs(predicted-d["randomized_theory_any_fraction"])<1e-4
    for key,expected in [("locked_any_fraction",p_exact),("randomized_any_fraction",predicted)]:
        assert abs(d[key]-expected)<.02,(key,d[key],expected)
    assert d["jitter_1ms_any_fraction"]<d["randomized_any_fraction"]
    assert d["bounded_optical_always_open_false_positive_count"]==0
    assert d["unbounded_optical_bias_partial_open_false_positive_count"]==12000
    print(json.dumps({"independent_analytic_phase_capture":p_exact,
        "independent_analytic_randomized_any":predicted,
        "primary_locked":d["locked_any_fraction"],
        "primary_randomized":d["randomized_any_fraction"],
        "quadrature_boundary_checks":5,"pass":True},indent=2))

if __name__=="__main__":main()
