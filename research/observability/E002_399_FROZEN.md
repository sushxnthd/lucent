# E002-399 — Frozen reference-adequacy triage on calibrated aperture intervals
Frozen 2026-10-23 before running the new synthetic instrument. **This is not human-aperture validation.**

## New scientific question
When can a high-speed reference legitimately label a whole interval as *no threshold crossing*, and when can it positively witness a crossing, given uncertain two-rater eyelid separation, exposure integration, camera-clock error, and independently bounded speed? This directly addresses the E002-398 annotation handoff and E002-387 reference-erasure risk. Never equate an EEG marker, a single high-speed negative frame, or an image classifier with physical ground truth.

## Model and precommitted decision rule
Let x(t) be normalized physical eyelid aperture with |x'(t)| <= V, where V is independently bounded on disjoint calibration material. The measured aperture *exposure mean* on frame i lies in [a_i,b_i], shutter is uniform with known duration e_i, nominal center t_i, and combined center/row timestamp error bounded by d_i. The shutter-averaged measurement implies at nominal center
L_i=a_i-V(e_i/4+d_i), U_i=b_i+V(e_i/4+d_i).
Thus a crossing is **confirmed** if any U_i < theta. No crossing is **confirmed** only if the exact minimum over [t_first,t_last] of max_i (L_i-V|t-t_i|) is strictly above theta. Otherwise the reference is **UNRESOLVED**. Equality abstains. These are conditional logical certificates, not population probabilities. The interval starts and ends at the first and last nominal centers; no extrapolation is allowed. Exposure calibration, optical/geometry calibration, timebase, independent velocity, nuisance resolution and sufficient shutter-model evidence are mandatory gates.

## Frozen synthetic stress protocol
Use triangular excursions with baseline 0.85, minimum 0.10, max speed 60 normalized units/s, threshold 0.20; always-open baseline 0.85; and marginal always-open baseline 0.38. Random acquisition phase and independent bounded timestamp perturbations. For each cohort use 200 trials and deterministic seed 399. Compare 30 Hz / 10 ms exposure and 240 Hz / 1 ms exposure and 960 Hz / 0.5 ms exposure; include measurement interval half-width 0.02, time uncertainty 0.1 ms, and 0.5-ms exposure for the marginal open condition. Use a 0.2-second interior window. The actual mean is computed from the true synthetic trajectory by analytic piecewise integration, not center samples.

## Frozen predictions
P1: >=95% of calibrated 240-Hz always-open trials are certified no crossing.
P2: >=95% of calibrated 960-Hz triangular-crossing trials are confirmed crossing.
P3: <=30% of 30-Hz triangular-crossing trials are positively witnessed; no false no-crossing certificates.
P4: marginal always-open at 240 Hz: >=95% certified no crossing with all frames, and >=95% unresolved after dropping every other frame.
P5: missing independent speed calibration or an unresolved glare/blur flag always abstains.
P6: across all cohorts, **zero incorrect certificates** against an independent continuous-trajectory oracle. Unresolved is not scored as a negative.
P7: increasing time uncertainty or measurement uncertainty must never convert a previously unresolved reference to a certified one on identical data.

## Independence and product boundary
The independent checker uses direct trajectory minima and dense interval evaluation rather than reusing the forward/backward envelope implementation. Any discrepancy is a failure. Do not change hypotheses after seeing outcomes; record failed predictions. This synthetic instrument does not supply human annotations, physical shutter calibration, optical mapping or untouched human/device validation. Product stays ABSTAIN_UNCALIBRATED until those prerequisites are independently verified. Never upload private E002-398 linkage.
