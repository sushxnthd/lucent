# E002-389 — preregisterable physical/human falsification protocol

**Status:** prospective protocol only. No participants enrolled, no new video acquired, no ethics approval, no hardware purchased. Synthetic E002-389 results cannot be treated as physiological evidence.

## Claim to falsify
For calibrated exposure-mean *physical eyelid aperture*, the joint shutter-integral LP can issue a sound no-hidden-threshold-crossing decision under valid timing, transfer, and independent Lipschitz bounds. The independent per-exposure envelope should abstain on some intervals the joint LP certifies. Predefine all tolerances before revealing human holdout labels. A no-crossing decision on any reference-confirmed crossing is a decisive counterexample to the claimed deterministic calibration assumptions.

## Stage A — calibrated mechanical/optical instrument (before humans)
Use a programmed occluder or eyelid phantom with externally measured position, adjustable movement profile, neutral illumination, optional glasses-like reflective layer, and synchronized photodiode/LED trigger. Capture the *same* event with a high-speed reference (target >=960 fps, independently measured <=0.5-ms exposure and frame times) and ordinary RGB (target 30/60 fps, raw and H.264, independently measured exposure windows). Use at least two ordinary camera models and two optics/illumination setups. A device's advertised FPS is not exposure calibration. Measure true aperture through the entire exposure using reference interpolation with an independently bounded motion model; when reference itself cannot exclude a crossing, mark UNKNOWN, not negative.

Before test, freeze 100 randomly generated motion programs (including strict threshold crossings and always-open negatives), their phase schedule and predicted LP decisions. Reserve 50 unseen programs for evaluation. Predeclare maximum allowed timestamp drift, optical-response residual, saturation/blur/glare thresholds, and camera-transfer envelope. Repeat with gaze translation, brightness steps, motion blur, glasses reflections, partial occlusion, frame loss, H.264 bitrate changes and rolling-shutter motion. Report every abstention and failure.

## Stage B — human evidence
A proposed 60-person pilot: 30 participants for velocity/optical calibration and 30 untouched participant holdouts, stratified by eyewear, gaze, skin/iris contrast and lighting. Reserve an unseen camera model as a device holdout. Record synchronized ordinary RGB and independently calibrated high-speed reference with timestamps and exposure duration verified by hardware trigger. Predefine consent, privacy handling, secure local storage and a clinical/ethics review appropriate to the jurisdiction. Avoid diagnosis or intervention.

Estimate subject-normalized aperture from high-speed reference with multiple blinded annotators, record inter-rater uncertainty, and propagate reference exposure ambiguity into three labels: confirmed crossing, confirmed absence, unresolved. Calibrate the RGB-to-aperture transfer on *different participants* than those evaluated. The speed limit must be established independently of the test recording; finite empirical maxima are **not** universal deterministic physiological bounds. A statistically estimated speed envelope supports only a calibrated probabilistic claim with explicit failure probability, not a hard guarantee.

## Frozen endpoints and falsification
Primary: false exclusion rate = confirmed reference crossings among intervals where Lucent issued a no-crossing certificate, plus a one-sided confidence interval, stratified by held-out device and participant. Secondary: coverage/abstention fraction, gain in qualified coverage over independent exposure envelopes, error calibration by nuisance stratum, and runtime. A single confirmed false deterministic certificate requires invalidating or narrowing the associated physical assumptions. Unresolved reference intervals must not be counted as correct negatives.

No tuning on held-out sequences. If performance fails under any nuisance stratum, disable certification for that stratum. Preserve raw timing traces, event annotations, optical calibration curves, preregistered predictions, and scripts. Publish anonymized/consented data or a fully specified access protocol.

## Release blocker
No camera or human evidence has yet established the deterministic worst-case optical, velocity, clock or reference adequacy bounds. Therefore deployed Lucent must **ABSTAIN** on hard absence-of-blink/closure claims. The E002-389 product gate is a research scaffold, not a validated detector.
