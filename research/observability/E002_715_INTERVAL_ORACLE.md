# E002-715 — Interval-robust exclusion oracle

**Evidence:** executable synthetic arithmetic validation, not physical or human evidence. Supports the frozen E002-714 prospective protocol without changing its thresholds.

## Result

An independent constructive oracle compares the conservative certificate `V_upper * delta_upper < aperture0_lower + aperture1_lower` against a piecewise-linear trajectory that reaches zero and reopens. An exhaustive rational grid uses five values (0, 1/4, 1/2, 1, 2), 15 intervals per parameter, and 50,625 combinations of endpoint aperture, elapsed-time, and velocity intervals. The local execution returned **PASS: 50,625 interval cells; 21,582 exclusions; 29,043 feasible closure witnesses**. No false exclusions were observed in this exact rational grid. The test includes equality, zero-speed/zero-aperture, and invalid nonfinite input. Reproduce with `python research/observability/e002_715_interval_oracle.py`.

## Falsifiable acquisition consequence

Stage A must supply independently calibrated *intervals* for instantaneous aperture, elapsed time, and continuous-time velocity. It must never substitute nominal FPS, point estimates, or a video-derived maximum slope. When bounds are invalid, missing, or unsupported, abstain. If a closure is feasible under any admissible interval endpoint, do not certify absence. A reference-confirmed hidden closure in any certified trial falsifies the combination of sensor calibration, model, and certificate assumptions.

## Limitations

The exhaustive grid is synthetic and not a physical experiment; 50,625 cells are not independent human trials. The witness is a Lipschitz aperture curve, not a biomechanical eyelid model. Its construction does not validate that a human can achieve the stipulated velocity, that brightness measures aperture, or that any clock and exposure intervals are calibrated. No physical sensors or participant data were acquired. Human physiological claims remain BLOCKED / ABSTAIN_UNCALIBRATED.
