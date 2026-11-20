# E002-572 RESULT | Independent-edge timing instrument substitute

Date 2026-10-31. Frozen protocol committed first at [79c1409](https://github.com/sushxnthd/lucent/commit/79c14092888edf2551f9d74c3ff3672ce92e2323), then executable, tests and hosted workflow. This is **synthetic optical-instrument verification only**, not new human eyelid data, not a calibrated physical camera and not a new physiology theorem.

## Result

A photodiode-timed optical transition observed inside a verified raw-linear, fixed-shutter exposure yields a bounded exposure-start time without trusting camera FPS metadata. For rising edges, the independently measured post-edge fraction f satisfies s=t-w(1-f); falling edges must convert the measured fraction to *post-edge darkness*. The program intersects conservative affine clock constraints in (offset, rate), and **does not refit on held-out optical edges**.

Frozen synthetic oracle: true clock offset 12 ms, rate 1.000020, shutter 4 ms. Four calibration edges at camera timestamps 0/10/20/30 s with post-edge fractions 0.2/0.4/0.6/0.8, ±50 μs photodiode uncertainty, ±0.01 fraction uncertainty, ±30 μs row-skew allowance and shutter width interval [3.95,4.05] ms.

- Feasible calibration polygon: **8 vertices**; independently generated true affine clock satisfies every calibration interval.
- Clean held-out edge at camera time 40 s: independently inferred exposure start **[40.0126545, 40.0129445] s**; calibration predicts **[40.01257283, 40.01302617] s**. Result **CONSISTENT**.
- Same held-out edge with +10 ms independent reference delay: measured interval **[40.0226545, 40.0229445] s**; predicted interval unchanged. Result **CONTRADICTION**.
- One corrupted calibration reference edge shifted +10 ms: **CALIBRATION_REJECTED** rather than silently deleting an outlier.
- Non-affine 20-ms final-edge perturbation: **CALIBRATION_REJECTED**.
- Saturation, uncertainty crossing a plateau, absent independent timing uncertainty, negative shutter interval, nonfinite/bool timestamps and insufficient distinct clock coordinates: fail closed.

## Reproduction and independent checks

[Executable](e002_572_optical_edge_calibration.py) · [14-test suite](test_e002_572_optical_edge_calibration.py) · [Frozen protocol](E002_572_FROZEN.md) · [Dedicated workflow](../../.github/workflows/e002_572_optical_edge_calibration.yml).

**14/14 local Python tests passed** in a locally reproduced copy of the committed source/test logic. A separately written JavaScript pairwise-inequality solver confirmed the uncorrupted feasible rate range **[1.0000103333,1.0000296667]**, rejected the +10 ms calibration corruption (infeasible rate bounds [1.000991,0.999047]) and rejected the -20 ms nonlinear edge. These are independent arithmetic checks, not a separately collected instrument dataset.

Hosted CI was configured, but no completed E002-572 hosted job has been verified as of this report. Do not promote the test result to hosted success without inspecting the exact run logs. The implementation uses double precision and a 1e-12 clipping tolerance, not formally verified interval arithmetic; it must not serve as a production trust root without a numerical robustness review.

## What this does and does not change

The instrument pipeline now has an executable acceptance/rejection gate for independently timed optical-edge calibration, a concrete adversarial held-out test and an explicit fail-closed condition for inconsistent calibration. This is a bounded **physical-study readiness artifact**, not a physical validation substitute of equal evidential strength. Gamma-compressed RGB, unknown automatic exposure, rolling-row offsets outside the specified bound, nonuniform shutter kernels, LED pulse ringing, frame loss, motion blur and nonlinear response violate assumptions unless separately measured and bounded.

Even a successful physical optical clock calibration would **not** provide a deterministic human eyelid velocity ceiling, a reference camera sensitivity certificate, or positive anatomical labels. No blink/PERCLOS/fatigue/absence-of-closure claim is enabled.

Remaining independent human rater pairs **0**; authenticated physical shutter captures **0**; continuous-time physiological upper speed bounds **0**; held-out physical closure predictions **0**. Lucent remains `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. The next non-synthetic work must execute E002-567's private human-rater and borrowed photodiode/camera protocol. Do not create another synthetic timing law merely to generate commits. Hush remains on its separate branch/PR, unchanged in this primary run.
