#!/usr/bin/env python3
"""E002-391: frozen synthetic phase-sweep acquisition experiment; not human evidence."""
import json
from pathlib import Path
import numpy as np

SEED=39111
F=1/30
EXPOSURE=.005
SPEED=40.
THETA=.2
N_EVENTS=12
N_TRIALS=12000
EPS=.03

def deficit_primitive(x):
    """Exact integral of max(0,1-V|x|) from -infinity to x."""
    x=np.asarray(x,dtype=float)
    r=1/SPEED
    return np.where(x<=-r,0.,np.where(x<0.,x+SPEED*x*x/2+r/2,
           np.where(x<r,r/2+x-SPEED*x*x/2,r)))

def shutter_mean(start,exposure=EXPOSURE):
    return 1-(deficit_primitive(np.asarray(start)+exposure)-deficit_primitive(start))/exposure

def minimum_mean(phase):
    phase=np.asarray(phase)
    return np.minimum(shutter_mean(phase-F),shutter_mean(phase))

def numerical_mean(start,exposure=EXPOSURE,steps=8000):
    t=np.linspace(start,start+exposure,steps+1)
    aperture=np.minimum(1.,SPEED*np.abs(t))
    return float(np.trapezoid(aperture,t)/exposure)

def main():
    rng=np.random.default_rng(SEED)
    phase_grid=(np.arange(12000)+.5)*F/12000
    p=float(np.mean(minimum_mean(phase_grid)<THETA))
    locked_phase=rng.uniform(0,F,N_TRIALS)
    randomized_phase=rng.uniform(0,F,(N_TRIALS,N_EVENTS))
    jitter_phase=(locked_phase[:,None]+rng.uniform(-.001,.001,(N_TRIALS,N_EVENTS)))%F
    locked=minimum_mean(locked_phase)<THETA
    randomized=np.any(minimum_mean(randomized_phase)<THETA,axis=1)
    jitter=np.any(minimum_mean(jitter_phase)<THETA,axis=1)
    optical_error=rng.uniform(-EPS,EPS,(N_TRIALS,N_EVENTS))
    conservative_randomized=np.any(minimum_mean(randomized_phase)+optical_error+EPS<THETA,axis=1)
    open_errors=rng.uniform(-EPS,EPS,(N_TRIALS,N_EVENTS))
    false_positive_bounded=int(np.sum(np.any(1.+open_errors+EPS<THETA,axis=1)))
    # Nonclosed a=0.4 is falsely called closed under unbounded -0.3 optical bias.
    false_positive_unbounded=int(np.sum(np.full(N_TRIALS,.4-.30)<THETA))
    oracle_rng=np.random.default_rng(39112)
    oracle_phases=oracle_rng.uniform(0,F,100)
    oracle_maxerr=0.
    for phase in oracle_phases:
        for start in (phase-F,phase):
            oracle_maxerr=max(oracle_maxerr,abs(float(shutter_mean(start))-numerical_mean(start)))
    reference_starts=np.arange(-.03,.030,.001)
    reference_detection=bool(np.min(shutter_mean(reference_starts,.00025))<THETA)
    predicted_randomized=1-(1-p)**N_EVENTS
    result={
      "evidence_tier":"synthetic instrument only; no physical camera or human evidence",
      "seed":SEED,"frame_period_s":F,"exposure_s":EXPOSURE,
      "speed_limit_normalized_per_s":SPEED,"threshold":THETA,
      "cycles":N_EVENTS,"trial_sets":N_TRIALS,
      "single_cycle_phase_grid_capture_p":p,
      "locked_any_detected":int(locked.sum()),"locked_any_fraction":float(locked.mean()),
      "randomized_any_detected":int(randomized.sum()),"randomized_any_fraction":float(randomized.mean()),
      "randomized_theory_any_fraction":float(predicted_randomized),
      "jitter_1ms_any_detected":int(jitter.sum()),"jitter_1ms_any_fraction":float(jitter.mean()),
      "bounded_optical_conservative_any_detected":int(conservative_randomized.sum()),
      "bounded_optical_conservative_any_fraction":float(conservative_randomized.mean()),
      "bounded_optical_always_open_false_positive_count":false_positive_bounded,
      "unbounded_optical_bias_partial_open_false_positive_count":false_positive_unbounded,
      "independent_quadrature_max_absolute_error":oracle_maxerr,
      "simulated_1000hz_reference_detected":reference_detection,
      "predictions":{
        "P1":.05<p<.5,
        "P2":abs(float(locked.mean())-p)<.02,
        "P3":float(randomized.mean())>.9 and abs(float(randomized.mean())-predicted_randomized)<.02,
        "P4":false_positive_bounded==0,
        "P5":false_positive_unbounded>0
      },
      "product_rule":"phase sweep only for independent repeatable calibration events; never single-event absence certificate; abstain without optical and timing bounds"
    }
    assert oracle_maxerr<1e-6
    assert all(result["predictions"].values()),result
    Path(__file__).with_name("e002_391_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
