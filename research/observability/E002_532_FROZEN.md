# E002-532 FROZEN | Optical shutter calibration by independently timed LED duty fractions

2026-10-30. Lucent E002-371 human-validation kernel; existing branch `research/observability-human-boundary`, draft PR #26. **Prospective instrument-calibration executable, not a human measurement.** Freeze this protocol before code, test execution or any physical capture.

## Instrument question

Can an independently measured binary LED waveform and row-resolved camera brightness distinguish exposure duration, clock offset and rolling-shutter row delay? This is an *instrument calibration feasibility* question, not a physiological blink theorem. In particular, an apparently high frame rate must not be promoted to an authenticated exposure or clock bound without an independent timebase and photometry.

For LED-on intervals `[a_k,b_k)` on a photodiode-attested clock, candidate exposure for frame timestamp `t_i` and ROI row index `j` is `[t_i+delta+j*r, t_i+delta+j*r+e)`. Under independently verified linear normalized photometry, predicted normalized LED brightness is the total overlap length with the LED-on intervals divided by `e`. The candidate parameters are clock offset `delta`, positive exposure duration `e`, and rolling-shutter delay per ROI-row unit `r`. This model excludes temporal gain control, nonlinear gamma, auto-exposure, flicker, spatially varying response, saturation and clock drift; those are *kill conditions* until measured or bounded.

## Frozen synthetic instrument design

All times in milliseconds; no actual LED, photodiode or camera was used.

- 20 synthetic frames with nominal starts `t_i=10*i` for `i=0..19`; rows `j in {0,2,4}`; 60 integrated observations.
- LED pulses `k=0..39`: start `5*k+offset_q[k]/4`, end start `+width_q[k]/4`. Exact quarter-ms arrays:
  - `offset_q=[1,1,3,0,1,2,2,2,1,3,2,2,0,0,2,0,0,2,2,1,0,0,2,3,2,3,3,0,3,2,1,1,1,0,3,0,2,2,3,2]`
  - `width_q=[6,2,4,2,5,3,6,3,4,3,6,6,2,2,3,6,6,3,3,5,6,4,6,2,6,6,2,2,4,6,2,4,5,2,2,5,5,4,2,6]`
- True parameters: `delta=1`, `e=2`, `r=1/2`. Training frames 0..9, held-out frames 10..19. No held-out observations may select candidates.
- Finite candidate grid: `delta in {-1,0,1,2}`, `e in {1,2,3}`, `r in {0,1/2,1}`; exactly 36 candidates. An observation fits if absolute discrepancy <= `1/50`. Training feasible set is the intersection over all observed training rows.
- Exact arithmetic with rational numbers, no floating-point boundary certificates. The synthetic pulse schedule and grid are **illustrative**, not physical calibration resolution.

## Frozen predictions and falsifiers

1. All 30 noiseless training observations identify exactly `(1,2,1/2)` among the 36 grid candidates; 30 held-out observations have zero residual. If not, reject the identifiability claim.
2. Replacing the LED waveform with a continuously illuminated field and observed brightness 1 makes all 36 candidates feasible; output `AMBIGUOUS_GRID`, never a calibration.
3. Restricting the candidate grid to `r=0` under the true rolling-shutter data yields zero feasible candidates; output `MODEL_FALSIFIED`, not a global-shutter certificate.
4. Perturbing one held-out brightness by 1/10 while keeping the training data unchanged fails held-out prediction; output `FALSIFIED_HELDOUT` and preserve the failure.
5. If independent photodiode timebase, linear photometry, native frame identity, rolling-row geometry or clock trace are unverified, even a unique held-out fit is `UNVERIFIED_PHYSICAL_INPUT`. A discrete grid fit is **never** a continuous-time exposure guarantee.

## Real-camera protocol and decision consequence

Borrow equipment, do not purchase. Drive a hardware LED with pseudorandom pulses; independently capture **actual optical output** with a photodiode and timestamp it on an independently calibrated clock. Record camera native frames, raw exposure settings, per-frame timestamps, at least three vertically separated LED ROIs, dark and steady-on controls, shutter/scanline orientation, autofocus/auto-exposure state, illumination, dropped frames and photodiode-clock uncertainty. Normalize ROI brightness only after checking linearity, clipping, gamma, saturation and flicker. Freeze candidate grid and photometric tolerance before viewing held-out frames; use phase diversity rather than a fixed periodic LED that aliases with the frame clock. Fit only calibration trials; challenge on new pulse phases, brightness, exposure settings, rows and camera restart. Report all infeasible and ambiguous cases. This procedure cannot establish camera-to-camera synchronization or anatomical aperture transport without separate experiments.

Release decision stays `ABSTAIN_UNCALIBRATED`, `BLOCKED` until physical captures and independently blinded human anatomy are available. No synthetic or published data may be described as a physical calibration. Hush remains untouched.
