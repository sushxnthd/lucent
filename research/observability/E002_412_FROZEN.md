# E002-412 — frozen real-human optical-proxy temporal-decimation experiment

**Frozen 2026-10-24 before implementation or execution.** Primary kernel: E002-371 empirical observability. This experiment uses previously verified high-frame-rate S01/S19 human video, not new dataset discovery. **This is an exploratory image-intensity surrogate and does not provide physical eyelid aperture, independently calibrated exposure, or a human blink label.** It must never revive the glare-failed E002-397 optical-flow feature.

## Deterministic inputs and selection
- Reuse E002-407's exact checksum-verified S01/S19 ZIPs, deterministic first two complete EEG-event/control pairs per participant, four 0.5-s clips per participant, and crop `frame[90:220,70:260]`. Do not select clips based on this experiment's optical outcomes. No raw frames, per-clip identifiers, timestamps, EEG labels or event/control mapping in public output.
- Derive a **non-aperture** scalar optical-darkness proxy from the median intensity of top/bottom skin-reference bands versus the 20th-percentile intensity of a fixed central ROI, normalized by skin intensity. Reject frames with insufficient illumination or central saturation. The fixed geometry is a convenience, **not an anatomical measurement**.
- Simulate 15/30/60-Hz instantaneous point-sampling (NOT actual finite camera shutter) at 16 equally spaced phases, using the nearest high-speed synchronized frame within 7 ms; mark an invalid sample as missing, do not interpolate. Use the source's EEG-synchronized timestamps only as an exploratory sampling grid; do not label them independent camera clock.

## Predictions frozen without looking at E002-412 outcomes
- H1: eight selected clips and at least 600 total high-speed frames.
- H2: at least 90% of clean frames are photometrically valid; at least four clips have clean optical-proxy range >=0.02.
- H3: at least one 30-Hz phase/clip combination loses >10% of its high-speed proxy range, showing a phase-sensitive optical-information loss; failure is a valid negative result, not a reason to change thresholds.
- H4: >=95% of jointly valid clean frames have absolute score changes <=0.08 under each fixed gain (0.70, 1.30) and Gaussian blur sigma 2.
- H5: >=95% of frames with a fixed central white glare patch are rejected by the predeclared saturation gate. Glare must never be interpreted as closure.
- H6: all reported 15/30/60-Hz range-capture ratios are bounded [0,1] and all samples use observed source frames without gap interpolation.

## Independent verification and nuisance boundaries
Test deterministic synthetic image controls, invalid-clock/missingness behavior and a separately implemented decimation oracle. Include gain, blur, glare, translation (8 px horizontal/6 px vertical), and sampling phase. Translation has no guaranteed invariant score: report its perturbation, and explicitly reject transfer if >0.08 for >5% of jointly valid frames. Camera clock error, rolling shutter, exposure weighting, gaze, glasses and physical velocity remain **uncontrolled**, so this experiment cannot authorize a no-hidden-closure certificate. A negative result must be retained.

## Decision and privacy
The only allowable scientific conclusion is how a **fixed optical image proxy** changes under temporal point decimation and synthetic nuisances on real high-speed human recordings. EEG marker associations, proxy minima and 30-Hz losses are **not** measured eyelid closure, blink duration or PERCLOS. Regardless of all hypotheses: `ABSTAIN_UNCALIBRATED`. Publish aggregate counts/ratios and reproducible code only; no eye images, raw scores, source clocks, participant-event mapping or private linkages in artifacts.

The decisive follow-up remains E002-407/408 independent blinded human landmark sheets and physical camera/exposure/velocity calibration on untouched participants/devices.
