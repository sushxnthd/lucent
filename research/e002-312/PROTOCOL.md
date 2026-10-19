# E002-312 frozen scientific protocol

1. Signal/reference: entire exposure-integrated RGB eyelid-edge image versus synchronized high-speed anatomical edge crossing/peak time. No human recordings used.
2. Frontier: Raskar et al. ACM TOG 2006 (10.1145/1141911.1141957); Zhang et al. IEEE TPAMI 2022 (10.1109/TPAMI.2021.3116135); Navascues Cornago et al. The Ocular Surface 2026 (10.1016/j.jtos.2026.01.003).
3. Metric: full-image event-time identified interval diameter given q and gain ratio r; triangular peak-time equivalence diameter.
4. Strongest nuisance: unobserved within-exposure contrast trace; for nonmonotone blink, time ordering loss even with constant contrast.
5. Model: global shutter; I(x)=B+C*int w(t)Phi((x-s(t))/sigma)dt/int w(t)dt; known blur; monotone edge or triangular pulse.
6. Falsification: find different complete images for claimed exact collision; prospectively demonstrate reference event outside independently calibrated identified interval.
7. Prediction: t/T in [r*q/(1-q+r*q),q/(r*(1-q)+q)]; r=.5,q=.5,T=16.667ms gives width 5.556ms; smooth collision gap 2.705ms; triangular peak width T-2A/L.
8. Untouched human test: not performed. Future: simultaneous global-shutter RGB and 240-500fps reference with optical timing fiducial; calibrate shutter/row readout/radiometry/PSF/speed/gaze; freeze nuisance bounds before unseen participant/device/lighting/glasses holdout.
9. Publication threshold: independent proof/checker, primary prior art, prospective paired human evidence, nuisance controls, unseen prediction, valid coverage/abstention, novelty beyond motion-blur theory. Not met.
10. Product: reject uncalibrated point-valued within-exposure blink timing, pupil waveform and five-second fatigue certification; conditionally allow calibrated exposure-occupancy and interval timing with abstention.

Synthetic test plan frozen before independent checker: 101 complete-image pixels; 480 randomized LP feasibility checks; 41-pixel constant-brightness triangular collision; geometry-only, brightness-only, missingness-only and temporal smoothness controls. No human outcomes.
