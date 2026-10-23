# E002-390 — Self-calibrated eyelid velocity is not an observability bound

**Status:** frozen synthetic software-instrument falsification, 2026-10-23. This is not human or physical-camera validation, and the underlying temporal aliasing is established sampling theory, not a new general theorem.

## Research question
E002-371 is a conditional shutter-gap/Lipschitz-velocity law. Can the required physical speed upper bound be estimated from the *same* ordinary-camera exposure means used for the certificate? E002-390 tests that circular substitution. Protocol: [E002_390_FROZEN.md](E002_390_FROZEN.md).

## Frozen design
Synthetic 30-Hz camera, 10-ms rectangular exposures, seven frames. Aperture is a continuous piecewise-linear excursion in [0,1], with a physically known maximum slope. Threshold is 0.2. An independent calibration cohort of 1,000 simulated trajectories (seed 39001) supplies a deliberately conservative speed envelope, 1.1 times the calibration maximum. The untouched holdout consists of 1,500 different simulated trajectories (seed 39002), with maximum slope <=120/s. A 1000-Hz reference with 0.25-ms exposure is simulated separately.

The circular plug-in estimator is max absolute difference between consecutive shutter-averaged aperture measurements divided by 1/30 s. This **is not** a valid upper bound on physical velocity. Each candidate certificate uses the valid pointwise inequality

a(t) >= mean_i - epsilon - V * mean_{s in exposure_i} |s-t|,

maximized across exposures and minimized across time, with a V*h/2 grid correction. The inequality is sound only when V is a real independent upper bound and the shutter means are correctly calibrated.

## Observations
- **Exact collision:** A triangular excursion from 1 to 0.19 and back, with physical velocity 90/s, occurs entirely between 10 ms and 33.333 ms. All seven exact shutter means equal 1 (floating-point tolerance), identical to an always-open trajectory. Plug-in velocity is effectively zero and its no-crossing certificate is **false**. The independent 131.94/s bound abstains.
- **Holdout:** 1,483/1,500 hidden-threshold-crossing trajectories received a false plug-in no-crossing certificate. The correctly bounded reference calculation issued **zero** false certificates. This is a deliberately adverse synthetic distribution, not an estimated population failure rate.
- **Reference adequacy:** All 829 holdout events lasting >2 ms below threshold were detected by the simulated 1000-Hz/0.25-ms reference. This does not validate labels for shorter events or for real reference cameras.
- **Speed gap:** median physical maximum slope 95.54/s versus median ordinary-camera plug-in 10.92/s.
- **Nuisances:** gain, gaze, glare, blur, missingness, glasses and timestamp uncertainty invalidate the calibrated-means premise unless independently bounded. A fail-closed policy must abstain in those cases. The synthetic nuisance shifts were not used to estimate real-world prevalence.
- **Independent oracle:** 100 held-out trajectories recomputed with 4,000-point per-exposure quadrature and a separate absolute-value antiderivative. The exact collision and 829 reference coverage cases were independently checked.

## Scientific interpretation and negative controls
This experiment **falsifies velocity self-calibration from sparse exposure differences as a deterministic upper bound**. It does not falsify E002-371 when an independently valid speed bound is provided. The zero-error reference-bound result is largely a mathematical consequence of the model assumptions, not evidence of human reliability. The very brief excursions include events that should not be described as complete physiological blinks. The adversarial holdout is selected to contain threshold crossings, not representative no-blink negatives.

Known literature on temporal sampling/aliasing and high-speed blink kinematics must be credited; the prospective scientific contribution, if any, must come from independent physical calibration, human unseen-condition prediction and demonstrated measurement validity.

## Product enforcement consequence
**Reject:** velocity upper bounds derived solely from ordinary-RGB adjacent-frame differences, even when apparent shutter means are clean and stable. **Abstain:** absent independent kinematic envelope, exposure timing, optical transfer and nuisance bounds, or under out-of-envelope motion. **Allow only conditionally:** camera observability certificates whose actual physical calibration and human validation meet the frozen protocol. This is not a fatigue detector, PERCLOS instrument, or unconditional blink reconstruction.

## Reproduction
```bash
python -m pip install numpy
python research/observability/e002_390_velocity_aliasing.py
python research/observability/e002_390_independent_check.py
```
Seeds, 30-Hz/1000-Hz acquisition parameters, exact shutter integrals and separate calibration/holdout cohorts are embedded in the scripts. Run the independent checker without importing the primary implementation. Preserve any prediction failures rather than adjusting seeds or thresholds.

## Next human study
Synchronized ordinary RGB (30/60 Hz) and >=1000-Hz short-exposure eyelid reference; separately measure camera exposure/clock error and aperture transfer; obtain a velocity upper envelope from **disjoint high-speed calibration participants** with a stated statistical or physical interpretation. Freeze phase/gap predictions before held-out participant and camera evaluation. Report all reference-ambiguous labels as unresolved. Include gaze, glasses, illumination, geometry, blur, missingness and timestamp shifts. Require a preregistered bound on false certificates among issued decisions, not only marginal frame accuracy. Do not upgrade product claims until this gate passes.
