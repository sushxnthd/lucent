# E002-482 RESULT — exposure averages cannot be substituted for instantaneous eyelid apertures

**Date:** 2026-10-27. **Kernel:** E002-371. **Evidence tier:** constructed moving-aperture and spatial image-formation model only. Predictions frozen in E002_482_FROZEN.md before implementation at commit dd91290af1ae670cd54035a050844e48075b8f00. No new physical acquisitions or anatomical human trajectories.

## Scientific result and negative control

Two continuous, nonnegative aperture trajectories have the same 30-fps, 20-ms global-shutter *linear scalar exposure average* of **1 mm** and identical exposure boundary apertures. The stationary world never closes. The moving world reaches **0 mm** at 15 ms, with an assumed peak speed of **200 mm/s**. Its triangular trajectory first opens to 2 mm and then closes, so this is a constructed admissible motion, **not an observed natural human blink**. Exact trapezoidal integration of the piecewise-linear motion yields identical scalar measurements.

**Crucial limitation:** the scalar average is not a real camera's complete image. Under a calibrated spatial edge-response model with Gaussian blur sigma=0.2 mm, the two worlds differ by a maximum of **0.283199 normalized pixel units**. The model therefore does **not** assert that full sharp camera images are identical. This is a successful negative control.

With 41 pixels at 0.1-mm pitch, sigma=1 mm and one unconstrained global affine brightness gain/offset, the *constructed* maximum residual falls to **0.018091**. Under hypothetical independently bounded per-world pixel errors of +/-0.01, the two model predictions admit a common observation because the maximum residual is below 0.02. The fitted gain is approximately 0.922876 and offset 0.038562. At sigma=2 mm, the residual is **0.001441**. This is an **existence witness**, not a probability or an empirical sensor noise measurement. When brightness is calibrated and fixed, the sigma=1-mm maximum difference is 0.036570, above the 0.02 two-world overlap tolerance. Unconstrained brightness is therefore a decisive nuisance in this model.

## Timing and occlusion falsification controls

A second camera row shifted by 2 ms has moving-world scalar average **0.98 mm**; a 5-ms shift gives **0.875 mm** rather than 1 mm. However, if the 2-ms row offset has independent +/-2-ms timing uncertainty, the guaranteed difference is **zero**. A 5-ms row offset with +/-1-ms uncertainty guarantees at least **0.08 mm** separation under the frozen waveform. Removing the upper half of spatial pixels does not destroy an existing indistinguishability witness. Rolling-row timing is therefore potentially useful only when externally calibrated; unknown row offsets do not automatically rescue closure identification.

The Gaussian spatial integral was independently cross-checked by 8,000-sample midpoint time quadrature at 15 frozen blur/position settings; maximum discrepancy was below **7e-8**. Fourteen local Node adversarial tests passed before persistence, including invalid inputs, timing uncertainty, sharp-optics control, blur, missing/occluded pixels and claim abstention. Hosted CI must be checked separately.

## New product consequence

An exposure-averaged scalar feature cannot be used as the *instantaneous endpoint aperture* in E002-371's conditional velocity/shutter-gap exclusion. A valid product pathway requires independent shutter/row calibration, measured blur and image-formation uncertainty, brightness/gain controls, reference aperture trajectories, and explicit identifiability testing. Otherwise output **ABSTAIN_UNCALIBRATED**. This is stricter than a simple frame-rate threshold, but does not overturn E002-371's mathematical theorem under its stated instantaneous-measurement assumptions.

## External human evidence and immediate physical gate

A newly located FaceBase release from September 1, 2026 describes **400-fps hardware-synchronized three-dimensional eyelid marker trajectories** from eight adults across five eyelid behaviors. It is **restricted-access** and requires an approved data request, so no rows were obtained or tested: https://doi.org/10.25550/88-28BJ ; associated primary paper https://doi.org/10.1073/pnas.2508058122 . A separate 2025 Scientific Data multimodal eye dataset exists (https://doi.org/10.1038/s41597-025-04861-9), but its readily accessible EEG mirrors do not establish anatomical high-speed eyelid trajectories suitable for this test. Neither source is represented as validated here.

**Physical handoff:** independently log camera exposure windows, rolling-row phase, photodiode pulses and a 400+ fps anatomical/moving-aperture reference. Freeze participant-disjoint and held-out lighting, gaze, glasses, blur, brightness, row-offset and dropped-frame challenges. Test the full pixel forward model rather than scalar averages. Reject hidden-closure exclusion whenever a second admissible trajectory fits within measured image and clock error budgets. Do not infer a universal physiological hard velocity cap from a finite sample maximum.

Physical shutter acquisitions **0**; new anatomical reference sequences **0**; E002-371 physical validation **NOT ESTABLISHED**; hidden-closure, blink-duration, PERCLOS, fatigue and medical outputs **ABSTAIN_UNCALIBRATED**. No merge, release or deployment.
