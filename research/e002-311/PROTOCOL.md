# Frozen scientific kernel E002-311

1. Signal/reference: RGB normalized 50%-eyelid-edge crossing vs simultaneous trustworthy high-speed anatomical eyelid position at shutter midpoint.
2. Frontier: classical subpixel edge localization, coded-exposure motion blur (Raskar et al. 2006), high-speed human blink studies (2019, 2026).
3. Metric: worst-case |x50-s(0)|/|v| and prospective calibrated interval coverage.
4. Strongest confound: within-exposure contrast variation w(t) despite frame-level plateau normalization.
5. Model: moving Gaussian-blurred step, m<=w(t)<=M, uniform exposure T, independently known v and sigma.
6. Falsifier: a synchronized RGB/high-speed-reference case violating the frozen boundary after measured geometry/noise allowance; or valid mathematical counterexample inside the assumptions.
7. Mechanism prediction: u* from rG_k(T/2+u)=G_k(T/2-u), k=|v|/sigma.
8. Untouched human test: NOT RUN. Calibrate gain, blur, velocity and gaze on training participants/devices; freeze boundary-crossing prediction; open separate participant/device/lighting/glasses holdout.
9. Publication threshold: rigorous check + primary prior art + human prospective boundary test + geometry/brightness/missingness/smoothness controls and independent checker.
10. Product: reject unconditional subframe blink-event timing, rapid pupil-waveform and five-second fatigue certification. Permit calibrated intervals with abstention only.

Controls: geometry-only common translation persists unless canthus-registered; constant affine brightness preserves crossing; temporally varying contrast biases crossing; missingness with r=0 can move crossing toward shutter edge; smooth gain can approximate the sharp bound. Synthetic prediction does not substitute for human holdout.
