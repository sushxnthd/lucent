# E002-542 | Frozen crossed-stimulus falsification of shutter calibration

Date: 2026-10-30. Primary E002-371 kernel; existing branch and draft PR #26. **Frozen before experiment implementation.** This is one bounded instrument-design preflight, not a physical measurement or further threshold optimization.

## Scientific question

E002-541 accepted two explicitly misspecified camera transfer models (gamma 1.6 and temporal three-tap blur) under its original binary-coded training illumination. Does freezing its best timing and fitted affine radiometry, then testing *different illumination amplitudes and isolated edge pulses*, reveal model mismatch that the original calibration residual missed?

## Fixed experiment and predictions

Use the unchanged E002-541 1-ms grid, 20 frames separated by 33 ms, two rows, truth (phase, exposure, row delay)=(7,8,5) ms, seed 20261030, gain 0.65, offset 0.20, and unchanged 0.025 training RMSE acceptance. Fit only on amplitude-one coded training samples; freeze the returned timing, gain and offset. Do not refit on the challenges.

1. **Radiometry challenge:** use the same 20-frame coded sequence at LED amplitudes 0.25 and 0.50, treating dark and full LED intensity as independently controlled physical levels in a future bench. Compare frozen affine predictions against synthetic linear sensor (gamma 1) and nonlinear gamma 1.6 sensor. Predeclared failure criterion: held-out RMSE > 0.025 for the gamma model while the linear model is <=0.025.
2. **Temporal-response challenge:** use a *different* illumination waveform: 1-ms flashes immediately before and immediately after the known row-0 shutter interval in every frame. Compare the frozen shutter integration model with (a) instantaneous LED/sensor response and (b) a three-tap symmetric temporal response (0.25,0.50,0.25). Predeclared model-failure criterion: max absolute held-out residual > 0.015 for the blurred response while the instantaneous response is <=0.015. Include both rows in the evaluation; do not discard low-signal samples.
3. Preserve any failure of these predictions. No post-hoc threshold, code seed, gain or waveform changes. Report whether the old E002-541 training gate still accepted the nuisance, as an independent baseline check.
4. Negative controls: missing or duplicate frame IDs, saturation, source-length mismatch, a wrong frozen timing triple, and a wrongly paired LED reference must not be interpreted as physical certification.
5. A second implementation must verify the arithmetic independently. Report all numeric residuals and uncertainty limitations. No real shutter/clock, photodiode, eyelid anatomy or human continuous-time motion limit is established by simulation.

## Physical study consequence

If synthetic crossed-stimulus testing exposes model failure, add both challenge families to the real photodiode-timed bench before attempting human closure predictions. If not, explicitly report the residual failure and require direct independent sensor temporal-impulse characterization. A future physical run must capture photodiode emission, raw native sensor brightness, locked manual settings, multiple amplitudes and pulse-edge offsets on a common clock, plus camera restarts, row positions and held-out settings. Optical success still does not certify physiological speed bounds. All Lucent product states remain `ABSTAIN_UNCALIBRATED` / `BLOCKED`. Stop software-only coded-light work after this preflight and prioritize real captures and two independent blinded anatomical raters.
