# E002-433 — actionable human and instrument validation handoff

**Status:** protocol only; **zero new participants recorded**. This document does not substitute for consent, institutional ethics review, or access permission. It is a concrete route to falsifying E002-371 under joint nuisances rather than another synthetic theorem.

## Scientific endpoint and pre-registration

**Primary endpoint:** among participant-disjoint ordinary-camera intervals for which the **fully joint** calibrated lower bound exceeds the preregistered physical closure threshold, count witnessed physical threshold crossings. A witnessed false no-closure certificate fails the deterministic model/assumptions. Reference-negative intervals with unresolved between-frame minima **must not** be counted as verified successes. Report total candidate count, witnessed false candidates, unresolved reference candidates, abstentions, participant-macro and nuisance-stratified rates with uncertainty. Distinguish deterministic assumption failures from statistical population-risk claims.

**Precommitted contrast:** a pipeline that conjunctively accepts separate geometry-only and gain-only checks versus a pipeline propagating both uncertainty sets jointly. Predict that incomplete composition can falsely certify under crossed illumination and head/gaze changes, while the joint gate either abstains or requires tighter calibration. Do not tune thresholds after reading holdout labels.

## Sources and provenance

1. **Preferred:** authorized synchronized 400-fps 3D eyelid-margin traces from FaceBase (DOI 10.25550/88-28BJ; restricted GRU/NPU), only after approved access. No claim of existing access.
2. **Alternative:** consented 400–600-fps synchronized camera or 3D capture from a collaborating lab. The camera acquisition rate must be authenticated from raw sensor metadata; playback/export frame rate is not evidence of capture rate.
3. **Feasibility-only fallback:** a borrowed 120–240-fps phone slow-motion mode may witness positive closures and stress annotation/transfer pipelines, but cannot establish complete negative physical reference intervals or hard physiological velocity limits. Never infer a deterministic speed cap from the phone's measured secants.

## Minimum acquisition manifest (one immutable row per sequence)

`study_id, participant_pseudonym, session_id, sequence_id, consent_scope, access_license, camera_make_model, raw_file_sha256, original_sensor_frame_id, exposure_start_hw_ns, exposure_end_hw_ns, hardware_clock_domain, clock_sync_reference, clock_error_upper_ns, shutter_calibration_sha256, gain_calibration_sha256, geometry_calibration_sha256, frame_drop_mask_sha256, reference_device_id, reference_frame_rate_verified_hz, reference_scale_mm_per_unit, reference_scale_error_mm, nuisance_condition_id, operator_id, independent_reviewer_id`.

Every physical-calibration digest must resolve to a signed or independently archived calibration artifact, not merely a self-asserted string. If raw capture timestamps are unavailable, label the sequence **NOT_PHYSICALLY_CERTIFIABLE**.

## Nuisance crossing (randomize within participant)

- Independently vary head pose and gaze direction, then cross each with fixed/external illumination and camera auto-exposure/auto-white-balance settings; record both camera controls and measured illuminance. Do not infer physical gain from brightness alone.
- Repeat with and without glasses where appropriate, controlled partial occlusion, motion blur, and multiple exposure lengths. Preserve negative and failed acquisitions.
- Introduce recorded frame drops and clock offsets in a **separate software challenge** after the original sensor stream has been sealed. Keep natural missingness distinct from injected missingness.
- Measure upper/lower eyelid landmarks against an independent physical scale/multi-view geometry. Single-view pixel aperture is a proxy, not ground-truth millimeters.

## Blinding, physical calibration and splits

- Rater A and rater B independently mark upper/lower eyelid margins and intervals of uncertain visibility on raw reference frames. They cannot see Lucent's predictions, and each cannot see the other's labels before sealing.
- Compute reference aperture intervals from both raters and independent scale uncertainty; disagreement or an unresolved between-reference-frame gap stays **UNRESOLVED** unless an independently justified velocity/acceleration envelope excludes a crossing.
- Fit joint optical/shutter/geometry/clock uncertainty on **training participants and calibration objects only**. Never estimate a hard speed cap from a held-out participant's own ordinary-camera stream.
- Seal the complete predicted candidate/abstention ledger, participant split, nuisance ranges, threshold and code commit using E002-426's prospective-lock instrument, independently archive the seal, then expose held-out reference annotations.
- Keep the first two recording sessions of each held-out participant entirely out of calibration, not just the last frames. Do not leak paired eyes, repeated trials or sessions across split boundaries.

## Testable gates

1. Independently timed LED/photodiode pulses and random off-grid, multiwidth calibration must validate the shutter/rolling-row response on held-out pulse conditions; a good fitted-boxcar score alone is insufficient (E002-424/425).
2. Joint geometry/illumination calibration must be valid on **crossed** conditions. If separate-gate candidates survive but joint candidates do not, report the product abstention and the compositional failure.
3. Original hardware capture times and missingness masks must survive decode/re-encode and restart; no timestamp compression (E002-432).
4. Every candidate must be associated with a bounded reference status: witnessed closure, verified nonclosure under authenticated reference assumptions, or unresolved. Do not silently drop unresolved trials.
5. For any claimed population-risk rate, use participants as the sampling units and prespecified one-sided uncertainty; E002-428 shows that 25 zero-exceedance participants cannot support a 1% population-tail upper bound.
6. Any false physical certificate under independently verified assumptions blocks release and triggers an assumption/implementation root-cause investigation. An unattested instrument, unbounded nuisance, rater disagreement, reference ambiguity or out-of-distribution condition returns **ABSTAIN_UNCALIBRATED**.

## Deliverables for the first real study

A consent/ethics/access record; raw acquisition and calibration manifest; photodiode/clock traces; independent physical aperture reference; blinded A/B annotation sheets; frozen predicted ledger and archived seal; held-out per-participant confusion/abstention/unresolved table; and a reproducible script reproducing the primary endpoint and figures. Public release must honor participants' privacy and dataset licenses; deidentified derived features alone are not automatically authorized for redistribution.

**Current evidence gap:** no authenticated human sequences, physical shutter/clock/geometry/gain measurements, independent rater sheets or hard physiological velocity bound. Physical hidden-closure, blink-duration, PERCLOS and fatigue claims remain unauthorized.
