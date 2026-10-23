# E002-389 frozen experiment — joint exposure-integral observability (2026-10-23)

## Primary scientific question
Does treating the actual exposure integrals jointly, rather than independently as nominal frame-center aperture samples, produce strictly stronger *sound* exclusion of hidden threshold crossings under the same independently assumed aperture-speed bound? This is a synthetic, bounded-instrument test, not a human/physical-camera validation or novelty claim.

## Frozen model and protocol
A continuous aperture a(t) belongs to [0,1] on [0,0.100] seconds and is V=60/s Lipschitz. Threshold theta=0.2. Camera exposures are nonoverlapping intervals [0.010,0.030], [0.040,0.060], [0.070,0.090] seconds. Each exposure reports its *time average* y=0.96 with deterministic absolute error <=0.005. Target observation interval is [0.020,0.080]. Compare an outer-only camera (first and third exposures) against a three-exposure camera (all). Grid h=0.001 seconds. Represent a piecewise-linear interpolation of node apertures. For arbitrary continuous Lipschitz signals, node interpolation error is bounded by V*h/2, so enlarge each exposure-mean tolerance by V*h/2 and subtract V*h/2 from the minimum node certificate. Report both grid-conditional and conservative continuum bounds.

Use linear programming to minimize each target node aperture, constrained by a in [0,1], adjacent speed <=V, and exact integrated exposure means for piecewise-linear interpolation. A certified no-crossing conclusion requires the *continuum-conservative* minimum >theta. Independently verify primal feasibility and reconstruct explicit hidden-closure witnesses when a certificate is not possible. No statistical confidence language for these deterministic conditional bounds.

## Frozen predictions
P1. The outer-only camera will admit a hidden crossing at t=0.050, and must abstain.
P2. Adding the middle exposure at the same high measured mean will exclude hidden crossings over the entire target interval under the continuum-conservative calculation, yielding a strict certificate improvement.
P3. Lowering the middle exposure mean to 0.50 (other means unchanged) will restore at least one feasible threshold crossing or else make the observations inconsistent. If inconsistent, report this instead of tuning.
P4. Inflating measurement error to 0.20 will weaken or remove the three-exposure guarantee; report the actual decision even if the prediction fails.
P5. Independent dual/primal checks will find no LP feasibility or measurement residual >1e-7 in the grid model, and a direct constructed trajectory from P1 will obey the speed bound and measured means.

## Critical limitations and product consequence
The speed V is assumed, not measured from independent human data. The y values are synthetic. A camera RGB value cannot be substituted for physical exposure-mean aperture without independently validated optical transfer. The grid correction is a sufficient, not sharp, continuum certificate. Reject any unqualified product inference; implement only an explicitly calibrated qualification gate. Preserve failed predictions and LP solver tolerances. Human validation still requires synchronized, calibrated ordinary RGB/high-speed reference with participant/device holdouts.
