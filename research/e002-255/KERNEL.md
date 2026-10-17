# E002-255 — Human calibration ceiling and prior-art collision (17 October 2026)

**One active question:** Can ordinary RGB, with geometry/photometry normalization and independently certified exposure timing, recover a same-eye pupil waveform that prospectively agrees with native-time Tobii diameter under participant/device/lighting/glasses holdout?

- **Exact signal/reference:** Lucent RGB pupil-to-iris normalized radius at exposure timestamps versus same-eye native Tobii pupil diameter. **Secondary diagnostic here:** released EyeDentify/PupilSense RGB-crop regressor versus its Tobii labels, summarized by participant; not the Lucent detector.
- **Frontier:** E002-244/E002-246/E002-253 rejected the old Lucent radial-edge detector; E002-254 showed nearest-reference availability does not establish clock sync. EyeDentify (WACV 2025) and PupilSense (ETRA 2025) are direct prior art. Public human participant summaries permit an exploratory calibration-ceiling audit, not raw waveform replay.
- **Scalar:** primary held-out participant-bootstrap lower 95% Pearson r with frozen lag/amplitude/NRMSE and nuisance gates; this run's secondary scalar is the **best in-sample positive-slope affine-calibrated NRMSE** normalized by reference SD.
- **Strongest confound:** screen color changes both image photometry and physiological pupil size; geometry/scale, reflections, gaze and uncertified camera exposure timing also matter.
- **Decisive falsification:** under independently synchronized untouched human conditions, normalized ocular signal fails frozen waveform gates or brightness/geometry placebo matches it. Here, oracle affine calibration fails stringent exploratory error thresholds for most subjects of the released checkpoint.
- **Publishable success:** >=8 untouched participants as a feasibility minimum with sufficiently powered holdouts, independent replay, mechanism-derived unseen prediction, primary-literature novelty, and strongest nuisance controls. **Not met.**
- **Product relevance:** >=75% prospectively accepted accurate quantitative windows with calibrated uncertainty and rejection; **not met**.
- **Kill:** two blocked attempts on one data path force a switch; three nondiscriminating primary runs or prospective failure kill/reformulate. No fatigue claim.

**Exact conditional identity (standard least-squares algebra, not novel):** For nonconstant paired vectors x (RGB estimate) and y (reference), min over a in R and b>=0 of RMSE(y,a+b*x)/SD_pop(y) equals sqrt(1-max(r,0)^2), where r=Pearson(x,y). Thus oracle NRMSE<=0.5 requires r>=sqrt(3)/2=0.8660254. An intercept cannot change r. This is a limit on **this fixed predictor under affine calibration**, not on all RGB estimators.

**Status:** secondary post-hoc audit of independently published human summaries, not untouched human pixels, not a five-second within-session evaluation, not a certified clock. NRMSE thresholds 0.4/0.5/0.6/0.7/0.8 are exploratory sensitivity, not prospectively frozen. Wildcard: participant 36 shows negative within-person r on both eyes; preserve as a detector-specific anomaly, not physiology.
