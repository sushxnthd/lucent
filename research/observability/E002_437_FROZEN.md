# E002-437 — frozen acceleration-to-velocity reference bridge

**Frozen 2026-10-25 before implementation.** Parent kernel E002-371. Evidence planned: analytic inequality, independent numerical adversarial oracle, synthetic reference instrument. **No human physical validation or certified physiological acceleration limit.** Do not modify the established research branch/PR topology.

## Falsifiable question

Can a reference study convert *sampled, independently physically calibrated aperture intervals* into a conservative continuous-time eyelid-speed envelope without treating observed secant speeds as hard speed limits? Does increasing reference frame rate monotonically improve that envelope when localization error is nonzero?

For a differentiable physical aperture x(t) with |x''(t)| <= A throughout each reference segment, nominal sample spacing h, independent sample aperture errors <= epsilon, and absolute sample-time errors <= delta (h>2delta), define

U(h) = (|y_(i+1)-y_i| + 2epsilon)/(h-2delta) + A(h+2delta)/2.

For exact timestamps delta=0 this implies sup_segment |x'| <= U(h). The inequality follows by bounding the difference between any instantaneous derivative and the segment secant by A*actual_spacing/2, and bounding the true secant using observed differences and endpoint errors. This is a conditional *reference* bound, not an independently measured physiological A. A is a required, separately validated physical premise. If A is missing, geometry is uncalibrated, nuisance is unresolved, clock order is ambiguous, or segment coverage is incomplete, **ABSTAIN**.

The uncertainty contribution for delta=0 is B(h)=2epsilon/h + Ah/2, minimized at h*=2sqrt(epsilon/A), with minimum 2sqrt(epsilon*A) for epsilon,A>0. This is elementary derivative/mean-value calculus, **not a novel general theorem**. It predicts a nonmonotonic error floor versus sample rate if absolute landmark uncertainty is held constant.

## Prespecified numerical tests

1. A quadratic segment with constant acceleration -3600 mm/s², h=2.5ms, epsilon=.005mm and endpoint errors of opposite sign will attain equality at t=0 for a suitable positive initial derivative. A naive observed secant will underestimate instantaneous speed.
2. At A=3600 mm/s², epsilon=.005mm, delta=0, uncertainty penalties at 200, 400 and 1000 Hz must equal 11.0, 8.5 and 11.8 mm/s. Optimal h*=2.3570226ms (~424.264Hz); minimum 8.4852814 mm/s.
3. Across 500 deterministic seeded synthetic smooth traces, independently differentiated dense-time truth must never exceed the bound when A, epsilon and clock assumptions are met. Deliberately underspecifying A or epsilon must produce a witnessed failure on a separate constructed adversarial trace.
4. Increasing clock uncertainty must never reduce the bound; invalid/overlapping time intervals, untrusted physical scale, unresolved nuisance, missing acceleration evidence, and excessive reference gaps must abstain. A result must never authorize physical closure, PERCLOS, fatigue or blink-duration claims.
5. A high-speed reference bound is useful only if it remains small enough to change E002-371's predicted ordinary-camera decision. Otherwise the correct output is abstention. No synthetic pass may be described as measured human reliability.

## Scientific handoff

For an actual human study, independently estimate/validate **upper** acceleration and anatomical measurement-error limits on a calibration apparatus or independent participants, including motion blur, gaze, geometry, illumination, glasses, frame loss and sensor-clock uncertainty. Test unseen participants with two blinded anatomical raters. Do not estimate A from the same held-out interval and call it independent. Freeze ordinary-camera decisions before disclosing reference labels. If a defensible physical A cannot be established, this instrument remains a conditional sensitivity analysis only.

## Reproduction and failure

Use standard-library Python only. An incorrect bound on any admissible synthetic smooth trace, an invalid provenance record producing a numeric certified physical claim, or a failed nonmonotonic sampling-rate prediction fails E002-437. All results must carry `ABSTAIN_UNCALIBRATED` and identify synthetic premises.