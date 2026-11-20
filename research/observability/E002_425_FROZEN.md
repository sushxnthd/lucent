# E002-425 — frozen finite-resolution shutter-kernel identification challenge

**Frozen before implementation and numerical evaluation, 2026-10-25.** This is a synthetic/instrument-design experiment, not a real camera or human eyelid validation. The active kernel remains E002-371. E002-424's exact alias is the preregistered adversary; do not reselect it after inspecting results.

## Question
Can an inexpensive off-grid, multi-width optical-pulse protocol identify a 48-cell nonnegative shutter-response approximation where the E002-423 fixed-width grid protocol provably cannot? How much noise sensitivity remains, and what can the instrument legitimately authorize?

## Fixed experiment
- Work in **one camera row** with a 2.4-ms exposure window [0,2.4] ms, partitioned into 48 equal 0.05-ms bins. The unknown vector x contains nonnegative bin **masses**, sum(x)=1. This finite-resolution model is an assumption, **not** a bound on arbitrary sub-bin structure.
- Fix two true kernels: uniform x[j]=1/48, and alternating x[j]=(1+0.99*(-1)^j)/48. Both normalized and nonnegative. No fitting of the true kernels.
- Each pulse measurement is the exact fractional overlap of a known unit-amplitude rectangular pulse [start,start+width] with each bin, dotted with x. This is a linear model with a **known** optical pulse; photodiode calibration is absent in this synthetic study.
- **Legacy design:** starts from -1.0 through +2.4 ms inclusive at 0.10-ms steps, width exactly 0.50 ms. Rank-test its design matrix; the two fixed kernels must produce identical outputs to floating-point tolerance.
- **Proposed design:** use NumPy default_rng(20261025) to generate 384 start phases uniformly in [-0.8,2.4] ms, each assigned a pulse width by a fixed independent integer draw from [0.37,0.43,0.51] ms. First 256 observations are calibration, remaining 128 are held-out. No post-hoc resampling.
- Compute numerical rank using numpy.linalg.matrix_rank (default tolerance) and singular values of the calibration matrix. Record its condition number. Report absolute held-out separation of the two true kernels.
- Fit x from the 256 calibration responses of the alternating kernel by bounded nonnegative least squares (scipy.optimize.lsq_linear with bounds [0,1]), with an extra normalization equation weighted by 10. Evaluate held-out mean absolute error, mass L1 error and minimum fitted mass. Repeat for deterministic noisy responses with independent Gaussian standard deviation 0.0005 (rng seed 20261026). Do not silently truncate negative simulated observations.
- Compare the recovered kernel against the wrong uniform model on held-out pulses. Report errors for both noiseless and noisy cases; do not tune the model or sample allocation after observing results.

## Prespecified decisions
H1: legacy design is rank-deficient (<48) and uniform/alternating responses match within 1e-12.
H2: proposed 256-row calibration design is full column rank (48).
H3: maximum held-out difference between the two fixed kernels exceeds 0.01 (resolves this alias).
H4: noiseless recovery has held-out MAE <1e-8 and mass L1 error <1e-5.
H5: noisy recovery has held-out MAE <0.01 and mass L1 error <0.25; **failure is a legitimate negative result**.
H6: the instrument never authorizes real physical hidden-closure, blink-duration, PERCLOS or fatigue claims; product remains ABSTAIN_UNCALIBRATED.

## Independent verification and limitations
Implement an independent midpoint or binwise quadrature oracle for selected pulse responses, explicit rank/null-vector checks, invalid-input rejection, and holdout accounting. Report all numerical outcomes even when a gate fails. Synthetic Gaussian noise is not sensor noise; bin resolution, timing uncertainty, optical pulse shape, rolling shutter, nonlinear RAW response, brightness, blur, gaze, glasses, geometry and physiological velocity are not validated. Real hardware would need independently photodiode-verified pulse timing and waveform, randomized off-grid pulses, multiple widths, multiple rows/brightness/exposure modes, and untouched-device evaluation. Two blinded human rater sheets and independent velocity/physical aperture calibration remain missing. This work may reject insufficient calibration designs; it cannot unlock product claims.

**Novelty limitation:** finite-dimensional linear inverse-system identifiability, nullspaces and pulse-system excitation are established. Claim only a falsifiable, reproducible design improvement for this restricted Lucent shutter surrogate.
