# Untouched human validation protocol (no holdout outcomes inspected)

1. Simultaneously record native 30/60-fps ordinary RGB and independent >=150-fps high-speed anatomical eyelid reference with actual exposure, readout and clock timestamps. Reject unrecoverable synchronization failures.
2. Freeze participant and device holdouts and lighting/gaze/glasses strata before looking at paired outcomes.
3. Calibrate physical aperture/iris-width, photometric feature error, gaze/glasses nuisance, V, exposure widths and clock offset on development participants only. Empirical quantiles are probabilistic, not hard deterministic bounds.
4. Before holdout, predict a boundary crossing in shutter mismatch using V*W1, and possible event disagreement when q<(wL-wS)/(2*wL). The latter is a possibility, not a guarantee about natural blink phase.
5. Compare native RGB, high-fps pure decimation, and high-fps shutter-matched integration. Strong controls: geometry-only, brightness-only, missingness-only and temporal-smoothness-only.
6. Report event-level onset/offset interval coverage, false certificates, sensitivity, abstention and device/participant stratification. Exact binomial uncertainty bounds.
7. Falsify any deterministic certificate with a single independent reference counterexample under calibrated assumptions. A failed scalar instrument calibration is an instrument failure.
8. Publication requires a prospective held-out human boundary crossing, primary priority differentiation and independently reproducible data/code. None has been achieved in this run.