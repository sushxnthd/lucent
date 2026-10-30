# E002-550 RESULT | A real 400-Hz human eyelid-kinematics source changes the validation design

2026-10-30. Primary E002-371 kernel. [Frozen protocol](E002_550_FROZEN.md) committed first at `e509e2314ee80acba19241648406f48d362552a6`, before the executable and tests. **Evidence: primary-literature source qualification plus conditional mathematical/instrument software; no restricted human records accessed, no physical measurement.**

## Substantive new source and scientific consequence

The 2026-09-01 FaceBase release [88-28BJ](https://doi.org/10.25550/88-28BJ) reports 3D eyelid-margin motion capture at **400 frames/s**, hardware-synchronized with intramuscular EMG, in **eight adults** performing spontaneous, voluntary, reflexive, soft, and forced eyelid behaviors. Raw data are **restricted access**, with General Research Use and Not-for-profit Use Only limitations. The associated [2025 PNAS primary study](https://doi.org/10.1073/pnas.2508058122) reports behavior-dependent **two-dimensional** eyelid kinematics, not a universal one-dimensional opening/closing trajectory. The source provides a more relevant prospective human-velocity test than nominal 150-fps Phantom metadata or ordinary video labels. It is not an authenticated 400-fps continuous-time anatomical ground truth and not yet a permitted commercial training source.

**Claim change:** a scalar palpebral aperture bound, even if ultimately validated at one vertical slice, must not be presented as a whole-eyelid blink-type or fatigue biomarker without separate 2D and cross-behavior validation. A sample-rate claim does not certify the hard continuous-time speed ceiling needed by E002-371.

## New falsifiable speed-certificate requirement

For observed normalized aperture samples `y_i`, nominal adjacent spacing `d_i`, bounded aperture observation error `e`, bounded per-timestamp error `u`, and an **independently physically justified** hard continuous-time acceleration bound `A`, a conservative local velocity ceiling is:

`U_i = (|y_(i+1)-y_i|+2e)/(d_i-2u) + A(d_i+2u)/2`, provided `d_i>2u`.

The mean-value identity bounds the true secant from the observations, while a hard Lipschitz bound on velocity controls instantaneous departure from that secant by at most `A*actual_interval/2`. Over complete contiguous coverage, `max_i U_i` bounds the scalar velocity conditionally. This is a standard bounded-acceleration sampling inequality, **not a novel mathematical theorem**. The exact calibration of A/e/u, marker-to-anatomy geometry and optical transfer must come from independent physical evidence; no such certificates exist here. A hard A cannot be obtained merely by taking the maximum sampled acceleration.

### Frozen constructed test outcomes (NOT human data)

| Test | Result |
|---|---|
| Exact linear 400-Hz samples 0.4 to 0.5, A=e=u=0 | Conditional speed upper = **40/s** |
| Same, stipulated A=1000/s² and e=0.01, u=0 | Conditional upper = **49.25/s** |
| Same, stipulated u=0.1 ms | Conditional upper = **53.523913/s** |
| 400-Hz sinusoid `0.5+0.2sin(10*pi*t)`, stipulated hard A=200/s² | Sample secant max **6.276728/s**, conditional upper **6.526728/s**, analytic true peak **6.283185/s** |
| Flat 400-Hz samples, no independent A | **ABSTAIN**, despite zero sampled speed |
| Unknown marker identity, occlusion, blur, gaze, illumination, geometry or missing coverage | **ABSTAIN** |

The constructed between-sample triangular spike with fixed amplitude and shrinking width shows why no finite upper bound follows from finite differences alone. No physiological claim follows from these illustrative parameter values.

## Implemented and verification

- [Fail-closed conditional calculator](e002_550_conditional_velocity.py), requiring explicit complete coverage, all nuisance checks and finite externally stipulated A/e/u; always returns `CONDITIONAL_BOUND_ONLY_NOT_AUTHENTICATED` or `ABSTAIN_NO_HARD_SPEED_CERTIFICATE`. Never returns a human certificate or product approval.
- [15 Python adversarial test methods](test_e002_550_conditional_velocity.py) for the analytic sinusoid, noise, acceleration, clock, missingness, all nuisance gates, malformed values and unbounded intersample speed.
- [Independent Node.js arithmetic replay](e002_550_independent.cjs).
- [Dedicated hosted workflow](../../.github/workflows/e002_550_kinematics.yml) committed. **Hosted CI was queued at reporting time; do not claim hosted success.** Synthetic arithmetic was also independently checked offline, including sinusoid max 6.526727658227621/s and clock-widened upper 53.52391304347827/s.

## Next decisive physical/human experiment

Request authorized access to FaceBase 88-28BJ through its controlled-access procedure; do not bypass the restrictions. Preserve the frozen participant-disjoint four/four split, all five behaviors, 3D rigid head geometry and the full nuisance table. Independently measure marker-localization/clock bounds and a defensible acceleration bound. If A is not independently bounded, report observed secant speeds as **lower-bound evidence only** and refuse E002-371 certification. Test the locked 30-Hz/10-ms shutter counterfactual against held-out motion after calibration, retaining all negatives as censored where reference sensitivity is unknown. In parallel, complete the already prepared two-person blinded S01 anatomical review and photodiode-authenticated shutter acquisition. The restricted FaceBase dataset is not a replacement for those instrument measurements.

**Human kinematics analyzed: 0. Independent anatomical ratings: 0. Authenticated physical shutter captures: 0. Certified continuous-time human speed bounds: 0. Held-out physical predictions: 0.**

Lucent `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. Hush PR #45 unchanged. No merge, force-push or deployment.
