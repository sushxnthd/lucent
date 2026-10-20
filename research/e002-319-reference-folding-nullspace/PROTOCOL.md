# Frozen E002-319 measurement-science kernel

1. **Signal/reference:** 30-fps RGB eye frame I_j with true shutter time, 90-Hz Tobii pupil diameter x(t), and processed label y_j. Only the documented reference operator was analyzed, no human samples.
2. **Frontier:** Shah et al., EyeDentify 2024, https://arxiv.org/abs/2407.11204; published implementation at https://github.com/vijulshah/eyedentify/blob/main/data_creation/eyedentify/tobii_and_webcam_data_alignment.py. Rank-nullity and sampling theory are classical.
3. **Metric:** exact operator rank/nullity, spectral |H(f)|, bounded-speed label error L*B_j, session-mean preservation, native-versus-folded slope, future corrected-label holdout coverage.
4. **Strongest confound:** nonlocal three-second reference folding; further RGB nuisances: differential optics, aperture, gaze, illumination, glasses, blur, camera response, exposure and clock offset.
5. **Generative model:** I_j=Gamma_j(integral over exposure E_j of w_j(t)[K_j,t * F(q(t),h(t),g(t),illumination(t),optics(t))]dt)+noise; x_n=q(n/90)+reference noise; y_j=(x_j+x_{j+90}+x_{j+180})/3 under equal bins.
6. **Falsification:** public released dataset uses different corrected per-frame alignment; actual records do not satisfy equal-bin idealization; source implementation materially differs. Revise dataset-specific conclusion, not the conditional theorem.
7. **Frozen prediction:** 0.333333-Hz 0.2-mm sinusoid folds to constant, a 0.1-mm/s drift appears as 0.033333-mm/s on webcam time, B_45=2/3s. Frozen before running synthetic checks.
8. **Untouched human test:** obtain native Tobii samples and true webcam frame/exposure timestamps; estimate offset/drift on calibration participants only; construct shutter-matched labels with uncertainty intervals; freeze before held-out participants/devices/lighting/gaze/glasses. Include geometry-only, brightness-only, missingness-only, temporal-smoothness baselines. Not performed.
9. **Publication threshold:** verify actual dataset bytes, correct alignment on raw human recordings, untouched human holdout, external checker and meaningful new RGB observability result. Source-only analysis does not qualify.
10. **Product:** reject folded per-frame pupil waveform/lag labels for Lucent certification; conditionally allow independently checked session-mean endpoint; require native timestamps and uncertainty-aware alignment; continue calibrated eyelid-occupancy research.

Acceleration: at most one additional substantive EyeDentify data-access attempt; if blocked, pivot to independent measurement science. Do not spend unlimited runs on metadata.
