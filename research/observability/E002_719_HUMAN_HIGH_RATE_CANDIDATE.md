# E002-719 — Human high-rate acquisition candidate and falsifiable replay decision (2026-11-08 UTC)

Evidence tier: independently published dataset identification and prospective test design. **No downloaded human frames or empirical validation.**

## Acquisition candidate found
**OpenEDS** (Garbin et al., 2019, https://arxiv.org/abs/1905.03702) reports *two synchronized eye-facing cameras at 200 Hz*, 152 participants, controlled illumination, and 91,200 frames of 1.5-second video snippets. Access is described as *upon request* via the OpenEDS challenge. This is a concrete high-rate human candidate, but published nominal 200 Hz is not a sensor-timestamp or shutter-exposure calibration; the published dataset description does not establish that snippets contain independently verified complete blinks.

**LPW** (Tonsen et al., 2015, https://arxiv.org/abs/1511.05768) reports 66 eye-region videos, 22 participants, ~95 FPS, with glasses, contact lenses, makeup, indoor/outdoor light and gaze variation. This is a valuable nuisance challenge, not an independently calibrated continuous-time velocity reference.

**mEBAL2** (https://github.com/BiDAlab/mEBAL2) provides blink labels and RGB/NIR streams, but requires a signed access agreement and does not establish a high-speed continuous-time anatomical velocity ceiling. **MPEblink** (https://zenodo.org/records/7754768) offers 21.6 GB of untrimmed videos but its listing does not establish high-rate capture. Do not download large archives or infer high-rate ground truth from labels alone.

## Frozen decision before looking at test outcomes
1. Request OpenEDS access and confirm actual acquisition timestamps, exposure duration, participant IDs, continuous eye aperture visibility, and complete-blink reference. If any are unavailable, use OpenEDS only as a stress test, not as proof of E002-371.
2. Assign participants disjointly to calibration and held-out groups *before* extracting outcomes. For each high-rate sequence, preselect ordinary-camera downsampling schedules at 15, 24, 30, 60 Hz, fixed/random phase, and missing-frame bursts. Keep original reference frames untouched.
3. Define complete closure from two independent blinded anatomical annotations; disagreements become indeterminate. Estimate aperture intervals with calibrated geometry and measurement uncertainty. **Never use a maximum observed discrete slope as a deterministic continuous-time velocity ceiling.**
4. Issue E002-371 exclusions only with independent velocity upper bound, conservative aperture lower bounds and shutter/clock upper-gap bounds. Predict exclusion vs abstention before revealing held-out reference closures.
5. Report false exclusions, certified-trial coverage, participant-stratified counts, nuisance strata (glasses, gaze, blur, brightness, geometry, missingness, exposure and clock error), and exact uncertainty bounds. Any confirmed closure in an excluded interval falsifies the joint assumptions. Do not suppress failures.
6. If independent continuous-time velocity calibration is unavailable, **all physiological exclusion claims abstain**, while a separately labeled *conditional mathematical replay* may still report what would follow under an explicitly hypothetical velocity bound. This is not empirical certification.

## Acquisition fallback and product consequence
If access or metadata fails after two documented attempts, execute the already frozen E002-714 physical occluder protocol with independently timed shutter/occluder and randomized phase, and publish a participant recruitment/consent and measurement plan. Neither the OpenEDS nominal 200 Hz nor LPW nominal 95 FPS by itself warrants changing `ABSTAIN_UNCALIBRATED` or production `BLOCKED`.

This report intentionally does not claim any downloads, participant-level results, dataset licenses beyond verified descriptions, or physiological validation.
