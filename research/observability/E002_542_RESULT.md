# E002-542 RESULT | Crossed illumination falsifies two falsely reassuring shutter fits

2026-10-30. Primary E002-371 measurement-science kernel. Frozen protocol: [E002_542_FROZEN.md](E002_542_FROZEN.md), committed at `ddc0acc` **before** the executable, independent replay, and tests. Same persistent research branch, draft PR #26. **Evidence tier: synthetic instrument-transfer falsification only. No new physical camera, photodiode, eyelid, or human measurements.**

## Scientific question and outcome

E002-541 found two realistic sensor-response misspecifications that passed a binary-coded shutter-timing fit. Here the E002-541 estimator is **unchanged**: fit timing, gain and offset on amplitude-one coded illumination; freeze them; test on unseen illumination amplitudes and isolated 1-ms flashes immediately outside the predicted shutter interval. The challenge is not fitted or used to choose timing.

| Frozen transfer test | Original training RMSE | New held-out error | Frozen decision |
| --- | ---: | ---: | --- |
| Linear radiometry, amplitude 0.25/0.50 | 0.000000 | RMSE 0.000000 | Pass synthetic control |
| Gamma 1.6, amplitude 0.25/0.50 | 0.008929 | RMSE **0.026307** | **Falsified** at 0.025 |
| Instantaneous response, edge flashes | 0.000000 | max absolute 0.000000 | Pass synthetic control |
| Three-tap temporal blur, edge flashes | 0.016153 | max absolute **0.017679** | **Falsified** at 0.015 |

Both nuisance training fits still returned `SYNTHETIC_IDENTIFIED` and recovered the correct injected timing (7,8,5) ms. Thus the new test does **not** demonstrate timing bias; it demonstrates that a model can recover the right timing for the wrong sensor-transfer reason, and that independent illumination interventions can expose this error. The phase/exposure/row-delay estimator itself is not reoptimized.

**Sensitivity warning:** the gamma failure margin is only 0.001307 brightness units above the preregistered 0.025 cutoff, and the blur failure margin is 0.002679 above the 0.015 cutoff. These synthetic reversals are not robust to unspecified noise, illumination uncertainty, gamma changes or sensor ISP behavior. Do not extrapolate them to physical devices without a measured noise floor and uncertainty analysis. The edge-flash construction deliberately targets the injected shutter boundaries; a real experiment must sweep unknown phases rather than using the true phase.

Negative controls: incorrect reference code, duplicate sample identity, 15/20 frames, and saturated samples return `ABSTAIN`. No physical attestation is inferred from a synthetic result. The experiment's no-retuning constraint is intentional: E002-541's heuristic residual thresholds are **not** calibrated statistical tests.

## Reproducibility

- [Frozen protocol](E002_542_FROZEN.md) precedes the code.
- [Python experiment](e002_542_crossed_stimulus.py) imports the unchanged E002-541 estimator and produces all held-out predictions.
- [14 adversarial tests](test_e002_542_crossed_stimulus.py) cover control pass, nuisance acceptance, new falsifications, pulse support, incorrect reference, missingness, duplicate identities, saturation and explicit noncertification.
- [Independent Node replay](e002_542_independent_replay.cjs) separately implements LCG illumination, affine least squares, convolution and held-out arithmetic.
- [Dedicated GitHub Actions workflow](../../.github/workflows/e002_542_crossed_stimulus.yml) runs all three and checks that no product certification is emitted.

The independent Node arithmetic calculated gamma RMSE 0.0263067296 and blurred-edge maximum residual 0.0176790, agreeing with the Python formulas to the reported precision. **Hosted CI status must be checked separately; no hosted pass is claimed here.**

## Practical physical validation consequence

A real coded-light calibration must be challenged with **held-out optical stimuli**, not just a good training fit. Use photodiode-recorded LED emission, dark/bright references and calibrated intermediate LED intensities; hold camera settings fixed. Add independently timed 1-ms-or-shorter flashes swept across candidate exposure edges. A source-side photodiode alone does not measure the camera shutter gate: compare the sensor's native pixel response to the measured optical waveform, including rolling rows and ISP/RAW differences, under a common independently verified clock. Predeclare allowable residuals from measured noise/uncertainty, not the synthetic cutoffs above. See [E002_542_PHYSICAL_HANDOFF.md](E002_542_PHYSICAL_HANDOFF.md).

A physical result could validate an instrument transfer envelope. It **cannot** supply a hard continuous-time human eyelid-velocity ceiling, confirm anatomical threshold crossing, or justify a hidden-blink absence claim. Follow with the existing E002-502 blinded two-rater packet and E002-519/525/527 prospective participant-disjoint study gates. Negative reference frames remain censored, never certified clear.

## Novelty, stop decision and release

Cross-validation with held-out illumination is established system-identification practice, not a new general theorem or first demonstration of camera calibration. E002-532/541 already established coded-light calibration and its nuisance limitations. **E002-542 contributes a narrowly preregistered counter-test of those two observed failures and a concrete physical acquisition consequence.** This completes the bounded synthetic preflight. No further software-only LED threshold tuning is justified without physical captures.

Physical shutter captures: **0**. Independent blinded anatomical ratings: **0**. Certified continuous-time human speed bounds: **0**. Participant-disjoint physical predictions: **0**. Lucent remains `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. Hush PR #45 unchanged; no merge, deployment, or schedule change.
