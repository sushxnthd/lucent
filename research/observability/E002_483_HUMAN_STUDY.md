# E002-483 PHYSICAL HANDOFF — blinded shutter and human validation protocol

**Date:** 2026-10-27. **Status:** prospective protocol, not executed. **No new human data or hardware calibration.** This is a feasibility pilot, not a population-wide physiological bound or medical study.

## Instrument-first gate (must pass before people)
1. Independently measure *actual* shutter transmission versus time and sensor row using a pulsed LED, photodiode and separate clock/logic capture. Log raw pulse edge times, frame IDs, dropped frames, exposure integration, clock drift, rolling-row offsets, phase jitter, saturation, optical gain and detection floor. Do not infer an exposure kernel from FPS metadata.
2. Independently actuate a moving slit/aperture with encoder or optically timed reference. Include stationary, hidden-closure, near-boundary, out-of-plane and adversarial brightness/blur cases. Blind the analysis to the reference waveform until all predictions are written to immutable files.
3. Run E002-483's *two separately timed 10-ms gates* only on a genuine two-gate instrument. Ordinary RGB frame outputs cannot be relabeled as complementary gates. Verify that per-gate gain drift <=10%, combined offset/noise <=0.03 mm-equivalent, and common phase error <=2 ms are **measured bounds**, not convenient defaults. Otherwise this particular contrast certificate is inapplicable.
4. Test at least 100 independent randomized phase/gain/blur conditions, with phase held out from calibration. Reject the instrument model on any confident reference contradiction. Log all rejected/missing trials and preserve raw data and software commit hashes.

## Human pilot, subject-disjoint and blinded
Only after appropriate local ethics review and informed consent, recruit 24 adults for a feasibility pilot (12 calibration, 12 held-out, split by participant before recording). Do not recruit minors or make fatigue/medical diagnoses. Aim for >=30 naturally occurring or voluntary blink trials per participant, randomized across lighting, gaze and glasses strata, without implying this sample supports a universal speed maximum.

Record an independently timed >=400-fps anatomical eyelid reference where available, together with the target ordinary-camera stream (30/60/120/240 fps where genuinely acquired). Use independently recorded LED synchronization, shutter-phase calibration, source frame IDs and a documented pixel-to-mm geometric calibration. A downsampled 400-fps reference is **not** a substitute for independently measured 30-fps shutter/exposure behavior. Annotate upper/lower lid margins, uncertainty, full-closure timing and missingness by two blinded annotators; resolve disagreements under a prespecified protocol.

**Freeze predictions before opening reference labels:** per interval, store `EXCLUDED_CONDITIONALLY`, `POSSIBLE` or `ABSTAIN_UNCALIBRATED`, the assumed velocity bounds, shutter kernel/row, endpoint interval uncertainty, nuisance bounds and all software versions. In human subjects, a finite calibration-sample maximum is NOT a hard speed bound. Therefore any exclusion that relies on such a maximum remains conditional and cannot authorize physical absence-of-closure claims.

## Minimum record schema
`participant_id, trial_id, split, consent_provenance, device_id, independent_reference_device_id, nominal_fps, measured_frame_edges_ns, shutter_row, shutter_kernel_file, pulse_log_file, clock_offset_ns, clock_uncertainty_ns, gain_bounds, offset_bounds, blur_bounds, gaze_condition, glasses_condition, geometry_calibration_id, missing_frame_mask, raw_video_sha256, reference_trace_sha256, reference_annotation_uncertainty, prediction_json_sha256, blinded_label, adjudication_reason`.

## Primary endpoints and kill criteria
- **Primary:** count of independently confirmed closures in intervals the *conditional model* excludes, stratified by independently verified assumption satisfaction. One such event falsifies the joint model or its calibration and triggers `INVESTIGATE`; do not suppress the trial.
- **Secondary:** fraction abstained, interval coverage and calibration errors, separately by subject and nuisance stratum; report participant-clustered uncertainty, not frame-iid confidence intervals.
- **Negative controls:** phase jitter beyond budget, unmeasured shutter tail, saturated LED, blur beyond bound, gain drift above bound, glasses occlusion, gaze change, dropped reference frame, missing anatomical annotation, and intentional mismatched frame IDs. Each must cause rejection or abstention, never an unqualified exclusion.
- **Stop/revise:** any unmodeled reference contradiction, unreliable clock synchronization, or calibration evidence weaker than the declared budget.
- **Allowed product outcome:** only instrument-specific, calibrated, assumption-qualified measurements with explicit abstention. No blink-duration, PERCLOS, fatigue, diagnostic or safety guarantee until separately validated.

## Public evidence triage
- FaceBase high-speed synchronized eyelid trajectories (released 2026-09-01): https://doi.org/10.25550/88-28BJ ; **restricted access**, not acquired.
- TEyeD eyelid segmentation/landmark dataset: https://arxiv.org/abs/2102.02115 ; high-frame-rate anatomical shutter/clock provenance for this specific test not established.
- MPEblink public event-detection videos: https://doi.org/10.5281/zenodo.7754768 ; not a calibrated anatomical high-speed ground truth.
- OpenEDS 200-Hz eye images: https://arxiv.org/abs/1905.03702 ; access upon request, not acquired.

All evidence tiers must remain separate. Do not claim any public human sequence was processed in E002-483.
