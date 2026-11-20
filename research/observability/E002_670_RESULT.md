# E002-670 | Frozen held-out synthetic certificate challenge (2026-11-06 UTC)

## Question and evidence tier
Can the sharp within-exposure exclusion rule of E002-669 survive an independently implemented, reproducible trajectory generator and bounded measurement errors? This is a **synthetic validation substitute**, not human or instrument evidence. The rule is evaluated without changing its threshold or velocity bound.

## Frozen protocol
Use seed 6702026, 5,000 piecewise-linear aperture trajectories, five equally spaced knots over a 1/30 s rectangular exposure, normalized aperture in [0,1], threshold tau=0.30, and V=60 aperture/s. A constrained random walk enforces the V-Lipschitz condition exactly. Integrate the resulting trajectory by exact rational trapezoids; independently sample bounded synthetic observation error in [-0.01,0.01]. Certify absence of threshold crossing within the exposure only when measured_mean - 0.01 > 351/400. Ground truth closure is the minimum over the piecewise-linear knots. Preserve every abstention, including false-negative opportunities. Reproduce with `python3 research/observability/e002_670_validation.py`.

## Local execution, not hosted CI
Standard-library Python execution passed locally: n=5000, certified=2, abstained=4998, true closures=3821, false certificates=0. Thus coverage was **0.04%** on this deliberately broad synthetic distribution. Zero false certificates here is a theorem-consistency check, **not** a statistical estimate of safety in people. The generator heavily samples low apertures and does not approximate a human blink distribution. Exact boundary-ramp equality and the required strict inequality were also checked.

## Scientific interpretation and next falsification
The conditional bound survives this synthetic challenge but yields almost no positive certificates under these parameters. This negative utility finding rules out presenting the method as a broadly useful consumer blink-absence detector without new evidence. A separate instrument study must calibrate exposure kernel and gain with a photodiode and phase-randomized LED shutter, then independently measure aperture/velocity from high-frame-rate video. Freeze subject-held-out calibration, 24/30/60 Hz downsampling, gaze/lighting/glasses/blur/missingness/rolling-shutter/clock-shift strata, and report false certificates, abstention, and coverage with uncertainty by stratum. Reject any deterministic human claim when velocity ceilings are merely empirical sample maxima.

## Product consequence
Only a *conditional, within-exposure* exclusion certificate is mathematically supported. No natural-blink absence, fatigue, sleepiness or clinical inference is supported. Human validation 0; physical camera validation 0; external replay 0. Keep `ABSTAIN_UNCALIBRATED` and production `BLOCKED`. Next substantive priority: real instrument/human evidence rather than another synthetic theorem.
