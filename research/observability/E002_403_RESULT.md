# E002-403 — shutter temporal-response falsification and enforceable first-moment calibration

**Date:** 2026-10-24. **Frozen protocol:** [E002_403_PROTOCOL.md](E002_403_PROTOCOL.md), committed at `1cc882c` before experiment implementation. **Evidence tier:** deterministic analytic witness, 1,000 seeded adversarial synthetic acquisitions, independent pulse quadrature and source-level regression. **Not** human validation, measured physical camera shutter response, or a new general theorem.

## New wrong-certificate witness

The reference-adequacy certificate previously substituted the uniform shutter temporal first absolute moment `e/4` for every calibrated exposure. E002-401 also accepted equal row exposure profiles without verifying temporal *weight uniformity*. Two adjacent exposures with different, nonuniform electronic temporal response can therefore produce a wrong no-closure certificate despite an independently correct physical velocity bound.

Set `a(t)=0.19+20|t-0.005|`, threshold 0.20, nominal frame centers `0` and `0.010` s, exposure duration `e=0.010` s, and exact independent velocity bound `V=20/s`. The first exposure integrates a 0.2-ms rectangular pulse at the **earliest** edge; the second integrates the same-width pulse at the **latest** edge. The two observed exposure means are both `0.388`, although the true physical aperture crosses to `0.19` at `t=0.005`.

Under the incorrect uniform weighting assumption, each frame's lower instantaneous center bound is `0.388 - 20(0.010/4)=0.338`; the minimum Lipschitz envelope between frame centers is `0.338-20(0.010/2)=0.238>0.20`. The old implementation therefore returns **CONFIRMED_NO_CROSSING**, a false physical certificate.

For the actual temporal kernels, the first absolute moments are `0.005-0.0002/2=0.0049` s. Corrected center lower bounds are `0.388-20(0.0049)=0.290`, and the minimum interval envelope is `0.190<0.20`: **UNRESOLVED**, correctly allowing the hidden crossing. With truly uniform shutters on the same trajectory, the observed means are `0.290` and the certificate is also unresolved.

## General operational law

For normalized, nonnegative temporal exposure weights `w_i(s)` supported on the calibrated exposure interval and an independently bounded Lipschitz aperture speed `V`:

```
M_i = integral |s - t_i| w_i(s) ds
|a(t_i) - exposure_mean_i| <= V M_i.
```

The factor `e_i/4` is valid for uniform exposure weighting, **not** arbitrary rolling-shutter or temporally modulated camera responses. For any unknown nonnegative normalized shutter kernel with verified support `[t_i-e_i/2,t_i+e_i/2]`, `M_i <= e_i/2` is conservative. If even support is not independently established, no deterministic shutter-time certificate is allowed. A useful dimensionless acquisition diagnostic is `kappa_i=4M_i/e_i`: uniform shutter `kappa=1`; edge-concentrated shutters approach `kappa=2`. This is an application of the weighted Lipschitz inequality, not a new mathematical theorem.

## Frozen experiment and enforcement

The reproducible experiment `e002_403_shutter_kernel.py` tests the exact witness and 1,000 seeded cases with velocity 10–40/s, exposure 5–20 ms, narrow outer-edge temporal pulses and an independently known true threshold crossing. The independent oracle `e002_403_independent_check.py` numerically integrates 100 independently randomized pulse pairs and exercises the human annotation bridge.

The source correction adds an optional explicit per-frame upper bound `temporal_first_abs_moment_s` to the physical reference `Frame`. The standalone E002-399 simulator continues to use `e/4` only under its *explicitly synthetic uniform-shutter* calibration. The human annotation bridge now **requires** `temporal_kernel_calibration.first_absolute_moment_fraction_upper` (range 0..0.5) and provenance before any physical certificate. It supplies the quantitative moment to every frame. Missing calibration returns `ABSTAIN_UNCALIBRATED`; malformed bounds are rejected. Increasing the moment bound cannot strengthen a certificate. A provenance string is **not** external verification.

The E002-399/400/401/402 independent checkers are retained and updated to declare synthetic verified uniform temporal weighting in their positive controls. Dedicated CI workflow: `.github/workflows/e002-403-shutter-kernel.yml`.

## Physical-camera calibration and human validation required

A real-camera test must measure the exposure kernel, not assume it from nominal shutter speed. Synchronize a high-bandwidth LED/photodiode pulse generator with sensor output; phase-sweep a narrow light pulse through each nominal exposure; measure intensity response versus offset at multiple brightness levels, row positions, ISO/gain settings, codecs, and temperatures; deconvolve the independently measured pulse width; bound response normalization, nonnegativity, support, first absolute moment, phase jitter and frame-to-frame changes. Repeat with rolling shutter, automatic exposure, HDR, flicker reduction and dropped frames. If temporal response changes with row or acquisition mode, propagate the **worst independently bounded** first moment or abstain.

Only after this instrument calibration, independently annotated upper/lower human eyelid trajectories, validated anatomical geometry, and independently bounded human velocity should E002-371 predictions be frozen on untouched participants/devices. The previous two-participant EEG-proxy results do **not** supply physical aperture ground truth.

**Product boundary:** No uncalibrated hidden-closure exclusion, blink duration, PERCLOS or fatigue diagnosis. Keep draft PR #25 open. The strongest currently justified capability is conditional measurement qualification with abstention.
