# E002-570 FROZEN | Exposure-average substitution kill test

Date: 2026-10-31. Primary E002-371 kernel. Existing branch `research/observability-human-boundary`, draft PR #26. Frozen **before** implementation, numeric execution, and test results. This is an **idealized instrument-model falsification**, not human validation or measured camera hardware.

## Testable failure hypothesis

An ordinary camera reports a shutter-integrated **mean aperture** rather than a pointwise aperture at the exposure edge. Even with an exactly known global-shutter boxcar, a perfectly linear noiseless aperture sensor, a true hard Lipschitz speed ceiling, and zero clock error, treating the exposure average as an endpoint value can issue a false `EXCLUDE` verdict for a hidden closure.

## Precommitted geometry and prediction

Normalized aperture a(t) in [0,1], |da/dt| <= V=25/s, threshold theta=1/5, period F=1/30 s, first exposure [0,w], second [F,F+w], w=1/100 s. The unexposed gap H=F-w=7/300 s. Construct piecewise-linear trajectory with aperture 37/50 at t=0, 49/100 at t=w, a symmetric V-speed V-shaped minimum at t=(F+w)/2, 49/100 at t=F, and 37/50 at t=F+w. No clipping or unphysical jump. The exact exposure means are A=B=123/200 (0.615). The gap midpoint aperture is 119/600 (0.198333...), strictly below theta.

Prediction P1: the **invalid** point-endpoint substitution `L_naive=(A+B-V*H)/2` is 97/300 (~0.323333), strictly above theta, and would falsely exclude closure.

Prediction P2: the **valid conservative** boxcar-aware lower bound `L_boxcar=max(0,(A+B - V*(H+(w1+w2)/2))/2)` is 119/600 (~0.198333), does **not** exclude, and is attained by this trajectory. The exposure-edge uncertainty penalty is V*w_i/2 for each exposure; exact only for the stipulated linear boxcar aperture observation model.

Prediction P3: independently integrate each exposure by a second numerical implementation and check the analytic means within 1e-6; test continuity, Lipschitz slopes, hidden positive-duration threshold crossing, and perturbation monotonicity. With no authenticated linear aperture transfer function or hard human V, **both** inference methods must remain unavailable to the product. Exposure duration uncertainty, rolling shutter, brightness nonlinearities, gaze, glasses, blur, geometry, missing frames, and clock error cannot be silently treated as calibrated.

## Falsification/stop rules

If the stipulated path violates [0,1], |slope|<=25/s, or exact shutter averages, or the corrected bound exceeds theta, the hypothesis fails and the negative result is retained. Do not tune parameters after this freeze. Report no measured human blink, no independent rater, no physical shutter capture, and no release readiness. This experiment is a **new synthetic instrument counterexample**; it must not delay or substitute for the E002-567 physical study and blinded human annotation.
