# COGBEACON-REALDATA-001 Preregistration

**Frozen before analysis of the target result.**

## Objective

Test whether Lucent's temporal-locality observation generalizes to an independent human dataset and a different cognitive-performance task.

The prior MTS result found that the most recent 2 seconds of passive eyelid behavior predicted the next PVT response better than longer 5–60 second windows under a fixed target and model family.

CogBeacon provides an independent cohort, different task, different camera pipeline, and facial landmarks recorded at 2 FPS alongside per-round response times.

## Dataset

Papakostas, Rajavenkatanarayanan & Makedon (2019), CogBeacon.

Public source:
https://github.com/MikeMpapa/CogBeacon-MultiModal_Dataset_for_Cognitive_Fatigue

Use:
- facial keypoints;
- user-performance tables;
- session identity.

Do not use EEG for the primary experiment.

## Unit of analysis

One correct WCST round.

Facial frames are grouped by the round ID encoded in the published filename.

Only rounds with at least 10 recorded facial-keypoint frames are retained so that every tested duration uses the same observations.

Because facial keypoints were recorded at 2 FPS, the fixed windows are:

- 1 s = final 2 frames;
- 2 s = final 4 frames;
- 3 s = final 6 frames;
- 4 s = final 8 frames;
- 5 s = final 10 frames.

## Target

Per-round response time in seconds, log transformed.

Evaluation is within session, so stable between-person response-speed differences cannot create the primary correlation.

## Predictors

The model receives:

1. task covariates that are identical for every duration:
   - level;
   - question number under the current rule;
   - round progress through the session;
   - round number under the same rule;

2. facial-landmark summaries computed only from the selected final window:
   - normalized mean landmark geometry;
   - normalized landmark variability;
   - end-minus-start landmark displacement;
   - eye-aspect-ratio summaries;
   - mouth-aspect-ratio summaries;
   - frame-to-frame normalized motion.

Landmarks are normalized within each frame by inter-eye distance and eye-midpoint translation.

## Model

No hyperparameter search.

- StandardScaler
- Ridge(alpha=10)

A task-covariate-only Ridge model is also fitted as a baseline.

## Generalization protocol

Strict leave-one-person-out evaluation.

The b suffix in CogBeacon denotes a later collection day and is collapsed to the same person ID, so a person's second-day session can never appear in training when that person is held out.

## Primary metric

For every eligible held-out session with at least 12 retained rounds:

- Pearson correlation between predicted and observed log response time.

Session correlations are Fisher-z transformed, averaged, then transformed back to obtain macro-r.

## Primary contrast

**2 s minus 5 s** full-model macro-r.

A paired session bootstrap with 10,000 resamples and seed 20260929 provides a 95% CI.

### Confirmatory success criterion

The independent temporal-locality hypothesis is supported only if:

1. macro-r(2 s) > macro-r(5 s), and
2. the paired bootstrap 95% CI for r(2 s) - r(5 s) excludes 0 on the positive side.

## Secondary analyses

Exploratory after the primary result:

- 1, 3, and 4 second windows;
- full-model improvement over the task-only baseline;
- 3 s vs 5 s contrast;
- sensitivity after requiring at least 15 or 20 eligible trials per session.

These do not replace the primary criterion.

## Interpretation boundary

A positive result would support a target-specific temporal-locality principle across a second human dataset. It would not validate APST-5 active probing, smartphone pupillometry, or fatigue diagnosis.

A null or reversed result will be retained.
