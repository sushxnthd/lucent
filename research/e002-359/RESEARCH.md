# E002-359: joint shutter–occlusion observability
2026-10-22. Model-conditional synthetic result; human validation NOT RUN; publication novelty NOT ESTABLISHED.

For a calibrated pixel-integrated RGB pupil-change template a, contrast c, frame period F, exposure w<=F, short rectangular event duration D<=F, and whole-video bounded residual norm epsilon, the worst-phase separation from no event is

d_min = |c| ||a||_2 [D-(F-w)]_+ / (sqrt(2) w).

The event is guaranteed distinguishable from no event iff d_min > 2 epsilon. At equality bounded-error observations collide. This is NOT a full pupil-waveform or fatigue-state theorem.

Illustrative 30-fps, 10-ms shutter, 30-ms event, radii 5 and 5.5 px, c=.3, epsilon=.1: continuous annulus-area proxy predicts critical lid h=4.8615 px; 48x48 pixel integration yields h~3.0625 px. At h=4 px the area proxy falsely predicts guaranteed detection. Independent synthetic checker: 205,150 checks PASS; human tests NOT RUN.

Strong nuisance: eyelid aperture, pixel integration, blur, gaze, illumination, glasses, shutter response and camera ISP. All require independent calibration. Do not claim physiological pupil reconstruction or five-second fatigue diagnosis.

Prior art: Hayes & Petrov 2016 (gaze foreshortening), Petersch & Dierkes 2022 (pupil-size gaze artifact), Shah et al. EyeDentify WACV 2025 (webcam/Tobii paired images), classical bounded-noise detection. Human route: EyeDentify official Kaggle dataset; local DNS access failed once. Frozen participant/device holdout and four nuisance controls required before human conclusions.

Product: calibrated binary event detection with abstention remains research-only; reject unconditional rapid pupil waveform and fatigue certification.
