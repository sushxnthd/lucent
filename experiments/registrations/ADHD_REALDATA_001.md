# ADHD-REALDATA-001: Independent temporal-locality preregistration

**Status:** frozen before examining duration-performance outcomes.

## Purpose

Test whether Lucent's exploratory Temporal Locality effect from MTS-REALDATA-001 generalizes to a completely independent pupil + reaction-time dataset.

This is a **conceptual replication**, not a fatigue study.

## Dataset

Rojas-Líbano et al. (2019), *A pupil size, eye-tracking and neuropsychological dataset from ADHD children during a cognitive task*.

- article DOI: https://doi.org/10.1038/s41597-019-0037-2
- dataset DOI: https://doi.org/10.6084/m9.figshare.7218725.v3
- license: CC BY 4.0
- 50 participants: 22 controls, 28 ADHD; 17 ADHD participants have a second medication-state session
- 160 trials/session
- EyeLink 1000 at 1 kHz
- trial-level reaction time, accuracy, pupil time series and gaze data

The dataset is entirely independent of Massoz et al. used in MTS-REALDATA-001.

## Question

Does ocular information closest in time to an immediate behavioral response predict trial-to-trial reaction performance better than a longer history from the same trial?

## Inclusion

A session is included if:

1. task epochs decode successfully;
2. at least 40 trials have valid reaction time;
3. pupil time stamps permit a deterministic pre-response or pre-probe anchor without using outcome correlations.

Reaction time must satisfy:

\[
100 \le RT \le 5000\text{ ms}.
\]

Incorrect trials are excluded from the continuous RT primary analysis but retained for descriptive reporting.

## Anchor rule

The analysis will inspect documented task-event timing and use the latest event that occurs **before the behavioral response and is common to every trial** (preferably probe onset).

No temporal offset may be selected by maximizing reaction-time correlation.

If a leakage-free anchor cannot be established from the documented event structure, the confirmatory analysis will be marked non-executable.

## Windows

Candidate pre-anchor durations are fixed in advance:

\[
T\in\{1,2,3,5\}\text{ s}
\]

subject to the available pre-anchor trial duration.

### Primary comparison

\[
r_{2s}-r_{5s}
\]

if a full 5-second leakage-free history exists.

If task structure makes 5 seconds unavailable for all trials, the longest common preregistered duration becomes the comparator and that deviation will be recorded before outcome computation.

## Target

Reciprocal reaction speed:

\[
v=1000/RT_{ms}.
\]

Within each session, standardize:

\[
z=(v-\mu_s)/\sigma_s.
\]

The task is therefore trial-to-trial deviation rather than stable between-person speed.

## Features

From each pupil window, with the same map at every duration:

- mean;
- standard deviation;
- 10th, 25th, 50th, 75th, 90th percentiles;
- linear slope;
- mean absolute first difference;
- first-difference standard deviation;
- valid-sample fraction.

If gaze vectors are unambiguously aligned in the same epoch, add:

- x/y dispersion;
- radial dispersion;
- sample-to-sample displacement mean and 90th percentile.

No post-outcome feature selection.

## Model

- StandardScaler
- Ridge(alpha=10)
- no tuning

## Evaluation

Leave-one-**participant**-out.

If a participant has both medication sessions, both sessions stay together in the same held-out fold.

Session/group/medication labels are not predictors.

## Metric

Per held-out participant Pearson correlation between predicted and observed within-session standardized reciprocal RT.

Aggregate in Fisher-z space.

Primary statistic:

\[
\Delta=r_{2s}-r_{5s}.
\]

## Uncertainty

Paired participant bootstrap, 10,000 samples, seed 1517.

## Confirmatory support

Temporal Locality receives independent conceptual support if:

1. \(r_{2s}>r_{5s}\);
2. the paired 95% bootstrap interval for \(\Delta\) excludes zero.

## Failure

If the interval overlaps zero, the independent dataset does not confirm the 2-second advantage.

The null result remains part of the Lucent evidence record.

## Claim boundary

A positive result would show cross-dataset temporal locality in ocular prediction of immediate behavioral performance.

It would not prove:

- sleep-deprivation inference;
- fatigue diagnosis;
- smartphone observability;
- active-probe superiority;
- clinical utility.
