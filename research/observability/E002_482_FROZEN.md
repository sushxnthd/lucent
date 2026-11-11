# E002-482 FROZEN — exposure-integrated aperture alias and spatial nuisance witness

Date: 2026-10-27. Kernel: E002-371. Status: preimplementation, synthetic moving-aperture instrument experiment. **No physical or human data.**

## New question
E002-371's conditional shutter-gap criterion assumes calibrated instantaneous endpoint apertures. Test whether an *exposure-integrated camera signal* can be silently substituted for such an endpoint measurement, and whether spatial pixels and independently calibrated nuisance parameters can resolve the ambiguity. This is a new acquisition-model falsification, not a revision of the E002-481 phase-island theorem.

## Frozen worlds
Period T=1000/30 ms, global shutter exposure E=20 ms, baseline aperture a0=1 mm. World S has a(t)=1 mm. World M has a(t)=1+f(t) mm for t in [0,E] and 1 mm outside, repeated every frame, where f is piecewise linear through (0,0), (E/4,+1), (3E/4,-1), (E,0). Both are nonnegative, have identical exposure boundary apertures, and |da/dt|<=200 mm/s. World M closes fully at t=15 ms. A calibrated *linear scalar exposure-average aperture sensor* should report exactly 1 mm in both worlds on the global-shutter row. This does not assert that a camera's pixels are linear aperture sensors or that this motion is a natural human blink.

## Independent spatial witness and controls
Use an ideal blurred moving boundary pixel response B(y,a,sigma)=Phi((a-y)/sigma), with y from -1 to 3 mm in 0.1-mm steps and Phi the standard normal CDF. Integrate exactly over the piecewise-linear trajectory. Predict that a spatial image is **not identical** to the stationary world under calibrated gain and blur. Fit one global affine brightness mapping (gain and offset) by ordinary least squares to test nuisance-induced overlap, and compute its maximum absolute pixel residual. With independent per-world per-pixel bounded error epsilon=0.01, residual <=0.02 establishes *existence* of observational overlap, not a measured noise distribution.

Frozen predictions:
1. Exact global scalar mean equality despite one fully closed moment; speed cap 200 mm/s is a **hypothetical** bound.
2. A rolling row offset +2 ms yields scalar mean 0.98 mm in M versus 1 mm in S; +5 ms yields 0.875 mm versus 1 mm, if actual row timing is independently known.
3. At blur sigma=0.2 mm, calibrated-gain spatial maximum difference exceeds 0.02; therefore the two *specific* worlds are distinguishable under bounded 0.01 errors.
4. At sigma=1 mm, the affine brightness-fit residual is below 0.02, providing a constructed overlap certificate even with all 41 spatial pixels.
5. At sigma=2 mm, affine-fit residual is below 0.002. Do not generalize this to all camera images, gain priors or blur kernels.
6. Unknown blur, gaze/geometry, occlusion, dropped rows, brightness/gain, shutter shape and clock offset require explicit abstention. A scalar exposure average must never be promoted to an instantaneous anatomical aperture or hidden-closure exclusion.

## Verification and kill rules
Implement standard-library executable simulator, exact piecewise integration for the scalar channel, independent numeric time quadrature for the spatial channel, deterministic aggregate and adversarial tests. Test zero/negative invalid geometry, row shifts, blur monotonic examples, strict error-overlap criterion, and a sharp-optics negative control. If the spatial model distinguishes both worlds under the frozen affine/noise configuration, record falsification rather than changing the constants. This is a **synthetic acquisition substitute**, not physical shutter or human validation. The product remains ABSTAIN_UNCALIBRATED.
