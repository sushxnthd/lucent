# COGBEACON-TARGET-ALIGNMENT-001 Preregistration

**Status: frozen before any target-horizon outcome is computed.**

## Purpose

Independently replicate Lucent's Temporal Alignment result in a different human dataset, task, camera pipeline, and behavioral outcome.

The prior MTS-TARGET-SMOOTHING-001 result showed that broadening a PVT target from an immediate response to a 60-second performance summary made long ocular history more useful relative to a short ocular history.

This experiment asks whether the same **interaction direction** appears in CogBeacon when the behavioral target is broadened across future WCST rounds.

## Dataset

Papakostas, Rajavenkatanarayanan & Makedon (2019), CogBeacon.

Public source:
https://github.com/MikeMpapa/CogBeacon-MultiModal_Dataset_for_Cognitive_Fatigue

Use only:

- published 68-point facial landmarks recorded at 2 FPS;
- per-round WCST-like performance tables;
- session / participant identity.

Do not use EEG or fatigue self-report in this analysis.

## Unit of analysis

One currently correct task round.

The current round must:

1. have a valid positive response time;
2. have at least 10 facial-landmark frames, so both 2-second and 5-second windows are available;
3. have at least four subsequent correct rounds with valid positive response times in the same session.

The same anchor rounds are used for every sensor duration and target horizon.

## Sensor histories

Use the final:

- **2 seconds** = 4 facial frames;
- **5 seconds** = 10 facial frames;

from the current round.

No post-response or future-round facial data enter the predictor.

The facial feature map is frozen to the one used in COGBEACON-REALDATA-001:

- normalized mean landmark geometry;
- normalized landmark variability;
- end-minus-start landmark displacement;
- eye-aspect-ratio summaries;
- mouth-aspect-ratio summaries;
- frame-to-frame normalized motion.

Landmarks are normalized per frame by eye-midpoint translation and inter-eye distance.

## Behavioral target horizons

Let (z_j = log(RT_j)) for valid correct rounds in chronological order within a session.

For an anchor round (j), define:

- **H1**: (Y_1=z_j);
- **H3**: (Y_3=(z_j+z_{j+1}+z_{j+2})/3);
- **H5**: (Y_5=(z_j+z_{j+1}+z_{j+2}+z_{j+3}+z_{j+4})/5),

where subsequent terms refer to the next valid correct rounds in the same session.

H3 is secondary. H1 and H5 define the primary interaction.

This is a behavioral aggregation horizon measured in task rounds, not wall-clock seconds.

## Task covariates

The same current-round nuisance/task covariates are included at every sensor duration and target horizon:

- task level;
- question number under the current rule;
- normalized round progress through the session;
- round number under the same rule.

No future task covariates are supplied to the model.

## Model

No tuning.

- StandardScaler
- Ridge(alpha=10)

## Generalization

Strict leave-one-**person**-out evaluation.

CogBeacon's `b` suffix denotes a later data-collection day and is collapsed to the same person ID. All sessions from the held-out person remain outside training.

## Metric

For every held-out session with at least 12 common anchor rounds:

- Pearson correlation between predicted and observed target.

Session correlations are combined within each person in Fisher-z space.

Across-person macro-r is the Fisher-z mean of the person-level correlations.

## Primary contrast

For target horizon (H), define the relative long-history advantage

[
D(H)=r_{5s,H}-r_{2s,H}.
]

The preregistered interaction is

[
Delta=D(H5)-D(H1).
]

### Confirmatory prediction

Independent Temporal Alignment support requires:

1. (Delta>0); and
2. a paired **person-level** bootstrap 95% interval for (Delta) lies entirely above zero.

Bootstrap:

- 10,000 resamples;
- seed 20260929.

This criterion does **not** require the 2-second window to win at H1 or the 5-second window to win at H5. It tests whether broadening the target makes the longer sensing history **relatively more useful**.

## Secondary analyses

After the primary result:

- the full 2x3 sensor-duration x target-horizon matrix;
- (D(H3));
- task-covariate-only baseline at each horizon;
- sensitivity requiring at least 15 or 20 anchors per session.

Secondary results do not replace the primary criterion.

## Failure

A null or negative interaction is retained.

If the prediction fails, Temporal Alignment remains supported by MTS-TARGET-SMOOTHING-001 but is not independently replicated in CogBeacon.

## Claim boundary

A positive result would be an independent cross-dataset replication of the **directional target-horizon x sensor-history interaction**.

It would not establish:

- APST-5 active-probe validity;
- smartphone pupil measurement;
- fatigue diagnosis;
- a universal optimal scan duration;
- a causal neurophysiological mechanism.
