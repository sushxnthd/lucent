# E002-255 two ledgers

## SCIENCE (what is true?)
- EyeDentify (2024 preprint, WACV 2025) already pairs ordinary 30-fps webcam crops with 90-Hz Tobii pupil diameter from 51 participants; PupilSense (ETRA 2025) already implements webcam pupil regression. A general first-to-measure-webcam-pupil claim is precluded. Primary sources: https://arxiv.org/abs/2407.11204v1 ; https://arxiv.org/abs/2407.11204v2 ; https://doi.org/10.1145/3715669.3723125 .
- Independent 2026 reproduction https://github.com/CondadosAI/pupil-diameter-webcam at commit aa9bddf498a3b6e4104c2c000d2cc0c06a816aae provides public participant-level aggregates. Pooled checkpoint Pearson r=0.8755 (left), 0.8587 (right), but median participant r=0.7378 (left), 0.7147 (right). The 51 participants contribute 211,988 left and 211,919 right paired crop/label rows.
- Standard exact affine calibration identity: best in-sample positive-slope calibrated NRMSE=sqrt(1-max(r,0)^2). At exploratory NRMSE<=0.5 only 2/51 participants pass on left, 2/51 on right, 4/51 on either, 0/51 on both. At 0.6: left16/right11/either16/both11. At 0.7: left30/right26/either34/both22. At 0.8: left41/right35/either42/both34. This is a conditional *checkpoint-specific* calibration limit.
- The original EyeDentify data were collected under deliberately varying screen colors; participant-level correlation across sessions does not establish a photometry-independent within-session waveform. Webcam/Tobii alignment uses session timestamps and averaging 90-Hz readings to 30 fps, not an independent subframe exposure clock certificate.
- Checkpoint training split is not documented for this independent reproduction, so none of these participants can be called untouched holdouts. All sensitivity thresholds are post-hoc.

## PRODUCT (what changes?)
- **Remove** absolute millimeter regression and pooled correlation as sufficient Lucent measurement certificates. An oracle person-specific intercept/slope cannot fix poor waveform agreement of the released checkpoint.
- **Retain** the active normalized pupil/iris waveform hypothesis with explicit rejection; do not infer this model's failure proves RGB impossibility.
- **Require** within-session/within-condition and participant-level metrics, exposure-clock certification, photometric placebo, geometric scale placebo, independent reference replay, nondegeneracy, and holdout devices/glasses before any five-second state inference.
- **Next highest-information test:** obtain truly synchronized RGB/reference paired human data and compare frozen normalized ocular observable with brightness-only and geometry-only baselines. EyeDentify crop/label pairs are useful for exploratory analysis but cannot alone certify rapid lag.

**Smallest supported claim:** In an independently published reproduction of a released webcam pupil regressor, strong pooled correlation masks materially weaker typical participant-level agreement; affine calibration alone cannot achieve an exploratory 0.5 NRMSE gate for most subjects. No field-level breakthrough or general RGB impossibility.
