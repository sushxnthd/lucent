# E002-690 — Frozen prospective human and instrument acquisition packet

**Evidence tier:** prospective human-validation artifact; no human recordings or instrument measurements acquired. This is a preregistration, not an empirical result. Prepared 2026-11-07 UTC. Supersedes no prior frozen protocol; use alongside E002-671 and E002-685/688.

## Primary falsifiable question
Does the E002-371 conditional aperture exclusion rule ever certify **NO CLOSED EYELID** across a low-rate camera gap while an independent synchronized high-rate anatomical reference unambiguously records closure inside that gap? A single authenticated counterexample under the declared assumptions blocks the corresponding certificate regime. No use of low-rate video to estimate the speed ceiling.

## Acquisition and custody
1. **Instrument stage (before human):** programmable mechanical occluder with a known aperture reference and independent photodiode/encoder; simultaneously film at 30 and 60 fps and >=240 fps reference if available. Record raw uncompressed sensor timebase, LED synchronization pulses visible to both systems, per-frame start/end exposure timestamps, shutter mode, dropped frames, and actual exposure duration. If any item cannot be measured, mark timing **UNKNOWN** and forbid certificates; do not infer timing from nominal fps.
2. **Human stage:** recruit consenting adults under local ethics/consent review; start with >=20 participants, >=40 eligible blink or no-blink intervals per participant across sessions (design targets, not achieved sample sizes). Reference >=240 fps with independently documented acquisition rate, shutter and frame timestamps; phone 30/60 fps simultaneously; a synchronization LED and physical scale marker. Include natural and prompted blinks, left/right eye, gaze shifts, glasses, illumination, motion, blur and deliberately missing phone frames. Do not infer a hard human velocity ceiling from finite differences of this reference.
3. Keep immutable originals, acquisition logs, sensor calibration certificates, SHA-256 file hashes and blinded annotation decisions. Obtain explicit permission for any redistribution. Separate calibration subjects and held-out subjects; predeclare random seed and split manifest before holdout analysis.

## Frozen decision and analysis
- Physical aperture in millimeters, closure threshold c in millimeters, and uncertainty intervals for both endpoint apertures come from independent calibration. Determine actual blind-gap upper bound h+ from exposure/shutter/synchronization logs and clock uncertainty. When unknown, **ABSTAIN**.
- Specify a physically justified hard velocity bound V with external evidence and explicit applicability domain. If none is independently defensible, report **conditional sensitivity curves** over V and **zero unconditional certificates**.
- For endpoint intervals [aL,aU] and [bL,bU], find jointly feasible smallest endpoints a*=max(aL,bL-Vh+), b*=max(bL,aL-Vh+). If either exceeds its upper interval endpoint, **ABSTAIN_INCONSISTENT**. Otherwise L=max(0,(a*+b*-Vh+)/2). Certify exclusion only if L>c strictly; equality abstains.
- Reference labels: CLOSED if calibrated upper uncertainty on reference minimum <=c; OPEN if calibrated lower uncertainty >c; otherwise INDETERMINATE. Annotators must not see the phone decision. A CLOSED reference paired with CERTIFY_EXCLUSION is a **false exclusion** and blocks that condition; preserve ambiguous and missing reference rows.
- Primary endpoint: count of independently verified false exclusions and coverage (certificates / all eligible trials), with participant-cluster bootstrap uncertainty. Report exact binomial one-sided 95% upper bounds only as descriptive under independence assumptions, not a deterministic guarantee. Stratify by glasses, gaze, light, blur, motion, missing frames, exposure regime and clock quality. Never suppress failed/abstained trials.
- Held-out predictions are frozen before viewing high-speed labels; report all thresholds, V assumptions and participant IDs as a preregistered manifest. Do not tune thresholds or exclude nuisance strata post hoc.

## Mandatory data contract
One gap per row: participant_id,session_id,trial_id,phone_camera,phone_frame_left_id,phone_frame_right_id,reference_file_sha256,reference_start_ns,reference_end_ns,phone_exposure_start_ns,phone_exposure_end_ns,clock_error_upper_ns,aperture_left_low_mm,aperture_left_high_mm,aperture_right_low_mm,aperture_right_high_mm,closure_threshold_mm,velocity_ceiling_mm_per_s,velocity_evidence_id,blind_gap_upper_s,reference_min_low_mm,reference_min_high_mm,reference_label,phone_decision,glasses,gaze,illumination_lux,blur_metric,missing_frames,rolling_shutter,calibration_id,split,provenance_verified.

## Release gates
- **Instrument gate:** a full replay from original time series, including clock offset uncertainty, reproduces blind-gap bounds and demonstrates at least one deliberately hidden closure plus one confidently excluded closure under authenticated instrument constraints. If unavailable, remain blocked.
- **Human gate:** participant-disjoint held-out evaluation with no false exclusions in authenticated eligible cases, calibration valid in each proposed operating stratum, and coverage reported. Even zero observed failures does not establish a hard physiological V ceiling.
- **Product gate:** expose only measured camera-timing quality and explicitly conditional exclusion under authenticated physical constraints; otherwise `ABSTAIN_UNCALIBRATED`. No fatigue, sleep-stage or clinical claims are supported by this packet.

## Acquisition feasibility
If public high-rate footage lacks original acquisition metadata, shutter timing, scale, or participant-disjoint identifiers, it may illustrate blinks but cannot validate deterministic closure exclusion. After two bounded source attempts, move to the instrument protocol above. This document does not claim those attempts were completed in this run.

## Next executable task
Collect or obtain one independently timed physical occluder recording and run E002-688 replay on it. Do not create another theorem-only artifact as a substitute for acquiring physical data.
