# MTS-REALDATA-001 Preregistration

**Frozen before the full real-data analysis is run.**

## Source data

Public data accompanying:

Q. Massoz, J. G. Verly, M. Van Droogenbroeck,
"Multi-Timescale Drowsiness Characterization Based on a Video of a Driver's Face,"
Sensors 18(9):2801, 2018.
https://doi.org/10.3390/s18092801

The public repository contains:

- frame-level left/right eyelid-distance sequences at 30 Hz;
- Psychomotor Vigilance Test (PVT) stimulus/reaction timestamps.

Lucent does not redistribute those data.

## Question

Does a **past personal baseline** make very short pre-stimulus ocular windows more informative about subsequent vigilance performance than population-only normalization?

This is a passive-data test of the Baseline Compression Principle. It is not a test of APST-5 active stimulation.

## Cohort

Use the 29 subjects listed by the original authors for their leave-one-subject-out study:

\[
\{1,2,3,4,5,6,8,10,12,13,14,15,16,17,18,19,20,21,22,23,25,26,27,28,29,30,33,34,35\}.
\]

A subject is included if:

1. PVT1 eyelid-distance and RT files are available;
2. at least one later test (PVT2 or PVT3) has both files;
3. PVT1 has enough valid RTs to estimate a baseline mean and standard deviation.

PVT1 is used **only as prior baseline information**. PVT2/PVT3 provide held-forward samples.

## Sample definition

For each valid PVT2/PVT3 stimulus:

- use the ocular window immediately **before stimulus onset**;
- exclude RTs below 100 ms or above 2000 ms;
- require the complete requested ocular window to lie inside the recorded sequence.

Pre-stimulus windows prevent the reaction movement itself from leaking into the predictor.

## Durations

Evaluate fixed windows:

\[
T \in \{2,5,15,30,60\}\text{ seconds}.
\]

**Primary duration: 5 seconds.**

## Target

For subject \(i\), let reciprocal reaction speed be

\[
v = 1000 / RT_{\mathrm{ms}}.
\]

Using PVT1 only, compute baseline mean \(\mu_i\) and standard deviation \(\sigma_i\).

The later-test target is

\[
z_{it} = \frac{v_{it}-\mu_i}{\sigma_i}.
\]

Thus the task is to predict **within-person vigilance deviation from an earlier rested/reference session**, not raw between-person reaction skill.

## Ocular normalization conditions

### Population-only

For each held-out-subject fold:

1. estimate open-eye scale from PVT1 of training subjects only;
2. estimate a population baseline feature vector from PVT1 of training subjects only;
3. normalize held-out PVT2/PVT3 windows using only those population quantities.

The held-out subject contributes no ocular baseline to this condition.

### Personalized

For every subject:

1. estimate left/right open-eye scale from that subject's own PVT1 only;
2. estimate that subject's PVT1 baseline feature vector;
3. express PVT2/PVT3 windows as deviations from that earlier baseline.

No PVT2/PVT3 observation is allowed to update the baseline.

## Features

The same deterministic feature map is used in both conditions after normalization:

- mean aperture;
- standard deviation;
- 5th, 10th, 25th, 50th, 75th, 90th, 95th percentiles;
- fraction below 0.8, 0.7, and 0.5 normalized aperture;
- mean absolute first difference;
- first-difference standard deviation;
- closure-entry rate below 0.7;
- mean absolute left/right asymmetry.

No feature selection will be performed after seeing results.

## Model

For every duration and normalization condition:

- StandardScaler;
- Ridge regression with fixed \(\alpha=10\).

No hyperparameter search.

## Evaluation

Strict **leave-one-subject-out** evaluation.

The held-out subject's PVT2/PVT3 samples are never used to fit the population model.

The personalized condition may use that held-out subject's chronologically prior PVT1 baseline because that is the intervention under test.

## Primary metric

Macro within-subject Pearson correlation:

1. calculate Pearson \(r\) separately for each held-out subject between predicted and observed \(z\);
2. Fisher-transform valid correlations;
3. average in Fisher space;
4. transform back.

Primary comparison:

\[
r_{\mathrm{personal},5s} - r_{\mathrm{population},5s}.
\]

## Uncertainty

Paired subject bootstrap with 10,000 resamples and fixed seed 1517.

Report the 2.5% and 97.5% quantiles of the macro-correlation difference.

## Secondary metrics

- pooled Pearson correlation;
- pooled MAE;
- pooled \(R^2\);
- duration-performance curves;
- whether personalized 5 s reaches or exceeds longer population-only windows.

## Support criterion

The Baseline Compression Principle receives real-data support if:

1. personalized 5 s macro correlation exceeds population 5 s;
2. the paired subject-bootstrap 95% CI for the difference excludes zero.

A stronger temporal-compression result occurs if personalized 5 s equals or exceeds population-only performance at a longer duration.

## Failure criterion

If the primary CI overlaps zero, the public dataset does not provide confirmatory evidence that PVT1 ocular personalization improves 5-second vigilance tracking under this analysis.

That null result will be retained.
