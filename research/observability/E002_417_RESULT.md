# E002-417 — completed held-source human-video falsification (2026-10-24)

**Decision: REJECT the two automatic pixel-gap estimators as transferable eyelid-aperture measurement candidates.** This is a negative necessary-condition test, not a physical E002-371 validation. Frozen predictions are in `E002_417_FROZEN.md`, established before execution. The machine-readable aggregate is `E002_417_HUMAN_AGGREGATE.json`; the successful execution log is https://github.com/sushxnthd/lucent/actions/runs/40091786115 (real-human-aggregate job).

## Data and denominators

- Exact previously selected MD5-verified Eye-BCI S01/S19 source archives; eight fixed clips; 632 **frame occurrences**, not 632 independent humans. Only two participants. No additional selection, fitting, tuning, or relabeling.
- Method A: opposite-polarity gradient-ridge pixel gap; method B: adaptive dark-region pixel gap. Both are unvalidated computer-vision candidates; agreement is not anatomical accuracy.
- Clean A valid: **585/632 (92.56%)**. Clean B valid: **374/632 (59.18%)**. Both valid: **374/632 (59.18%)**. Agreement within 5 px: **152/632 (24.05%)** of *all frames*, or 152/374 (40.64%) conditional on both being valid. The preregistered H2 threshold was **at least 60% of all frames**.
- Nuisance H3 denominator: **374 clean joint-valid frames** for each transformation. Missing or unstable output counts as a failure. All-frame joint-valid counts are separately preserved in the JSON.

| Transform | Joint valid among all 632 | Retained AND stable among 374 clean joint-valid | Required |
|---|---:|---:|---:|
| Brightness ×0.70 | 204 (32.28%) | 108 (28.88%) | ≥95% |
| Brightness ×1.30 | 425 (67.25%) | 207 (55.35%) | ≥95% |
| Gaussian blur σ=2 px | 342 (54.11%) | 202 (54.01%) | ≥95% |
| Translation (+8,+6), reflected border | 245 (38.77%) | 18 (4.81%) | ≥95% |
| Central white glare | 0 (0.00%) | 632/632 both abstained (100%) | ≥95% both abstain |

The translation test compares gaps rather than absolute positions. It still fails severely. The glare result demonstrates conservative rejection of this **specific artificial glare mask**; it is not evidence of robustness to natural reflections or glasses.

## Frozen hypotheses, evaluated without threshold changes

- **H1 PASS:** eight clips, 632 frames.
- **H2 FAIL:** 152/632 = 24.05% all-frame joint agreement, below 60%.
- **H3 FAIL:** each of four nuisance transformations fails 95% retained-and-stable criterion (28.88%, 55.35%, 54.01%, 4.81%).
- **H4 PASS:** 632/632 frames both abstain under the prescribed white-glare mask.
- **H5 PASS:** idealized 24-pixel synthetic gap control recovered within 3 px by both methods; no product authorization.
- **Joint transfer gate FAIL.** A successful CI job signifies successful *execution*, not acceptance of the scientific hypothesis.

## Scientific interpretation and product consequence

Both methods were independently specified in code but share the same video, crop, central intensity profile, and image nuisances. Their disagreement is an observed falsification of the **necessary transfer criterion**, not a measure of ground-truth physical gap error. We do not infer an anatomical error rate, eyelid velocity, blink sensitivity, PERCLOS, fatigue, or a camera shutter guarantee from this result. The video frame occurrences are temporally correlated and come from two people. Artificial transforms do not cover all realistic gaze, glasses, rolling-shutter, exposure, geometry, clock, or occlusion failures.

**Kill decision:** Do not promote either E002-417 method, their agreement, or a tuned variant to Lucent's physical eyelid-aperture product claim on these data. Do not optimize these thresholds post hoc on the same clips and report that as independent validation. Existing E002-397 and E002-412 rejected surrogates remain rejected. For hidden-closure exclusion, blink duration, PERCLOS, and fatigue claims, return **`ABSTAIN_UNCALIBRATED`**. No camera-based physical no-closure certificate is authorized.

## Decisive next human experiment

Use the already prepared E002-407 independent, blinded **human** upper/lower lid-margin annotation sheets and E002-408 adjudication, with two genuinely separate raters, on fixed frames and unseen participants. Quantify rater disagreement, ambiguous/occluded frames, and all-frame coverage. Do not use agreement between automated algorithms as ground truth. Calibrate pixel-to-physical aperture, actual exposure integration and row timing with independent instrument evidence. Derive velocity bounds from independent calibration participants and hold out participants/devices for precommitted shutter-gap predictions. Count ambiguous high-speed reference intervals as unresolved, per E002-416, not as negative closures. An external independent reproduction is required before product certification.

**Evidence tier:** real human-eye videos with known source selection and synthetic nuisance perturbations; *not* independently labeled anatomical aperture, independent shutter metrology, or physical validation of E002-371. This falsification does not assert novel general mathematics.
