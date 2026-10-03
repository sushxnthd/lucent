# E002 external segmentation stress: AmbientEye

Status: auxiliary pre-outcome robustness test; does not modify RGB-REFERENCE-OBSERVABILITY-002.

## Motivation

AmbientEye (Han et al., 2026; arXiv:2606.03774) provides 2,606,225 pupil-annotated eye images from 35 participants across 19 countries, captured outdoors under natural ambient infrared illumination with two off-axis camera configurations and two sun-orientation conditions. The authors report a pupil-segmentation performance drop from 0.928 on controlled-IR datasets to 0.767 on AmbientEye.

This is not RGB and has no synchronized pupil-diameter reference, so it cannot establish E002 waveform observability. It is useful only as an adversarial external segmentation-domain stress test.

## Frozen role

1. Do not tune E002 waveform thresholds, smoothing, lag, missingness, or gates using AmbientEye.
2. Evaluate the selected pupil segmentation front end on AmbientEye without training on AmbientEye.
3. Report mask IoU/Dice, failure rate, predicted pupil area/diameter bias versus annotation, and quality-score calibration where available.
4. Stratify by camera configuration and sun orientation; participant-wise summaries where metadata permit.
5. Treat severe degradation as evidence that segmentation uncertainty must be propagated into E002 rather than hidden by clip exclusion.
6. Do not claim RGB generalization from AmbientEye because its modality is ambient NIR.
7. Preserve all failures in the denominator.

## Claim boundary

A good result supports only robustness of the segmentation component under a difficult independent ocular-imaging domain. A poor result is informative negative evidence. Neither outcome establishes ordinary-RGB pupil waveform fidelity, APST-5 state validity, or smartphone deployment.

## Source

Han M, Han H, Thommakoon N, Park G, Han J, Zhang X, Oakley I. AmbientEye: A Dataset for Pupil Segmentation under Natural Ambient Infrared Illumination. arXiv:2606.03774 (2026).
