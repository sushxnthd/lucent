# E002-644: Instrument-first shutter-gap falsification (2026-11-04 UTC)

## Scope and evidence tier
This is a **prospective physical-instrument protocol**, not acquired data, not an independently calibrated physiological envelope, and not human validation. It supersedes further synthetic grid expansion as the next acquisition task. The E002-371 hidden-closure theorem remains conditional on certified endpoint aperture intervals, a closure-threshold upper bound, a continuous-time eyelid velocity envelope, and the true unobserved interval.

## Predeclared acquisition
Use a blinking LED driven by a microcontroller with an independently timestamped photodiode (or oscilloscope) as a shutter-time fiducial. Record simultaneously using the candidate ordinary camera and the timing reference. Record raw videos, reference waveforms, device model, camera mode, nominal FPS, exposure/rolling-shutter setting, resolution, clock source, temperature where available, and a SHA-256 manifest before analysis. A phone screen animation is **not** a timing reference: refresh scheduling and exposure aliasing can shift its edges.

Pre-register 3 LED pulse widths (shorter than, approximately equal to, and longer than nominal interframe gap), randomized phase relative to frame acquisition, and 30 repetitions per width per camera mode. The reference instrument must resolve each edge to substantially better than the shortest pulse width; otherwise mark that trial uncalibrated. Preserve all failed synchronizations and dropped frames.

## Primary observable and falsification
For each trial, determine a conservative interval [g_lo,g_hi] for the true unobserved camera interval from reference-clock alignment, exposure support and rolling-shutter row timing. Do **not** infer g from container FPS alone. Classify an LED pulse as definitely invisible only if its entire reference-timed support lies outside all relevant row-exposure windows. A pulse visible in a frame despite that certified prediction falsifies the acquisition model. A pulse absent despite a predicted guaranteed exposure falsifies it unless intensity/SNR is below the predeclared detection floor. Ambiguous overlap -> ABSTAIN. Report pulse-width × phase confusion matrices with trial-level counts, and full uncertainty intervals.

## Independent certification and human transfer
The LED test can validate camera timing and missed-event classification, **not** eyelid kinematics. Human transfer requires a separate synchronized high-rate reference, anatomical eyelid-aperture annotation, geometry calibration, and independent bounds on continuous-time motion; high-rate frame differences alone cannot certify these bounds (E002-639). Split by participant before tuning, blind ordinary-camera decisions to reference closures, and report the number of *eligible* independent participants rather than frames. Use E002-643's primary decision rule and nuisance strata (gaze, glasses, lighting, blur, missingness, pose, clock drift).

## Release blocker
Until instrument data, independent physiological calibration, and held-out human evidence exist, product status remains ABSTAIN_UNCALIBRATED / BLOCKED. No inference of sleepiness, safety fitness, or absence of blinks from a camera gap is authorized.

## Data contract
Each trial row must include trial_id, raw_video_sha256, reference_sha256, camera_mode, exposure_interval_lo_us, exposure_interval_hi_us, row_index, pulse_start_lo_us, pulse_start_hi_us, pulse_end_lo_us, pulse_end_hi_us, measured_visibility, visibility_floor, sync_status, exclusion_verdict, and adjudication_notes. Missing reference fields force ABSTAIN. Store negative and invalid trials. Freeze the detector and timing thresholds before inspecting the reference-labeled holdout.
