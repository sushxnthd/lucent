# Frozen ten-part scientific kernel

1. **Signal/reference:** RGB-derived per-exposure normalized eyelid closure mean vs concurrent high-speed reference c_ref(t)=1-h_ref(t)/h_open with native timestamps.
2. **Frontier:** 2013 600-fps voluntary blink kinematics, 2019 240-fps spontaneous smartphone blink study, 2025 80-person high-frame-rate video study. These do not establish hard population-wide speed bounds.
3. **Metric:** false certified-no-crossing rate against reference, peak/occupancy interval coverage, abstention fraction, holdout calibration coverage.
4. **Strongest confound:** illumination, glasses and gaze/scale bias in RGB inverse proxy; clock offset and missing frames affect gap.
5. **Generative model:** Y_kc(x)=Q_kc[(1/E_k) integral_{t_k}^{t_k+E_k} K_kc*F_c(x;scale(t),eyelid_aperture(t),pupil_radius(t),gaze(t),brightness(t)) dt]+noise. Calibrated inverse T(Y_k) must satisfy |T(Y_k)-mean_exposure(c_ref)|<=eta_k. Without this, theorem is not applicable to pixels.
6. **Falsification:** any native-reference crossing theta>H with preregistered independently valid hard U,D,eta, timing falsifies the claimed certificate.
7. **Frozen unseen synthetic prediction:** U=15/s,D=3/s,E0=8ms,E1=14ms,G=25ms,m0=.006,m1=.013: H=.09636240805676727. theta=.095 possible; theta=.100 excluded. Missing 40ms gives H=.19636240805676725. No human outcome used.
8. **Untouched human test:** freeze participant/device/lighting/glasses holdout before labels; train calibration on disjoint people/devices. Geometry-only, brightness-only, missingness-only and temporal-smoothness baselines mandatory. Require native RGB exposure times and reference synchronization.
9. **Publication threshold:** prospective unseen human boundary crossing + independent checker + exhaustive primary prior art + reproducible timestamps and calibration + false-certificate control. Synthetic theorem alone is insufficient.
10. **Product:** conditional negative threshold certificate only; otherwise abstain. Reject uncalibrated pupil waveform, precise blink velocity, PERCLOS and five-second fatigue inference.

**Acceleration:** do not repeat dataset archaeology. Two blocked data-path attempts force a switch to another path/theory. Zero spend and no user-laptop compute.