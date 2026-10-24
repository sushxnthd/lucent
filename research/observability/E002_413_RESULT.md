# E002-413 — Real-human optical-proxy nuisance survivorship falsification

**Status:** Retrospective, independently testable audit of the preregistered E002-412 experiment. Written 2026-10-24 after observing E002-412's outcome. This is **not** a preregistered new experiment. Evidence tier: checksum-verified human-eye video, fixed exploratory optical-darkness proxy, digitally simulated nuisances and point-decimation. No independently calibrated physical eyelid aperture, shutter response, velocity bound, camera clock, blink labels or clinical outcome.

## Provenance and reproducibility

Source: [E002-412 successful workflow run](https://github.com/sushxnthd/lucent/actions/runs/40071978620), real-human-aggregate job 120807274103, completed 2026-10-24 06:59 UTC. The job printed the exact aggregate stored in `E002_413_AGGREGATE.json`. Source S01/S19 ZIP MD5s were checked in the workflow; 8 selected 0.5-s human-eye clips, 632 frames, 623 valid clean proxy values, 8/8 dynamic clips. No source frames, source timestamps, event/control linkage, or per-clip scores are published.

Reproduce this audit without redownloading private eye videos:

```sh
cd research/observability
python test_e002_413_robustness_gate.py
python e002_413_robustness_gate.py --input E002_413_AGGREGATE.json
```

The audit explicitly corrects a **survivorship interpretation** of E002-412's H4. H4 asked for >=95% stability *among jointly valid frames*, and did pass as preregistered. That does **not** establish >=95% end-to-end repeatability across all input frames, because invalid transformed frames disappear from H4's denominator. We make no claim that the preregistered H4 itself was computed incorrectly.

## Human-video results and end-to-end decision

| Nuisance | Joint valid / 632 | Conditional fraction with abs score change <=0.08 | Conservative stable fraction of all frames | Transfer decision |
|---|---:|---:|---:|---|
| Gain x0.70 | 474 / 632 (75.00%) | 100.00% | 75.00% | **REJECT** |
| Gain x1.30 | 623 / 632 (98.58%) | 100.00% | 98.58% | Pass this *necessary* control |
| Gaussian blur sigma 2 | 622 / 632 (98.42%) | 100.00% | 98.42% | Pass this *necessary* control |
| Translation +8,+6 px | 621 / 632 (98.26%) | 45.41% | ~44.60% | **REJECT** |
| Central white glare | 0 jointly valid | Not defined | Not defined | **632/632 correctly abstained** |

Of 623 clean-valid frames, only 474 remain jointly valid at gain x0.70: **149 clean-valid observations (23.92%) lose the measurement under reduced brightness**. The clean-relative coverage is 474/623 = 76.08%. A conditional 100% stability statistic cannot override these abstentions. Translation changes the proxy beyond the threshold for approximately 54.59% of jointly valid frames. The 95% end-to-end stability/coverage criteria introduced in this retrospective audit therefore fail for reduced brightness and translation. They are diagnostic gates, **not** claims of prospective preregistration.

## Temporal point-decimation (real video, exploratory proxy)

Across 8 clips x 16 sampling phases = 128 phase/clip combinations per simulated rate, the fraction losing >10% of the high-speed optical-proxy range was:

| Rate | >10% proxy-range loss | Median captured range | Worst captured range |
|---|---:|---:|---:|
| 15 Hz | 80/128 = 62.50% | 84.37% | 36.77% |
| 30 Hz | 48/128 = 37.50% | 95.66% | 69.68% |
| 60 Hz | 26/128 = 20.31% | 100.00% | 76.54% |

Thus at 30 Hz, the worst tested sampling phase lost **30.32%** of this optical proxy's observed high-speed range. This is an observed image-proxy aliasing result, **not a missed-blink probability or physical hidden-closure frequency**. Phase combinations share clips and participants and are not independent human trials. Exposure integration and actual camera shutter effects were not simulated.

## Product consequence and scientific next step

**Reject the fixed darkness proxy as a transferable physical eyelid-closure measurement.** The safe white-glare abstention and some conditional brightness/blur stability do not rescue the large translation sensitivity or brightness-induced missingness. Retain `ABSTAIN_UNCALIBRATED` for no-hidden-closure guarantees, blink duration, PERCLOS and fatigue claims. The attached standard-library-only gate enforces this interpretation on the verified aggregate and refuses to promote any passing synthetic controls into a physical certificate.

**Priority:** stop adding optical surrogate families. Obtain two independent blinded E002-407 full-event landmark sheets; adjudicate using E002-408; then validate the E002-371 shutter-gap predictions against independent camera exposure and physical velocity calibration on untouched participants. The exact observational boundary remains mathematically conditional, not empirically validated.

**Limitations:** only two source participants, selected EEG event/control windows, fixed crop, non-anatomical image proxy, digitally introduced nuisances, shared correlated frames, no glasses/gaze/geometry-domain validation, no real ordinary-camera paired recordings, and no human ground-truth aperture. This experiment is a falsification of a proposed product surrogate, not a world-class physical measurement validation.
