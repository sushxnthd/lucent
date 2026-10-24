# E002-410 — executable human shutter-gap validation protocol (not yet conducted)

**2026-10-24. Evidence tier:** prospective study design, not human physical-aperture evidence. This is the concrete follow-up to E002-371, E002-407/408 and E002-410. No participant recruitment, annotations or hardware calibration are claimed.

## Target and units

Primary estimand: for each 30-fps exposure gap, whether a physical eyelid closure (normalized vertical aperture <= prespecified threshold) occurred between exposures, with high-speed reference frames and all uncertainty retained. **Unit of calibration is an independent participant/session maximum of physical eyelid velocity**, not thousands of within-person frames. Separate a *witnessed closure* from an *unobserved closure*: reference video can positively witness closure; absence of sampled closure does not prove physical absence without its own calibrated reference error envelope.

Freeze one aperture threshold (0.20 in calibrated iris-scale units), anatomical measurement plane and shutter-gap boundary before inspecting held-out participants. Do not train or retune a detector on the held-out set. Maintain three labels: witnessed closure, independently certified no crossing, and reference unresolved.

## Acquisition / calibration checklist

1. **Recruitment:** consented adults; prespecify participant-level train/calibration/test disjointness, diverse gaze/glasses/brightness conditions. No medical claims. Never release identifiable eye images without specific consent.
2. **High-speed reference:** >=240 actual frames/s (nominal 240-fps video metadata alone is insufficient). Independently measure real exposure start/end, rolling-shutter readout, temporal weighting, dropped frames and hardware clock drift. A borrowed laboratory high-speed camera with exposure documentation is preferable. Smartphone slow-motion footage without independent timing is exploratory only.
3. **Ordinary camera:** >=30 actual frames/s, log or measure each exposure interval and shutter weighting, rolling-shutter row offsets and clock uncertainty; verify both cameras with a common visible, externally timed optical pulse sequence. A display animation of unknown scan timing is *not* independent timing calibration. If no independent optical timebase is available, fail closed and label timing uncalibrated.
4. **Reference geometry:** two blinded raters trace upper and lower eyelid margins at the same physical column and normalize by independently calibrated anatomical scale. Require explicit landmark uncertainty, contour curvature, pupil/gaze variation, glasses and occlusion flags. Keep rater sheets separate and immutable until adjudication. Report inter-rater agreement before any threshold comparison.
5. **Velocity envelope:** a sample maximum cannot be called a hard physical bound. Use a separately justified physical bound with traceable instrumentation for deterministic certificates; otherwise restrict to *marginal participant-level statistical rank* claims under an independently reviewed exchangeability assumption. The reference camera itself also has inter-frame blind spots, so certify negatives only if reference error permits them.
6. **Integrity:** checksum original videos, log independent exposure and synchronization uncertainty, retain a private participant/event mapping, and publish deidentified numeric trajectories, code, preregistration and aggregate outcomes where consent permits.

## Frozen validation and controls

For each held-out ordinary-camera gap, issue one of `CONFIRMED_NO_CROSSING`, `POSSIBLE_HIDDEN_CLOSURE`, `ABSTAIN_UNCALIBRATED` **before revealing the high-speed reference labels**. The product may emit the first label only with independently authenticated deterministic physical calibration; conditional rank results must be marked research-only and never use that label.

Nuisance conditions: camera pose/geometry, illumination gain and saturation/glare, missing frames, motion blur, gaze, glasses, timestamp jitter, exposure-kernel error, rolling-shutter row skew, optical inversion, and cross-camera clock offset. Randomize nuisance order within participant; hold out at least one device and at least one participant; report all abstentions and all erroneous certificates separately, with participant-clustered confidence intervals. An error under any preregistered critical nuisance rejects the relevant physical product observable; no post-hoc threshold rescue.

## Sample-size and interpretation constraints

For `n` exchangeable participant-level maximum velocities and `m` *future participant maxima*, `P(any future max exceeds calibration max) <= m/(n+m)`. A 20-participant calibration set yields at best **4.76% marginal risk for one future participant** and **33.33% for a batch of ten future participants**. A 5% family-wise bound for ten future participants requires at least **190 independent calibration participants**, not 190 frames. These bounds do not include aperture, optical, camera timing or reference errors, and are not conditional-on-calibration guarantees.

Stage 1 (no-cost feasibility): existing 8 blinded S01/S19 clips / 632 frames, two independent raters, E002-408 adjudication. These **two participants cannot validate a 5% participant-level calibration claim**; their role is annotation reproducibility and optical-reference feasibility. Stage 2 (borrowed/partner equipment): 20+ distinct calibration participants and an independently held-out participant for a single-session pilot; if external equipment or raters are unavailable, stop at bounded synthetic/instrument validation and keep physical outputs abstained. Stage 3 (independent replication): prospective unseen-device and unseen-participant evaluation, with sample size calculated from desired *batch* risk, nuisance strata and statistical power.

## Analysis / release gate

Publish (a) witnessed-closure recall conditioned on reference quality, (b) false no-crossing certificates / eligible gaps, (c) abstention fraction and its stratification, (d) agreement and uncertainty between raters, (e) errors under each nuisance and unseen device, and (f) exact acquisition metadata. Zero observed false certificates in a small sample is not proof of zero risk. Include negative results and reject transfer claims that fail nuisance gates.

**Until all physical calibration and human-reference requirements are met: `ABSTAIN_UNCALIBRATED`.** Do not infer blink duration, PERCLOS, or fatigue from image-motion energy (E002-409 failed glare transfer).

## Scientific priority
Participant-level exchangeability and finite-sample rank calibration are established conformal-prediction ideas, not a new theorem. See https://doi.org/10.1145/3736575. Novelty, if any, must come from independently replicated, quantitatively sharp shutter-gap measurement limits under realistic camera and human nuisance.
