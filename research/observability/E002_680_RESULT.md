# E002-680 | Frozen synthetic phase-alias challenge (2026-11-06 UTC)

Evidence tier: deterministic constructed trajectories, **not** human/physical validation. This is a sampling-phase falsifier for any product rule that interprets the absence of a low-aperture sample as absence of closure. A symmetric triangular normalized aperture reaches zero once per event. Frames are 30 Hz, 1,000 equally spaced sub-frame phases, ideal box shutter, 200-point midpoint quadrature, event durations 10/20/40/60 ms, exposures 0/5/10 ms, observed closure threshold 0.30. A miss means every sampled exposure-average aperture exceeds 0.30 despite a true zero aperture in the underlying trajectory.

Frozen grid and output from independent JavaScript reproduction of the same explicit formula (Python executable included for independent replay):

| Event duration (ms) | Exposure (ms) | Missed phases / 1000 |
|---:|---:|---:|
| 10 | 0 | 910 |
| 10 | 5 | 932 |
| 10 | 10 | 1000 |
| 20 | 0 | 820 |
| 20 | 5 | 820 |
| 20 | 10 | 866 |
| 40 | 0 | 640 |
| 40 | 5 | 640 |
| 40 | 10 | 640 |
| 60 | 0 | 460 |
| 60 | 5 | 460 |
| 60 | 10 | 460 |

**Interpretation:** This is an idealized existence/coverage stress test, not an estimated human miss rate. Exposure averaging can conceal short closures; nominal frame rate alone cannot support an absence claim. Neither these triangular events nor normalized units establish human eyelid speed ceilings, camera calibration, or anatomical label validity. No threshold tuning or release approval is permitted on this synthetic grid. Product stays `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. Next decisive evidence is the E002-671 paired high-speed/ordinary camera human protocol, independently calibrated shutter and velocity, blinded reference labels and held-out evaluation. Reproduce with `python research/observability/e002_680_phase_alias.py`.
