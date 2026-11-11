# E002-600 | Frozen blinded synthetic-eyelid rater calibration challenge

Frozen: 2026-11-02, before generator/grader implementation. Primary E002-371 human-validation workstream, existing `research/observability-human-boundary` branch and draft PR #26. Evidence tier **SYNTHETIC_REVIEWER_INSTRUMENT_ONLY**.

## Question and falsifiable prediction
Can the actual E002-598 offline anatomical-review workflow produce calibrated, appropriately abstaining eyelid-margin annotations when the geometry is known independently of the reviewer? This is a **necessary reviewer-instrument check**, not evidence for a physiological eyelid-velocity ceiling, physical shutter law, or clinical fatigue detection.

Build ten synthetic 19-frame, 640x480 PNG clips, plus native E002-574 A/B blank reviewer templates and an owner-only truth/manifest file. Reviewer-visible packet must not contain truth labels or synthetic aperture values. Use an optional owner-only seed; default to a fresh unpredictable seed. The generator must preserve exact frame count, naming and dimensions required by E002-598, and report SHA-256 per PNG in the owner-only manifest. No synthetic PNGs or ratings are committed to GitHub.

## Locked adversarial arms
- Clean always-open control; one-, two-, three-, and four-frame closed pulses at predetermined positions; a sampled-endpoint closure control.
- Brightness variation, blur, partial occlusion/glasses, and gaze/geometry shifts. Nuisance arms must be labeled separately from clean controls in the private truth manifest.
- Ground truth uses explicit per-frame upper/lower eyelid functions at x=320 and an independently known *synthetic* iris diameter of 100 px. These are not human kinematic or anatomical distributions.
- The challenge must not imply that native-frame decimation is physical exposure integration. No shutter or clock evidence is inferred.

## Locked rater qualification metrics
For each independently completed reviewer export, validate exact E002-598 native schema, count missing/nuisance abstentions, and score only clean, measurable frames against the private known truth:
1. At least 80% of clean frames measured.
2. At least 95% of measured clean-frame intervals cover true aperture, using the reviewer's declared uncertainty and fixed synthetic iris scale. Report numerator and denominator.
3. No more than one clean open frame falsely certified CLOSED and no more than one clean closed frame falsely certified OPEN at threshold 0.20. Threshold-straddling intervals abstain.
4. Report all nuisance-arm abstentions, but do not penalize abstention as a false anatomical prediction. Do not pool A/B scores into independent evidence without actual distinct reviewers.

All thresholds are **instrument qualification choices**, not statistical validation of human anatomical accuracy. If no human reviewer completes the challenge, the outcome is **INSTRUMENT_BUILT_NOT_HUMAN_VALIDATED**.

## Integrity and stopping rules
Test deterministic replay under a fixed test seed; changed seed must alter at least one frame hash. Test 190 PNGs, exact 640x480, template shape, owner-only truth separation, and failure on malformed/missing reviewer exports. Independent verifier should recompute ground-truth score from exported rows without importing the grader's scoring function. Stop on mismatch. Report no reviewer success unless actual completed human exports exist. Product stays `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Hush branch/PR untouched.
