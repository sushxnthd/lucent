# E002-540 FROZEN | Exposure-integrated endpoints can reverse a shutter-gap exclusion

Date: 2026-10-30. Primary E002-371 kernel. Existing `research/observability-human-boundary` branch and draft PR #26. Freeze before running the new executable or independent optimizer. Evidence tier: exact idealized forward-model counterexample and synthetic instrument validation; **not** a measured shutter, calibrated image-to-aperture transform, or human physiological evidence.

## Falsifiable question

E002-371 and E002-539 require *pointwise anatomical aperture* at the ends of a fully blind interval. A real global-shutter frame normally integrates light over a nonzero exposure. Does replacing a **linear exposure-average aperture** with the same numerical pointwise aperture produce a false hidden-closure exclusion, even with perfect timestamps, no blur, and a valid hard speed ceiling?

Assume a scalar aperture `a(t) in [0,1]` is V-Lipschitz. Two ideal global-shutter measurements are exact means over `[0,E]` and `[T,T+E]`, where `T>E>0`, and the blind interval is `[E,T]` of duration `D=T-E`. The mean-to-aperture relationship is **assumed linear and perfectly calibrated** solely to isolate exposure integration; real pixel intensities are not known to satisfy it.

## Frozen numeric predictions

Set `T=1/30 s`, `E=1/100 s`, `D=7/300 s`, `V=45 normalized-aperture/s`, exposure means `b_1=b_2=9/10`, and closure threshold `c=1/5`.

1. **Invalid point-sample shortcut** treats each mean 9/10 as aperture at E and T: predicted minimum `9/10 - V*D/2 = 3/8`, strictly above 1/5, hence falsely excludes.
2. **Actual exposure-compatible witness:** at E and T the aperture can be `7/10`. First exposure is `min(1,7/10+45*(E-t))`, second is its time mirror. Both exposure means are **exactly 9/10**. In the blind gap, a symmetric speed-limited V-shaped path reaches `7/40=0.175`, strictly below `1/5`. Its below-threshold dwell is `1/900 s` (1.111... ms). No speed violation or aperture range violation is allowed.
3. **Sharp exposure-edge inference:** for any exposure with average b and end-aperture x, its maximum possible average at fixed x is the integral of `min(1,x+V*(E-t))` divided by E. The least compatible x is `max(0,b-VE/2)` when `b<=1-VE/2` (with correct saturation handling at zero), or `1-sqrt(2VE(1-b))` otherwise. A symmetric bound on the hidden minimum is `x_min - VD/2`. Check this exact expression for the frozen case.
4. **Unseen speed control:** V=40/s with the same T,E,b,c must **exclude** a hidden closure under the idealized assumptions; V=45/s must **not exclude**. This is a prediction, not a physiological speed estimate.
5. **Adversarial controls:** zero exposure duration must reduce to the point-sample law; unknown exposure length, nonlinear photometry, rolling shutter, timing error, missing frames, occlusion, gaze, blur, glasses, uncalibrated geometry, and sampled/cohort velocity peaks must not yield a real-world certificate.

## Independent falsification and kill criteria

Implement a Fraction-based exact witness and a separately written numerical linear-programming adversary with bounded range, speed differences, two exposure-average constraints, and a freely optimized blind midpoint. Use at least two grid resolutions with exact grid alignment at 0, E, T and T+E. Freeze acceptance tolerance of 0.025 normalized aperture for the LP minimum; a larger disagreement must be reported, not retuned. Independently verify exact exposure integrals by a second arithmetic implementation (Node BigInt or symbolic integration). Include negative controls for incorrectly substituting means as point samples.

If the frozen witness does not integrate to 9/10, dips below 1/5, or satisfy the 45/s Lipschitz bound, reject the proposed counterexample. If independent LP cannot produce an admissible dip within 0.025, report disagreement rather than changing the frozen parameters.

## Product and physical handoff

No ordinary-camera measurement can be called a pointwise eyelid aperture merely because it has an FPS label. An eventual product must authenticate exposure start/end, transfer function, geometry, and endpoint uncertainty before evaluating the exclusion; otherwise `ABSTAIN_UNCALIBRATED`. A photodiode-calibrated mechanical-aperture phantom should be the next physical experiment, followed by blinded participant-disjoint human validation. This synthetic model cannot certify a continuous-time human speed bound or physical shutter. No production release.

Hush PR #45 is separate and remains unchanged during this primary experiment.
