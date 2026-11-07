# E002-652 | Pre-registered physical acquisition stop/go gate (2026-11-04)

## Scientific decision
The E002-371 shutter-gap theorem is not empirically validated by the E002-642–651 synthetic protocols and logical counterexamples. Further refinement of the CSV analyzer is not a substitute for reference-timed camera measurements. **Freeze the current analyzer and stop generating new purely logical E002 variants until new independently acquired timing evidence exists.**

## Two distinct targets
1. **Instrument target:** establish whether the physical camera's effective integration windows, row timing, and sensor persistence agree with a *separately measured* timing envelope. A photodiode observing only the LED does **not** independently measure the camera shutter. Camera exposure must be characterized using a second, independently calibrated optical timing method (e.g. swept LED edge / stroboscopic row response, or direct shutter trigger where available), with uncertainty including rolling shutter, ISP latency, and clock alignment.
2. **Human target:** establish whether a high-frame-rate eyelid aperture trajectory, measured by blinded raters and calibrated with independent velocity bounds, produces the prespecified hidden-closure feasibility predictions under simulated ordinary-camera sampling. Instrument success alone cannot establish this.

## Frozen randomized physical challenge
For each camera mode, randomize (with recorded seed) LED-off controls, positive intersections, near-boundary intersections, and nominal guaranteed misses. Interleave conditions, not blocks. Collect at least 30 independent phase draws per condition; report all exclusions, dropped frames and corrupted captures. Positive controls must establish the pulse is optically detectable under the same exposure/brightness/ISP settings. Negative controls bound ambient and persistence false detections. Include two independently measured exposure envelopes and deliberately mis-specified timing envelopes as blinded challenge models. Require independent camera timebase and source timebase logs with uncertainty budgets, not only video metadata.

## Frozen analysis before acquisition
- **Primary endpoint:** rate of *source-attributed* positive LED signals among independently certified guaranteed-miss trials, with source attribution using randomized LED-off controls and time-localized reference traces.
- **Positive control endpoint:** detection probability of independently certified positive intersections above a separately calibrated minimum integrated contrast. A timing-only intersection is not an optical guarantee.
- **Calibration endpoint:** interval coverage of independently measured camera exposure timing by the proposed uncertainty envelope; report undercoverage and mode-specific drift.
- **Adversarial conditions:** varying brightness, blur, gain, compression, rolling-shutter row, missing frames, occlusion, clock drift and ISP temporal filtering.
- **Decision:** any confidently source-attributed pulse in an independently certified guaranteed miss is a falsification of the combined timing/exposure model (or its stated uncertainty); ambiguous attribution, failed positive controls, incomplete exposure enumeration, or inconsistent clocks force ABSTAIN. Negative-only trials never validate the model.
- Report per-camera-mode denominators and confidence intervals. Do not pool correlated rows as independent trials. Preserve raw files, instrument calibration logs, random seed, blinded labels and SHA-256 checksums.

## Human acquisition handoff
Acquire consented synchronized high-speed reference video and ordinary camera video, or use high-speed reference video with authenticated frame rate and exposure information. Freeze aperture annotation criteria, closure threshold, independently estimated per-participant velocity upper bounds, held-out participant split, and nuisance strata before testing. A shutter-gap exclusion claim is permitted only when the **worst-case** feasible closure is impossible under independently validated timing and velocity bounds; otherwise abstain. Do not claim sleepiness, fatigue, or health-state detection from this geometric exclusion.

## Release blockers
No human reference trajectories; no independently verified camera exposure envelope; no independent physiological velocity upper bound; no held-out human prediction test. Consequently product remains ABSTAIN_UNCALIBRATED and production BLOCKED. This document is an acquisition decision gate, **not** an executed study or empirical result.

## Stop rule
If no independently timed physical or authenticated high-frame-rate human measurements are available, do not label another synthetic test as empirical progress. Prioritize obtaining data, an independent collaborator, or a reproducible public acquisition. Preserve negative results and uncertainty.