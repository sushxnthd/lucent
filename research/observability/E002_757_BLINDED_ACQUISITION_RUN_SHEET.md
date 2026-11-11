# E002-757 | Blinded physical acquisition run sheet and preregistered release decisions (2026-11-11 UTC)

**Evidence tier:** prospective human/instrument-validation artifact, not measured data. Extends frozen E002-744 without changing its R>1 decision threshold. Do not use this sheet to claim a physical experiment occurred.

## Acquisition roles and blindness

Operator A builds the shutter/LED and independently timed photodiode/encoder reference. Operator B receives only ordinary-camera frames, calibration constants, and camera timestamps, generates an immutable prediction CSV, and hashes it before A reveals reference event labels. Operator C audits timing, phase coverage and reference sensitivity before unblinding. If only one operator is available, enforce the same order with sealed timestamped files and immutable hashes, and explicitly mark lack of independent blinding.

**Clock requirement:** independently log rising/falling event edges and actual camera exposure windows. Record measured synchronization residual, drift over each run, photodiode bandwidth/threshold, LED driver latency, and shutter transit time. Never use nominal fps or a single camera's frame index as ground truth.

## Locked trial design

Instrument development: 30 fps and 60 fps ordinary camera, >=240 fps reference camera, independent edge logger. Calibrate photodiode pulse-width response and temporal phase coverage with a *separate* pulse source before assigning reference negatives. Hold out a distinct shutter motion program and randomized phases. Run >=100 independently timed closure and nonclosure intervals in the held-out motion program (not 100 adjacent frames from one repeated event). Use a cryptographically logged random seed fixed before acquisition, then freeze the trial order and hash the manifest. A run that lacks measured phase coverage cannot establish detector sensitivity regardless of trial count.

For each event, record a unique event ID, rig/session ID, actual pulse width, intended phase, measured phase, shutter regime, source-clock ID, camera timestamps and exposures, photodiode edge times, photodiode threshold, calibration ID, detector sensitivity status, geometry, illumination, blur, dropped-frame count and clock uncertainty. A detector-negative interval is **UNCERTAIN_REFERENCE** unless the calibrated reference sensitivity applies to that width/phase/condition.

## Prelabel predictions

For each ordinary-camera gap compute conservative endpoint aperture lower bounds l0,l1, a certified (not fitted) upper velocity V, and conservative physical separation D including timestamp and rolling-shutter uncertainty. The deterministic verdict is EXCLUDE only if l0+l1>V D, else ABSTAIN. If any required calibration is missing, return ABSTAIN_UNCALIBRATED. Keep an additional exploratory velocity-fit verdict in a separate column; never substitute it for the certified verdict. Freeze predictions before revealing reference labels.

## Unblinding and primary falsifier

Count every independently confirmed closure within a certified EXCLUDE interval as a falsifier. Do not discard it as tracking failure post hoc. Report the denominator of independently adjudicated EXCLUDE intervals, uncertain-reference counts, session and event clustering, nuisance-specific denominators, and exact confidence bounds at the appropriate independent unit. Negative reference labels are not confirmations unless sensitivity has been independently established. One falsifier blocks the deterministic claim for the affected calibration scope.

## Human feasibility and release

Only after ethical/privacy review and consent, acquire >=20 participants with >=10 entirely held out and >=100 adjudicable held-out blink intervals as the *target*, not a power guarantee. Two blinded eyelid raters plus a third adjudicator retain UNCERTAIN labels. Participant-disjoint analysis, per-session failures and gaze/glasses/illumination/blur/missingness strata are mandatory. Empirical maximum eyelid speed is **not** a certified universal V; without such a bound, the human EXCLUDE verdict is exploratory only. Do not make a zero-risk claim from zero observed failures.

**Release decision:** T2 instrument evidence can support only rig-specific physical calibration; T3 human evidence can support condition-specific statistical performance, not deterministic physiological exclusion absent a defensible velocity ceiling. Until then product ABSTAIN_UNCALIBRATED; release BLOCKED.

## Minimal CSV contract

`event_id,session_id,subject_id,split,condition,ordinary_frame_t0,ordinary_frame_t1,exposure0,exposure1,aperture_l0,aperture_l1,velocity_upper_source,velocity_upper,delta_t_upper,verdict,reference_label,reference_sensitivity_status,reference_phase,clock_error_upper,annotator_disagreement,manifest_sha256`

Allow reference_label values CLOSURE, NO_CLOSURE, UNCERTAIN_REFERENCE; never coerce UNCERTAIN_REFERENCE to NO_CLOSURE. Subject ID is blank for shutter trials. Prediction-side fields and manifest hash must be committed before reference_label is populated.

**Stop condition:** no further synthetic refinement substitutes for physical acquisition; next eligible primary experiment should acquire instrument traces or report the exact physical-resource blocker.