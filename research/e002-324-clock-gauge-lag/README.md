# Lucent E002-324 — clock-gauge and physiological-lag identifiability
Date: 2026-10-20. **Conditional exact timing result, NOT a human RGB validation or a novel clock-synchronization theorem.**

## Active question
Can a temporal delay between a geometry/photometry-normalized RGB ocular feature and a trustworthy eye-reference feature be assigned a direction when camera/reference clocks have uncertain offset and drift?

## Signal / reference
RGB: a pre-specified normalized eyelid-aperture or pupil/iris observable extracted from exposure-integrated frames, with camera exposure-midpoint timestamps. Reference: a concurrently measured high-rate eyelid or pupil trace with native timestamps. The lag estimator must be frozen independently of the held-out data.

## Sharp result
Given apparent lag y = ell + b(t) + e, |e| <= eta, affine clock offset b(t), and two independently calibrated anchor intervals b(a) in [ma-da,ma+da], b(z) in [mz-dz,mz+dz], the EXACT identified interval for physiological lag ell is:

wa=(z-t)/(z-a), wz=(t-a)/(z-a)
m=wa*ma+wz*mz
R=|wa|*da+|wz|*dz+eta
**ell in [y-m-R, y-m+R]**.

This interval is sharp. Sign is certifiable iff y-m>R (positive) or y-m< -R (negative); equality means abstention. For one anchor and unconstrained affine drift, any non-anchor time has unbounded lag uncertainty. More frames and greater SNR alone cannot remove this gauge.

## Frozen synthetic crossing
Anchors at 0 and 60 s, offset uncertainty 2 and 8 ms, estimator error 1.5 ms, test at t=45 s: R=8.0 ms. Observed 7.5 ms must abstain; 8.5 ms must certify positive. At t=90 s, R=14.5 ms because extrapolation magnifies drift uncertainty. Exact-rational and 10,000 randomized independent corner tests passed.

## Controls and failed gates
Geometry-only, brightness-only, missingness-only, and temporal-smoothness controls are specified in PROTOCOL.md. They are NOT human-evaluated. No real-world clock anchor or independent RGB/reference evaluation has been obtained. Publication-level novelty is NOT established.

## Product consequence
Reject uncalibrated RGB-to-reference physiological lag, pupil response latency, rapid fatigue timing, and five-second fatigue certification. Allow interval-valued lag direction only after independent timebase/exposure calibration and reference-quality gating. Otherwise abstain.

Run `python independent_checker.py` (standard library only). See THEOREM.md, PROTOCOL.md, PRIOR_ART.md, FAILED_GATES.md, FROZEN_PREDICTION.json, results.json.
