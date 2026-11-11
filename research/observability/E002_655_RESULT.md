# E002-655 | Exposure-integrated observations cannot be treated as instantaneous aperture samples

Evidence tier: deterministic synthetic falsification only; no human, shutter, or sensor calibration.

A continuous triangular aperture trajectory with minimum 0.2 at t=0.5, threshold 0.3, and Lipschitz speed 0.8/0.12 has a **0.4-time-unit rectangular exposure centered exactly on the closure** whose mean aperture is 0.76. A classifier comparing this mean to 0.3 would report open although the true center is closed. This is not a sensor-image model; it is a scalar aperture observation model. See executable `e002_655_exposure_alias.py` for numerical quadrature and assertions.

For a uniform shutter of duration e centered at t, the point-aperture and exposure-mean discrepancy obeys |mean(a)-a(t)| <= V e/4 when |a'| <= V. Therefore an endpoint certificate using exposure means as instantaneous samples is not sound without a shutter-integration uncertainty term. For nonuniform unknown exposure weighting, the bound must use V times the shutter-weighted mean absolute temporal offset, and if the kernel is unverified, abstain.

**Product consequence:** do not treat brightness/eyelid scores from exposure-integrated frames as exact point samples; enforce `ABSTAIN_UNCALIBRATED` until exposure kernel, timing, geometric aperture extraction, and physiological speed bounds are independently verified. This does not validate the shutter-gap law against humans.

Reproduction: `python3 research/observability/e002_655_exposure_alias.py`. The test is deterministic, dependency-free and contains no external dataset. Its numeric units are dimensionless. Adversarial next step: calibrate actual exposure windows with synchronized LED/photodiode and independently annotated eyelid aperture trajectories, then prospectively evaluate held-out subjects.