# E002-336 — Frozen paired-clock measurement kernel
Frozen 2026-10-21 05:xx IST before remote EOTT probe outcomes. Previous EyeBlink8 annotations are RGB-derived, not independent eye-reference validation.

1. Signal/reference: ordinary webcam RGB pupil/iris ratio or eyelid trajectory versus simultaneous Tobii Pro X3-120 pupil diameter, gaze and validity at 120 Hz (EOTT candidate; NOT yet evaluated).
2. Frontier: EOTT has 51 participants with webcam video and raw pupil diameter; EyeDentify has webcam/Tobii but published reference folding is unsuitable for rapid temporal claims. Elementary clock synchronization and uncertainty propagation are established.
3. Metric: signed physiological-lag identification interval, then held-out signal/reference coherence and abstention coverage.
4. Confound: clock offset, drift and nonlinear residual; also gaze, eyelid aperture, lighting, glasses and auto-exposure.
5. Generative model: I_k(u)=Q_k[E_k^-1 integral(t_k,t_k+E_k) Phi(u; pupil radius, iris radius, scale, gaze, eyelid, illumination, glasses) dt]+noise. Apparent ratio z≈(pupil/iris)*gaze_factor*visibility_factor*photometric_factor after exposure. Reference clock g(t)=affine(t)+h(t), h(t0)=h(t1)=0, |h'|<=kappa, with anchor errors epsilon0/epsilon1 and event errors c/r.
6. Falsification: independent sync/event controls fall outside predicted interval, or geometry-only, brightness-only, missingness-only or smoothness-only nuisance reproduces certificate. Unknown clock bounds invalidate precise lag.
7. Frozen mechanism prediction: within anchors B(t)=(1-u)epsilon0+u epsilon1+kappa*min(t-t0,t1-t)+c+r; signed lag iff |d|>B. With T=10 s, anchor errors 4 ms each, kappa=1 ms/s, RGB error 6 ms, reference error 10 ms: B(5)=25 ms; d=24 ms abstain, d=26 ms positive.
8. Untouched human test: if archive byte ranges work, freeze participant/device split before decoding; hold out one device and glasses/lighting where feasible. Calibrate clocks from independent anchors. No human outcomes inspected.
9. Publication threshold: independent paired RGB/reference humans, clock calibration, four nuisance baselines, participant/device holdout, prospectively predicted boundary crossing, independent checker and prior-art novelty audit. Clock theorem alone FAILS.
10. Product: reject uncalibrated rapid pupil waveform, precise lag, and five-second fatigue certification; permit only validated interval estimates with abstention.

Dataset acceleration: one bounded EOTT HEAD/Range probe only, no bulk download or laptop. If blocked, pivot to a different dataset or exact model without repeated metadata work. The WebGazer EOTT extractor warns WebM frame timestamps can be wrong.

Planned human metrics: normalize iris/pupil contour geometry; compare geometry-only, brightness-only, missingness-only, smoothness-only controls; report device/participant/glasses strata and calibration/abstention rates. Never publish raw participant video.
