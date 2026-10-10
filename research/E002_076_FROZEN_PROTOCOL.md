# E002-076 FROZEN PROTOCOL — Original-human pupil-mask phase aliasing

Frozen 2026-10-10 before decoding any of the 12 selected PNG masks. Study class: DISCRIMINATION / EXPLOITATION of E002-071/072. Not RGB model evaluation, iris normalization, waveform fidelity, or state inference.

## Sampling and non-leakage
Take the first 12 JPEG *file entries* from the public MEYELens ZIP central directory, ignoring folder entries, in original archive order. Match PNG masks by exact filename stem. The resulting prespecified stems, chosen without inspecting their masks:
1. eye 22_frame_000071_pic_2487
2. eye 9_frame_000161_pic_4227
3. camera0_20250717_153932_332_frame_000112_pic_112
4. eye 4_frame_000069_pic_3218
5. eye 15_frame_000114_pic_1253
6. eye 22_frame_000065_pic_2481
7. eye 9_frame_000116_pic_4182
8. pupillometry_frame_000422_pic_4784
9. eye 22_frame_000169_pic_2585
10. eye 4_frame_000156_pic_3305
11. eye 14_frame_000161_pic_1123
12. eye 6_frame_000075_pic_3598

No person labels are verified. Capture-series prefixes must NOT be represented as independent participants. This is a convenience sample (archive order), not random or population representative.

## Hypothesis
Nearest-neighbor sampling of original binary human pupil masks at webcam-like pupil sizes creates phase-dependent false pupil diameter changes even when anatomy is static. Prediction: quantization envelope grows as spatial resolution decreases.

## Algorithm and endpoints
Use red channel > 0 of original 640x480 RGB PNG annotation as binary pupil mask; ignore green channel. Verify decoded PNG dimensions, ZIP CRC32, and nonempty pupil area A. For each integer downsampling factor s in {4,8,16,32}, enumerate ALL s^2 sampling phases (dx,dy) in 0..s-1. For phase (dx,dy), count positive red pixels whose 0-indexed row mod s = dy and column mod s = dx. Let N_phase be that count. Define phase-normalized diameter d_phase / d_oracle = sqrt(s^2*N_phase/A), with zero if N_phase=0. Compute the peak-to-peak range R_s = max_phase(d_phase/d_oracle) - min_phase(d_phase/d_oracle). Report min/median/max, R_s, R_s/0.05, A, effective radius sqrt(A/pi)/s, and phase dropout fraction.

Primary endpoint: per-mask R_16 and the median across 12 masks. Prespecified 5%-response reference is purely a synthetic effect size, not measured physiology.

Gates:
- G1: all 12 original masks decode with valid CRC and nonempty pupil area.
- G2: at least 9/12 masks have R_16 > 0.05.
- G3: median(R_16) > median(R_8).
- G4: independent direct-coordinate counting matches residue histogram for all 12 masks at s=8 and s=16.
These are measurement artifact gates, not evidence of physiological observability. No post hoc threshold adjustment.

## Adversarial checks
Check both row and column phase orientation; no wrapped translation. Do not assume circular pupils. Compare with oracle area A/s^2 as denominator (this is ground truth unavailable to an RGB algorithm). Explicitly report failures, subgroup reversals, zero-count phases, and anomalous masks. Report confidence only as descriptive sample distribution, not person-level CI. The cheapest next discriminator is a separately selected archive segment and original RGB photometric/segmentation model with held-out capture series.

## Claims
Normalization, raster aliasing, and mask phase enumeration are prior art. The result may establish a reproducible, dataset-specific quantization boundary only. No novel law or RGB/Tobii waveform or APST-5 fatigue validity claim. Preserve prior PupilSense and E002-068/069/070 negatives.