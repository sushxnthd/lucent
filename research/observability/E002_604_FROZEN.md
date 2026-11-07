# E002-604 | Frozen shutter-integration alias falsification protocol

Date: 2026-11-02. Parent E002-371. Evidence tier: SYNTHETIC_PHYSICAL_MEASUREMENT_MODEL_ONLY.

## Hypothesis and falsifier
A camera's *exposure-averaged* eyelid aperture cannot be treated as an instantaneous aperture observation. Even if a continuous-time eyelid trajectory reaches exact closure, every recorded frame can remain above a chosen aperture threshold. This is distinct from the previously tested zero-duration frame-sampling alias.

## Locked instrument model
Use normalized eyelid aperture a(t)=1-d(t), with a single triangular deficit d(t)=max(0,1-2|t|/w). The closure occurs at t=0 and the Lipschitz ceiling is V=2/w. A global-shutter frame centered at c reports y(c)=E^{-1} integral from c-E/2 to c+E/2 of a(t)dt, not a(c). Use exact piecewise-linear integration, not a point sample. Frames are centered at c=kT+phi, with k in [-4,4] and phi uniformly swept over [0,T) using 10000 equally spaced phases. Reject a closure only when some y(c)<=theta=0.2. Compare to instantaneous point samples and report the proportion of phases with no closure detection.

## Precommitted predictions
1. Set w=0.010 s, T=1/30 s, E=0.020 s, theta=0.2. Every phase misses the actual zero-aperture closure by the exposure-averaged threshold test. The exact minimum over all exposure centers is 1-w/(2E)=0.75, hence no threshold crossing, regardless of sample phase. In contrast, instantaneous point sampling has a nonzero detection-phase window.
2. For a window E<=w, the minimum shutter-averaged aperture is E/(2w); for E>=w it is 1-w/(2E). Verify the formula with exact integration at E={0.002,0.005,0.010,0.020} s.
3. A nominal 95-fps stream with E=0.005 s has minimum integrated aperture 0.25 and can therefore never cross theta=0.2, even though an instantaneous 95-fps sample may cross the threshold in some phases.
4. An independent JavaScript implementation must match Python for all predicted minimum values and phase-sweep missed fractions, with numerical tolerance 1e-9 for the minima and 1/10000 for fractions.

## Controls and interpretation
This is an intentionally idealized **global-shutter, linear photometric, correctly registered anatomical-aperture oracle**. It omits rolling shutter, image formation, optical blur, gamma, occlusion, gaze, glasses, geometric errors and clock uncertainty; none of these are claimed calibrated. A failure in this idealized model is a necessary observability counterexample, not a human blink rate or a physiologically certified velocity law. Do not infer V=200 aperture units/s as a human physiological bound. The 30-fps and 95-fps shutter lengths are hypothetical, not measured LPW metadata. Product must not interpret a frame-averaged aperture as an instantaneous no-closure certificate. Maintain ABSTAIN_UNCALIBRATED and release BLOCKED until physical shutter/clock calibration and independent human anatomy validation.
