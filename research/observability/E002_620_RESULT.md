# E002-620 | Exposure-average-aware abstention instrument (2026-11-03)

## Scientific contribution and evidence tier
This run turns E002-619's identifiability counterexample into an executable **conditional decision rule** that refuses to treat exposure averages as instantaneous eyelid apertures. It is a synthetic/analytic instrument, **not** human or physical validation and **not** a new physiological velocity ceiling.

For an absolutely continuous scalar aperture x(t) with certified |x'| <= V, exposure duration T, and certified lower bound m on its temporal mean, the end-of-exposure aperture obeys x(T) >= max(0,m-VT/2). The same applies to the beginning of the following exposure. The bound follows from x(t) <= x(T)+V(T-t) and integration; the affine extremizer shows sharpness when nonnegative geometry permits it. For two exposure averages m1,m2, durations T1,T2, and an intervening exposure-free gap G, define a=max(0,m1-VT1/2), b=max(0,m2-VT2/2). For closure threshold c, a closure in the gap requires V G >= max(0,a-c)+max(0,b-c). Hence **strictly greater** required travel than V G conditionally excludes closure; equality never certifies exclusion.

This calculation assumes a validated linear scalar exposure-average observation, certified measurement lower bounds, an independent global speed upper bound, a common calibrated physical aperture geometry, an upper bound on the *actual* dark gap, and reliable shutter synchronization. No camera pixel intensity is assumed to be a linear eyelid-aperture measurement. Rolling shutters, motion blur, photometric changes, occlusion, gaze, glasses, missingness, uncertain exposure integration and unverified speed bounds force **ABSTAIN_UNCALIBRATED** upstream. The executable returns only a conditional decision; it cannot itself validate its inputs.

## Prospective physical falsification and product gate
1. Independently measure exposure start/end with photodiode/LED instrumentation and bound clock error. A camera nominal FPS is insufficient.
2. Acquire synchronized high-speed human eyelid reference, blinded double anatomical annotations and independently calibrated aperture geometry; freeze participant-disjoint development/test split.
3. Estimate a conservative speed ceiling on independent calibration subjects with a defensible inter-frame acceleration/regularity envelope; a maximum observed finite difference is **not** a certified continuous-time ceiling.
4. Freeze predictions and interval uncertainty budgets before inspecting held-out closure outcomes. Report all abstentions, missed events, false exclusions, participant clusters, and nuisance strata.
5. A trusted reference closure in a gap marked NO_HIDDEN_CLOSURE_CONDITIONAL falsifies at least one model/measurement assumption. A high abstention rate or unstable certificate under realistic nuisance controls blocks product use.

## Reproduction
`python research/observability/e002_620_exposure_certificate.py` runs nine synthetic conditional assertions. No external dependencies or data. Source file: `e002_620_exposure_certificate.py`. These tests do not independently verify physics or the implementation. Existing E002-617 one-frame annotation uncertainty removes all two-sided robust virtual omissions, strengthening the case for calibrated ground truth.

**Release consequence:** default product remains `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. No automatic fatigue/sleepiness diagnosis or blink-absence inference is justified by this certificate.
