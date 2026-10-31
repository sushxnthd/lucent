# E002-522 | Frozen bounded-shutter-response concentration experiment

Date: 2026-10-29. Same E002-371 primary kernel, branch `research/observability-human-boundary`, draft PR #26. Protocol frozen **before** the executable, tests or result were written.

## Distinct question and negative control

E002-521 establishes a positive physical closure-time lower bound under *uniform* temporal exposure integration and correctly refuses unbounded nonuniform shutter weighting. Test whether a separately calibrated **upper bound on the shutter response's temporal concentration** rescues a rigorous physical-time inference without assuming uniform integration.

Let an independently timed reference exposure E have duration T >= T_min > 0, strictly contained in the ordinary-camera guaranteed blind interior. Let q(t) be its independently calibrated nonnegative normalized temporal weighting, integral_E q=1, and assume the *pointwise* upper envelope q(t) <= R/T almost everywhere, with finite R>=1. Let physical ordinary-camera aperture a_o(t) lie in [0,1], closure predicate a_o(t)<=theta, 0<theta<1, and let the transported **weighted** mean satisfy integral_E q(t)a_o(t)dt <= M=K U+B with nonnegative independently calibrated K,B and reference weighted mean upper U.

Freeze the proposed dimensionless law for total physical closure measure C={t:a_o(t)<=theta}:

- If M<theta, |C|/T >= (1-M/theta)/R, so |C| >= T_min (1-M/theta)/R.
- If M>=theta, R is absent/unbounded, or any independent calibration prerequisite fails, no positive physical-time inference.
- R=1 must reproduce E002-521. R=2 must halve its conditional 0.4-ms lower bound to 0.2 ms at theta=.2, M=.19, T_min=8 ms.
- A sequence of increasingly concentrated shutter kernels with R->infinity must defeat every positive bound that ignores R.
- Show infimum sharpness by two-level aperture and piecewise shutter weights; verify a calibrated upper bound R is necessary rather than assuming R from nominal FPS or a camera's datasheet.
- A finite R is a **sensor/instrument** assumption, not a physiological eyelid-speed ceiling. No contiguous blink, fatigue, PERCLOS or no-hidden-blink claim follows.

## Independent falsification and adversaries

Use exact rational arithmetic for frozen examples and for deterministic held-out piecewise-constant trajectories with varied aperture, shutter response, geometry scale and threshold. Compute each weighted mean by direct integration of the discrete step functions, not by using the proposed bound to generate the mean. Independently count physical closed intervals and test the inequality. Include deliberate counterexamples with falsely understated R, nonlinear/negative weights, missing clock, no native sequence provenance, missing radiometry, uncertain geometry, and reference-censoring. The evaluator must fail closed on uncalibrated R and all absent attestations; no input can set product release to allowed.

This is a *synthetic instrument-response test* only. No physical response function, human eyelid sequence or independent anatomical rating has been measured. The pre-existing E002-519 human handoff remains the decisive empirical gate. Do not run further dataset archaeology or claim this as novel general measure theory.

## Stop/decision rule

A valid counterexample under every frozen assumption kills the law. If it survives, add only a conditional offline duration evaluator, a reproducible independent finite-grid replay and an explicit instrument requirement to measure a conservative response-envelope R. Do not weaken the existing abstention gate.