# E002-541 RESULT | Coded-light calibration can disambiguate a synthetic shutter, but cannot authenticate a real one

Date: 2026-10-30. Primary Lucent E002-371 kernel, established branch `research/observability-human-boundary`, draft PR #26. Protocol [E002_541_FROZEN.md](E002_541_FROZEN.md) was committed first at `3be3a618`, before implementation. **Evidence tier: simulated optical instrument only, with independently implemented numerical replay. No physical camera, photodiode, human aperture measurement, or hard physiological motion ceiling.**

## Falsifiable question and acquisition consequence

Previous E002-540 showed that exposure-averaged brightness cannot be substituted for pointwise anatomical aperture. A prerequisite to any physical E002-371 study is therefore **knowing what temporal interval each sensor observation actually integrated**. Can a clock-referenced, temporally coded light source distinguish shutter phase, exposure duration, and two-row rolling-shutter delay, while periodic flashes leave the inverse problem ambiguous?

This study simulates a binary LED clock at 1-ms resolution, 20 frames 33 ms apart, two rows, affine unknown brightness gain and offset. Candidate phase 0..20 ms, exposure 4/8/12 ms, row delay 0/5/10 ms. The injected truth is (7,8,5) ms. Estimation fits gain and offset independently for every candidate and requires both absolute residual <=0.025 and runner-up minus best residual >=0.004. **Those tolerances are heuristic software gates, not calibrated confidence intervals or physical error bounds.**

## Frozen predictions and executed results

The local standard-library Python run and 18 adversarial unit tests passed. An independently written Node.js LCG, exposure integrator and affine least-squares estimator reproduced the noiseless result and all 40 held-out code seeds. Hosted CI is configured but must be checked separately.

| Condition | Best phase / exposure / row delay (ms) | RMSE | Decision |
| --- | --- | ---: | --- |
| Aperiodic LED, exact linear response | 7 / 8 / 5 | 0.000000 | Synthetic identification |
| Same, uniform sensor noise +/-0.01 | 7 / 8 / 5 | 0.005277 | Synthetic identification |
| 4-ms periodic light | Nonidentifiable | N/A | Abstain |
| Fit incorrectly assumes zero row delay | 12 / 8 / 0 | 0.047719 | Abstain |
| True frame period 34 ms, fit assumes 33 ms | 16 / 12 / 5 | 0.069617 | Abstain |
| Row-dependent gain factor 0.75 | 7 / 8 / 5 | 0.035148 | Abstain |
| Deterministic 0/1/2-ms frame phase jitter | 8 / 8 / 5 | 0.045855 | Abstain |
| Constant light / 15 of 20 frames / clipped sensor | N/A | N/A | Abstain |

For the exact coded case, the next-best candidate (3,12,5) ms has RMSE 0.042699, yielding an observed margin of 0.042699. With the frozen additive noise, the next-best RMSE is 0.043347 and margin 0.038071. The **40/40** deterministic held-out LCG seeds recovered the same injected timing triple in noiseless simulations, without seed-specific tuning. This is a finite software sweep, not statistical validation over cameras.

**Exact periodic ambiguity:** for an 8-ms exposure, the 4-ms square-wave LED integrates to 0.5 regardless of phase; phase 7 ms and phase 11 ms generate identical two-row exposure means across all 20 frames. The estimator rejects the flat brightness sequence. The observation map is many-to-one, so a nominal shutter timestamp cannot resolve it.

## Exploratory adversarial nuisance failures: residual clearance is not sensor calibration

Two nuisance conditions, **not preregistered as successful controls**, were added and preserved as negative evidence rather than changing the frozen fit thresholds:

- Nonlinear gamma=1.6 camera response returned `SYNTHETIC_IDENTIFIED` with RMSE **0.008929**, although the fitted affine brightness model was false.
- A three-tap temporal LED/sensor blur (weights 0.25, 0.5, 0.25) also returned `SYNTHETIC_IDENTIFIED` with RMSE **0.016153**, despite the wrong instantaneous light-response assumption.

