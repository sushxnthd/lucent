# E002-548 | Frozen one-sided human-reference witness protocol

Frozen 2026-10-30 **before executable publication**. Primary E002-371 shutter-gap kernel. Evidence tier: published human-data source and prospective design; **zero downloaded or analyzed human sequences**.

## Source and acquisition constraints

Primary source: Guttmann-Flury, Sheng & Zhu, *Scientific Data* 12, 587 (2025), DOI https://doi.org/10.1038/s41597-025-04861-9. Data deposit https://doi.org/10.7303/syn64005218, indexed Phantom folder https://www.synapse.org/Synapse:syn64102305. The paper reports 31 participants, 63 sessions, Phantom Miro M310 monocular **150 frames/s** video at 320x240, E-Prime/Arduino 6.6-ms triggers, Tobii TX300 eye tracking at approximately 300 Hz, and EEG/EOG. **300 Hz is the eye-tracker rate, not the video rate.** CC0 is reported for the dataset, but actual retrieval, usage terms, and completeness must be checked at download. Video exposure duration, optical response, clock uncertainty and anatomical calibration are **not independently certified by the publication**.

Silesian5 (100 fps, five participants, signed-agreement access) and OpenEDS (200-Hz eye-facing system, access restrictions) remain alternatives. Prefer acquiring one authorized Eye-BCI participant's native video/XML and synchronized timestamps. Never publish facial videos or participant-level outputs.

## Locked participant split and no peeking

For published IDs S-01 through S-31, sort ascending by SHA256 of UTF-8 `lucent-e002-548-v1|S-XX`. First 15 IDs exploratory: S-24,S-22,S-27,S-17,S-23,S-01,S-18,S-04,S-19,S-29,S-14,S-12,S-05,S-11,S-25. Last 16 IDs held out: S-08,S-28,S-16,S-21,S-31,S-07,S-10,S-02,S-15,S-20,S-30,S-06,S-26,S-09,S-03,S-13. Ordered-list SHA256: `d4dc15a099c590f805cf3eb90b1e89b558131d06fe05d6bc47dd2f42d8b8c15f`. Keep all sessions/windows of one participant in the same partition. Report missing subjects, never replace or rebalance after inspection. Zero witnessed failures among 16 independent participants would still imply a one-sided 95% binomial upper bound ~17.1% on **witness prevalence** under strong ascertainment assumptions, not a bound on false exclusions when reference sensitivity is unknown.

## Frozen one-sided witness predicate

Let `I` be a guaranteed ordinary-camera blind interval with a **precommitted** E002-371 `EXCLUDE` and an independently justified continuous-time motion ceiling. Let `E` be the actual high-speed camera exposure, with independently bounded possible support `[E_min,E_max]`; let `a(t)` be normalized anatomical aperture and `c` the predeclared closure threshold.

A candidate contradiction requires **all**:

1. The whole possible exposure support is **strictly inside** `I` under worst-case shutter/rolling-scan/clock error; boundary touch or partial overlap is censored.
2. Independent optical and anatomical-transfer calibration supplies a valid upper bound `U` on the **exposure mean of anatomical aperture**, not raw pixel brightness/classifier score, with `U <= c`. Then some instant in the exposure must have `a(t) <= c` by the integral mean inequality. This establishes existence only, not duration.
3. Matching participant/session/eye/ROI, native frame identity and digest, acceptable geometry/brightness/blur/gaze/glasses/missingness, two independent blinded rater agreements, and authenticated calibration evidence.
4. Prediction digest committed **before** held-out frames are inspected. Independent external review authenticates the claimed certificates and rater independence; a parser cannot do so.

A human record meeting these syntactic checks is `HUMAN_WITNESS_CANDIDATE_EXTERNAL_REVIEW`, **not** certified falsification. A synthetic input is `SYNTHETIC_WITNESS_ONLY`. Any reference-negative or missing high-rate observation is `REFERENCE_CENSORED`, never `NO_CLOSURE`. Predeclared `ABSTAIN` is `ABSTAIN_NO_EXCLUSION`.

## Locked analysis and kill criteria

Primary endpoint: externally confirmed false-exclusion **participants** in held-out subjects, not frame-level accuracy. One authenticated contradiction kills the affected exclusion claim/stratum. Report all candidates, censored and abstained gaps, and participant-level denominators, plus timing/geometry/brightness/gaze/blur/glasses/missingness strata. A positive witness needs physical transfer calibration; neither nominal 150 fps nor 300-Hz pupil absence suffices. No continuous-time closure-free labels from high-rate negatives.

**Constructed sensitivity only:** for the earlier *hypothetical* 10-ms triangular closure (`V=180/s, c=0.2`), 150-fps reference with a 4-ms linear boxcar has 1/5 threshold detection probability under uniform phase; 5-ms exposure gives 0. These are **not** Eye-BCI observations. The actual dataset exposure duration is unknown.

Human video acquisition, independent optical calibration, native frame hashes and blinded raters remain prerequisites. No fabricated evidence. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Hush branch/PR untouched.
