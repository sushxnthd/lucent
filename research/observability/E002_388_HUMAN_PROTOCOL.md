# E002-388 — physical-camera and paired-human falsification protocol

**No human recordings were collected or analyzed.** The E002-388 H264 phantom is software-only.

## Gate A: independently calibrated moving-eye phantom
Build a non-human eyelid aperture target with externally measured displacement (encoder or high-resolution optical ruler) and programmable 8/20/50/80-ms plateaus. Record with at least two actual 30/60-fps consumer RGB cameras and one >=960-fps reference at exposure <=0.25ms, plus a photodiode/LED timing fiducial. Measure actual start/end exposure times, frame drops, readout rows and clock drift. Physically vary glare/glasses, 0–20 px image-plane motion, gaze-like aperture deformation, light gain, local shadows, defocus, motion blur, codec compression and missing frames in a randomized factorial design. Calibrate intermediate aperture, not just open/closed endpoints. Record whether each qualified RGB exposure detects a true physical plateau and whether open-eye controls produce false closure labels. Pre-register thresholds on separate phantom calibration sequences, then evaluate untouched device, compression and nuisance combinations.

**Prospective prediction:** clean 50-ms plateaus at 30fps/10ms must intersect a full exposure in the timing model; if decoded RGB fails, the failure is optical/algorithmic rather than temporal. Unqualified nuisance metadata must force abstention. The model predicts no guaranteed full exposure for an 8-ms plateau.

## Gate B: paired human validation
After ethics review and written consent, recruit 60 adults: 40 calibration, 10 untouched participant holdout, 10 external-device holdout. Capture synchronized ordinary RGB and calibrated >=960-fps reference with measured shutter/clock uncertainty. Include spontaneous blinks, voluntary partial blinks, glasses, illumination changes, head/gaze motion and real compression. Annotate reference aperture with two independent blinded raters and uncertainty intervals; unresolved reference negatives remain unresolved. Derive velocity/acceleration and optical calibration using training participants only. A sample maximum is not a universal physiological bound.

## Frozen evaluation
Before any holdout is opened, freeze code SHA, thresholds, device calibration, the E002-371 hidden-closure interval calculator, nuisance domain and the primary outcome. For every ordinary-camera shutter gap, predict EXCLUDED, POSSIBLE or ABSTAIN using independently calibrated physical endpoint bounds and actual exposure timing. A verified crossing in a qualified EXCLUDED gap falsifies the hard certificate. Report issued fraction, false exclusion count with exact binomial interval, false closure detections, abstention, reference-unresolved rate and performance by glasses/gaze/blur/brightness/geometry/codec/device. Keep the product in research-only mode until external replication and independent review.

## Release blocker
No public hard no-hidden-closure, PERCLOS, pupil-waveform or five-second fatigue claim without physical phantom calibration, human participant/device holdouts, validated reference labels, adversarial nuisance testing and an independent reproduction. This study design is not evidence that those gates have been passed.
