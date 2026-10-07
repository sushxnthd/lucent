"""E002-019 synthetic high-coverage mask adversary. Run: python experiments/e002_dense_mask_adversary_019.py
Requires numpy. NO human data, no webcam data, no physiological inference.
Reimplements the legacy O4 waveform interpolation and E002-018 support criterion.
"""
import itertools
import json
import numpy as np

T = np.arange(0, 5.00001, 0.05)

def latent(t, rep):
    return (0.5 + 0.08*np.sin(2*np.pi*t/5)
            + 0.03*np.sin(4*np.pi*t/5)
            + (rep-1)*0.00005*t/5
            + 0.00005*rep*np.sin(3.2*t+0.4))

def keep_mask(period, phase):
    keep = np.arange(len(T)) % period != phase
    keep[0] = keep[-1] = True
    return keep

def centered(y):
    return y - np.median(y[T <= 0.40])

def o4(groups):
    def rmse(a,b): return float(np.sqrt(np.mean((a-b)**2)))
    within = [rmse(a,b) for c in groups for a,b in itertools.combinations(groups[c],2)]
    between = [rmse(a,b) for a in groups["A"] for b in groups["B"]]
    wi, be = np.median(within), np.median(between)
    return {"ratio": float(be/wi), "withinMedianRMSE": float(wi),
            "betweenMedianRMSE": float(be), "legacyPass": bool(be/wi > 1.25)}

def supported_fraction(observed_t):
    # Exact reproduction of the E002-018 nearby-grid support definition:
    # a grid point counts as supported if within 0.10 s of ANY observation.
    distance = np.min(np.abs(T[:,None] - observed_t[None,:]), axis=1)
    return float(np.mean(distance <= 0.10 + 1e-10))

def experiment(period):
    traces = {"A": [], "B": []}
    dense = {"A": [], "B": []}
    common = {"A": [], "B": []}
    derivatives = {"A": [], "B": []}
    uncentered = {"A": [], "B": []}
    masks = {"A": keep_mask(period,1), "B": keep_mask(period,2)}
    jointly_observed = masks["A"] & masks["B"]
    support = []
    for c in traces:
        t = T[masks[c]]
        support.append(supported_fraction(t))
        for rep in range(3):
            y = np.interp(T, t, latent(t,rep))
            traces[c].append(centered(y))
            uncentered[c].append(y)
            derivatives[c].append(np.diff(y)/0.05)
            dense[c].append(centered(latent(T,rep)))
            common[c].append(latent(T[jointly_observed],rep))
    return {"period": period,
            "observedFraction": float(masks["A"].mean()),
            "maxGapS": float(np.max(np.diff(T[masks["A"]]))),
            "supportedFraction": float(min(support)),
            "provisional018Veto": bool(min(support)<0.8 or
                                     np.max(np.diff(T[masks["A"]]))>0.2),
            "legacyO4": o4(traces),
            "denseControl": o4(dense),
            "coObservedControl": o4(common),
            "uncenteredO4": o4(uncentered),
            "firstDifferenceO4": o4(derivatives)}

if __name__ == "__main__":
    results = [experiment(p) for p in (3,4,5,6,8,10)]
    assert all(not x["provisional018Veto"] for x in results)
    assert all(x["legacyO4"]["legacyPass"] for x in results)
    assert all(abs(x["coObservedControl"]["ratio"]-1)<1e-8 for x in results)
    assert all(abs(x["denseControl"]["ratio"]-1)<1e-8 for x in results)
    print(json.dumps({"experiment":"E002-TRACE-SUPPORT-019",
                      "dataType":"DETERMINISTIC SYNTHETIC ONLY",
                      "nTracesPerSetting":6,
                      "results":results,
                      "claimBoundary":"Software false-positive only; not a human, RGB, pupil-reference or fatigue result."},
                     indent=2))
