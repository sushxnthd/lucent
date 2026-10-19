# Prior art and priority risk

- Park et al. ECCV 2020, EVE: https://ait.ethz.ch/eve and https://github.com/swook/EVE/blob/master/DATASET.md . EVE includes Tobii pupil sizes and RGB webcams, but its documentation warns reliable synchronization exists only between Basler and eye-tracker data.
- Daza et al. Pattern Recognition Letters 2024, mEBAL2: https://github.com/BiDAlab/mEBAL2 . RGB/NIR 30-Hz blink recordings with manually refined event labels; signed access required.
- Ehinger et al., concurrent EyeLink and Pupil Labs: https://github.com/behinger/etcomp . Lucent main contains a positive preregistered transfer result but neither device is an ordinary RGB phone.
- PyPlr (2022): https://doi.org/10.3758/s13428-021-01759-3 . Camera timing offsets can be tens of milliseconds.
- High-resolution binocular PLR (2015): https://doi.org/10.1186/s12938-015-0016-6 . 4-ms binocular reference research.
- RocSync (2025): https://arxiv.org/abs/2511.14948 . Optical clock synchronization is established engineering.
- Classical interval overlap, set-membership identification, cross-spectral delay estimation and shutter sinc attenuation predate Lucent.

**Novelty attack:** A referee can correctly reject this as a new mathematical theorem. Only prospective physical nuisance calibration with held-out ordinary-RGB/high-speed binocular validation could justify a significant measurement-science claim.
