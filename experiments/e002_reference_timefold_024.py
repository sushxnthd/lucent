"""E002-024: synthetic, source-style EyeDentify temporal reference audit.

Reproduce: python experiments/e002_reference_timefold_024.py
No human images or real participant measurements used.
"""
import json
import numpy as np
import pandas as pd

FS_TOBII = 90
FS_RGB = 30
SECONDS = 3
N_RGB = FS_RGB * SECONDS

def source_style_alignment(pupil_90hz):
    """Mimic upstream's three per-second Series, index-wise mean, frame pairing."""
    arr = np.asarray(pupil_90hz, dtype=float)
    assert arr.shape == (FS_TOBII * SECONDS,)
    bins = [pd.Series(arr[k*FS_TOBII:(k+1)*FS_TOBII]) for k in range(SECONDS)]
    return pd.concat(bins, axis=1).mean(axis=1).to_numpy()[:N_RGB]

def independent_fold(pupil_90hz):
    return np.asarray(pupil_90hz).reshape(SECONDS, FS_TOBII).mean(axis=0)

def frequency_gain(f):
    return abs(sum(np.exp(2j*np.pi*f*k) for k in range(SECONDS))/SECONDS)

def metrics(name, fn):
    ref = fn(np.arange(N_RGB)/FS_RGB)
    folded = source_style_alignment(fn(np.arange(FS_TOBII*SECONDS)/FS_TOBII))
    rng = np.ptp(ref)
    r = float(np.corrcoef(ref, folded)[0,1]) if np.std(folded)>1e-9 else None
    return dict(case=name, reference_range_mm=float(rng),
                folded_range_mm=float(np.ptp(folded)),
                range_ratio=float(np.ptp(folded)/rng),
                waveform_pearson=r,
                nrmse_over_reference_range=float(np.sqrt(np.mean((ref-folded)**2))/rng))

def run():
    cases = {
        "linear_ramp_3s": lambda t: 3.0+0.1*t,
        "single_cycle_3s": lambda t: 3.0+0.2*np.sin(2*np.pi*t/3),
        "two_cycles_3s": lambda t: 3.0+0.2*np.sin(4*np.pi*t/3),
        "one_cycle_per_second": lambda t: 3.0+0.2*np.sin(2*np.pi*t),
        "gaussian_response_1p2s": lambda t: 3.0+0.3*np.exp(-0.5*((t-1.2)/0.22)**2),
        "delayed_exponential_response": lambda t: 3.0+0.3*np.where(t>0.6,
            (1-np.exp(-np.maximum(t-0.6,0)/0.35))*np.exp(-np.maximum(t-0.6,0)/3),0)
    }
    rng=np.random.default_rng(24)
    for _ in range(100):
        x=rng.normal(size=270)
        np.testing.assert_allclose(source_style_alignment(x), independent_fold(x))
    for f in (1/3,2/3,4/3,5/3):
        assert frequency_gain(f)<1e-12
    assert np.ptp(source_style_alignment(cases["single_cycle_3s"](np.arange(270)/90)))<1e-12
    return {"experiment":"E002-REFERENCE-TIMEFOLD-024",
            "data":"synthetic only",
            "outcomes":[metrics(name,fn) for name,fn in cases.items()],
            "spectral_nulls_hz":[1/3,2/3,4/3,5/3],
            "claim_boundary":"Source-conditioned counterexample; released dataset not independently verified."}

if __name__=="__main__":
    print(json.dumps(run(),indent=2,allow_nan=False))
