# E002-437 — acceleration-bridge human validation handoff

**Status:** preregistered acquisition/analysis protocol, **no new participants enrolled**. This supplements E002-433's physical camera protocol and E002-407's existing two-rater human clips. It does not authorize collection without consent/appropriate ethics and dataset access approval.

## Primary hypothesis and estimands

H1: for held-out participants, the conservative acceleration-conditioned velocity envelope computed from **independently physically calibrated** reference frames covers independently measured high-rate instantaneous eyelid speed whenever the separately stipulated acceleration and localization-error premises hold. Report the count of witnessed violations and the exact assumption violated for each failure; a single violation under independently authenticated premises falsifies the deterministic conditional bridge.

H2: for a **fixed independently measured absolute localization-error envelope**, downsampling from 400 to 200 Hz increases the bound's worst-case penalty for the frozen illustrative A, epsilon setting, whereas moving from 400 to 1000 Hz also increases it. Actual rates/optimal rate must be recomputed from independently measured A and epsilon; do not transfer the toy 424-Hz optimum to humans.

H3: replacing an independently justified A with a training-set maximum acceleration can produce false conditional speed caps on unseen participants. Record this as a **statistical tail failure**, not a theorem counterexample.

## Concrete acquisition and independent calibration

1. First complete the local-only, blinded E002-407 landmark sheets for S01/S19, but label their outputs **pixel-proxy feasibility** only. EEG time is not authenticated camera-exposure time. Keep raw video and rater sheets off public GitHub.
2. Obtain consented adult recordings on a calibrated 400–600-fps lab camera (or approved controlled-access 400-fps 3D eyelid-margin records). Capture raw sensor exposure start/end timestamps, row-readout characterization, clock sync pulses observed by independent photodiode, camera calibration target and scale/geometry uncertainty, and gain/exposure settings. A phone's nominal slow-motion frame rate or video container PTS is not sufficient.
3. Two blinded independent raters mark upper/lower eyelid margins and intervals of visibility uncertainty; convert to physical aperture with externally verified 3D/scale registration and uncertainty. Preserve raw rater disagreement, do not shrink intervals by averaging.
4. Independently characterize \(\epsilon\) from landmark/geometry reference objects and rater disagreement **outside the evaluation participants**. Independently constrain acceleration \(A\) from an external mechanical/physiological model or separately measured calibrated reference, recording its validity domain. A finite observed sample maximum does not prove a deterministic human acceleration cap.
5. Freeze the exact analysis commit, sensor/geometry/clock calibrations, velocity/acceleration hypotheses, nuisance strata and participant split before accessing held-out labels. Reserve whole participants (both eyes, all sessions) for the holdout. Include crossed gaze/head pose, illumination/gain, glasses, blur, missing frames, shutter and clock perturbations; invalidate rather than interpolate failed intervals.
6. On each eligible reference segment, calculate Equation (1) using physical mm, true hardware timing uncertainty, and independently bounded A/epsilon. On a separately acquired denser reference channel, estimate instantaneous velocity with **its own interval uncertainty**, never call finite differences exact instantaneous truth. If the reference cannot resolve a violation, mark `UNRESOLVED`.
7. Use the resulting velocity bound only to make **prospectively frozen** ordinary-camera E002-371 predictions. Adjudicate physical closure against independent dual-rater high-rate reference, with explicit witnessed / conditional-negative / unresolved labels. Count abstentions, unresolved reference intervals, false certificates and participant-level failures separately.

## Minimum sealed artifacts and release blockers

Privately archive raw frame IDs, sensor exposure timing, photodiode trace, calibration hashes with resolvable signed artifacts, physical mm aperture and interval errors, independent A evidence, independent rater sheets, nuisance masks, and the prediction seal. Publicly release only license-permitted deidentified aggregates, frozen scripts and methodological documentation. If no authenticated A or epsilon exists, the **correct output is `ABSTAIN_UNCALIBRATED`**, regardless of how well a synthetic study performs. Require independent measurement-science review before any physical product claim.
