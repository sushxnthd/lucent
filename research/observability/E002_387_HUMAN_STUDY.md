# E002-387 paired-human validation and reference-adequacy protocol

**No human data have been collected or analyzed in E002-387.** Obtain ethics approval, written consent and privacy-preserving storage before recruitment.

## Hardware and physical validation
Use >=960-fps high-speed eye-facing reference with exposure <=0.25ms where feasible, plus synchronized ordinary 30/60-fps RGB. Capture real exposure intervals, row times, missing frames and hardware clock offsets/drift using an LED/photodiode time code. Do not infer timing from nominal FPS. Before human recruitment, record a calibrated moving eyelid phantom with encoder/photodiode ground truth across the threshold. Vary event width, contrast, gain, blur, gaze proxy, glasses glare, brightness and dropped frames. Compare reference video labels to encoder truth; use three labels: CONFIRMED_CROSSING, EXCLUDED_CROSSING and REFERENCE_UNRESOLVED.

## Participant design
Recruit 60 consenting adults. Calibration participants n=40, untouched participant holdout n=10, untouched external-device holdout n=10, with at least two ordinary RGB device models not used in calibration. Record spontaneous blinking for five minutes, voluntary partial closures for two minutes, and controlled gaze/lighting/head motion for two minutes. Repeat across three sessions when feasible. Balance age, glasses, eye morphology and skin tones. No subject overlap across partitions.

## Independent calibration
Two blinded annotators plus adjudicator mark high-speed eyelid aperture with uncertainty intervals. Establish physical transfer error over intermediate apertures. Estimate speed and acceleration distributions using calibration participants only; a sample maximum is NOT a universal physiological limit. Freeze thresholds and code hash before holdout evaluation. Any unqualified participant, device, optical condition or reference timestamp requires abstention. Use device identity and measured exposure intervals, not video metadata alone.

## Prospective E002-371 test
For each ordinary-camera shutter gap, compute admissible hidden-closure interval from independent endpoint-aperture bounds, gap/timing uncertainty and independently qualified V. Predict EXCLUDED, POSSIBLE or UNRESOLVED. Compare with high-speed reference labels only where the reference's own shutter-exposure and optical uncertainty exclude aliasing. Primary endpoint: number of independently verified crossings inside gaps falsely certified EXCLUDED, with exact uncertainty intervals. Report issued fraction, abstention, reference-unresolved fraction and results separately for glasses, brightness, blur, gaze, missingness, device and timestamp shift.

## Falsification / product gate
One verified counterexample to a claimed deterministic exclusion with all prerequisites satisfied invalidates that guarantee. Statistical speed bounds must be marketed only as calibrated risk, never as hard per-event exclusion. Require prospective boundary crossing in human data, independently reproduced device/participant holdouts, robust nuisance controls and reproducible metadata before product claims beyond experimental camera qualification. Unconditional PERCLOS, pupil waveform and five-second fatigue diagnosis remain prohibited.