In these particular fixtures the recovered timing triple happened to be correct. **That does not vindicate the response model.** The gate can accept a misspecified sensor transfer function. Consequently, a good coded-light fit cannot by itself authenticate exposure support, temporal impulse response, radiometric linearity, clock provenance, or a worst-case timing uncertainty. These failures block promoting the simulated estimator to a real-camera calibration certificate. The frozen thresholds were not tightened after observing these outcomes.

Geometry, gaze, glasses, eyelid localization, blur of anatomy, sensor clipping, and inter-camera clock uncertainty remain outside this timing-only model. Their absence is a reason to abstain on physiological claims, not an implicit robustness success.

## Prior-art priority audit

This is an **instrument-design application of established optical timing/system-identification principles**, not a novel LED synchronization theorem. Relevant primary work:

1. Smid and Matas, *Rolling Shutter Camera Synchronization with Sub-millisecond Accuracy* (2019), https://arxiv.org/abs/1902.11084 . Demonstrates flash-based rolling-shutter temporal synchronization with reported 0.3–0.5 ms standard deviation on a multi-camera recording.
2. Huai et al., *Automated rolling shutter calibration with an LED panel*, Optics Letters 48(4), 847–850 (2023), https://doi.org/10.1364/OL.474375 . Calibrates line delay using LED patterns and actual consumer/industrial cameras.
3. Schatz, *Measurement of the timing behaviour of off-the-shelf cameras*, Measurement Science and Technology (2017), https://doi.org/10.1088/1361-6501/aa5d8a . Uses controlled illumination to measure camera timing and reports non-ideal sensitivity/photometric behavior.

## Concrete physical validation and human-study handoff

**Stage A, real instrument (not yet performed):** obtain an independently clocked LED controller and photodiode/oscilloscope or logic-analyzer capture; use an ordinary camera with locked manual exposure, gain and focus. Record raw sensor-row brightness and the physical LED pulse trace on a common clock, with per-run source hashes and device settings. Preregister coded vs periodic, shutter phase, 4/8/12-ms exposure conditions, row-delay estimates, and 0/5/10-ms controlled timing changes where hardware supports them. Repeat under gamma/ISP, autoexposure, LED rise/fall time, rolling-shutter rows, clipping, missing frames, clock drift and ambient flicker. Validate on **unseen** pulse sequences and camera settings. Compare estimated exposure intervals against independently measured optical sensitivity, not metadata alone. Reject if confidence regions are multimodal, reference time is unauthenticated, or transfer/blur is unresolved. A real photodiode pulse trace alone does not directly measure a camera's shutter gate; use timed illumination sweeps or independent camera exposure measurements to validate the shutter model.

**Stage B, mechanical aperture:** place an opaque moving aperture/fiducial in the same optical field, independently measure its motion and synchronized exposure times, then freeze predicted feasible hidden crossings before inspecting the high-speed reference. Include geometry, illumination, blur and dropped-frame adversaries. This validates instrument geometry/observation transfer only, never human velocity.

**Stage C, human:** use the existing private E002-502 blinded two-rater S01 handoff for a feasibility pilot; collect participant-disjoint consented high-speed eyelid sequences and independently authenticated timing. Freeze E002-371/538/539 exclusion predictions using independently justified **continuous-time** motion envelopes; sampled cohort peaks are not hard bounds. Treat absent reference crossings as censored when high-rate sensitivity is insufficient. Report per-participant abstention and error, with gaze/glasses/brightness/blur strata. E002-537 already shows 12 calibration participants cannot furnish a nontrivial distribution-free 95% split-conformal participant-level guarantee; E002-509 requires 299 independent zero-error participants for a fixed-challenge 1% risk upper bound at 95% confidence under its assumptions.

## Product consequence and stop decision

Coded illumination is a **candidate tool for future camera calibration**, not a certified physiological measurement or a production feature. Do not promote a timing fit into a hidden-closure exclusion. The model's acceptance of gamma and temporal blur is a concrete release blocker: require independently measured response and timing uncertainty, or abstain. No new human anatomical ratings, physical shutter/clock acquisitions, hard human speed or acceleration ceilings, or participant-disjoint physical predictions occurred. Keep `ABSTAIN_UNCALIBRATED`, production `BLOCKED`, draft PR unmerged. Stop further software-only coded-light threshold search until actual physical captures become available. Hush PR #45 remains untouched.
