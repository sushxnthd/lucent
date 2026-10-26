# E002-455 — prospective real-human high-rate optical aliasing challenge

**2026-10-26. Frozen first:** [E002_455_FROZEN.md](E002_455_FROZEN.md) committed at `8f5843f41fc998db4f9cb026e0541c5715f92ca5`, before the analyzer, tests, or new S19 evaluation. This is an **empirical image-space temporal-decimation experiment**, not a physiological theorem, eyelid-aperture measurement, or a repeat of E002-454's participant-cap statistics.

## Scientific question
Can actual high-rate human-eye image contrast exhibit an interior excursion even when the two frames retained by an ordinary-camera-like decimator are nearly identical? This is a narrower, falsifiable image-space test of the *information-loss mechanism* motivating E002-371. It cannot establish that the excursion is a blink or anatomical closure.

## Frozen methods and predictions
- Reuse the published MD5-verified S19 Phantom AVI; decode exactly 12,000 frames; do not touch S21/S22.
- Freeze center-minus-border grayscale contrast z and border-left-minus-border-right nuisance control w. Calibration uses frames 0..1999 only, threshold T=max(4/255, 8*median absolute first difference of z). Evaluation uses frames 2000..11999.
- For strides K=8 and K=17, enumerate all K phase offsets. Every phase has nonoverlapping endpoint intervals, but different phases overlap; **no binomial iid inference**.
- Primary positive event: endpoint difference <=T/2, yet a strictly interior frame deviates from the endpoint-linear interpolation by >=T. The exact expected numbers of enumerated windows are **9,992** (K=8) and **9,983** (K=17), regardless of signal.
- Preregistered positive decision requires >=1 primary event for **both** K values. If the border control has as high an event fraction at either K, reject optical spatial specificity even if the primary has events. Preserve a null result if neither threshold is crossed.

## Instrument and adversarial controls
- [Executable S19 experiment](e002_455_optical_aliasing.py) uses existing verified acquisition and frame decoder. Emits only a nonidentifying aggregate; no participant imagery, timestamps, or raw traces.
- [14 synthetic/adversarial tests](test_e002_455_optical_aliasing.py) cover hidden triangular pulses, monotone controls, equal nuisance controls, additive global illumination invariance, spatially localized **nonanatomical** illumination confounding, missing/corrupt frames, nonfinite inputs, phase accounting, fixed threshold and fail-closed product behavior.
- [Dedicated hosted experiment](../../.github/workflows/e002_455_optical_aliasing.yml) runs tests and downloads/decodes real S19, then publishes only the nonidentifying aggregate.

**Execution status at report creation:** code and CI workflow committed; new hosted real-S19 outcome and actual 14-test pass/fail count are **not yet verified**. Do not infer empirical success from synthetic predictions. Once CI completes, copy the verified aggregate and log evidence into this branch, without rewriting the frozen protocol.

## Nuisance and novelty limitations
The scalar z cancels uniform additive brightness only in unclipped frames. Spatially varying illumination, camera motion, gaze, eyelid vs pupil identity, glasses, blur, compression, missing exposures and unknown shutter kernel can all cause or hide an optical excursion. The w control is not an anatomical ground truth. K=8/17 are frame-index strides; they are **not authenticated 60/30-fps camera exposure experiments**. Only one previously inspected pilot subject is used. No participant-disjoint performance or physical closure accuracy is estimated.

E002-371 already established conditional mathematical nonobservability; E002-445 already measured spatial optical association on S19; E002-447 already tested synthetic shutter integration. This experiment contributes only a **prospectively frozen high-rate human-video temporal-decimation test** of a defined optical scalar. Do not present the mathematics or optical proxy as new anatomy.

## Release consequence and next gate
Irrespective of optical outcome, **E002-371 physical validation remains NOT_ESTABLISHED** until two independent anatomical raters, authenticated exposure and geometry calibration, defensible independently estimated velocity bounds, and prospective participant-disjoint hidden-closure predictions are available. S21/S22 remain untouched. Physical hidden-closure, blink duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. Keep draft PR #26 unmerged; Hush PR #45 independent and untouched.
