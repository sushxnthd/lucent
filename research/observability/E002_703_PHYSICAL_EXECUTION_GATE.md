# E002-703 — Physical acquisition execution and falsification gate (prospective; no measurements)

**Evidence tier:** executable-study design, not instrument or human validation. This document is a prospective acquisition contract for E002-690 and E002-695. Do not claim that any trial has been run.

## Instrument configuration

Use an opaque translating occluder over a calibrated backlit aperture (not a human eyelid), with a fixed high-speed reference camera or photodiode, a separate ordinary rolling-shutter camera, and a common observable LED timing pulse in both channels. Preserve raw files and clock-domain metadata. Measure aperture-to-pixel geometry against a ruler or calibration target. The high-rate reference must resolve each imposed closure duration by at least five independently timestamped samples; if it does not, mark that trial **reference-indeterminate**. Do not infer timing from container nominal FPS.

Record an independent occluder displacement trace, using a ruler/encoder or calibrated high-rate images, to bound maximum velocity **before** ordinary-camera prediction. Estimate uncertainty from repeat calibration and reference quantization; never fit velocity ceilings on test closures. Verify shutter exposure start/end for the actual eyelid ROI row: rolling shutter makes frame timestamps alone insufficient. Measure the LED pulse row offset, camera clock drift, missing frames and maximum inter-exposure blind gap, including their conservative error bounds. If the LED cannot be resolved, abstain.

## Frozen experimental contrasts

Randomize gap phase relative to occluder motion; block by (i) low/high speed, (ii) short/long closure, (iii) near/far aperture, (iv) bright/dim, (v) blur, (vi) ROI row, (vii) frame drops. Reserve entire randomized blocks as held-out, and do not tune on them. Capture at least 20 valid physical trials per cell as an initial feasibility target, **not** a powered human safety claim. Include negative-control trials with no closure and positive controls with a known closure inside a camera blind gap. Record reference-indeterminate trials, not just successful captures.

For each low-rate observation, write calibrated aperture lower/upper intervals and an exposure-aware observation model. Freeze all low-rate predictions, input provenance, nuisance stratum, software version, and SHA-256 before opening the high-rate closure labels. Use E002-695 for prediction locking; extend it rather than bypassing provenance checks if the exposure-mean certificate is evaluated. Run the original E002-371 instantaneous-endpoint certificate only when actual instantaneous endpoint calibration is justified. Otherwise use the conservative exposure-aware E002-694 rule or abstain. Never substitute pixel brightness or landmark openness for anatomical aperture without independent calibration.

## Primary preregistered outcomes

1. **False exclusion:** any certified 'no hidden closure' whose independently labelled reference minimum crosses the preregistered closure threshold, after reference uncertainty is considered. One unequivocal false exclusion falsifies the operational certificate under its stated calibration.
2. **Abstention fraction:** report across *all* attempted trials and by nuisance stratum, including invalid calibration and reference-indeterminate cases.
3. **Certificate yield:** fraction of valid reference-determinate trials with certified exclusion; report Wilson intervals and raw numerators/denominators, not a population safety guarantee.
4. **Calibration coverage:** verify that observed true aperture, speed, and blind-gap values remain inside frozen uncertainty envelopes. Any violation invalidates certificates relying on that envelope, regardless of outcome.
5. **Prediction boundary:** plot certificate margin versus dimensionless gap-speed-to-aperture margin, separately for rolling-shutter row, exposure, and timing-uncertainty strata.

## Human transfer

Only after the physical gate passes, recruit consented participants with varied gaze, eyelid geometry, glasses, skin/illumination conditions and camera positions. Calibrate physiological velocity on development participants; freeze a *conservative upper envelope* and its coverage target before participant-disjoint testing. Obtain two blinded independent anatomical raters and adjudicate disagreement without inspecting the low-rate predictions. Report participant-level clustered uncertainty, not frame-iid intervals. No deterministic human certificate is permitted if velocity-envelope coverage is not defensible.

## Stop/release gates

No physical data => **instrument validation absent**. No independent velocity bound => **ABSTAIN_UNCALIBRATED**. Any clock/geometry/exposure calibration failure => **abstain**. Any unequivocal false exclusion => **stop and investigate**. Physical success alone never authorizes a human or sleep/fatigue claim. Production remains **BLOCKED** until independent replay, participant-held-out human validation, nuisance tests, priority audit, and external review.

This artifact intentionally contains no fabricated acquisition, numerical results, or claims of human evidence.
