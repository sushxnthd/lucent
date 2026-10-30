# E002-541 | Frozen coded-light shutter identifiability bench

Date: 2026-10-30. Primary E002-371 human-validation kernel. Branch: `research/observability-human-boundary`, draft PR #26. **Frozen before implementation or execution.** This is a software-instrument surrogate, not physical camera capture, physiological validation, or a new general coded-light calibration invention.

## Independent variable and observation

A clock-referenced LED emits a deterministic 1-ms binary optical sequence. A hypothetical global/rolling camera integrates this illumination over exposure windows, with two spatially separated rows and a possible row delay. Sample frame starts are 33 ms apart. In each row, brightness is `offset + gain * exposure_average + noise`; fit unknown common affine gain and offset, never substitute brightness for anatomical aperture. Candidate shutter start phase is 0..20 ms in 1-ms steps, exposure 4/8/12 ms, and row delay 0/5/10 ms. A 20-frame synthetic sequence supplies row samples. Nominal injected truth: phase 7 ms, exposure 8 ms, row delay 5 ms. An independent optical clock and linearly responding LED are **assumed**, not measured.

## Frozen predictions and falsifiers

1. A 4-ms-periodic 0/1 LED pattern is phase-ambiguous: at least two distinct shutter phases produce identical integrated observations. The estimator must abstain rather than pick an arbitrary winner.
2. A seeded aperiodic binary code should uniquely recover the injected triple in a noiseless experiment, despite affine brightness gain/offset. If not, report failure and do not retune the code seed.
3. With a seeded, bounded per-sample additive disturbance of magnitude at most 0.01 and gain=0.65, offset=0.2, the coded experiment should still recover the injected triple. Record the actual residual margin.
4. An unmodeled row-delay candidate grid (restricting the fit to 0 ms) must not be accepted as a valid global-shutter fit; high residual or ambiguity forces abstention.
5. Constant illumination, clipping/saturation, fewer than 80% known-ID samples, unknown frame IDs, or a deliberately corrupted clock assumption must abstain. Explicit source authenticity, sensor response linearity, and real clock/shutter timing are never inferred from synthetic fits.
6. A held-out deterministic seed sweep of 40 coded sequences with the same frozen candidate grid should yield at least 38/40 uniquely correct noiseless recoveries. Failure must be preserved, not tuned away.
7. No model may produce a physical eyelid exclusion, PERCLOS, blink-duration or fatigue claim.

## Acceptance

Exact candidate uniqueness for noiseless code, zero false physical certifications, unmodeled-row abstention, reproducible seed sweep, and clear negative controls. Treat a best-fit residual below tolerance as **insufficient** if competing candidates fit equally well. Report distinct true-vs-alternative residual gap and all failed trials. Compare to prior art: optical flash timing and LED rolling-shutter calibration already exist (Smid & Matas 2019, arXiv:1902.11084; Huai et al., Optics Letters 2023, DOI:10.1364/OL.474375; Schatz, Measurement Science and Technology 2017, DOI:10.1088/1361-6501/aa5d8a). No novelty claim for coded illumination or LED timing.

## Instrument/human gate

A genuine bench must replace simulated LED samples with photodiode-recorded light emission, separately authenticated frame/line exposure timing, multiple gain/exposure/rolling-shutter conditions, measured clock drift and missing-frame intervals, and a moving mechanical aperture with independently measured geometry. Human follow-up requires two independent blinded native-frame anatomical raters and participant-disjoint frozen predictions with independently defensible continuous-time motion ceilings. All unsupported conditions retain `ABSTAIN_UNCALIBRATED` and production `BLOCKED`.
