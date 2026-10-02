# E002 external segmentation robustness note

Date: 2026-10-03
Parent protocol: RGB-REFERENCE-OBSERVABILITY-002 (frozen; unchanged)

## New public resource

MEYELens (Vecchieschi et al., Behavior Research Methods, 2026; DOI 10.3758/s13428-026-03157-z) released an open RGB eye-region/pupil segmentation dataset associated with its model pipeline. Public descriptions report 4,895 RGB 640x480 images with pixel-level pupil and visible-eye-region masks plus subject/source metadata. The project also released updated SegFormer pupil/eye segmentation models in September 2026.

## Role in E002

This resource is NOT an independent pupil-waveform reference and therefore cannot satisfy any frozen E002 waveform gate. It must not be used to tune E002 after held-out EyeDentify outcomes are inspected.

It is useful as a pre-outcome external segmentation robustness audit: candidate pupil segmentation can be evaluated on a public RGB dataset that is independent of EyeDentify before the E002 waveform outcome is computed. This can test whether a candidate front-end is merely overfit to EyeDentify image statistics.

## Frozen-safe use

Before E002 outcome inspection:
1. evaluate pupil-mask overlap/segmentation quality on MEYELens by subject/source held-out splits where metadata permits;
2. freeze any segmentation model/checkpoint and confidence rejection rule;
3. then apply that unchanged front-end to EyeDentify;
4. keep the existing E002 waveform gates and missingness denominator unchanged.

No claim of phone/webcam waveform fidelity follows from MEYELens alone.

## Claim boundary

The dataset strengthens the external-validity design for the RGB segmentation front-end only. It does not validate pupil dynamics, fatigue/sleepiness, APST-5, smartphone deployment, or ordinary-RGB performance under the exact EyeDentify acquisition domain.
