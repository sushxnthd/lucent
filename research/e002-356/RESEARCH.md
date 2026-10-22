# E002-356 — Full-RGB nuisance-orbit observability (2026-10-22)

**Status:** exact *conditional* image-space separation theorem; independently checked synthetic boundary and nonlinear-nuisance failure. No human paired-reference validation; no novel mathematics.

## Active ten-part kernel
1. **Signal/reference:** native linear-light RGB eye patch, vectorized; prospective reference: concurrently timestamped high-speed physical pupil/iris diameter, gaze and eyelid aperture with reference-specific optical calibration. Human reference NOT tested.
2. **Frontier:** Scharf & Friedlander, *Matched subspace detectors* (1994), DOI 10.1109/78.301849; Hayes & Petrov (2016), DOI 10.3758/s13428-015-0588-x; *Snip & Stitch* (2026), DOI 10.3758/s13428-026-02980-8. Core projection result is established.
3. **Metric:** d=||P_perp(mu1-mu0)||_2; deterministic collision at epsilon=d/2; ideal Gaussian equal-prior projected midpoint error Phi[-d/(2*sigma_pixel)].
4. **Strongest nuisance:** differential gaze/scale/iris edge/blur/aperture/photometry/glasses; nonlinear nuisance outside a local additive span is the decisive failure.
5. **Measurement:** I_k(x)=Q_k Gamma_k{w_k^-1 integral_shutter [PSF_k*L(x;r(t),R,a(t),g(t),illum(t),glasses(t))]dt}+noise. Reduced model y=mu_j+A nu+u_j+e, j=0/1, common A, ||P_perp u_j||<=gamma_j, ||P_perp e_j||<=epsilon_j.
6. **Falsification:** freeze A, gamma, epsilon, shutter/timebase and pupil-change bins on development subjects; reject on untouched participant/device if reference-constant pupil yields certified dilation, measured nuisance residual exceeds preregistered bounds, or reference agreement fails.
7. **Sharp boundary:** P_perp is maximal invariant under arbitrary additive A nu. The two full-image classes mu_j+col(A)+B(epsilon) are disjoint **iff** d>2 epsilon. At d<=2 epsilon, decompose mu1-mu0=A c+r; choose nuisance c in state 0 and 0 in state 1, then errors +r/2 and -r/2 produce identical observations. With isotropic projected nuisance residual balls, threshold d>epsilon0+epsilon1+gamma0+gamma1 is sharp; for structured nonlinear nuisances it is only sufficient.
8. **Untouched test:** NOT RUN. Synthetic preregistered blur crossing at sigma_pixel=0.02, radius 8->8.5 px, aperture half-height 14 px: target <=5% error requires d>=0.065794. Blur sigma 0.7 px predicts 0.372% error; 1.5 px predicts 10.739%. Fresh 240k Gaussian draws each produced 0.375% and 10.639% errors. NOT a human prediction.
9. **Publication threshold:** native RGB + independent eye reference, participant/device/lighting/gaze/glasses holdout, calibrated gamma, prospectively predicted human boundary crossing, geometry-only/brightness-only/missingness-only/smoothness baselines, reproducibility and novelty beyond matched-subspace theory. NOT MET.
10. **Product:** allow nuisance-projected RGB ocular change as research feature; calibrate/abstain on physical pupil-change inference; reject uncalibrated pupil waveforms and five-second fatigue certification; blink events remain primary human endpoint.

## Synthetic phase boundary (not webcam calibration)
48x48x3 eye renderer, pupil 8->8.5 px, iris 18 px, local nuisance basis (per-channel gain/offset, illumination gradients, translation, focus, aperture, scale, iris edge, glare). For aperture half-height 14 px:
- blur 0.7 px: d=0.107051, ideal 5%-target passed
- blur 1.5 px: d=0.049622, failed
- blur 3 px: d=0.020289, failed
- numerical 5% crossing: blur sigma=1.165003 px (uniqueness checked only on finite grid)
- aperture half-height 6 px: crossing=0.828306 px.

## Critical negative control
Finite nonlinear nuisance perturbations were rendered and projected against baseline local A. In 80 random tests for aperture 14 px, blur 0.7 px, one projected mismatch was 0.3467, larger than the pupil-state separation d=0.1071. Thus the gamma=0 local model **fails** finite-variation transport. This is NOT an exact collision for the nonlinear physical renderer. A calibrated bound is required.

## Reproducibility
Independent checker: 450 random subspace distance tests, 450 maximal-invariance tests, 450 exact collision constructions, 5 synthetic RGB image checks, and 480,000 held-out Gaussian draws; all passed. Maximum distance discrepancy 8.66e-15. Full source, raw synthetic outputs, stress tests, phase diagram, protocols and SHA256 manifest are in the downloadable E002-356 package. GitHub file coverage is recorded separately.

**Smallest claim:** exact conditional full-image nuisance-orbit boundary; synthetic blur/aperture crossing; demonstrable failure of uncalibrated nonlinear nuisance transfer. Publication-level novelty and human validation absent.
