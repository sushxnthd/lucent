# E002-609 | Frozen cross-camera falsification bridge for human validation

Date: 2026-11-02. Parent: E002-371 and E002-608. Research branch: `research/observability-human-boundary`; draft PR #26. **Evidence tier: preregistered prospective physical/human protocol; no human data yet.**

## Question, not novelty claim

Can a high-rate *exposure-integrated* reference camera provide a logically sound witness that falsifies an ordinary-camera conditional "no hidden closure" certificate? The bridge must never equate a high-speed frame's nominal timestamp or generic "blink" label with instantaneous eyelid closure. This is an operational consequence of elementary integral and interval reasoning, **not a new mathematical theorem**.

For continuous anatomical aperture `a(t) in [0,1]`, threshold `tau`, and an independently calibrated **linear aperture exposure average** `m_ref=(1/e) integral_{u}^{v} a(t)dt` with `e=v-u>0`, an authenticated conservative **upper** bound `m_ref_hi <= tau` guarantees at least one `t* in [u,v]` with `a(t*) <= tau`. This is a witness of existence, **not proof that the eye stayed closed for the whole exposure**. If the complete reference exposure, including independently bounded timing errors, is strictly inside the ordinary camera's independently bounded **unexposed gap**, the closure was hidden from both ordinary exposures.

The witness is incompatible with a separately precommitted `MODEL_EXCLUDE_CONDITIONAL` E002-608 prediction **if all model premises actually hold**. A conflict falsifies the *joint physical certificate*, not necessarily the underlying mathematical inequality. If the reference exposure only overlaps a gap, or the image is a generic binary "closed" label rather than a calibrated linear anatomical average, **ABSTAIN**.

## Frozen input and output rules

One deidentified JSON file per prospectively precommitted ordinary-camera gap. Fields:
- `experiment="E002-609"`, `gap_id` non-identifying string, `prediction` one of `MODEL_EXCLUDE_CONDITIONAL` or `ABSTAIN_HIDDEN_CLOSURE_POSSIBLE`; prediction must have been sealed *before* held-out reference adjudication. `prediction_sha256` is a syntactic digest reference, not self-authentication.
- `ordinary_gap` with exact decimal millisecond conservative bounds `left_end_latest_ms`, `right_start_earliest_ms`; require strictly positive certain dark gap.
- `reference` with conservative `start_earliest_ms`, `end_latest_ms`, `linear_aperture_upper`, `threshold`; `start_earliest < end_latest`. Reference time intervals include shutter, rolling-row and cross-device clock uncertainty.
- `evidence_sha256` with distinct 64-hex digests for `ordinary_clock_shutter`, `reference_clock_shutter`, `linear_anatomy`, `reference_annotation`, `prediction_seal`.
- `attestations` all true: `independent_clock_sync`, `both_shutters_physically_calibrated`, `reference_linear_anatomy_calibrated`, `two_blinded_reviewers_adjudicated`, `heldout_prediction_precommitted`.
- `nuisances` all false: geometry, brightness, missingness, blur, gaze, glasses, sampling, clock_error, occlusion, saturation, rolling_shutter. A caller-declared flag or digest does **not** independently authenticate any claim.

Outputs: `WITNESS_CONTRADICTS_CONDITIONAL_EXCLUSION` only when every premise is supplied, the reference exposure is **strictly contained** in the certain dark gap, `linear_aperture_upper <= threshold`, and the sealed prediction was EXCLUDE. `HIDDEN_CLOSURE_WITNESS_CONDITIONAL` when the same witness exists but prediction was ABSTAIN. `NO_REFERENCE_WITNESS` for valid non-witness controls; never treat it as proof of absence. `ABSTAIN` on missing physical premises, nuisance uncertainty, touching/overlapping interval boundaries, or uncertain aperture threshold. Invalid numeric/schema input must fail closed. Every output has product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.

## Preregistered adversarial fixtures and falsifiers

1. An ordinary dark gap (0,10) ms, reference exposure [3,5] ms with mean-aperture upper 0.15 and tau 0.20, and a sealed EXCLUDE prediction: **conditional contradiction**.
2. The same evidence with prediction ABSTAIN: **conditional witness**.
3. Reference [9,11] ms overlaps ordinary exposure: **ABSTAIN** despite aperture <= tau.
4. Reference [0,2] or [8,10] touches a gap boundary: **ABSTAIN** (strict containment).
5. Reference aperture upper 0.21 with tau 0.20: **NO_REFERENCE_WITNESS**, not "no blink".
6. Missing reference linear-anatomy attestation, missing digest, one nuisance, or ambiguous clock: **ABSTAIN**.
7. A one-millisecond widening of timing uncertainty must not create a witness from a non-witness; increasing aperture upper bound must not create a witness.
8. Independent Node.js implementation must agree with Python on the core strict containment and threshold cases; all tests use synthetic inputs.

## Human/physical acquisition handoff and stop conditions

Custodian first obtains ethics/privacy approval and consent, then two synchronized cameras (reference preferably >=240 fps; ordinary ~30 fps), external coded-LED/photodiode clock/shutter evidence, geometric and linear-aperture calibration, and two blinded anatomical raters. Separate spontaneous and instructed blinks; vary gaze, lighting, glasses and exposure, with participant-disjoint heldout conditions. Seal ordinary-camera E002-608 predictions **before** opening high-rate annotations. The reference image is exposure-averaged; a generic full-closure label or pixel-darkness score is **not** a calibrated anatomical mean. If the physical linear transfer cannot be defended, do not manufacture a witness. Do not publish faces, raw images, person-level annotation exports, or credentials.

This instrument cannot supply the missing physical evidence. Do not mistake passing synthetic tests for empirical E002-371 validation. A real contradiction triggers review of timing, anatomy, velocity and observation-model premises; no claim of mathematical falsification follows automatically. Report participant-clustered outcomes and abstention strata, not frame-level independent confidence intervals. Do not promote product claims without external review.

**Release:** `ABSTAIN_UNCALIBRATED` / `BLOCKED`. No private human data are included.
