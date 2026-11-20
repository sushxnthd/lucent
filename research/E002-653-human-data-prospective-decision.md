# E002-653: prospective human-data acquisition decision (2026-11-05 UTC)

Evidence tier: **source triage and preregistered acquisition decision only**. No frames downloaded, no human prediction scored, no independent timing calibrated. This is NOT empirical validation.

## New lead with direct relevance

**OpenEDS (Garbin et al., 2019)** reports synchronized eye-facing video at **200 Hz**, 152 participants, and a subset of **91,200 frames of 1.5-second sequences**. Primary description: https://arxiv.org/abs/1905.03702 . Dataset access was described as **upon request** via the OpenEDS challenge. It is a candidate, not confirmed accessible or suitable: the paper's 200-Hz sampling statement alone does not certify per-frame exposure timing, timestamp uncertainty, or that sequences contain enough complete blinks for independent velocity calibration and held-out testing.

**GazeBase (Griffith et al., Scientific Data 2021)** has 1000-Hz eye-tracker samples, but provides gaze/pupil-area/missingness rather than independently calibrated palpebral-aperture image trajectories; its missing samples cannot be equated with eyelid closure. https://doi.org/10.1038/s41597-021-00959-y . Reject as direct validation of the shutter-gap/eyelid-aperture theorem unless paired aperture ground truth is independently recovered.

**mEBAL** includes 3000 annotated blink events with 19-frame windows (~600 ms), i.e. approximately 30-Hz temporal resolution, and requires a license-request workflow. https://github.com/BiDAlab/mEBAL . It can assess ordinary-frame detection, but cannot independently identify fast eyelid velocity extrema. Reject as high-speed velocity ground truth.

## Frozen prospective test, before inspecting any validation trajectories

1. Obtain original high-rate sequence, acquisition FPS and timestamp/exposure metadata, consent/license, camera geometry, and whether each clip actually spans full closure. Preserve source hashes and subject/clip IDs. Do not assume constant frame interval from nominal FPS.
2. Split **by subject** before calibration. Estimate an upper velocity bound V from high-rate aperture annotations in calibration subjects only, with annotation uncertainty, geometry and scale conversion, timing jitter and exposure blur included. A sampled maximum is NOT a certified upper bound: report an empirical tolerance bound with stated coverage/confidence, or abstain from a deterministic guarantee.
3. For each held-out sequence, simulate low-rate cameras using integration over measured exposure windows (not point sampling). Perturb FPS, exposure phase, timestamp drift, dropped frames, gaze, pose, illumination, glasses, segmentation uncertainty, and motion blur. Declare a closure only when independent high-rate human annotations meet a prespecified closed-aperture threshold over a nonzero interval.
4. Evaluate the E002-371 gap rule on the **observable open endpoints** and the independently calibrated V. Label a gap CERTIFIED_NO_HIDDEN_CLOSURE only when the theorem's conservative inequalities hold for all allowed timing/measurement intervals; otherwise ABSTAIN_POSSIBLE_HIDDEN_CLOSURE. Never infer closure from abstention.
5. Primary falsification endpoint: count independently verified complete closures in gaps labelled CERTIFIED_NO_HIDDEN_CLOSURE, stratified by nuisance. Any such event invalidates the applied certificate or one of its assumptions. Secondary: abstention fraction, coverage, timing sensitivity, and subject-bootstrap intervals. Preserve all failures, not just aggregate accuracy.
6. Run an independent implementation of the inequalities and a separate human-annotation adjudication process. Report calibration/test subjects, exposure settings, and exact unseen-condition partitions before viewing outcomes.

## Fallback if high-speed video cannot be obtained

After the second documented access attempt, implement a physically timed programmable occluder / printed-eye aperture rig with independently logged motor position and LED/photodiode exposure synchronization, including clock uncertainty and rolling-shutter distortion. This can validate the **instrument and timing logic**, not biological eyelid-velocity assumptions. A prospective human protocol must then enroll consenting adults, use high-speed reference imaging plus ordinary phone imaging under synchronized illumination, preregister participant-level splits and nuisance conditions, and obtain appropriate ethics/privacy review before acquisition.

## Product consequence

Keep `ABSTAIN_UNCALIBRATED` and production `BLOCKED`. A nominal 200-Hz dataset citation or ordinary 30-Hz blink labels cannot unlock a phone-camera claim. Only independently calibrated timing, aperture velocity, held-out falsification and a stated uncertainty regime can support a bounded no-hidden-closure certificate.
