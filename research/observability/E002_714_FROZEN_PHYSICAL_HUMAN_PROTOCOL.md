# E002-714 — Frozen physical-to-human validation protocol for E002-371

**Evidence tier:** prospective preregistration and falsification design. No physical or human measurements were collected. This document does not validate a velocity ceiling.

## Primary question and falsifiable prediction

Given two independently timestamped ordinary-camera observations with measured open apertures a0 and a1, an independently justified upper bound V on the *continuous-time* aperture speed, and a maximum possible elapsed time Δ+ after clock/exposure uncertainty, a complete intervening closure is impossible if **V Δ+ < a0_low + a1_low**, where a0_low and a1_low are conservative lower bounds on aperture at the observation instants. This follows from total variation required to travel from a0 to zero and back to a1. When the inequality fails, classify **POSSIBLE_HIDDEN_CLOSURE**, not “closure happened.” Equality is not an exclusion certificate. If V is unverified, classify **ABSTAIN_UNCALIBRATED**. Note that a *lower* bound on aperture must itself be validated against occlusion, blur, glasses, gaze, illumination and camera geometry. Frame-integrated intensity is not an instantaneous aperture measurement.

**Primary endpoint:** false-exclusion count: cases certified “NO_HIDDEN_CLOSURE” despite reference-confirmed closure between the corresponding ordinary-camera observation instants. The target is zero observed violations; report a one-sided exact binomial confidence bound rather than claiming a deterministic universal guarantee from finite human data. Report coverage (fraction certified) alongside errors, and stratify all abstentions.

## Stage A: independent instrument challenge (before humans)

Use a motor-driven opaque shutter or a repeatable mechanical occluder with a separately timestamped photointerrupter/photodiode as ground truth, and a smartphone camera with recorded per-frame exposure-start/end metadata. **Do not use nominal FPS as timestamps.** Acquire 3 independently seeded sessions with randomized occlusion onset relative to camera frame boundaries, at least 100 complete occlusion events per session and 100 non-occlusion controls per session. Include shutter durations both shorter and longer than nominal interframe gaps. Calibrate actuator displacement and maximum speed with an independent encoder or high-rate position sensor; do not estimate a hard maximum from sampled video slopes. Freeze thresholds before opening the holdout session.

Controls must cross: illumination steps/flicker; contrast; geometric scale/angle; optical defocus and motion blur; rolling-shutter row position; missing/dropped frames; timestamp jitter/drift; occluder partial coverage. For each challenge, log measured rather than assumed bounds on clock uncertainty, aperture error, speed, and reference-sensor response. If the sensors cannot bound these, mark the condition UNCALIBRATED and do not issue exclusion certificates. Release the raw timebase logs, calibration artifacts, trial schedule, and deterministic replay code.

## Stage B: human acquisition (requires consent and appropriate review)

Recruit adults with informed consent; no medical/sleepiness inference. Aim for >= 20 participants with >= 30 natural blinks each, subject to feasibility, and document all exclusions. Capture a synchronized high-frame-rate reference stream and ordinary-phone stream, with hardware synchronization or a continuously visible timing signal independently checked for drift. Record *actual* reference exposure intervals, not only nominal acquisition rate. Capture glasses/no glasses where feasible, varied gaze, head pose, brightness and skin/eyelid appearance without treating demographic group as a substitute for optical calibration. Annotators blind to the ordinary-camera verdict label reference closures and ambiguous events separately; dual annotation with adjudication. A reference frame sequence alone does not certify the absence of subframe closures (E002-709).

## Velocity ceiling identification: mandatory independent gate

No observed finite-frame displacement, including a high-speed reference stream, is a deterministic global speed ceiling. A candidate V must come from independent physical sensing with known bandwidth/anti-aliasing and an explicit biomechanical assumption, or be treated as a *conditional sensitivity parameter* rather than a human-validated hard bound. Publish results as a sweep over assumed V when this gate is not met. Never derive V on the held-out participants and then use it to certify those same participants. An observed velocity quantile supports only a probabilistic statement under a declared population/exchangeability model, not a universal impossibility certificate.

## Frozen split and decisions

Participant-disjoint development and held-out evaluation; group all sessions from each person together. Freeze extraction, error bounds, V source, event definitions, abstention reasons, and primary endpoint before accessing held-out reference labels. Compare (1) timing-only bound, (2) calibrated instantaneous aperture bound, and (3) exposure-integral candidate as a separate exploratory arm. Negative controls: shuffled timing, deliberately incorrect clock offset, brightness shifts, gaze changes, glasses, blur and dropped frames. If any condition violates the measurement error envelope, withdraw its certificate and abstain.

Report per-condition confusion counts, false-exclusion exact confidence intervals, certificate coverage, timing/scale uncertainty, and all ambiguous reference events. A statistically clean result cannot transform a conditional theorem into a physiologically unconditional claim.

## Release gate

Until Stage A passes and Stage B supplies independently calibrated evidence, Lucent must remain **ABSTAIN_UNCALIBRATED** and production **BLOCKED** for hidden-closure exclusion, fatigue, and sleep-state claims. A future allowed feature may expose timestamp integrity and explicitly conditional observability warnings, but not a sleepiness or physiological measurement inferred from this protocol alone.

**Immediate actionable deliverable:** acquire a real sensor-timestamped occluder session; if no instrument access, obtain public high-rate footage only when its original acquisition clock, exposure duration and ground-truth provenance are verifiable. Do not perform a third metadata-only dataset search.
