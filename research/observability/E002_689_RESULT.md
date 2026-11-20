# E002-689 — Clock uncertainty falsifies nominal-gap exclusion

**Evidence tier:** exact-rational deterministic synthetic adversarial test. No human or physical measurements.

## Conditional result
For anatomical aperture endpoints a,b, speed bound v and actual blind interval h, the exact minimum aperture under a Lipschitz speed constraint is max(0,(a+b-vh)/2) when |a-b| <= vh. If endpoint intervals are [al,ah], [bl,bh], and the blind gap lies in [hlo,hhi], the worst case occurs at hhi. If the endpoint intervals are feasible at hhi, the jointly minimal endpoints are a*=max(al,bl-v*hhi), b*=max(bl,al-v*hhi). Their minimum envelope is max(0,(a*+b*-v*hhi)/2). Otherwise the data are inconsistent and require abstention. This assumes the clock interval truly bounds all exposure, rolling-shutter, dropped-frame and timestamp uncertainties.

## Falsification
A nominal h=1, a=b=1, v=1 implies minimum aperture 1/2 and excludes closure at threshold 1/4. If the same timing system only guarantees h in [1,2], minimum aperture becomes 0, so exclusion is invalid. The regression enumerates 432 rational configurations; 80 nominal-gap certificates at threshold 1/4 are withdrawn after accounting for endpoint and clock intervals. A separately sampled feasible-grid oracle produced zero contradictions. The oracle is a coarse-grid check, not independent exhaustive proof.

Run: `python research/observability/e002_689_clock_uncertainty.py`. Local run returned `cases 432 grid_contradictions 0 nominal_false_certificates 80`.

## Product consequence
Do not use nominal frame period or frame timestamps as a hard blind-gap upper bound. Without externally measured acquisition timing and uncertainty budget, output `ABSTAIN_UNCALIBRATED`. Even with a measured gap, anatomical calibration and independently justified human velocity bound are prerequisites. This test is not physiological validation and does not authorize production.

## Next decisive experiment
Execute frozen E002-671 synchronized physical shutter/photodiode acquisition; estimate actual maximum blind intervals and timing uncertainties under exposure, dropped-frame, rolling-shutter and jitter perturbations. Pre-register predictions before held-out human sequence inspection. No additional theorem-only runs should substitute for this experiment.
