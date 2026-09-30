# E002 Photometric Specificity Audit — Pre-Data Amendment

**Status:** frozen before any real E002 phone capture is analyzed.

## Motivation

The APST-5 display deliberately changes screen luminance. On an ordinary front camera, that can change:

- automatic exposure;
- white balance;
- sensor gain;
- local eye-region pixel intensity;
- segmentation contrast.

A split-vs-contiguous difference in the extracted pupil trace is therefore not automatically a biological pupil-response difference.

This amendment adds a **negative-control photometric audit** without changing the original E002 stimulus, capture order, O1–O4 gates, or engineering exit criterion.

## Additional per-frame diagnostics

The pupil extractor records, where face landmarks are available:

- whole-frame median grayscale;
- face-bounding-box median grayscale;
- mean iris-region median grayscale;
- mean iris radius in pixels;
- inter-eye distance in pixels.

The first three are photometric controls.

Iris radius and inter-eye distance are geometry controls that should not exhibit a true pupillary constriction waveform.

## Trace preprocessing

For every usable active capture:

1. interpolate each channel to the same 20 Hz, 0–5 s grid used for O4;
2. baseline-center over 0–0.40 s;
3. retain only captures that pass the original timing/pupil quality requirements.

Channels:

- pupil-to-iris ratio;
- face median grayscale;
- iris median grayscale;
- iris radius;
- inter-eye distance.

## Condition separation

For each channel (c), define the same O4 separation ratio

[
S_c =
rac{mathrm{median between-condition RMSE}}
{mathrm{median within-condition RMSE}}.
]

The pupil channel remains the primary E002 waveform.

## Photometric coupling

Within every active capture, compute Spearman correlation between pupil ratio and:

- face median grayscale;
- iris median grayscale.

Report the median absolute correlation across captures.

## Predeclared confound flag

Set **photometric_confounded = true** if either:

1. (S_{face}ge S_{pupil}) or (S_{irisBrightness}ge S_{pupil}); or
2. median absolute pupil–iris-brightness correlation is >= 0.80.

Set **geometry_confounded = true** if either geometry control has

[
S_{geometry}ge S_{pupil}.
]

These thresholds are deliberately conservative and are not used to tune the pupil result.

## Interpretation rule

The original E002 engineering exit criterion remains unchanged.

However, a condition-specific pupil waveform may be described as **biologically specific** only if:

- E002 O1/O2 pass;
- O4 passes;
- photometric_confounded is false;
- geometry_confounded is false.

If the original E002 clears but this audit flags a confound, the correct conclusion is:

> the phone can reproducibly distinguish the display sequences, but the current RGB pupil-extraction pipeline cannot yet establish that the discriminative waveform is biological rather than camera/segmentation response.

## Claim boundary

This audit cannot eliminate all camera confounds. It only adds explicit negative-control channels available from the same video.
