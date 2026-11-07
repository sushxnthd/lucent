# E002-456 — frozen prospective physical-reference challenge (2026-10-26)

**Frozen before implementing the evaluator.** This is a research-only bridge from E002-371 to participant-disjoint anatomical testing, not another proxy or proof refinement. No human reference annotations or camera calibrations are available to this run. Existing E002-448/450/451 annotation gates remain prerequisites, not substitutes for millimeter geometry and timing.

## Falsifiable question

For independently acquired, anatomically annotated high-rate eyelid trajectories, does a *frozen* conservative shutter-aware, velocity-limited ordinary-camera rule ever label an interval `EXCLUDED_CONDITIONALLY` while a high-rate reference contains an unequivocal interior closure? One such case falsifies the joint claim that the measurements, nuisance controls, timing, and chosen velocity bound were all valid. No such cases does **not** validate a universal physiological speed limit.

## Frozen analysis rule

Inputs per interval: two measured **shutter-averaged** aperture endpoints (mm), nonnegative measurement uncertainties, endpoint-center timestamps (ms), exposure width (ms), endpoint-center clock error (ms), a predeclared velocity limit V (mm/s), and a closure threshold c (mm). All units and provenance must be explicit. For uniform symmetric shutter use exposure correction `V * exposure_s / 4` at each endpoint; for unknown kernel with authenticated symmetric support use `V * exposure_s / 2`; otherwise abstain. Inflate gap by twice the center-time uncertainty. Conservative lower envelope:

`L = max(0, (a0-u0-s0 + a1-u1-s1 - V*(t1-t0+2*clock_error_ms)/1000)/2)`.

Here `s_i` is the shutter correction. Label `EXCLUDED_CONDITIONALLY` iff `L > c`; otherwise `NOT_EXCLUDED`. This is a conservative sufficient condition, not a new sharp theorem for uncertain shutter-averaged endpoints. Reject physically inconsistent endpoints and uncalibrated/unknown nuisance conditions.

A reference `WITNESSED_CROSSING` requires a strictly interior, independent high-rate anatomical measurement with `aperture + uncertainty <= c`, with verified provenance and all nuisance checks passed. A measurement whose uncertainty straddles c is indeterminate. The absence of a witnessed crossing, even in a dense sequence, **never** proves absence between reference frames. A `FALSIFIED_JOINT_ASSUMPTIONS` result requires an excluded interval plus a witnessed crossing. No inference from overlapped frame windows as iid trials.

## Preregistered negative controls and kill criteria

1. Triangular synthetic hidden closure with near-equal endpoints and V sufficiently high: NOT_EXCLUDED; if V falsely set too low and a witnessed crossing exists: FALSIFIED_JOINT_ASSUMPTIONS.
2. At L=c exactly, NOT_EXCLUDED (no equality promotion).
3. Same endpoints under longer shutter exposure or larger clock uncertainty must never become *more* excludable.
4. Missing reference frames, contaminated landmarks, blur, lighting changes, head geometry, gaze, glasses, rolling shutter, sampling/clock errors: explicit abstention or reference-indeterminate. No missing-is-open imputation.
5. Reference witnesses and input data must be from different instruments/annotation streams; fabricated synthetic witnesses are labeled synthetic and never used as physical evidence.
6. Participant-disjoint holdouts, session-level uncertainty, and all exclusions/abstentions must be reported. An excluded interval with independently witnessed closure is a kill, even if other intervals succeed.
7. All outputs are deidentified aggregate counts. No video, landmarks, exact subject identifiers or timestamps in public CI artifacts.

## Minimum prospective human study (not yet executed)

Consent and locally controlled storage; 2 blinded anatomical raters; >=240-fps high-rate reference with independent exposure/clock validation; simultaneously recorded ordinary camera or explicitly marked *virtual decimation* (not equivalent to physical shutter). Independent mm-scale target in eye plane with quantified uncertainty, and a hardware-timed LED pulse train visible to both cameras. Calibration must record actual exposure window, dropped frames, rolling-shutter skew, clock drift and synchronization residual. Collect neutral/up/down gaze, glasses/no-glasses, lighting and motion, voluntary and spontaneous blinks. Freeze V, thresholds, nuisance exclusions and decision code on development participants, then seal participant-disjoint holdouts. Report witnessed-crossing false exclusions, abstention, coverage, and subject-cluster uncertainty by nuisance stratum. No deterministic guarantee from sample maxima or 0 observed errors.

## Evidence tiers and release

All evaluator results are `RESEARCH_CONDITIONAL_ONLY`; the code must always return `physical_release_authorized=false` and `ABSTAIN_UNCALIBRATED`. Without external hard-bound review, independently authenticated shutter/geometry calibration, and genuine human reference labels, no hidden-closure guarantee, blink duration, PERCLOS, fatigue or medical claim is allowed. S21/S22 remain untouched until the protocol is independently reviewed and frozen for their use. Hush branch/PR remain independent.
