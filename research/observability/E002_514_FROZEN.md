# E002-514 | Frozen coded-optical shutter calibration feasibility trial

Date: 2026-10-29. Primary E002-371 research branch, draft PR #26. Frozen before running the five held-out seeds listed below. Evidence tier: **synthetic instrument feasibility only**. This is not an anatomical study, hardware measurement, or certified camera shutter calibration.

## Hypothesis and falsification

Can a camera frame's exposure-start/end interval be identified **without nominal FPS or an affine clock assumption** from eight spatially separated, independently coded LED regions driven by a separately timestamped 1-ms optical stimulus, under an explicitly bounded linear-response/noise model? A set-valued inverse solver must retain **every** exposure interval consistent with the optical observations and return an upper bound on the blind gap, rather than a best-fit point estimate.

This addresses the specific E002-513 limitation: two distant timing anchors cannot certify a local shutter gap. The proposed instrument supplies *local, frame-specific optical signatures*. It must not infer human eyelid velocity or hidden closures.

## Fixed simulation, no threshold tuning

- Five held-out random seeds **101, 103, 107, 109, 113**; 40 frames per seed, with independent optical-code and camera-noise streams.
- Eight independent binary optical channels at exactly 1-ms ticks, 1,600-ms stimulus, camera exposure exactly 10 ms, frame-start nominal spacing 100/3 ms with per-frame integer jitter uniformly in [-2,2] ms, initial nominal start 20 ms.
- Camera response equals the mean of each LED's on/off samples over the exposure, plus independent uniform noise in [-0.004,0.004]. No saturation, nonlinear gamma, blooming, unknown optical mixing, clock drift, missing frames or rolling shutter in the positive-control model.
- The solver does **not** use the nominal frame period or true frame start. Exhaustively search **all** start ticks and exposure durations 8 through 12 ms within the optical-code record. Retain every interval whose maximum per-channel absolute residual is <=0.010. Empty feasible sets mean ABSTAIN.
- For consecutive frames with nonempty sets, compute the worst-case blind gap: max(0, max feasible next start - min feasible previous end). Do not substitute best-fit starts.
- Prespecified PASS on held-out simulation: 100% true exposures contained in feasible sets; zero unsafe underbounds; at least 80% of 195 adjacent gaps have nonempty sets; median conservatism <=2 ms. If any condition fails, publish failure, do not retune.
- Report per-seed counts and aggregate only. No claim of physical validity follows even if all conditions pass.

## Adversarial kill controls

1. Missing optical channel, unmeasured camera response/gain envelope, optical clock phase uncertainty, uncalibrated rolling-shutter line position, missing native frame, nonlinearity/saturation, motion/blur, unknown lighting or sensor mixing **must block physical certification**. Synthetic solver may be used to demonstrate failure, but cannot infer calibration validity from a small residual alone.
2. An intentionally perturbed ±15% per-channel gain is an **out-of-model stress**, not evidence of safe rejection unless a separate, independent calibration check rejects it.
3. Random optical-code seed and acquisition timestamps must be attested by an independent photodiode/logic analyzer, not a screen animation, video FPS header or software timer.
4. If the actual sensor response cannot be bounded by the chosen forward model, the interval set is not guaranteed to contain truth. Fail closed; never claim physical shutter-gap coverage from simulated set coverage.

## Concrete next human/instrument study

Use a hardware-timestamped LED pattern generator plus independent photodiode or logic analyzer, eight separately imaged LED patches, locked camera exposure/gain/white balance, a dark/flat radiometric calibration and an external trigger/clock cross-check. Record exact stimulus waveform and acquisition uncertainty, raw frame pixel means, camera scan direction/line-delay or verified global shutter, sensor-row geometry, and dropped frames. Pre-register timing residual and uncertainty bounds from independent calibration trials, then evaluate unseen exposures, lighting, blur, glasses/occlusion and camera configurations without tuning.

Separately, finish the already frozen E002-507 two-rater S01 anatomical packet. Only after both independent anatomical labels and physically calibrated per-gap exposures exist should E002-371 be tested on participant-disjoint high-rate sequences with a separately justified continuous-time eyelid-speed envelope. If any premise is missing, the product remains `ABSTAIN_UNCALIBRATED` and release `BLOCKED`.

Hush PR #45 is untouched. No raw human images or reviewer records belong in GitHub.
