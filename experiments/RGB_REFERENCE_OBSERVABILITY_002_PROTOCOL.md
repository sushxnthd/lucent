# RGB-REFERENCE-OBSERVABILITY-002

Status: FROZEN BEFORE OUTCOME INSPECTION
Date frozen: 2026-10-01
Parent commit: 44f6db2c1c4930658893c277bd4da59700136ef4

## Question

Can an ordinary RGB eye crop preserve the short pupil-response waveform needed by APST-5 after explicit dimensionless normalization, without relying on a learned absolute-millimetre estimate?

This is an observability experiment, not a fatigue-state validation experiment. A pass does not establish that APST-5 predicts sleepiness or fatigue.

## Primary dataset

EyeDentify: webcam eye crops paired with Tobii pupil-diameter reference. Splits are participant-wise. No frame or clip from a held-out participant may be used to fit thresholds, calibration, hyperparameters, or preprocessing choices.

## Candidate observables

The primary candidate is a dimensionless pupil/reference ratio derived from explicit image geometry:

    r(t) = pupil_diameter_px(t) / stable_eye_reference_px(t)

Preferred stable references, in order, are iris diameter when recoverable, then an explicitly documented stable eye geometry reference. Both eyes are evaluated separately before any fixed bilateral aggregation.

No absolute-mm conversion is permitted in the primary method. Raw pupil pixels and the already-audited learned absolute-mm path are fixed comparators, not rescue paths.

## Waveform construction

For each 3 s clip, construct the candidate and Tobii reference waveforms after the same fixed blink/missingness policy. Normalize each waveform to its own pre-response baseline using fractional change. Do not optimize smoothing, lag, or interpolation on held-out participants.

## Frozen primary gates

A PASS requires all applicable gates simultaneously on participant-held-out evaluation:

1. median within-clip Pearson waveform correlation >= 0.70;
2. participant-bootstrap 95% CI lower bound for the median correlation >= 0.50;
3. median normalized RMSE <= 0.35;
4. response-direction agreement >= 80%;
5. median response-timing error <= 0.50 s;
6. scale-confounding ratio <= 0.25, where the induced range under 0.9x-1.1x apparent-scale perturbation is divided by the reference temporal signal range;
7. no held-out subgroup (glasses when identifiable, eye side, stimulus family, or participant quartile by segmentation quality) has a median correlation below 0.30.

PASS/FAIL/INCONCLUSIVE only. Missing metadata makes the corresponding subgroup test INCONCLUSIVE; it does not silently pass.

## Stress tests

Evaluate apparent scale, frame-rate downsampling, blur, luminance/contrast perturbation, segmentation confidence, eye side, and stimulus color. Device/domain shift is tested only when a genuinely independent RGB dataset with compatible reference exists.

## Leakage rules

Participant is the atomic split unit. No personal calibration on test participants. No threshold, lag, smoothing, segmentation cutoff, stimulus subset, or eye-selection rule may be changed after held-out outcomes are inspected. Failed clips remain in the denominator under the frozen missingness policy.

## Baselines

- raw pupil diameter in pixels;
- released learned absolute-mm estimator, reported only as a comparator because RGB-SCALE-OBSERVABILITY-001 already falsified its geometry invariance for Lucent;
- a no-dynamics baseline that predicts the participant-independent training-set mean response waveform.

## Claim boundary

A PASS supports only: ordinary RGB contains enough reference-normalized information, under the tested conditions, to recover a short evoked pupil waveform with the frozen accuracy criteria.

It does NOT establish behavioral-state validity, smartphone deployment, clinical validity, or a 5-second fatigue/sleepiness estimate. Those require a separate untouched paired-state evaluation.
