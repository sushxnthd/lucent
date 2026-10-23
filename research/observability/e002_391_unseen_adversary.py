#!/usr/bin/env python3
"""E002-391 supplemental preregistered unseen 60Hz and adaptive-event instrument."""
import json
from pathlib import Path
import numpy as np

V=40.
E=.005
THETA=.2
N=12000
CYCLES=12

def primitive(x):
    r=1/V
    return np.where(x<=-r,0.,np.where(x<0.,x+V*x*x/2+r/2,
           np.where(x<r,r/2+x-V*x*x/2,r)))

def mean(start):
    return 1-(primitive(start+E)-primitive(start))/E

def capture(phase,F):
    return np.minimum(mean(phase-F),mean(phase))<THETA

def main():
    rng=np.random.default_rng(39113)
    F60=1/60
    p_theory=2*THETA/(V*F60)
    locked=rng.uniform(0,F60,N)
    independent=rng.uniform(0,F60,(N,CYCLES))
    a=float(np.mean(capture(locked,F60)))
    b=float(np.mean(np.any(capture(independent,F60),axis=1)))
    expected=1-(1-p_theory)**CYCLES
    F30=1/30
    randomized_phase=rng.uniform(0,F30,(N,CYCLES))
    trough=randomized_phase+F30/2
    starts_before=randomized_phase-trough
    starts_after=randomized_phase+F30-trough
    adaptive=np.minimum(mean(starts_before),mean(starts_after))<THETA
    result={
        "seed":39113,"unseen_60hz_single_capture_theory":p_theory,
        "unseen_60hz_locked_fraction":a,"unseen_60hz_randomized_fraction":b,
        "unseen_60hz_randomized_theory":expected,
        "adaptive_30hz_detected_event_count":int(np.sum(adaptive)),
        "adaptive_30hz_total_event_count":int(adaptive.size),
        "adaptive_30hz_minimum_shutter_mean":float(np.min(np.minimum(mean(starts_before),mean(starts_after)))),
        "predictions":{
            "unseen_locked":abs(a-p_theory)<.02,
            "unseen_randomized":b>.99 and abs(b-expected)<.02,
            "adaptive_hidden":not np.any(adaptive)
        },
        "evidence_tier":"synthetic instrument only; adversarial phase coupling is constructed"
    }
    assert all(result["predictions"].values()),result
    Path(__file__).with_name("e002_391_unseen_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
