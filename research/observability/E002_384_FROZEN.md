# E002-384 frozen prospective synthetic validation (2026-10-23)

Research question: Does a per-frame RGB aperture-error calibration envelope support an entire-recording no-hidden-closure certificate? This is a **synthetic** instrument test, not human validation.

One fixed kernel: E002-371 shutter-gap certification with independently stipulated V and exposure timing. Prior E002-383 showed a nonlinear optical counterexample. This run tests a new unit-of-analysis failure: marginal frame coverage vs whole-clip coverage, and camera transfer.

Freeze before any numerical evaluation: seed 20261023; 500 calibration clips, 1000 untouched same-camera clips, 1000 untouched camera-shift clips, 60 frames/clip. Generate correlated photometric error and framewise sensor noise; calibrate absolute residual 99th percentile per frame and 95th percentile of within-clip maxima on calibration only. Compare empirical per-frame and all-60-frame coverage, with Wilson confidence intervals. An unseen camera has independent gain/glare shift. If physical gap certification is attempted, count false certificates and abstentions separately. Never use test labels to set calibration.

Predictions: (1) 99% per-frame residual coverage need not yield 99% complete-clip coverage; (2) clip-max calibration improves complete-clip coverage in exchangeable conditions but is not a deterministic bound; (3) camera shift can invalidate both; (4) any threshold crossing wrongly certified from an exceeded envelope is a falsification of *the calibration*, not the mathematical gap law. Report negative outcomes unchanged.

Controls: independent high-rate ground-truth trajectory, physical aperture speed, exact shutter timing, shared gain drift, sensor noise, nonlinear transfer, glare, geometry and missingness flags. Reject unsupported conditions with abstention. Validate exposure averaging with a separate numerical implementation. No hard safety claim based solely on statistical calibration.

Human follow-up: independently calibrated synchronized >=240-fps reference and ordinary RGB, measured shutter and timestamp uncertainty, consenting volunteers, participant/device holdouts, clip-level error coverage and gap-level false-certificate risk. No fatigue, PERCLOS or diagnostic claim.
