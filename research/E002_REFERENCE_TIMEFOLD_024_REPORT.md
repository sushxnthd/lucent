# E002-REFERENCE-TIMEFOLD-024: temporal-reference provenance gate

**Date:** 2026-10-08. **Type:** DISCRIMINATION / CAPABILITY-BUILDING. **Evidence:** deterministic source-code counterexample and synthetic tests, **not human measurement**.

## Source audit

The [public EyeDentify alignment implementation](https://github.com/vijulshah/eyedentify/blob/main/data_creation/eyedentify/tobii_and_webcam_data_alignment.py) converts Tobii timestamps to strings with second-level resolution, selects the first three second groups, resets their indices, averages their rows column-wise across the groups, and pairs the resulting values by row index to webcam frames. This is not a frame-timestamp join.

For an ideal three-second session (90 Hz Tobii, 30-fps RGB), the algorithm implements

`label[i] = (p(i/90)+p(1+i/90)+p(2+i/90))/3`

but pairs label i to webcam time `i/30`. A sinusoid at frequency f is multiplied by `H(f)=(1+exp(2πif)+exp(4πif))/3`, and appears at frequency f/3 on the webcam timebase. In this idealized setting the 1/3-Hz and 2/3-Hz signals cancel exactly.

## Reproducible synthetic findings

Six noiseless source-style tests, with the true RGB pupil signal identical to the Tobii pupil signal:

| Input waveform | Folded/reference range | Waveform r | nRMSE |
|---|---:|---:|---:|
| Linear ramp | 0.333 | 1.000 | 0.195 |
| One cycle in 3 s | 0 | undefined | 0.354 |
| Two cycles in 3 s | 0 | undefined | 0.354 |
| One cycle per second | 1.005 | approximately 0 | 0.503 |
| Gaussian response | 0.283 | 0.207 | 0.306 |
| Delayed exponential | 0.228 | 0.161 | 0.364 |

**Anomaly:** Pearson r=1 can coexist with threefold attenuation, and amplitude preservation can coexist with a wrong frequency. Waveform scoring must examine amplitude, lag and timing, not just correlation. Seven automated tests passed in the cloud container, including a second implementation of the fold. Reproducibility package: `lucent_e002_reference_timefold_024.zip` in the corresponding ChatGPT run.

## Discovery Protocol V2

**KNOWN:** The examined upstream source code can fold/warp three-second reference waveforms. **BELIEVED:** Released EyeDentify reference timing must be audited before E002 waveform evaluation. **CONFLICTING:** The source is intended for per-frame diameter labels; its temporal alignment is not demonstrated. **FALSIFIED:** This source-code operation generically preserves the true pupil waveform at RGB frame times. **ANOMALOUS:** Ramp correlation survives while amplitude does not; 1-Hz amplitude survives while temporal frequency does not. **UNTESTED:** Whether the public Kaggle archive used this exact pipeline, actual distortion on human sessions, RGB-to-Tobii fidelity, and five-second fatigue-state validity.

Hypothesis: source-level timestamp folding can compromise temporal reference validity independently of RGB model quality. Prediction: certain sub-three-second pupil dynamics are suppressed, delayed or time-warped. Observation: deterministic cancellation and distortion in six idealized synthetic cases. Residual: actual irregular timestamps and frame rates can change numerical outcomes. Competing explanation: released CSVs may have been generated with revised alignment code. Cheapest next experiment: obtain a few released `session_data.csv` and original raw Tobii/webcam timestamp pairs in cloud storage; compare source labels against actual timestamp-matched reference.

## Prospective, frozen human-data gates

Before final scoring, verify dataset license/provenance, participant and session identity, and exact subsecond timestamps; abstain if reference alignment cannot be established. Hash `E002-024-v1|participant_id`, sort, and assign 70%/15%/15% to development/calibration/untouched evaluation. Primary RGB observable: segmented pupil/iris diameter ratio, not raw PupilSense millimetres. Compare eye-width normalization, temporal features, geometry-only, photometry-only and missingness-only controls. Record per-participant r, normalized RMSE, gain, lag, coverage, and abstention. Prospective engineering gate: r>=0.70 and nRMSE<=0.50 on >=75% of eligible held-out participants and >=0.10 correlation improvement over strongest nuisance control. These are **not** clinical thresholds and cannot validate a five-second state claim.

Adversarial roles: Explorer seeks alternative source versions; Skeptic rejects claims of corrupted public data without provenance; Experimentalist tests source-faithful code; blinded Analyst freezes gates; Anomaly Hunter probes spectral nulls and high-r amplitude failures; Prior-Art Auditor recognizes standard DSP; Replicator reimplements the fold; Theorist separates reference timing, RGB geometry, segmentation, and missingness.

**Claim boundary:** deterministic audit of one published alignment implementation, not an empirical finding about released human labels. The earlier PupilSense scale failure remains negative. Elementary phase-folding mathematics is prior art.
