# E002-459 — Prespecified gaze-shift transfer falsification of human speed-cap assumptions

**Date:** 2026-10-26. **Evidence tier:** frozen human-validation analysis instrument, with independent synthetic adversarial fixture; **human held-out outcome pending hosted execution**. Not anatomical trajectory validation, shutter authentication, or a new mathematical theorem.

## Scientific question
E002-457/458 used a pooled calibration sample maximum for each directional eyelid speed. Does a sample maximum calibrated **only in center gaze** transfer to **unseen top and bottom gaze** in five participant-disjoint human subjects? This is a stronger *unseen-condition* stress than same-study pooled-gaze holdout. The published 2026 human study reports gaze-dependent kinematics, making this a substantive transfer assumption rather than a metadata audit.

[Immutable preregistration](E002_459_FROZEN.md) was committed as `f494ff4b7d657e79405a109bf8beb77ab44122ae` **before** E002-459 analysis was implemented or executed. No change to split, outcome, or criterion is permitted after seeing the human result.

## Executable experiment
[Analyzer](e002_459_gaze_shift_transfer.py) verifies the published OSF `Blinks.csv` SHA256 using the existing independently hosted E002-457 parser. Calibration is the same 12 participants, held-out subjects 3/6/9/12/15. Fit three prespecified pairs of **sample maxima** for closing/opening speed: center-only, pooled all gaze, and gaze-matched. Test held-out bottom/center/top blinks, report both blink and distinct-person exceedance counts, and compute the **idealized conditional** 240-fps observability decision for a hypothetical 1-mm endpoint margin.

Primary kill criterion: **any** noncenter held-out blink exceeding either center-trained speed maximum falsifies that *sample-based transfer assumption* for that observation. It does **not** falsify E002-371's conditional theorem or certify the alternative pooled/gaze-matched maxima. No observed exceedances among five people cannot validate a universal physiological upper bound.

## Independent synthetic adversarial check
An independently constructed 17-person, three-gaze fixture sets center-only calibration C/O maxima at 200/100 mm/s, top/bottom calibration maxima at 300/150 and 250/125 mm/s. All five held-out people have top 230/105, bottom 210/120, center 190/90 mm/s. Therefore the prespecified center-only noncenter transfer yields **10/10 synthetic blink exceedances across 5/5 people**, while pooled and matched transfer have **zero**. The hypothetical center-only 1-mm critical gap is exactly **15 ms**. An independent JavaScript calculation reproduced these fixture counts. This verifies that the falsification rule can distinguish a constructed shift; it is **not a human experimental result**.

[Adversarial Python tests](test_e002_459_gaze_shift_transfer.py) cover strict equality, participant clustering, source count and schema, malformed speeds, missing gaze/participants, output privacy, and fail-closed physical release. The tests have been **committed but their hosted success is not yet established**.

## Human-data execution status
[Dedicated GitHub Actions run](https://github.com/sushxnthd/lucent/actions/runs/40282116947) was **queued** when this report was written. It must download the immutable public CSV, verify SHA256 `6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43`, run the frozen 12/5 and out-of-gaze analysis, and emit only a nonidentifying aggregate. **No human exceedance counts, gaze-transfer outcome, or CI pass are claimed until the actual run succeeds.** The complete aggregate must then be committed to the same branch without exposing participant-level records.

## Product and next scientific gate
Whether the center-only transfer is falsified or not, the data remain published **per-blink peak estimates**, not independently annotated continuous anatomical apertures. They cannot supply a physiological hard cap or authenticate ordinary-camera shutter, clock, projection, blur, gaze, glasses, missingness or illumination. E002-371 physical validation remains **NOT_ESTABLISHED**; hidden-closure, blink duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. Do not merge PR #26 or inspect sealed S21/S22.

The next decisive experiment remains prospective high-speed human **anatomical** reference trajectories and independently authenticated camera timing, using the E002-456 sealed protocol. This gaze-shift test can **reject an unsupported speed-calibration shortcut** but cannot replace that experiment.
