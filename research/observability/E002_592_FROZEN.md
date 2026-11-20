# E002-592 | Frozen sensor-transfer adversarial experiment

Date: 2026-11-01 UTC. Primary kernel E002-371, building on E002-591. Evidence tier: exact-rational synthetic camera-transfer falsification, **not** human or physical-camera validation.

## Question
E002-591 proves that a sustained eyelid closure cannot have the same *ideal aperture mean* as a constant-open reference for some dimensionless duration/speed regimes. Does that imply a usable no-hidden-closure decision when aperture is transferred to measured camera brightness with uncertain contrast, illumination offset and sensor error? Test the *same known shutter exposure* under calibrated and uncalibrated nuisance budgets.

## Predeclared exact construction
Use normalized exposure T=1, endpoints c=1/2, closure threshold tau=1/10, dwell d=3/5, speed bound L=VT=20. The E002-591 maximum sustained-closure aperture mean is M=839/2000=0.4195, whereas the always-open mean is c=1/2; aperture contrast Delta=c-M=161/2000=0.0805. Construct the speed-saturating piecewise-linear witness with exact knots (time, aperture): (0,1/2),(1/50,1/10),(31/50,1/10),(133/200,1),(39/40,1),(1,1/2). Assert endpoints, dwell, slope bound, range and exact integral.

Camera transfer: Y=b+kappa*mean_aperture+eta, with positive known kappa for each trial, baseline illumination offset b in [-B,B], and bounded read error eta in [-E,E]. Independent offsets/errors are permitted for the two candidate histories; this is a conservative uncertainty set, not a model of random Gaussian noise. With h=B+E, the constant-open observation interval is [kappa*c-h,kappa*c+h], while the closure upper observation bound is kappa*M+h. Their intervals are disjoint iff kappa*Delta>2h. Equality is **not** certification; boundary overlap requires abstention. When kappa unknown, require independently authenticated kappa_min>0 and use kappa_min*Delta; otherwise abstain. Note: this only distinguishes the constant-open reference from the specified closure class; it does NOT certify that an arbitrary real-world frame has no blink.

Frozen scenarios:
- kappa=1/5, B=1/100, E=1/200: kappa*Delta=161/10000=0.0161 <= 0.03 => OVERLAP_ABSTAIN.
- kappa=3/5, same nuisance: 483/10000=0.0483 > 0.03 => MODEL_SEPARABLE_ONLY.
- kappa=3/5, B=1/50, E=1/200: 0.0483 <= 0.05 => OVERLAP_ABSTAIN.
- kappa=3/5, B=1/100, E=1/200, but missing response calibration, gaze/geometry, glasses, blur, missingness, saturation or timing flags => ABSTAIN_UNCALIBRATED.
- kappa=3/5, B=1/100, E=1/200, speed L=100 => Delta=481/10000=0.0481 and pixel gap=0.02886 <= 0.03 => OVERLAP_ABSTAIN. Recompute the sharp M_d(L), not the L=20 witness.

## Adversarial verification
1. Exact-rational Python simulator validates all frozen cases, threshold equality, and constructs explicit indistinguishable measurements for the overlap case using permissible nuisance endpoints.
2. Independently written Node BigInt rational verifier reproduces numeric predictions without consuming Python output.
3. At least 100 deterministic seeded synthetic trials spanning kappa, B, E and speed; verify that whenever a no-overlap claim is emitted, all model-admissible closure measurements are below all admissible constant-open measurements. Include invalid-input, unknown-calibration and nuisance rejection.
4. Preserve negative cases, reproducibility and release consequence. No real images, participants or velocity calibration are claimed.

## Decision and limits
A MODEL_SEPARABLE_ONLY output is an idealized two-hypothesis sensor-transfer result, not physical or clinical certification. Product outputs remain ABSTAIN_UNCALIBRATED and release BLOCKED absent authenticated shutter/clock, anatomy, contrast, sensor response, hard velocity ceiling, independent raters and held-out human tests. This experiment must not imply full blink detection from mean brightness.
