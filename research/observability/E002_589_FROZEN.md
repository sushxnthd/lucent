# E002-589 | Frozen full-duty exposure-integration aliasing kill test

**Freeze:** 2026-11-01, before implementation or execution. Primary E002-371; parent E002-588. **Evidence tier:** exact synthetic instrument-model falsification, NOT physical shutter calibration or human physiological evidence. Existing branch `research/observability-human-boundary`; draft PR #26.

## Question

Does **zero uncovered shutter time** plus a perfectly known, linear, full-duty exposure-integrating imaging path guarantee that a closed eyelid cannot be hidden in exposure averages? Test a stronger setting than E002-588: perfectly known timing, 100% duty cycle, no rolling shutter, no dropped frames, no response nonlinearity, exact integration, equal known boundary aperture values and equal hard speed ceiling.

## Predeclared worlds and exact predictions

Let one frame period be dimensionless `u in [0,1]`, with observed normalized aperture proxy `Y=integral_0^1 a(u) du`. Threshold for anatomical closure is `tau=1/5`. All frames repeat continuously with equal endpoint values `a(0)=a(1)=1/2`, and a common Lipschitz ceiling `|da/du| <= 4`.

- **World O (open):** `a_O(u)=1/2` throughout.
- **World C (closure):** piecewise-linear interpolation through rational knots `(0,1/2),(1/8,1/2),(1/4,0),(3/8,1/2),(5/8,1/2),(3/4,1),(7/8,1/2),(1,1/2)`.

Freeze predictions BEFORE running code:
1. All 24 consecutive, full-duty frame exposure averages are **exactly 1/2** in both worlds. There are **no uncovered shutter intervals**. Frame-boundary aperture samples also match exactly. Any inequality kills the witness.
2. World C reaches zero at `u=1/4`, has `a_C<=1/5` over the exact interval `[7/40,13/40]` (duration `3/20` of a frame), whereas O never closes. Both have `0<=a<=1` and maximal absolute slope <=4. Any violation kills the witness.
3. Prospective, not used to fit the worlds: a *half-frame* optical exposure over `[0,1/2]` produces `Y_O=1/2`, `Y_C=3/8`; over `[1/2,1]` produces `Y_O=1/2`, `Y_C=5/8`. If these fail, the held-out discriminator is killed.
4. A pre-integration nonlinear sensor `g(a)=a^2` breaks the full-duty equality: O `1/4`, C `7/24`. This is a required nuisance sensitivity control, not a universal non-identifiability claim.
5. A single-sided perturbation to the positive bump (peak 9/10 instead of 1) must break equality. A calibrated hard velocity ceiling `L<3/5` (dimensionless per frame) with verified boundary apertures 1/2 excludes any `a<=1/5` by the elementary two-endpoint Lipschitz envelope; this is a *separate conditional certificate*, not evidence that a real human has such a ceiling.

## Execution and independent verification

Implement exact-rational integration over all knots in Python and an independent JS BigInt rational replay that recomputes all predictions. Include negative controls for timing phase, exposure width, pre-integration nonlinearity, perturbation, aperture bounds, closure interval, velocity threshold and post-integration gain. Retain deterministic aggregate outputs and all failed predictions. No private human data or hardware claims.

## Product and scope

If confirmed, **full optical duty cycle is not itself a certificate that an exposure-integrating image observed or excluded a brief anatomical closure**. Keep `ABSTAIN_UNCALIBRATED` unless the real sensor's exposure-to-aperture observation operator, physical shutter timing, geometry and independently justified human velocity ceiling are authenticated. An exposure-averaged proxy is not an instantaneous endpoint anatomical measurement. A calibrated faster/shorter-exposure capture is a prospective discriminator, not a universal solution. No novelty claim over temporal aliasing, exposure integration or classical sampling theory.
