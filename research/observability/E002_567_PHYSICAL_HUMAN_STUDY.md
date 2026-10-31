# E002-567 | Prospective physical human-validation execution plan and hard stop

Date: 2026-10-31. Primary kernel E002-371; existing `research/observability-human-boundary` branch and draft PR #26. **This is an executable study-design/human-validation artifact, not a completed experiment or another synthetic theorem refinement.** It supersedes no frozen E002-507 or E002-562 sampling, threshold, or split. No raw human imagery or identifiers may be committed.

## Decisive evidence separation

**S01 is a qualitative native-frame pilot only.** E002-566 verified authentic 260-frame source-to-two-private-reviewer packet construction, but two independent human ratings are still absent. Its paper's 150-fps rate, rehost's ~500-fps description, and AVI's 1-fps playback metadata remain unreconciled as independently authenticated acquisition timing. Even if both reviewers report a closed interior native frame between open native endpoints, that is a *frame-index alias witness*, not an E002-371 shutter-integrated 30-fps physical prediction. No more S01 metadata archaeology or automated optical-motion proxy tuning.

**E002-371 needs a different prospective instrument study.** A high-speed camera's nominal FPS or labels cannot certify a hard continuous-time human velocity ceiling or absence of a subframe closure. Use its independently rated *positive* closure witnesses for one-sided falsification; treat negative reference windows as censored unless an independent reference-sensitivity certificate exists. Do not turn finite differences into a universal speed maximum.

## Stage A: execute the already-frozen S01 human pilot

1. An authorized coordinator privately downloads the pinned Motor Imagery S01 archive, runs `e002_502_local_handoff.py` outside the Git checkout, and delivers separate unannotated bundles to **two different independent human raters**. The hosted CI runner cannot serve as a human rater or distribute private footage.
2. Before seeing S01, each rater independently completes the existing E002-418 blinded known-geometry nuisance qualification; preserve pass/fail, abstentions and versioned answer-key custody privately. Synthetic qualification is **not** an anatomical uncertainty certificate.
3. Both raters independently annotate all 260 frozen frames using E002-497. Neither sees candidate/control status, source frame indices, the other's marks or E002-507 predictions. Both exports are hashed and time-sealed before owner unblinding; no revisions after unblinding.
4. Independently justify a strictly positive per-clip iris-scale uncertainty `delta_px`. Rater agreement, synthetic qualification and same-image repeated marking alone cannot certify it. If no defensible bound exists, publish only descriptive agreement/abstention and **do not** run quantitative OPEN/CLOSED threshold promotion.
5. Execute E002-507 with its frozen indices (3 and 8 endpoints; 4-7 interiors), threshold 0.10 and nuisance abstentions unchanged. Preserve its >50% endpoint/interior unresolved pilot stop rules. A positive witness is only a native-frame observation; no witnesses is not proof of no blink.

**Stage-A stop:** missing actual human raters, independent scale uncertainty or authorized local custody => `HUMAN_PILOT_NOT_EXECUTED`. Never substitute AI annotations or generated reviewer JSON for independent people.

## Stage B: original, synchronized physical experiment (not simulated 30 fps)

Recruit consenting adults with an approved local research/ethics and privacy protocol. Use a no-fee borrowed high-speed reference camera and an ordinary camera recording the **same eye at the same time**, plus an independent optical timing reference. If traceable timing or permission is unavailable, stop; a display refresh animation, AVI FPS and a software clock do not authenticate acquisition.

- **Pre-register the endpoint:** for each ordinary-camera blind interval marked `EXCLUDE` by the frozen E002-371 rule, ask whether two blinded human raters identify at least one *reference-positive* anatomically closed observation inside it. One authenticated positive contradiction falsifies that exclusion under its claimed premises. Reference-negative frames are censored; report abstention and exposure coverage separately.
- **Independent time axis:** record externally timed optical edges visible to both cameras, independently bracket each sensor exposure/row interval, measure dropped/duplicated frames and drift, and fit an affine clock only if residuals support it. Verify shutter start/end and rolling-shutter line offsets at the actual eyelid row. Propagate worst-case clock and exposure uncertainty through the bound; do not replace exposure integration by point samples.
- **Anatomy:** predefine eyelid landmarks, a measured geometry/iris-scale error budget, a closure threshold and explicit abstentions. Both raters remain blind to low-rate predictions and each other until immutable exports. Confirm positive closures; do not infer negatives from unlabeled high-speed frames.
- **Nuisance matrix:** record separate sessions/strata for gaze angle, glasses/reflections, skin/iris brightness, illumination variation, motion blur, occlusion, face/eye geometry, autofocus, exposure changes, rolling shutter, missing frames and clock perturbations. Pre-register exclusions and coverage, not post-hoc cherry-picked clean intervals.
- **Prospective lock:** freeze participant-disjoint training/holdout IDs, original video hashes, camera parameters, calibration certificates, thresholds, velocity assumptions, low-rate predictions and their SHA-256 before any held-out anatomical labels are inspected. Use E002-562's one-sided adjudication semantics; its synthetic phase sweeps are **not** physical camera evidence.
- **Velocity claim:** an empirical peak velocity distribution or upper quantile with uncertainty is *not* a deterministic continuous-time bound. Without an independently defensible upper envelope and exposure/clock certificate, all deterministic no-hidden-closure claims abstain. A separately pre-registered **probabilistic** performance claim may be explored only with validated reference sensitivity, calibrated confidence and external replication.

## Frozen go/no-go endpoints

Pilot: a small participant-disjoint cohort (e.g. eight adults) is for counterexample discovery, usability, nuisance coverage and rater feasibility, not for population risk certification. Record all attempted sessions, eligible sessions, abstentions, positive reference opportunities, EXCLUDE predictions, contradictions, and participants with at least one contradiction. Never compute apparent accuracy by treating unlabeled/no-observed-positive windows as true negatives.

Population claim: E002-509 showed that, **only under independent exchangeable participant-session outcomes and perfect event ascertainment**, zero failures among 299 independent participants would yield a one-sided 95% upper bound below 1% for a participant-session failure rate. This is an illustrative minimum, not a sufficient study design or authorization to make a 1% claim: correlated repeated sessions, incomplete high-speed sensitivity, selection, coverage and domain shift invalidate the shortcut. Pre-register a participant-level analysis and coverage floor before collecting confirmatory data.

Stop or revise immediately if an authenticated positive reference closure falls in a conditionally excluded interval; if timebase/exposure cannot be independently verified; if rater calibration or positive sensitivity is inadequate; or if nuisance strata drive unacceptable abstention/contradictions. Preserve all negative results and reproduce every decision from immutable data and code. External replication is required before release.

## Product consequence and resource gate

Until Stage B yields valid evidence, Lucent may at most expose **uncalibrated, explicitly non-diagnostic image-quality/measurement-feasibility feedback**, not certified absence of closure, blink duration, PERCLOS, sleepiness or fatigue. The honest default remains `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.

Current authenticated physical shutter captures **0**, independent human anatomical rater pairs **0**, certified continuous-time human velocity upper ceilings **0**, held-out physical closure predictions **0**. The next external action is obtaining two actual blinded S01 rater exports and access to an independently timed optical bench. No additional synthetic dataset archaeology is justified. Hush remains a separate secondary branch/PR.