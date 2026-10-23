# E002-394 — executed dual-clock test (2026-10-23)

**Evidence:** verified CC0 Eye-BCI S01 human recording, MD5 `fef02cb7ebf62e4f3efb6303284fd6cb`; independently reproduced in [GitHub Actions run 39956772866](https://github.com/sushxnthd/lucent/actions/runs/39956772866). Frozen protocol: `E002_394_FROZEN.md`, committed before examining Phantom clock values.

## Frozen predictions: mixed result; do not count CI success as scientific success

- **Independent Phantom clock: FAILED/UNAVAILABLE.** All 53,680 `PhanTime` fields failed the preregistered seconds/HH:MM:SS parser (0% qualified). Therefore no camera-versus-EEG clock agreement can be claimed; the frozen >=95% within 2 ms prediction is **not met**. Do not silently fit units or use AVI 1-fps timestamps.
- **Gap sensitivity: PASSED conditional stability criterion.** Active rate varies with the predeclared gap cutoff: 15 ms -> 152.41027 fps (158 gaps); 20 ms -> 152.21778 fps (116); 30 ms -> 151.91151 fps (79); 50 ms -> 151.45816 fps (41). Spread 0.95211 fps < 1 fps. This does **not** resolve disagreement with the publication's nominal 150 fps.
- **Hypothetical shutter-marker coverage: PASSED (limited).** Across 100 uniform phases, 93 eligible EEG marker timestamps had mean coverage exactly equal to shutter duty cycle (30/60/120 Hz, 1/5/10 ms). Example 30 Hz/10 ms: mean 30%, phase range 17–44 of 93 markers; 60 Hz/5 ms: mean 30%, range 17–37. This is largely a geometric phase-averaging identity, **not an independent physiological discovery, actual blink detection, or a shutter-gap theorem validation**.
- **AVI timebase falsification retained:** 1 fps metadata is incompatible with sidecar frame-index cadence; the 150 fps source-paper value is not independently verified by a recovered camera clock.

## Independent verification and reproducibility

The dedicated CI job finished **successfully**, independently reparsed the verified archive, and checked 53,680 frames, 414,720 synchronization rows, 93 eligible markers, and the product abstention outcome. CI result artifact `e002-394-dual-clock-aggregates` (ID 12501909900; expires 2026-11-06) contains the exact aggregate JSON. Source scripts: `e002_394_dual_clock.py` and `e002_394_independent_check.py`.

## Consequence and next test

The human eye-video timing pipeline is now *EEG-clock-indexed only*. Without a qualified independent acquisition clock, exposure start/end, independently measured eyelid aperture, speed envelope, optical nuisance bounds and untouched participants/devices, hard E002-371 no-hidden-closure certificates are **not admissible**. Product: `ABSTAIN_UNCALIBRATED`.

Next: use the verified human video to evaluate a **strictly surrogate** video-only blink-associated image signal against untouched EEG marker windows and nuisance controls. Do not treat that surrogate as physical aperture or calibrate E002-371 from it. The necessary physical paired study remains a release blocker.
