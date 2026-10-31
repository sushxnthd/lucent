# E002-506 | Optical-pulse clock calibration: a falsifiable instrument design boundary

Date: 2026-10-28. Primary E002-371 branch and draft PR #26. Frozen protocol: [E002_506_FROZEN.md](E002_506_FROZEN.md). Executable: [e002_506_optical_pulse.py](e002_506_optical_pulse.py). **Evidence: synthetic instrument-model falsification, not a physical camera or human validation.**

## Conditional numerical result

Suppose two externally timed optical edges (each with +/-0.1 ms time bracket) are independently verified to occur within known native frame exposures, under an affine global-shutter clock with a calibrated 10-ms exposure. The code projects those constraints onto an exact rational interval for frame period T, then propagates the worst allowed blind gap through the existing E002-505 scalar hidden-closure bound (V=60/s, exposure mean 0.999 +/-0.001, closure threshold 0.2). These physiology and acquisition inputs are **stipulated**, not observed.

| Optical edge separation | Largest compatible period | Conservative risk upper | Conditional classification |
| --- | ---: | ---: | --- |
| 3 native frames (nominal 0.1 s) | 36.733333 ms | 0.850989795 | Not excluded |
| 300 native frames (nominal 10 s) | 33.367333 ms | 0.750009795 | Excluded **only if premises hold** |
| 300 frames, shutter minimum unmeasured (0 to 10 ms) | 33.367333 ms | 1.050009795 | Not excluded |

An independent JavaScript floating-point calculation reproduced the 3/300-frame reversal and missing-shutter failure. The exact-rational Python implementation includes 11 adversarial controls, including contradictory third pulse, duplicate indices, invalid event brackets, nonfinite values, widening timing brackets and unconditional product abstention. **Hosted verification is pending at this report's creation; do not report CI as passed until the exact-head run completes.**

The exact pairwise period constraints for idealized edge-in-exposure observations are given in the frozen protocol. Importantly, they rely on externally authenticated pulse times, independently established exposure overlap and no dropped native frames. An ordinary display's refresh rate or video-container FPS is not independent timing evidence. A 300-frame span can tighten clock-period uncertainty but **cannot replace shutter-duration calibration**.

An exploratory independent arithmetic sweep (not part of the preregistered 3/300 cases) places the conditional transition between 5 and 6 frame separation for these hypothetical inputs: 5 gives risk 0.810189795 and 6 gives 0.799989795. The 6-frame margin is extremely small and should not be interpreted as an instrument specification without independent timing, shutter and nuisance margins.

## Executable human/physical validation handoff

1. Preserve the existing private S01 E002-502 packet and obtain two genuinely independent, blinded anatomical reviews. This is a feasibility pilot, not a camera-speed or hidden-closure validation.
2. On a no-cost local bench, use an **independently calibrated optical timing source**, not a phone UI animation. Record pulse edge timing against a second reference (e.g., externally characterized photodiode/oscilloscope or traceable timing equipment). If this cannot be obtained at zero cost, mark the clock uncalibrated and stop rather than inventing precision.
3. Capture a sequence of edges at both short and long separations. For each event, independently establish which exact native frame exposure overlapped the edge and its uncertainty. Detect dropped/reordered frames, rolling-shutter row offsets, autoexposure changes, brightness clipping and blur; exclude ambiguous attributions. Fit an affine clock only after testing residual drift; non-affine clocks require a different model.
4. Measure shutter exposure start/end independently, with an uncertainty interval, for the same pixel row used to measure the eyelid. An optical edge merely visible somewhere in an image is not proof of edge-in-exposure attribution.
5. Freeze participant-disjoint high-rate human recordings and low-rate sampling masks **before** examining high-rate closure labels. Include independently measured geometry/iris scale, gaze, glasses, brightness, blur, missingness, clock and rolling shutter. Count false exclusions, coverage and abstentions; preserve every counterexample. Finite differences are not a continuous-time speed upper bound.
6. If independent timing, exposure, anatomy or speed envelopes remain unavailable, report measurement feasibility and keep all deterministic closure and fatigue claims disabled. External replication is required before any product release.

## Limits and decision

This instrument result is a **new conditional clock-calibration design test**, not a validated boundary law for human eyelids. There are zero new human ratings, zero authenticated camera/shutter measurements, zero independently certified human continuous-time speed envelopes, and zero participant-disjoint physical predictions. Do not perform another synthetic refinement on this example without external observations.

E002-371 physically unvalidated. Product `ABSTAIN_UNCALIBRATED`. Release `BLOCKED`. Hush remains on its separate branch and draft PR.

## Hosted independent verification (2026-10-28)

[GitHub Actions run 40686150586](https://github.com/sushxnthd/lucent/actions/runs/40686150586) **completed successfully** on executable/workflow commit `c594ef118688d80fca2fad98dbba188ab9ccabe6`. The frozen Python adversarial-controls step and independent Node arithmetic step both succeeded. The Python source defines **11** frozen test methods. This verifies software arithmetic and input rejection under stipulated synthetic premises, **not** any physical optical clock, camera exposure, eyelid velocity, anatomy, or held-out human prediction. Subsequent report-only commits do not change the verified executable. Product and release gates remain unchanged.
