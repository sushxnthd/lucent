# E002-445 — frozen spatial-specificity and illumination-control falsification (2026-10-25)

**Frozen before executing E002-445 against S19 pixels.** Existing E002-444 aggregate optical result is known; the below spatial and null-control outcomes are not. S19 first 12,000 frames only; S21/S22 remain sealed. This is a prospective *analysis* of already-seen participant S19, not a new independent participant validation.

## Hypothesis and disconfirmation
E002-444 found elevated whole-frame change across 21 candidate 10–100 ms sync gaps. If this association reflects a spatially localized ocular phenomenon, then a fixed central image region should show stronger brightness-adjusted enrichment than the complementary border. If it is explained by global illumination, compression, camera motion, or gaze changes, the association may vanish after global offset removal or occur equally in the border. **Neither result measures anatomical eyelid aperture.**

## Locked computations
Use the original MD5-verified S19 archive and exactly first 12,000 decoded 320x288 grayscale frames; candidate event gaps come from the original Time column at populated RelTime rows, in order, without claiming exposure alignment. Predeclare central rectangle **x=[80,240), y=[72,216)**, and the remaining pixels as border. No learned mask, post-hoc cropping, or threshold tuning.

For each adjacent frame pair define signed pixel delta D=I(t)-I(t-1). Record (1) mean |D|/255 and (2) mean min(|D|,|D-median(D)|)/255 in central and border separately; median(D) is over the *whole* frame, not each ROI. This conservative per-pixel clipping prevents a majority-region brightness shift from fabricating optical activity in unchanged pixels, and rejects uniform additive brightness offsets, but may erase true optical motion and does not eliminate spatially varying illumination, motion, compression, or gaze.

Gap groups: <=10 ms, >10 and <=100 ms, >100 ms, with the same floating-point tolerance 1e-8 seconds as E002-444. Define for each region and metric R=median(change | medium gap) / median(change | short gap). If short median is exactly zero, declare ratio unresolved (do not silently add epsilon). Primary statistic is log(R_central_adjusted/R_border_adjusted). Require >=10 medium gaps and >=100 short gaps, positive finite medians, otherwise ABSTAIN_INSUFFICIENT_EVENTS.

Construct **512 deterministic, unique circular shifts** of the change series relative to the fixed event-gap series, evenly spaced integer offsets in [257,n-257] inclusive; no random search. Calculate the same primary contrast for each shift. Report null 95th percentile and descriptive rank fraction (1 + number null contrasts >= observed)/(513). This is **not a calibrated p-value**, because the time series is autocorrelated and nonstationary and the gap process may be nonexchangeable.

A *necessary, non-sufficient* spatial-specificity screen passes only if adjusted central R>=1.5, adjusted central/border enrichment ratio>=1.5, and primary contrast exceeds the 95th percentile of the 512 shifts. If it fails, reject any eyelid-specific interpretation of the original optical-gap association. If it passes, classify ONLY `SPATIALLY_LOCALIZED_OPTICAL_ASSOCIATION_UNVERIFIED`, not eyelid motion, exposure timing, or E002-371 validation. No product physical release under any outcome.

## Integrity, controls and privacy
Use the existing archive hash and event/frame-count verification, require exactly 12,000 frames and strictly increasing candidate times. Synthetic tests must include uniform brightness shift (adjusted change zero), central-only change (central adjusted positive), border-only change (central adjusted zero, including majority-region shifts), invalid shape/dtype, no medium gaps, and no release. No raw images, per-frame trace, identifiable timestamps, or source ZIP in commits/artifacts; aggregate summaries only. Record negative results, CI failures and limitations. Hush untouched.

## Release boundary
S19 is calibration/pilot, not held out. No independent shutter/exposure calibration, physical anatomical scale, blinded aperture labels, physiological velocity upper bound, or nuisance-complete validation. All physical hidden-closure, blink duration, PERCLOS, fatigue, and medical claims remain `ABSTAIN_UNCALIBRATED`. E002-371 remains physically unvalidated.

**Pre-execution amendment:** During synthetic adversarial design, the originally specified unconditional |D-median(D)| adjustment was found to fabricate central activity when 75% of the border changes and the center does not. Before executing E002-445 on any human pixels, replaced it with the conservative per-pixel minimum min(|D|,|D-median(D)|), preventing this specific nuisance-induced false positive. This is a preregistered correction to an invalid instrument, not a post-hoc human-data adjustment.
