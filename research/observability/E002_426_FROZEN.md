# E002-426 — prospective human-reference lock and participant-weighted evaluation (frozen 2026-10-25)

**Status:** prospective human-validation artifact, not an observed human experiment. **Primary kernel:** E002-371 physical shutter-gap/velocity boundary. This study-control artifact is not another shutter theorem.

## Falsifiable objective

Prevent retrospective tuning of Lucent's ordinary-camera no-hidden-closure predictions after viewing high-speed human reference annotations. A participant-disjoint, SHA-256-sealed prediction registry must be frozen before independent rater/reference labels arrive. Any mutation, added trial, removed trial, subject overlap, duplicated identifier, or missing reference must be detected or explicitly counted. Report both frame-weighted and participant-macro *finite-evaluation-set* false-certificate identification intervals; these must not be mislabeled as population guarantees.

## Frozen test gates

1. **Seal:** Canonical JSON SHA-256 of the entire prediction manifest; changing a decision, nuisance tag, participant, timing, or evidence reference invalidates the seal.
2. **Separation:** Training and holdout participant sets are nonempty, disjoint; all trials are holdout-only, with unique trial IDs, valid strictly positive intervals, known device IDs, explicit nuisance flags and nonempty camera/model-calibration evidence identifiers.
3. **Reference:** Exact one-to-one matching of reference labels to frozen trial IDs. A missing/unresolved/ambiguous high-speed label is counted as unresolved, never as a true negative. A missing CSV row is a hard evaluation error, not silent exclusion.
4. **Finite-set bounds:** For N conditional no-closure predictions, F witnessed threshold crossings and U unresolved references, calculate sharp descriptive bounds [F/N,(F+U)/N]. All-abstain has undefined selective error, not zero.
5. **Participant aggregation:** Compute the macro-average of participant-specific identification intervals among participants with >=1 conditional prediction; preserve participant count and all eligible trials. A synthetic imbalance control with 99 resolved successes in one participant and 1 witnessed failure in another must give pooled 1% versus participant-macro 50%.
6. **Safety:** Outputs never authenticate submitted provenance strings, human rater independence, exposure kernels, physiological hard velocity bounds, or physical no-closure claims. Product remains ABSTAIN_UNCALIBRATED even if every descriptive test passes.

## Data contract and privacy

The registry is a study *pseudonym* manifest; it contains no face images, source video, raw anatomical coordinates, human names, or event/control linkage. Real study registry and reference sheets must remain in approved private storage. Public CI runs synthetic fixtures only. Hashes are tamper-evidence relative to a separately archived immutable seal, not proof of authorship or physical provenance. An attacker able to replace both registry and seal defeats this check.

The registry requires study_id, nonoverlapping training_participants and holdout_participants, device_ids, and trials with trial_id, participant_id, device_id, interval_start_s, interval_end_s, prediction (NO_CROSSING_CONDITIONAL | POSSIBLE_CROSSING | ABSTAIN), nuisance_flags (explicit booleans for brightness, blur, gaze, glasses, occlusion, missingness, clock), and nonempty model_input_sha256, camera_calibration_ref, velocity_bound_ref. Reference CSV has trial_id,reference_label where labels are WITNESSED_CROSSING, NEGATIVE_CONDITIONAL, UNRESOLVED, MISSING.

## Human execution gate

1. Independently calibrate actual shutter kernel, row/exposure timing, clock, physical geometry and optical transfer, with photodiode/oscilloscope records; use a separate velocity calibration cohort. Do not promote observed max speed to a hard bound.
2. Preselect untouched participants and devices, freeze this prediction manifest and archive its seal externally **before** any held-out high-speed reference annotation.
3. Qualify two independent human raters using E002-418; annotate E002-407/408 full events independently, preserve ambiguous/missing reference intervals and require authenticated camera-clock/physical-aperture metrology.
4. Score untouched predictions with E002-426. Publish participant-wise and nuisance-wise abstention, witnessed failures and unresolved fractions, and the worst-case finite-set error bounds. Cluster bootstrap may be reported separately as descriptive uncertainty, never as a deterministic physical guarantee.
5. If the required human/hardware evidence is unavailable, record a blocked physical validation, not a synthetic success.

## Expected scientific contribution

This artifact tests whether a future human-validation claim is genuinely prospective and participant-independent. The imbalance counterexample should show why an apparently small pooled error can conceal a severe held-out participant failure. This is established evaluation methodology, not a new mathematical theorem or physical empirical result. No further E002-371 product unlock is permitted without external physical verification.
