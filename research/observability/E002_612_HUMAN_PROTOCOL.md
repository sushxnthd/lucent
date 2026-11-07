# E002-612 | Concrete physical-camera and human anatomical study handoff

Status: PROSPECTIVE ONLY, NO HUMAN DATA ACQUIRED. Date: 2026-11-02. Builds on E002-567, E002-609, E002-611 and E002-612. This document is an execution protocol, not a claim of ethics approval or equipment availability.

## Two separable validation arms

**A. Physical shutter/clock instrument (no human participants).** With an existing 30-fps camera and a 240-fps-or-faster reference camera, place a calibrated high-contrast translating target and an externally timestamped coded LED in both views. Use an independent optical photodiode or equivalent timebase with an independently verified clock; without this, mark synchronization UNVERIFIED. Measure actual per-frame start/end integration windows, rolling-row delay, exposure response/linearity, dropped frames and inter-device offset/jitter. Move the target through independently measured trajectories, including an encoder-controlled speed/acceleration challenge if a suitable existing stage is available. Blind the reference-trajectory evaluator to the ordinary-camera exclusion predictions. Retain target trajectories with both expected passes and expected failures. Do not represent the translating target as a human eyelid or infer human speed limits from it.

**B. Human anatomical pilot (only after local consent/ethics and privacy approval).** Two independent eye-facing cameras record simultaneously, ordinary approximately 30 Hz and reference at least 240 Hz with known actual acquisition times; nominal 240-fps phone mode does not authenticate exposure or clock. At least eight consenting adults for an exploratory pilot, with spontaneous and separately labeled voluntary blink blocks, primary gaze and varied gaze, controlled low/high illumination, with/without spectacles where applicable, and intentional head motion/defocus as nuisance challenges. If participant safety, consent or device access is uncertain, do not collect. No clinical or fatigue claim is tested here.

## Source, custody and split

- Assign opaque participant IDs and session IDs before acquisition; secure raw face/eye videos in a restricted local custodian directory. Do not upload raw faces, participant IDs, location, demographics, private frame crops or unlicensed data to GitHub or CI.
- Freeze participant-disjoint development and holdout sets *before viewing anatomical labels*. For an eight-person pilot, use four development and four holdout participants, explicitly exploratory only. Larger follow-up sample sizes require an independently justified power analysis; E002-509 already showed eight participants cannot certify a 1% participant-session error rate.
- Obtain two genuinely independent, blinded anatomical raters. For each reference interval, annotate upper/lower lid margins, uncertainty, full/partial closure, occlusion and unresolved cases; raters do not see ordinary-camera predictions, each other's annotations or candidate event selection. Resolve disagreement only by predeclared adjudication; never convert unresolved cases into open or closed.
- Report rater agreement and uncertainty intervals, and require a third adjudicator for conflicting full-closure labels. A generic blink label, pupil missingness or dark pixel intensity does not certify anatomical zero aperture.
- Obtain calibrated physical aperture scale and conservative annotation uncertainty. If absolute mm scale is unavailable, do not report mm/s; if photometric linearity is unavailable, do not use brightness-derived exposure-mean closure witnesses.

## Prospective prediction and falsification

1. On each held-out ordinary-camera gap, seal `MODEL_EXCLUDE_CONDITIONAL` or `ABSTAIN_HIDDEN_CLOSURE_POSSIBLE` using the frozen E002-608 gate and externally defended velocity bound. Do not replace the hard bound with published mean/peak speed, or with E002-612's conditional bound if its acceleration premise is unverified.
2. Hash the sealed predictions before independent raters or high-rate anatomical results are opened. Record the shutter intervals and their timing error bounds from arm A. Real 30-fps integration must be measured; 100-Hz every-third-frame decimation is not an exact 30-fps physical surrogate (E002-606).
3. A reference positive witness needs a conservatively bounded *linear anatomical exposure average* at/below threshold with the **entire** uncertain reference exposure strictly within the certain ordinary-camera dark gap, as specified by E002-609. A high-rate instantaneous-looking frame or generic closed-eye label alone is insufficient.
4. Primary falsifier: any validated hidden closure witness contradicting a sealed conditional exclusion. Audit anatomy, geometry, shutter timing, clock synchronization, velocity premise and annotation leakage before attributing a cause. Negative witnesses do not prove absence.
5. Report participant-clustered contradiction and abstention rates, 95% confidence intervals appropriate to participant independence, and counts by spontaneous/voluntary blink, lighting, gaze, spectacles, motion, blur, missingness, saturation, rolling-shutter and timing-uncertainty strata. Never treat frames as independent participants.

## Exact minimum evidence manifest

Per experiment: device identifiers (non-sensitive), frame-rate **measured** not merely declared, exposure-start/end brackets, row-delay uncertainty, LED/photodiode timing evidence, optical response linearity, physical target/encoder reference, raw-data SHA-256 kept private, and protocol commit SHA. Per participant session: consent/ethics record held privately, blinded rater A/B exports, calibration and annotation uncertainty, precommitted predictions and seal hash, participant-disjoint split, missingness masks, and signed custodian provenance. Publish only aggregate, nonidentifying results with scripts and controlled-access data protocol.

## Decision gates

- **STOP / ABSTAIN** if no independent clock, no physically calibrated shutter, no independently bounded anatomical aperture, no genuinely blinded rater pair, no defensible hard continuous-time velocity premise, or unresolved nuisance. A synthetic test pass never waives these.
- If the acceleration premise in E002-612 cannot be independently established for real human eyelids, its numeric bound remains a scenario tool, not a product speed certificate. Reframe the human study as falsification and empirical calibration of *positive closure witnesses*, not deterministic exclusion of all hidden closures.
- A pilot of eight is for discovering failures and feasibility, not proving a low population error rate. External expert review and prospective independent replication are mandatory before release.

**Status:** Physical measurements 0; human ratings 0; holdout predictions 0. Product `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.
