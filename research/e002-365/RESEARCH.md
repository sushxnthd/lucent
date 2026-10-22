# E002-365 | Shutter-moment identifiability of PERCLOS (2026-10-22)

## One active scientific kernel
1. **Signal/reference:** calibrated ordinary-RGB shutter-integrated binary eyelid-closure signals vs independently synchronized high-speed eyelid reference.
2. **Frontier:** Nyström et al. 2024 DOI 10.3758/s13428-023-02333-9; Navascues-Cornago et al. 2026 DOI 10.1016/j.jtos.2026.01.003; vertical-gaze confound DOI 10.3758/s13428-026-02984-4. The linear algebra is established prior art, not claimed novel.
3. **Metric:** sharp interval [P_min,P_max] for closed-time fraction PERCLOS, threshold-certification and abstention.
4. **Nuisance:** shutter overlap/blind time, spatially nonuniform lid motion, gaze, glasses, photometric drift, timing uncertainty.
5. **Generative model:** I_i=I_open,i+(I_closed,i-I_open,i)*integral k_i(t)c(t)dt+n_i. After calibrated projection y_i=integral k_i(t)c(t)dt+e_i, with binary closure c(t). Requires stable open/closed radiance and known shutter kernels.
6. **Falsification:** two binary closure histories giving identical full calibrated RGB shutter integrals but unequal PERCLOS.
7. **Mechanism-derived law:** P=integral c/T is identifiable for all binary c iff constant temporal function 1 lies in span of calibrated shutter kernels k_i. Otherwise a nonzero nullspace perturbation creates distinct binary histories with the same observations. Sharp endpoints solve two LPs on time atoms: min/max sum(width_j*x_j)/T subject to A*x=y, 0<=x<=1 (or bounded residuals).
8. **Human test:** NOT completed; preregister before untouched participant/device/lighting/gaze/glasses holdout.
9. **Publication gate:** paired human validation, independently checked predictions, strong geometry/brightness/missingness/smoothness baselines, prior-art novelty audit, reproducibility.
10. **Product:** calibrated interval + abstention only; reject closed-frame-fraction-as-exact-PERCLOS, unconditional fatigue inference and rapid pupil waveform reconstruction.

## Exact full-coverage counterexample
Two shutters cover [0,0.6] and [0.4,1], jointly covering the entire second. Closure A: [0,0.4] union [0.6,1] has P=0.8. Closure B: [0,0.2] union [0.4,0.6] union [0.8,1] has P=0.6. Both produce integrated closure y=(0.4,0.4). This is an exact collision despite zero shutter blind time and closure intervals of 200ms or longer.

For exclusive-left L, overlap M, exclusive-right R, and observations y1,y2, overlap closure m ranges from max(0,y1-L,y2-R) to min(M,y1,y2); P=(y1+y2-m)/T. This is the sharp two-window boundary.

## Synthetic 30-fps 7-row result
T=1s, 10ms rectangular exposures, 7 informative rolling rows at offsets [0,4,8,12,16,20,24]ms; every time point is covered by at least one shutter. When each shutter integrates 50% closure, the sharp PERCLOS interval is [0.4303333333,0.5696666667] (13.933 percentage points) even without noise. With ±0.01 error in shutter-mean closure, interval widens to [0.4213333333,0.5786666667]. Exact binary witnesses exist and independently match every row integral.

For separate synthetic three-bout closure with true P=0.34: 10Hz/10ms [0.03,0.93], 30Hz global/10ms [0.106667,0.806667], 30Hz rolling 8ms [0.182,0.642], rolling 16ms [0.266,0.486]. These are conditional synthetic intervals, not measured human-camera limits.

## Explicit failures
No paired ordinary RGB/high-speed human evidence, no unseen human prediction, no empirical camera shutter calibration, no established publication novelty. Arbitrary binary closure witnesses can switch faster than physiology allows; physiological dwell constraints could tighten intervals. Rolling rows may not share one binary lid state in real blinks. If that or the photometric model fails, abstain. No CI run confirmed.

## Reproduction
Source files model.py, independent_checker.py, RESULTS.json, FULL_COVERAGE_COLLISION.json, PROTOCOL_FROZEN.md, PRIOR_ART.md, PRODUCT_GATE.md and FAILED_GATES.md are in the complete run archive. Independent checker passed 1,132 tests including rational exact collisions, randomized LP checks and nullspace constructions.
