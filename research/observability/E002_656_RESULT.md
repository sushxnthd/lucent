# E002-656 | Row-dependent timestamp error can reverse a closure certificate

**Evidence tier:** deterministic synthetic counterexample, not measured camera hardware or human evidence.

## Result
For a V-Lipschitz scalar eyelid aperture a(t), a uniform exposure average y centered at the *actual eye-row exposure time* s with duration e satisfies a(t) >= y - V(|t-s| + e/4). If the reported nominal center is n and |s-n| <= delta, the conservative bound is a(t) >= y - V(|t-n| + delta + e/4). This follows from the triangle inequality and the exact rectangular shutter mean absolute offset e/4. It is conservative rather than jointly sharp for multiple measurements.

## Constructive falsification
The executable `e002_656_rolling_shutter.py` uses a(t)=0.2+4|t-0.5|, closure threshold 0.3, nominal frame centers (0.46,0.54), actual eye-row centers (0.42,0.58), and exposure duration 0.02. Exposure means are both approximately 0.52. A nominal-center certificate predicts minimum aperture at the midpoint exceeds threshold by **+0.06**, although actual aperture at 0.5 is **0.20**. Accounting for independently bounded row-time error 0.04 and shutter integration changes the conservative certificate margin to **-0.12**, requiring abstention. The simulated row-time errors deliberately point in opposite directions; they represent uncertainty across two captures, not a claim about a particular camera's scan direction.

## Product consequence
A timestamp attached to a video frame is not automatically an eye-row exposure timestamp. Even if the exposure duration is known, a shutter-gap certificate must incorporate verified row timing, timestamp origin, clock jitter, and exposure-kernel calibration. Without those quantities, remain `ABSTAIN_UNCALIBRATED`; do not infer blink absence from nominal frame cadence.

## Reproduction and limitations
Run `python3 research/observability/e002_656_rolling_shutter.py`. Dependency-free, exact piecewise integral, deterministic assertions. This is not a new empirical validation, not a calibrated rolling-shutter sensor, and not a human measurement. Next falsification: acquire synchronized LED/photodiode timing across eye-image rows, estimate row offsets without looking at blink labels, then score held-out high-frame-rate eyelid trajectories with the predeclared E002-653 protocol.
