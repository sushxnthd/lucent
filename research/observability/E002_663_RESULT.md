# E002-663 — Finite-horizon calibration maxima are not velocity ceilings

**Evidence tier:** exact order-statistics result plus deterministic counterexample. No human, camera, or instrument validation.

## New prediction
Let n independently calibrated and m subsequently deployed **exchangeable, continuously distributed** eyelid-velocity observations have a common distribution. If the calibration ceiling is their sample maximum, the exact probability that at least one future velocity exceeds it is **m/(n+m)**. Proof: among n+m observations, the unique global maximum is equally likely to occupy any position. The exceedance event occurs exactly when that maximum lies in the future block.

For n=100 and m=100, the exceedance risk is 1/2, not 1/101. For 100 future observations and a 5% bound on exceedance risk, n must be at least 1,900 under these assumptions. This is an exact finite-horizon law, not a claim about actual human velocity distributions. Under ties, the continuous formula is not automatically exact; under participant shift, temporal dependence, gaze/illumination confounding, or adaptive selection, the exchangeability assumption may fail completely. A deterministic calibration/future shift from velocities 1 to 2 is a counterexample.

**Important:** the law bounds exceedance of a sample maximum, not probability of a missed blink. A velocity ceiling can only be used for deterministic shutter-gap certificates if it is independently physically justified. A statistical calibration maximum may at most support explicitly probabilistic, horizon-limited statements after the sampling unit, independence/exchangeability, and uncertainty are validated.

## Frozen empirical falsification
Before examining held-out participants, fix aperture normalization, velocity estimator, frame timestamp uncertainty, shutter response, endpoint errors, threshold, calibration sample count, and the number of future comparison units. Derive participant-separated velocity maxima from high-frame-rate reference sequences. Evaluate observed exceedances over prespecified future horizons m, with confidence intervals and stratification by gaze, brightness, glasses, blur, geometry, missingness, and clock uncertainty. Compare against m/(n+m) **only** for defensibly exchangeable sampling units. If the units are correlated frames, analyze at the independent recording/participant level or refuse the iid prediction. Include a predeclared held-out ordinary-frame decimation to test actual hidden-closure certificates separately.

## Product decision
No deterministic blink-absence claim may be justified by sample maxima, even when the observed calibration set is large. Statistical tail coverage requires an explicit horizon and validated exchangeability, and must never silently replace the physical velocity ceiling in E002-371. Maintain ABSTAIN_UNCALIBRATED and production BLOCKED.

Reproduce: `python research/observability/e002_663_horizon.py`.
