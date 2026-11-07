# E002-684 | Sharp finite-window acceleration-only closure exclusion

**Tier:** conditional analytic result plus locally executed exact-rational regression; not physiological or physical validation.

For a twice differentiable anatomical aperture x:[0,h]→R with |x''(t)|≤A almost everywhere, exact endpoint apertures x(0)=x0 and x(h)=x1, and independently justified physical acceleration ceiling A, the **sharp pointwise lower envelope** is

L(t) = x0 + (x1-x0)t/h - (A/2)t(h-t).

Proof: subtract the affine endpoint interpolant. The Green-function representation of the zero-endpoint residual, with |x''|≤A, bounds its absolute value by A t(h-t)/2. Equality for all t is attained by x(t)=L(t), whose second derivative is +A. Consequently min x(t)≥min L(t), and the bound is sharp in the unconstrained C^{1,1} class. Let d=x1-x0. For A>0 the minimizer is t*=clip(h/2-d/(Ah),0,h); for A=0 min L=min(x0,x1). A closure defined by x≤c is excluded **only if min L>c**. Equality is not exclusion. With equal endpoints x0=x1=x, the dimensionless criterion is A h²/[8(x-c)]<1 (for x>c).

Unlike E002-683's global range-to-speed law, this is a **finite-window** certificate that does not assume a global trajectory or a velocity ceiling. It does, however, require an *independent hard acceleration ceiling*, endpoint anatomical aperture calibration, and a verified effective blind interval. The extremal parabola may leave the physical aperture range; imposing range constraints can tighten the bound but cannot make this conservative exclusion unsound. Uncertainty in endpoints is handled conservatively by replacing each endpoint with its verified lower bound; uncertain gap length uses its verified maximum. Exposure-integrated pixels are not instantaneous anatomical endpoints.

**Numerical witness:** x0=x1=0.5, h=0.04 s, A=1000 aperture-units/s² yields min L=0.3. At closure threshold c=0.3 this is **NOT** an exclusion. A smaller independently verified A, or smaller effective gap, can permit exclusion. Changing units without transforming A and x invalidates the calculation.

**Locally executed test:** 81 exact-rational parameter configurations, 101 extremal time samples each, zero contradictions; this checks the constructed extremal, not a machine-checked proof. Reproduce using `python research/observability/e002_684_acceleration_gap.py`.

**Falsification and product gate:** before any human claim, independently measure and bound anatomical acceleration under held-out subjects and nuisance regimes (geometry, gaze, illumination, glasses, blur, missingness, exposure/rolling shutter and clock drift). Challenge the bound with synchronized high-speed reference and ordinary-camera downsampling, preserving all failures. The finite-sample maximum acceleration is not a deterministic hard ceiling; absent independently justified A and capture calibration, return `ABSTAIN_UNCALIBRATED`. Physical/human evidence: zero; release BLOCKED. This is a classical interpolation inequality, not claimed as new mathematical priority.
