# E002-629 | Frozen prospective human shutter-gap validation protocol (2026-11-03)

Status: prospective, NOT executed; no human data collected. This is a preregistration-style instrument specification, not evidence of validity. Supersedes no earlier mathematical kernel.

## Primary question
Can a physically calibrated ordinary camera, using independently justified continuous-time eyelid motion bounds, correctly exclude a hidden eyelid closure during exposure-free intervals? Primary endpoint: false-exclusion rate against synchronized reference truth. A single adjudicated false exclusion falsifies the universal certificate under the asserted envelope.

## Acquisition and independence
Record voluntary natural blinks with written informed consent and applicable institutional ethics review. Obtain synchronized reference video at >=240 fps (prefer >=500 fps) and an ordinary-camera stream at 30/60 fps, both with independently measured exposure start/end times. A photodiode/LED pulse train visible to both sensors and an oscilloscope or timestamp logger must measure relative clock offset, drift, frame drops, rolling-shutter row timing and exposure uncertainty. A camera's nominal FPS or metadata alone is insufficient. Preserve raw frames and clock logs; do not use interpolated labels as truth.

Use a motorized aperture/occluder with independently measured encoder trajectory first. Sweep gap duration, exposure duration, motion speed, blur, ambient brightness, and pulse phase. If instrument truth cannot be resolved between reference frames, classify UNKNOWN, never OPEN.

## Human study and locked split
Target at least 30 participants, multiple sessions, >=100 adjudicable blink/near-blink events in the held-out evaluation set; these are planning targets, not a power calculation. Randomize participants into development/calibration and held-out sets before fitting. Never transfer participants, trials, velocity bounds or thresholds from held-out to calibration. Obtain two blinded frame-level anatomical annotations, third-party adjudication of disagreement, and UNKNOWN for occlusion or ambiguous reference truth. Include glasses, gaze shifts, head pose, skin/lighting variation, motion blur and missing frames. Report all exclusions and abstentions by nuisance stratum.

## Predeclared predictions
For each ordinary-camera exposure-free gap, compute conservative lower bounds L0,L1 on instantaneous aperture at the gap endpoints from exposure-integrated observations, calibrated geometric error, synchronization uncertainty, and independently validated continuous-time motion envelopes. Let C_close(t)=integral from gap start to t of certified maximum closing speed, C_open(t)=integral from t to gap end of certified maximum opening speed. For closure threshold q, a hidden closure is excluded only when, for every t in the gap, either C_close(t) < L0-q or C_open(t) < L1-q. Equality is NOT exclusion. All other cases ABSTAIN, not a positive blink detection. If any envelope, endpoint, clock, or anatomical truth calibration is missing: ABSTAIN_UNCALIBRATED.

Freeze the model, bounds, thresholds and code hash before revealing held-out labels. Primary comparison: adjudicated hidden closures among EXCLUDE outputs. Secondary: coverage (fraction EXCLUDE), abstention by nuisance stratum, and false exclusions from naive exposure-average substitution. Give exact binomial confidence intervals for false-exclusion frequency; zero observed failures does not establish a universal bound.

## Calibration and kill criteria
Continuous-time velocity/acceleration envelopes cannot be certified from adjacent video-frame finite differences alone. Validate envelopes on the independent motorized system with faster independent encoder/photodiode ground truth; human physiological transfer requires a separately defensible envelope, not extrapolation from synthetic motor dynamics. A failed timing, endpoint, geometry or velocity assumption blocks the corresponding certificate. Any observed false exclusion under supposedly satisfied assumptions triggers failure investigation and suspension of product exclusion claims; do not quietly tune on held-out subjects.

## Required reproducible deliverables
Publish protocol version, consent/ethics status, hardware schematics, raw clock/exposure calibration, camera settings, raw/derived data manifest with checksums, subject split hashes, annotation instructions, signed prediction table generated before label reveal, scripts for reconstruction and uncertainty propagation, blinded adjudication record, nuisance-stratified results and all negative cases. Protect participant identity and eye video; release de-identified derived measurements only with consent.

## Product decision
Until the physical instrument and held-out human gates pass, no claim that ordinary-camera frames rule out hidden closures. Remain ABSTAIN_UNCALIBRATED; production BLOCKED. Passing an instrument test alone permits only an instrument-calibrated conditional claim, never physiological generalization.
