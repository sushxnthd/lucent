# E002-704 — Human transfer preregistration and acquisition manifest (prospective)

**Evidence:** protocol only. No participants recruited, no recordings acquired, and no velocity ceiling validated. This is not a continuation of synthetic efficacy sweeps.

## Primary estimand and admissible claim

For each ordinary-camera blind interval, decide **CERTIFY_NO_CLOSURE** only when an independently calibrated lower bound on the *continuous-time anatomical palpebral aperture* exceeds a frozen subject-independent closure threshold. Otherwise **ABSTAIN**. A missed closure is a critical falsification, not a classification error to average away. A zero observed miss count does not prove zero population risk.

## Recruitment, consent, and acquisition

Recruit consenting adults only initially; no sleep-deprivation induction and no medical diagnosis. Target at least 30 development and 30 entirely unseen test participants, with recruitment spread across glasses/no glasses, different eyelid geometries, gaze directions, illumination, and camera distances. This is a feasibility target, not a powered safety demonstration. Record consent, withdrawal, camera/firmware versions, privacy retention and de-identification plan. Do not publish identifiable eye videos without explicit permission.

Acquire synchronized >=200 Hz high-speed eye video *and* ordinary-rate phone video, plus a shared flashing timing target visible to both systems. Retain raw frame timestamps, actual exposure durations, rolling-shutter row positions, dropped-frame logs, and a calibration target. Verify that reference sampling resolves closures; otherwise label reference-indeterminate. High-speed nominal FPS alone is insufficient.

## Anatomical reference and velocity envelope

Two blinded raters independently annotate upper/lower lid boundaries at high rate, using calibrated physical units or a documented dimensionless eye-geometry normalization. Adjudicate discrepancies while blinded to low-rate certificates. Construct interval-valued aperture trajectories that include annotation, geometry, blur and sampling error. Estimate an *upper* eyelid-speed envelope exclusively on development participants, including uncertainty between reference frames (not just finite-difference point estimates). Hold out participants, not frames. If physical scale or maximum speed cannot be bounded independently, no deterministic certificate is admissible.

## Frozen prediction sequence

1. Freeze participant IDs and train/test partition before viewing held-out reference labels. Record a SHA-256 manifest of raw-file hashes, software version, thresholds, nuisance strata and exclusion rules.
2. On development participants only, calibrate camera-specific aperture measurement uncertainty, velocity ceiling, clock drift, shutter row/exposure uncertainty and the closure threshold.
3. For each held-out low-rate interval, compute conservative maximum blind gap and interval-valued exposure-aware aperture inputs. Reject brightness-only and landmark-only surrogates without independent anatomical calibration.
4. Execute E002-695 prediction locking, recording **CERTIFY_NO_CLOSURE**, **ABSTAIN**, or **INVALID_CALIBRATION**, plus reason codes and frozen digest. No held-out reference label may enter the prediction file.
5. Reveal high-speed reference labels only after the prediction digest is archived. Evaluate all attempted trials, including failed acquisition, missingness and indeterminate reference, with separate denominators.

## Nuisance challenges and unseen-condition predictions

Stratify by illumination, glasses, gaze, geometry, blur, camera motion, rolling-shutter row, frame drops and clock drift. Randomize ordinary-camera phase relative to spontaneous blinks where feasible. Preregister two falsifiable predictions: (a) certificate yield must decrease or remain unchanged when any uncertainty envelope is conservatively widened, with identical observations; (b) no certificate may survive when its calibrated lower bound reaches the closure threshold. Verify these software monotonicity properties separately from human validity. Test one unseen camera model only after the participant-disjoint evaluation; expect abstention absent new camera calibration.

## Primary analysis and stopping

Report (i) number of unequivocal false exclusions, (ii) total certified intervals, (iii) attempted intervals and abstentions, (iv) participant-level counts, (v) uncertainty-envelope violations, and (vi) results by nuisance stratum. One unequivocal false exclusion or calibration-envelope violation immediately blocks operational certification and triggers root-cause analysis. Report exact binomial upper confidence bounds only as descriptive interval-level summaries; intervals within a participant are dependent, so use participant-cluster bootstrap or participant-level sensitivity analysis. Even zero failures among N certificates does not establish a deterministic physiological speed ceiling or deployment safety.

## Minimal machine-readable trial manifest

Each row: participant_pseudonym, session_id, device_model, camera_firmware, acquisition_clock_id, high_rate_file_sha256, low_rate_file_sha256, exposure_start_interval, exposure_end_interval, roi_row, frame_drop_count, aperture_scale_interval, aperture_error_interval, speed_ceiling_source, clock_error_interval, shutter_gap_upper, closure_threshold, nuisance_tags, prediction_file_sha256, reference_status, adjudication_status. Preserve a versioned data dictionary and an immutable train/test partition file.

## Release boundary

Instrument-only evidence cannot justify a human claim. Human observations without a defensible independently established maximum velocity cannot justify a deterministic no-closure certificate. Neither blink detection nor closure exclusion alone supports fatigue, sleep-stage, or sleep-quality measurement. Until independent replay, priority audit, held-out human evidence and external review: **ABSTAIN_UNCALIBRATED / production BLOCKED**.
