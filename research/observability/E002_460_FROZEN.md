# E002-460 FROZEN — exposure-centroid reachability for a dark shutter gap
Date: 2026-10-26. Frozen before instrument execution or outcome inspection.
Status: conditional mathematics + synthetic validation only; NOT a physical human calibration.

## Question
E002-458 uses a conservative shutter erosion that may reject valid conditional exclusions. Can a shutter-averaged *anatomical aperture* observable recover a sharp dark-gap exclusion under directional velocity caps, and does it change the hypothetical 240-fps conclusion?

## Model and scope
Let continuous anatomical aperture a(t)>=0 mm obey -C<=da/dt<=O with C,O>0 mm/s. A closure witness is a(tau)<=c mm at a time tau strictly between nonoverlapping shutter supports [l0,r0] and [l1,r1]. Each measured value m_i is the *linear, calibrated shutter-weighted mean of anatomical aperture* over a known nonnegative normalized kernel k_i, with temporal centroid mu_i. This is NOT generally the output of a nonlinear landmark detector or pixel intensity average. No sensor saturation, exposure-dependent visibility bias, geometry change, missing frames, or uncertainty is permitted in the sharp theorem; those conditions force abstention. Require m0,m1>c, l0<=r0<l1<=r1, mu0 in [l0,r0], mu1 in [l1,r1], and C,O>0.

## Frozen necessary-and-sufficient prediction
A dark-gap closure is feasible iff the interval
  [max(r0, mu0+(m0-c)/C), min(l1, mu1-(m1-c)/O)]
has positive interior (with equality to r0/l1 interpreted as a support-boundary witness, not a strictly hidden dark-gap witness).
For non-boundary cases, equivalent intersection with (r0,l1) is nonempty. Equality of the directional timing bounds at an interior tau permits a closure. Derive necessity from the maximal closing/opening cone and linearity of exposure averaging. Construct a sufficient witness using a(t)=c+alpha*C*(tau-t) before tau and a(t)=c+beta*O*(t-tau) after tau, with alpha=(m0-c)/(C*(tau-mu0)), beta=(m1-c)/(O*(mu1-tau)); both in [0,1].

Predeclared illustrative test: c=2 mm, m0=m1=3 mm, C=567.103928 mm/s, O=274.616337 mm/s (published calibration sample maxima treated as HYPOTHETICAL caps, never physical hard limits), shutter centroids at 0 and 1000/240 ms, centered uniform exposures of width 2 ms. Predicted: no dark-gap closure, because 4.166667 ms < 5.404789 ms; previous conservative shutter erosion returns NOT_EXCLUDED at exposure widths >= about 2.177 ms, whereas sharp linear-average law still excludes *dark-gap* closure. For an illustrative 6-ms center separation with 2-ms exposures, a constructive hidden closure must exist. Also test equality at the exact critical gap, asymmetric exposure kernels, changing support width with fixed centroids, and cases where shutter support itself removes the feasible crossing region.

## Independent falsification and controls
1. Python implementation returns a feasible crossing witness or EXCLUDED_CONDITIONALLY, never PHYSICALLY_CERTIFIED.
2. Independent JavaScript algebra and deterministic random piecewise-linear witnesses verify the exact mean identities and derivative bounds; use distinct implementation logic.
3. Adversarial controls: clock centroid perturbation, incorrect kernel normalization, overlap, missing exposure support, unknown nonlinear camera observable, unknown mm scale, rolling shutter, nuisance flags, invalid C/O, and exposure-masked closures. All must abstain rather than certify.
4. Test monotonicity under expanding uncertainty (conservative interval arithmetic only); reject falsely precise centroids.
5. Preserve negative results and every failed test. No real human measurements are added. Do not infer physiology from published sample maxima.

## Product and priority gate
If supported, narrow E002-458's shutter-fragility statement to its conservative surrogate: that surrogate loses an exclusion, not necessarily the exact dark-gap exclusion for linear anatomical exposure means. Product remains ABSTAIN_UNCALIBRATED because ordinary cameras do not directly return linear mm aperture averages and velocity sample maxima are not universal bounds. Literature priority: this is a direct bounded-derivative cone/reachability calculation and Jensen-like linear averaging, not a novel general theorem. Continue pursuing prospective independent high-rate anatomical reference trajectories. S21/S22 remain sealed; Hush separate.
