# E002-623 | Acceleration-assisted velocity bridge (conditional, unvalidated)

## New inference
E002-622 proved that finite-difference speed alone cannot certify a continuous-time eyelid speed ceiling. There is a precise additional assumption that would make a bridge possible: for aperture x(t) with an independently validated bound |x''(t)| <= A on every sampled interval of duration h, and endpoint aperture errors <= epsilon, every instantaneous speed in that interval satisfies

|x'(t)| <= (|y_(i+1)-y_i|+2 epsilon)/h + A h/2.

Proof: write the secant slope as the mean of x' over the interval. Lipschitz continuity of x' gives |x'(t)-mean(x')| <= (A/h) integral_0^h |t-u|du <= Ah/2. Measurement error contributes at most 2epsilon/h. The Ah/2 term is sharp at the interval endpoints for constant acceleration. The resulting V is a conditional ceiling, **not** a physiological fact.

## Falsification and acquisition protocol
Before examining held-out subjects, measure an upper acceleration envelope independently on a faster synchronized reference instrument with calibrated exposure timing, position error, dropped-frame bounds and blinded anatomy. Predefine whether the claimed acceleration ceiling is deterministic or a population coverage statement; a quantile is not a hard bound. Compare held-out continuously reconstructed trajectories against the proposed envelope. Any reliable exceedance invalidates deterministic certification for that scope. Without a justified A, return ABSTAIN_UNCALIBRATED. If velocity is certified, use conservative shutter-gap upper bounds and aperture lower bounds; equality abstains.

The reproducible exact-rational implementation is `e002_623_acceleration_bridge.py`. It includes a sharp constant-acceleration extremizer and guards against applying a velocity certificate without the auxiliary A assumption. The earlier triangular counterexample has an unbounded cusp acceleration and therefore is not a counterexample to this *conditional* theorem.

## Evidence and product consequence
Evidence tier: analytic proof and local exact-arithmetic test fixture only. No new human video, motorized occluder capture, independent replay or externally certified acceleration bound. Do not promote this to camera-derived human closure detection. Product remains ABSTAIN_UNCALIBRATED and release BLOCKED. This instrument is useful only if the physical validation campaign can independently establish A and aperture error budgets; otherwise kill the certification pathway.
