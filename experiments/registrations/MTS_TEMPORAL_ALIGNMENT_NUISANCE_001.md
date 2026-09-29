# MTS-TEMPORAL-ALIGNMENT-NUISANCE-001 Preregistration

**Status: frozen before the nuisance-adjusted outcome is computed.**

## Motivation

MTS-TARGET-SMOOTHING-001 produced a large crossover:

- immediate PVT target: short ocular history was better;
- 60-second averaged PVT target: long ocular history was better.

Two independent replications have now failed to reproduce the positive interaction:

- COGBEACON-TARGET-ALIGNMENT-001;
- MARTIN-PVT-TARGET-ALIGNMENT-001.

The Martin PVT analysis also showed that simple task nuisance variables, especially time/block progress, predicted smoothed PVT targets better than the pupil-history model.

This raises a concrete falsification question:

> Is the original Massoz crossover still present after every sensor-duration model is given the same explicit time-on-task/session nuisance information?

This audit is preregistered before computing that adjusted interaction.

## Dataset and common observations

Use the same Massoz public eyelid/PVT dataset and the same common-event construction as MTS-TARGET-SMOOTHING-001.

Do not change:

- participant inclusion;
- valid RT bounds;
- sensor durations;
- target horizons;
- personal Block/PVT1 target normalization;
- ocular feature map;
- Ridge alpha;
- leave-one-subject-out split;
- bootstrap seed or count.

## Sensor histories

[
T in {2,5,15,30,60} mathrm{s}.
]

Every ocular window ends before the current PVT stimulus.

## Target horizons

[
H in {0,15,30,60} mathrm{s}.
]

Targets are exactly those from MTS-TARGET-SMOOTHING-001.

## Added nuisance covariates

Every full model at every (T,H) receives the same fixed nuisance vector:

1. normalized time-on-task within the current PVT session;
2. squared normalized time-on-task;
3. session/test indicator (PVT2 versus PVT3).

The nuisance vector is independent of sensor duration.

No reaction-time history or future information is used as a predictor.

## Models

### Nuisance-only

- nuisance vector only;
- StandardScaler;
- Ridge(alpha=10).

### Nuisance + ocular

- nuisance vector concatenated with the original ocular feature map for duration (T);
- StandardScaler;
- Ridge(alpha=10).

No tuning.

## Evaluation

Strict leave-one-subject-out, identical to MTS-TARGET-SMOOTHING-001.

Primary metric:

- held-out within-subject Pearson correlation;
- Fisher-z macro-r across participants.

## Primary interaction

Using the **nuisance + ocular** models, define

[
D(H)=r_{60s,H}-r_{2s,H},
]

and

[
Delta=D(60)-D(0).
]

### Robust support criterion

The original Temporal Alignment interaction survives nuisance adjustment only if:

1. (Delta>0); and
2. paired subject-bootstrap 95% CI for (Delta) is entirely above zero.

Bootstrap:

- 10,000 paired subject resamples;
- seed 20260929.

## Secondary diagnostics

After the primary outcome:

- full 5 x 4 adjusted matrix;
- nuisance-only macro-r at every target horizon;
- ocular incremental value = adjusted full macro-r minus nuisance-only macro-r;
- 2 s vs 60 s incremental-value differences at H0 and H60.

## Interpretation rules

### If supported

The crossover cannot be explained solely by explicit session progress/test identity under this fixed nuisance model. The result remains dataset-specific but gains a stronger interpretation.

### If not supported

The earlier crossover must be downgraded. It may reflect slow time-on-task/session structure or other low-frequency nuisance that becomes easier to exploit when both predictor and target are temporally smoothed.

The null will be retained.

## Claim boundary

This audit tests one specific temporal confound model. Passing it would not prove causality or universal generalization; failing it would not imply ocular signals contain no useful vigilance information.
