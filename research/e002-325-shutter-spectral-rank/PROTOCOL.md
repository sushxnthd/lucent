# Mandatory ten-part kernel

1. Signal/reference: canthal-normalized RGB eyelid occupancy or pupil-to-iris ratio, versus native synchronized >=120-Hz eye-reference anatomical measurement of the same quantity; exposure means are compared to integrated reference, not instantaneous labels.
2. Literature: Shannon 1949; Papoulis 1977; Unser 2000. RGBE-Gaze and EyeDentify are dataset candidates, not proof of human observability.
3. Metric: rank(A), sigma_min(A), Delta*sigma_min/(2eta), exact two-world collisions.
4. Strongest confound: framewise gaze/lighting/glasses/autoexposure gain and unknown clock offset.
5. Model: RGB_j=F(geometry,photometry,blur,exposure,x)+noise; conditional scalar y_j=E^-1 integral x+e.
6. Falsification: native human reference outside frozen calibrated uncertainty, or a verified rank/alias prediction failure under the assumed model.
7. Prediction: 4 vs -6 Hz collision at 10 fps; 13 vs 12 sample rank crossing at K=6; spaced vs clustered 13-frame masks have radically different sigma_min.
8. Human holdout: NOT EXECUTED. Freeze participant/device/lighting/glasses/gaze splits before seeing results, independently calibrate timestamps/exposures, run geometry-only, brightness-only, missingness-only, temporal-smoothness controls.
9. Publication: require genuinely new ocular-specific human boundary prediction surviving untouched holdout, or novel theorem beyond classical sampling, plus independent checker.
10. Product: allow only research-mode interval shutter means after calibration; reject uncalibrated waveform, blink timing, fatigue diagnosis.

Acceleration: E002-324 and this run examined raw-data routes. RGBE-Gaze OneDrive records were not ingested. Stop dataset archaeology and use exact theory until a feasible path appears. No personal spend or user-laptop compute.