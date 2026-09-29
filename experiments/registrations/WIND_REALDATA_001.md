# WIND-REALDATA-001 Preregistration

**Frozen before inspecting outcome relationships in the independent dataset.**

## Objective

Attempt an independent replication of Lucent's exploratory Temporal Locality result from MTS-REALDATA-001.

The claim under test is deliberately narrow:

> for an immediate behavioral response, the most recent few seconds of ocular behavior can be more informative than substantially longer passive history.

This study does **not** test APST-5 active stimulation.

## Independent source

Pillai et al. (2020), *Response time and eye tracking datasets for activities demanding varying cognitive load*, Data in Brief 33:106389.

- DOI: https://doi.org/10.1016/j.dib.2020.106389
- public data DOI: https://doi.org/10.17632/dp8g983t38.1
- license: CC BY 4.0
- participants: 28
- eye tracker: Gazepoint GP3, 60 Hz
- behavioral reference: vibrotactile Detection Response Task (DRT), stimuli every approximately 3–5 s

The dataset was collected independently of the Massoz dataset used in MTS-REALDATA-001.

## Data subset

Use only **Dual** conditions, where DRT reaction time and eye tracking were recorded simultaneously:

- Control;
- 0-back;
- 1-back;
- 2-back.

A participant-condition is included only if:

1. eye-tracking and DRT files both exist;
2. their time bases can be aligned using metadata available in the files without optimizing alignment against reaction time;
3. at least 20 valid DRT responses remain.

## Target

For each participant-condition separately, convert valid DRT response time to reciprocal response speed:

\[
v=1000/RT_{ms}.
\]

Then standardize within participant-condition:

\[
z=(v-\mu_{ic})/\sigma_{ic}.
\]

This removes the between-condition cognitive-load shift and asks whether local ocular variation predicts **trial-level immediate performance deviation**.

Valid responses must satisfy:

\[
100 \le RT_{ms} \le 2000.
\]

Missed responses are excluded from the continuous primary analysis.

## Prediction windows

Use only samples strictly **before DRT stimulus onset**.

Fixed durations:

\[
T\in\{2,5,15,30\}\text{ s}.
\]

The MTS finding predicts a short-window advantage.

### Primary contrast

\[
r_{2s}-r_{5s}.
\]

This is selected before running the outcome analysis because 2 s was the independent MTS exploratory optimum and 5 s is Lucent's original target duration.

### Secondary contrasts

- 2 s vs 15 s;
- 2 s vs 30 s.

No other duration is confirmatory.

## Ocular features

Use the same deterministic feature family for every duration.

### Pupil

From valid left/right pupil diameter:

- mean;
- standard deviation;
- 10th, 50th, 90th percentiles;
- mean absolute first difference;
- first-difference standard deviation;
- left/right asymmetry;
- valid-sample fraction.

### Gaze

From valid point-of-gaze coordinates:

- horizontal and vertical standard deviation;
- radial dispersion around window median;
- mean and 90th-percentile sample-to-sample displacement;
- valid-sample fraction.

### Blink

If the documented blink columns are present:

- blink count / entry rate in the window;
- mean reported blink duration where valid.

No feature selection will be performed after seeing results.

## Alignment rule

The eye-tracker and DRT time bases will be aligned using a deterministic rule based only on their recorded clocks / synchronization metadata.

No offset may be chosen by maximizing predictive correlation.

If no defensible deterministic alignment can be established, the experiment is recorded as **not executable on this dataset** rather than tuning an offset against outcomes.

## Model

For each duration:

- StandardScaler;
- Ridge regression with fixed \(\alpha=10\).

No hyperparameter search.

## Evaluation

Strict leave-one-participant-out evaluation.

All conditions for the held-out participant remain in the test fold.

To avoid using condition identity as a shortcut:

- target standardization is within participant-condition;
- features are centered within participant-condition using only ocular data, never reaction-time values;
- condition labels are not model inputs.

## Primary metric

For each held-out participant, calculate Pearson correlation between predicted and observed standardized reciprocal reaction speed over all valid held-out trials.

Aggregate correlations using Fisher-z averaging.

Primary statistic:

\[
\Delta r = r_{2s}-r_{5s}.
\]

## Uncertainty

Paired participant bootstrap:

- 10,000 resamples;
- seed 1517;
- 95% percentile interval for \(\Delta r\).

## Support criterion

Independent confirmatory support for Temporal Locality requires:

1. macro \(r_{2s}>r_{5s}\);
2. paired participant-bootstrap 95% CI for \(r_{2s}-r_{5s}\) excludes zero.

Secondary duration comparisons are reported regardless.

## Failure criterion

If the primary interval overlaps zero, the Windsor dataset does not independently confirm the 2-second advantage under this preregistered analysis.

The result will be retained.

## Scope boundary

Even a positive result would establish only a cross-dataset passive temporal-locality effect for immediate behavioral performance.

It would **not** establish:

- fatigue diagnosis;
- a smartphone implementation;
- APST-5 active-probe benefit;
- clinical utility.
