# Frozen Lucent E002-329 observability kernel — 2026-10-20

1. Signal/reference: RGB pupil/limbus log-radius ratio change versus native-timestamp >=90Hz eye-reference pupil diameter. Blink labels are not continuous pupil ground truth.
2. Frontier: Wang/Chern/Alexa (2019) two-conic projective recovery; Hayes/Petrov (2016) gaze foreshortening; pupil-size artefact (2021); visible RGB far-red pupillometry (2023).
3. Metric: selective sign error, abstention coverage, calibrated nuisance bound B, worst participant/device/glasses/light/gaze subgroup; synthetic conic residual and q threshold.
4. Main confound: differential effective pupil/iris magnification from gaze, cornea, optical depth and glasses; aperture, photometry and segmentation.
5. Measurement: exposure-integrated RGB radiance with camera gain, blur, quantization, optical projection and segmentation; equation in THEOREM.md.
6. Falsification: independent nuisance bound undercovers untouched subjects/devices; geometry-only, brightness-only, missingness-only or smoothness-only controls explain apparent response; failed native timestamp or contour-visibility gate.
7. Prediction: synthetic rho=.4, area bias 5% boundary |k|R=.27877880968035884. For measured d=.05 and B=.05 abstain; d=.06 certifies dilation. Freeze human B separately before holdout.
8. Untouched human test: freeze native videos, reference timestamps, exposure, masks and subject/device IDs; 60/20/20 subject split; hold out a complete camera model if possible; compare projective conic, area ratio, raw diameter and four nuisance-only baselines. Cluster bootstrap; report glasses, light, gaze, blur strata. Do not claim human testing if unavailable.
9. Publication threshold: >=95% B coverage in supported subgroups, <=5% sign error among certified frames, >=50% coverage, improvement over nuisance controls, prospective boundary crossing on untouched person/device and independent cohort replication; independent checker and primary prior art required.
10. Product: reject uncalibrated rapid pupil waveforms, active-probe physiological lag and five-second fatigue claims. Conditional conic/interval research output only after optical calibration. Pivot to independently referenced eyelid events if optical B cannot be bounded.

Dataset acceleration: EyeBlink8 twice failed download, mEBAL2 and MOBIUS license-gated; do not repeat those paths without new access. Human evidence NOT RUN.