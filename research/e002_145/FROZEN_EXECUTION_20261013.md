# E002-145 frozen original-human MEYELens replay

2026-10-13. Before running original-image evaluation. This is a replay of the earlier E002-141 frozen protocol, not a new threshold-tuning experiment.

Source: Zenodo record 20492528, `human_eyeregion_pupil_segmentation_dataset.zip`; expected annotations.csv SHA-256 `32ebe8e393eda64b1c9fbdbc7048578388a188a317ddb4e57d0e1f7190d266e6`.

Sequence split: lexicographically sorted filename prefixes before `_frame_`, development index 0, untouched holdout indices 5, 10, 15, 20, 25; up to 24 evenly spaced valid frames per sequence. Prefixes are sequences, not verified subjects. Match JPEG and PNG by unique identical stem. If ambiguous, mark incomplete, never substitute samples.

Crop union of pupil and eye-region masks plus 10% margin. Reference high-resolution ratio pupil area / visible-eye area. Downsample masks nearest neighbor or fractional BOX at 128x64, 64x32, 32x16, 16x8. Compare RGB threshold baselines, with oracle eye-region mask explicitly acknowledged as optimistic non-deployable. Development-only threshold search 21 fixed thresholds, 0 to 1 step 0.05; normalized (5th/95th percentile) and raw luminance. The 2026-10-13 E002-141 protocol says development **mean Dice**; any code using median is a deviation and must be reported, not silently ignored.

Frozen gates: G0 >=3/5 holdout sequences >=10 valid pairs; G1 BOX 32x16 median relative error <=5% on >=4/5 sequences; G2 NN 16x8 worse than BOX on >=4/5; G3 normalized threshold 64x32 median Dice >=0.50 on >=3/5; G4 normalized threshold 32x16 median area-ratio error <=25% on >=3/5. G5 synchronized reference waveform and fatigue inference NOT EVALUABLE. Report all failures, non-random missingness, subgroup reversals and sensitivity, without retuning holdouts.

This dataset uses wearable close-up RGB and segmentation labels, not ordinary front-phone camera or synchronized eye-tracker waveform. No fatigue claim. Preserve negative PupilSense scale result and EyeDentify timebase concern.