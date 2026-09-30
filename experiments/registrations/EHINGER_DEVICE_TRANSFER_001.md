# EHINGER-DEVICE-TRANSFER-001 Preregistration

**Status: frozen before any cross-device agreement outcome is computed.**

## Purpose

Test whether controlled luminance-evoked pupil dynamics measured by a lower-cost video eye tracker preserve the waveform structure measured concurrently by a laboratory EyeLink system.

This is an instrumentation bridge for Lucent. It does **not** test a phone camera and it does not test fatigue/state prediction.

## Dataset

Ehinger et al. (2019), public eye-tracker comparison dataset.

Sources:

- repository: https://github.com/behinger/etcomp
- Figshare collection: https://doi.org/10.6084/m9.figshare.c.4379810.v1
- preprocessed luminance data: `lum_binned.csv`

The released luminance table contains concurrent:

- EyeLink 1000 (`el`);
- Pupil Labs glasses (`pl`);

for 15 participants, six blocks, and screen luminance codes:

[
0,64,128,192,255.
]

The experiment code shows the display luminance is changed while participants maintain central fixation.

## Fixed analysis window

Use only:

[
0 le t le 2.8 mathrm{s}
]

after each luminance onset.

This window is frozen before analysis because non-black display conditions advance after approximately 3 seconds, while the black condition lasts longer. Restricting every condition to 2.8 seconds avoids contamination from the subsequent screen transition.

Use the released `pa_norm` pupil-area normalization without further outcome-driven filtering.

## Complete paired groups

A subject × block × luminance cell is usable only when both `el` and `pl` contain at least 15 finite samples in the fixed window.

The same time grid is matched by nearest `td` value after sorting. If the two devices have unequal rows, interpolate each onto the common 10 Hz-equivalent grid defined by the released binned `td` support in the fixed window.

## Train / held-out blocks

For every participant:

- blocks 1–3: device-calibration blocks;
- blocks 4–6: held-out evaluation blocks.

No held-out EyeLink value is used to fit device calibration.

## Per-participant device calibration

On blocks 1–3, fit the frozen affine mapping

[
hat y_{EL}=a_i+b_i y_{PL}
]

using ordinary least squares across all paired luminance/time samples.

No nonlinear mapping and no hyperparameter tuning.

Apply (a_i,b_i) unchanged to Pupil Labs measurements in blocks 4–6.

## Primary held-out metric

For each participant, concatenate all valid held-out samples across blocks 4–6 and all five luminance levels.

Compute:

1. Pearson correlation between calibrated Pupil Labs and EyeLink pupil waveforms;
2. normalized RMSE:

[
NRMSE_i =
rac{RMSE(hat y_{EL},y_{EL})}
{P_{95}(y_{EL})-P_{5}(y_{EL})}.
]

Aggregate correlation across participants using Fisher-z macro-r.

Bootstrap participants 10,000 times with seed 20260930.

## Primary support criterion

Cross-device waveform preservation is supported only if:

1. the participant-bootstrap 95% CI lower bound for macro-r is **> 0.70**; and
2. at least **80%** of participants have individual held-out (r>0.70).

The NRMSE distribution is reported but is not part of the primary pass/fail rule.

## Secondary analyses

After the primary result:

- uncalibrated Pupil Labs vs EyeLink held-out correlation;
- per-luminance held-out correlations;
- response-amplitude agreement using median `pa_norm` from 1.5–2.5 s;
- held-out results restricted to the four nonzero luminance codes;
- block-wise agreement.

These cannot replace the primary criterion.

## Failure

A null/weak result is retained.

## Claim boundary

A positive result would show that a public lower-cost **video eye tracker** preserves controlled luminance-evoked pupil waveform structure relative to concurrent EyeLink measurements after simple participant-specific calibration.

It would not establish:

- ordinary RGB webcam/phone pupil tracking;
- Lucent E002 split-vs-contiguous observability;
- state/fatigue inference;
- clinical validity.
