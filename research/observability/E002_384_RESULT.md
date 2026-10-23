# E002-384 — Clip-level calibration falsification (2026-10-23)

Frozen before evaluation in E002_384_FROZEN.md. Evidence: **synthetic instrument only**; no human, physical-camera or clinical validation.

500 independent calibration clips; 1,000 untouched same-camera clips; 1,000 untouched camera-shift clips; 60 frames per clip at 30 fps with 10-ms exposure. Three synthetic blinks per clip, V=40 normalized aperture/s, closure threshold 0.2. Optical transfer a^0.8 is integrated during exposure. Shared clip-level photometric gain, AR drift, sensor noise, rare glare, and camera-shift offsets are simulated. Seed 20261023.

Calibration absolute-error quantiles: 99th percentile **0.0169640** per frame, 95th percentile **0.0517174** of clip maxima.

| Test | Error envelope | Frame coverage | All-60-frame clip coverage (n=1000) | Wilson 95% CI |
| --- | --- | ---: | ---: | --- |
| Same camera | per-frame 99% | 59,585/60,000 (99.31%) | **736 (73.6%)** | [70.8%, 76.2%] |
| Same camera | clip-max 95% | 59,951/60,000 (99.92%) | **952 (95.2%)** | [93.7%, 96.4%] |
| Unseen camera | per-frame 99% | 55,923/60,000 (93.21%) | **23 (2.3%)** | [1.5%, 3.4%] |
| Unseen camera | clip-max 95% | 59,966/60,000 (99.94%) | **966 (96.6%)** | [95.3%, 97.6%] |

**Confirmed:** marginal frame coverage does not establish complete-recording coverage. **Partially falsified prediction:** unseen-camera shift destroyed framewise but NOT clip-max coverage in the frozen experiment. **Unsupported prediction:** zero false gap decisions were observed despite 5,399/5,395 true threshold-crossing gaps; the intended gap-falsification prediction did not materialize. Do not extrapolate zero synthetic errors to human reliability.

A candidate analytic gap certificate (using a statistical residual quantile as if it were a bound) would have issued 50,522/50,003 same-camera decisions and 50,707/50,151 unseen-camera decisions, respectively. Product-facing implementation correctly **abstains on every gap** because a finite-sample quantile is NOT a validated deterministic optical error bound. The 49,953/49,436 otherwise domain-eligible same-camera gaps are not approved as hard certificates.

Independent checker: 500 exact piecewise-linear exposure integrations (max error 3.125e-9) and 2,000 independent Lipschitz cone-intersection calculations (max error 1.67e-16), PASS.

**Product consequence:** no recording-level absence-of-closure guarantee from framewise quantiles; no hard certificate from finite-sample residual statistics alone; abstain for unseen camera, uncertain timing, glare, gaze, blur, glasses, missingness or unbounded physiology. Conditional physical calibration and paired high-speed human validation remain outstanding. No unconditional PERCLOS, pupil reconstruction or fatigue diagnosis.

**Novelty/priority:** Established statistical marginal-versus-joint coverage and distribution-shift principles; not a new universal theorem. Related: Kwon et al., J R Soc Interface (2013), doi:10.1098/rsif.2013.0227; Jung et al., ICLR 2023, Batch Multivalid Conformal Prediction. Full deterministic simulation, audit samples and vector figures are in the E002-384 reproducibility package.
