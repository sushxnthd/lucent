# MARTIN-PVT-TARGET-ALIGNMENT-001 Preregistration

**Status: frozen before any target-horizon prediction outcome is computed.**

## Purpose

Test whether the positive Temporal Alignment interaction from MTS-TARGET-SMOOTHING-001 replicates in an independent **PVT** cohort with a different ocular measurement system.

This experiment deliberately preserves the behavioral target family (psychomotor vigilance) while changing:

- participants;
- eye tracker;
- pupil signal;
- laboratory protocol;
- raw-data source.

That makes it a stronger generalization test than switching simultaneously to a different cognitive task.

## Dataset

Martin, Whittaker & Johnston (2022), Experiment 2 from:

*Pupillometry and the vigilance decrement: Task-evoked but not baseline pupil measures reflect declining performance in visual vigilance tasks.*

Raw data:

- Figshare DOI: https://doi.org/10.6084/m9.figshare.17317886.v1
- archive: `psychomotor_vigilance_data.zip`
- license: CC BY 4.0
- 25 participant folders
- EyeLink pupil/gaze samples at 250 Hz
- trial event logs with target-onset timestamps and reaction times
- three task blocks per participant

Lucent does not redistribute the participant data.

## Chronology and role of blocks

For each participant:

- **Block 1** is used only to estimate that person's horizon-specific behavioral target mean and standard deviation.
- **Blocks 2 and 3** are the prediction/evaluation observations.

No Block 2/3 outcome is used to normalize that participant's targets.

## Trial parsing

For every trial, parse from the published EyeLink event stream:

- recording START timestamp;
- target-onset timestamp from `DISPLAY_target`;
- reaction time from `TRIAL_VAR RT`;
- block number from `TRIAL_VAR blockn`;
- trial number from `TRIAL_VAR trialn`.

Pupil area is read from the published 250 Hz sample stream.

## Valid reaction time

A reaction time is valid when:

[
100 le RT le 2000 mathrm{ms}.
]

Reciprocal reaction speed is

[
v=1000/RT.
]

## Common anchor rule

An evaluation trial in Block 2 or 3 becomes an anchor only if:

1. current RT is valid;
2. the recording contains a full 5 seconds of validly addressable pre-target sample time;
3. target onset is at least 60 seconds before the final valid target onset of the same block;
4. the 15, 30, and 60 second target horizons defined below each contain at least two valid responses;
5. both preregistered 2-second and 5-second pupil windows have at least 70% finite pupil samples.

The same anchor trials are used for every sensor-duration x target-horizon cell.

## Sensor histories

Primary sensor durations:

[
T in {2,5} mathrm{s}.
]

Both windows end immediately **before target onset**.

No target-evoked or post-response pupil sample is used.

### Fixed pupil feature map

Within each pre-target window:

1. divide pupil area by the window median;
2. compute:
   - mean;
   - standard deviation;
   - 10th, 25th, 50th, 75th, and 90th percentiles;
   - linear slope per second;
   - mean absolute first difference;
   - first-difference standard deviation;
   - valid-sample fraction.

No outcome-driven feature selection.

## Fixed task/nuisance covariates

The same covariates are included for both sensor durations and all target horizons:

- actual pre-target foreperiod = target onset minus recording START;
- normalized progress through the current block.

No future trial information is provided as a predictor.

A nuisance-only Ridge model using just these two covariates is reported as a baseline.

## Behavioral target horizons

For an anchor at target onset (t):

### H0 — immediate

[
Y_0=v_t.
]

### H15 / H30 / H60

For (H>0):

[
Y_H=
rac{1}{|J_H|}
sum_{j in J_H}v_j,
]

where (J_H) contains valid responses whose target onsets lie in

[
[t,t+H].
]

At least two valid responses are required for every nonzero horizon.

Horizons are constructed separately within each block and never cross a block boundary.

## Personal target normalization

For each participant and each horizon (H), construct the same target on eligible Block 1 anchors.

Let the Block 1 target mean and standard deviation be

[
mu_{i,H},sigma_{i,H}.
]

Every Block 2/3 target is converted to

[
Z_{i,H}=
rac{Y_{i,H}-mu_{i,H}}{sigma_{i,H}}.
]

A participant is excluded entirely if Block 1 does not provide at least 12 usable values for every target horizon or if any horizon has degenerate variance.

This target normalization is fixed before model fitting.

## Model

No tuning.

- StandardScaler
- Ridge(alpha=10)

## Generalization

Strict leave-one-**participant**-out evaluation.

For each held-out participant:

- train only on Blocks 2/3 anchors from the other participants;
- evaluate only on the held-out participant's Blocks 2/3 anchors;
- the held-out participant's Block 1 data are used only for their own target normalization.

## Metric

Compute Pearson correlation separately in held-out Block 2 and Block 3 when a block contains at least 12 common anchors.

Combine eligible block correlations for each participant in Fisher-z space.

The reported macro-r is the Fisher-z average of participant-level correlations.

## Primary interaction

For target horizon (H), define

[
D(H)=r_{5s,H}-r_{2s,H}.
]

The preregistered statistic is

[
Delta=D(60)-D(0).
]

### Confirmatory support

The independent PVT replication supports the Temporal Alignment interaction only if:

1. (Delta>0); and
2. the paired participant-bootstrap 95% interval for (Delta) lies entirely above zero.

Bootstrap:

- 10,000 paired participant resamples;
- seed 20260929.

The criterion does **not** require any particular absolute correlation or require 5 seconds to be the best possible history.

## Secondary analyses

Only after the primary result:

- H15 and H30;
- nuisance-only baselines;
- exploratory 1-second sensor history on the same anchor intersection;
- sensitivity requiring at least 15 or 20 evaluation anchors per block.

These do not replace the primary criterion.

## Failure

A null or reversed interaction is retained.

If this experiment fails, the Massoz crossover remains a dataset-specific result rather than evidence for a general PVT target-history interaction.

## Claim boundary

A positive result would show that the directional target-horizon x pupil-history interaction replicates across two independent PVT cohorts/instruments.

It would not validate:

- APST-5 active probing;
- smartphone pupillometry;
- fatigue diagnosis;
- a universal sensing duration;
- a specific neurophysiological mechanism.
