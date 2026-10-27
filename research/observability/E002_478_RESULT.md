# E002-478 RESULT — frame-attribution ambiguity falsifies an unqualified periodic-shutter interpretation

Date: 2026-10-27. Kernel E002-371. **Evidence tier: synthetic instrument-model falsification only. Physical acquisitions: 0. New human anatomical reference trajectories: 0.** Protocol frozen in [E002_478_FROZEN.md](E002_478_FROZEN.md) at commit `dccf90015dc90510271c4a7fce497e99d87e4203` before implementation.

## Finding

The E002-477 optical intake reports `PASS_INTAKE_ONLY` for a synthetic two-period scan whose generated camera response uses **one rectangular exposure window** rather than a shutter response repeated every frame period. The compact `camera.csv` does not include a camera frame index or an explicit target-frame attribution rule. Consequently, the *same CSV* admits two different interpretations:

1. **Repeated-frame response:** Each pulse is read out from its corresponding frame. Under stationary shutter/illumination/gain, responses separated by one authenticated frame period must agree within measurement uncertainty. The existing synthetic fixture violates this necessary condition.
2. **Single-target-frame response:** Each pulse is read out only from a designated frame, including pulses emitted after that frame's exposure. The observed second-period zero response can be legitimate, and periodicity must **not** be demanded of this CSV.

This is a **measurement-protocol identifiability problem**, not evidence of a defective real camera. The frozen prediction is supported *conditional on interpretation 1*. E002-477's intake is intentionally only an integrity/completeness gate and does not certify shutter support; its prior `PASS_INTAKE_ONLY` was not a physical-release error.

## New necessary consistency test

For dark-subtracted response C to an identical pulse, a stationary periodic shutter, externally verified period T, phase-response Lipschitz bound L, per-record contrast error b, interperiod drift d and pulse-phase error u, paired phases t_i and t_j must satisfy

`|C(t_i)-C(t_j)| <= L*(abs(t_j-t_i-T)+2*u+p)+2*b+d`

where p bounds the independently verified period error. The test pairs first- and second-period samples using the independently recorded pulse starts, tolerates the noninteger 240-fps period/0.05-ms phase-grid offset, and applies the inequality row by row. The slope, noise, drift, clock and period budgets are **synthetic assumptions**, not calibrated real-world values. Passing this necessary condition cannot identify exposure support or certify a shutter.

## Frozen synthetic results

| Case | Necessary-condition decision | Details |
|---|---|---|
| Original E002-477 one-shot fixture, interpreted as repeated-frame | **REJECT_STATIONARY_PERIODIC_MODEL** | 42 violations among 166 phase pairs; maximum discrepancy/budget ratio 4.83871 |
| Independently reconstructed truly periodic two-period rectangular shutter | CONSISTENT_WITH_PERIODICITY_ONLY | 0 violations among 166 phase pairs; maximum ratio 0.806452 |
| Unbudgeted second-period brightness shift | REJECT_STATIONARY_PERIODIC_MODEL | Fails the stationary response assumption, not necessarily camera hardware |
| All-dark response | INDETERMINATE | No measurable optical signal |
| Missing slope budget | INDETERMINATE | Refuses uncalibrated model |
| Deliberately enlarged justified drift budget | CONSISTENT_WITH_PERIODICITY_ONLY | Correctly avoids claiming a contradiction beyond the declared uncertainty |

The standalone standard-library [evaluator](e002_478_periodic_replay.py), [nine adversarial tests](test_e002_478_periodic_replay.py), and [aggregate](E002_478_AGGREGATE.json) are committed. Nine local tests passed against a reconstructed E002-477 fixture with a lightweight SHA-integrity intake stand-in. Dedicated hosted CI runs the same tests against the **actual** repository E002-477 intake. The hosted result must be checked independently before claiming that verification.

## Acquisition change and decisive next step

The physical optical acquisition must now record **which exact frame** was read out for every pulse, along with independently measured pulse/frame phase and row identity. Declare one of two analysis modes **before acquisition**:

- `TARGET_FRAME`: record the absolute target-frame index and exposure-relative pulse time. Do **not** impose period-to-period response equality on a single target frame.
- `CORRESPONDING_FRAME`: record the actual frame index selected for each pulse and externally verify the period and matching logic. Apply the E002-478 repeatability test with independently measured response-slope, clock, noise and drift budgets; any rejection blocks stationary-shutter calibration pending diagnosis.

A manifest or SHA alone cannot authenticate the camera frame counter, photodiode independence, or a physical error budget. Raw traces, frame indices and pulse-to-frame mapping must be retained for external inspection. **Do not use the E002-477 descriptive phase centroids as shutter-edge estimates until this ambiguity is resolved.**

This is a new falsification of an *interpretation of the existing synthetic fixture*, not a new eyelid theorem, real optical experiment, physiological velocity limit or product validation. E002-371 remains **PHYSICAL_VALIDATION_NOT_ESTABLISHED**. Physical hidden-closure, blink duration, PERCLOS, fatigue and medical outputs remain `ABSTAIN_UNCALIBRATED`. The next decisive experiment is an actual independently timed optical acquisition with authenticated frame attribution, followed by moving-aperture ground truth and blinded human reference. Hush PR #45 is untouched.
