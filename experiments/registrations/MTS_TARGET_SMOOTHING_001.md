# MTS-TARGET-SMOOTHING-001 Preregistration

**Frozen before the target-smoothing outcome is computed.**

## Purpose

Directly test the second prediction of Lucent's Temporal Alignment Principle:

> deliberately broadening the temporal support of a behavioral target should increase the relative usefulness of a longer ocular sensing history.

This is a stronger test than comparing unrelated datasets because the source participants, ocular signal, feature family, model family, and evaluation protocol remain fixed while only the target timescale is manipulated.

## Dataset

Massoz, Verly & Van Droogenbroeck (2018), public eyelid-distance sequences plus PVT reaction-time logs.

Source:
https://github.com/QMassoz/mts-drowsiness

The source participant data are downloaded at runtime and are not redistributed.

## Participants and sessions

Use the same subject list and session structure as MTS-REALDATA-001.

- PVT1: chronologically earlier session, used only for subject-specific target normalization.
- PVT2/PVT3: evaluation sessions.
- strict leave-one-subject-out model evaluation.

## Common anchor rule

Every analyzed PVT event must:

1. have a valid current reaction time in [100, 2000] ms;
2. occur at least 60 s after the beginning of the eyelid sequence;
3. occur at least 60 s before the final PVT event in that session;
4. admit every preregistered ocular window;
5. admit every preregistered target horizon.

The same event intersection is used for every duration × target-horizon cell.

## Ocular sensing durations

Pre-stimulus windows ending immediately before the current PVT stimulus:

[
T \in \{2,5,15,30,60\}\text{ s}.
]

The feature map is unchanged from MTS-REALDATA-001:

- aperture mean and standard deviation;
- aperture quantiles;
- closure fractions;
- first-difference magnitude and variability;
- closure-entry rate;
- inter-eye asymmetry.

Use population-level eye-opening and feature baselines estimated from training subjects only.

No personalized ocular baseline is used in the primary experiment.

## Manipulated target timescale

For each current PVT event at time (t), define reciprocal reaction speed

[
v_j=1000/RT_j.
]

Four future-support targets are fixed:

[
H \in \{0,15,30,60\}\text{ s}.
]

For (H=0), the target is the current response speed.

For (H>0), the target is the mean reciprocal speed of valid PVT responses whose stimulus onsets fall in

[
[t,t+H].
]

At least two valid responses are required for a smoothed target.

For each participant and each horizon, the target is standardized using mean and standard deviation estimated only from that participant's chronologically earlier PVT1 session under the same target construction.

## Model

For every sensor-duration × target-horizon cell:

- StandardScaler
- Ridge(alpha=10)
- no hyperparameter tuning.

## Evaluation

Strict leave-one-subject-out.

Primary metric:

- within-subject Pearson correlation on held-out PVT2/PVT3 events;
- aggregate across subjects using Fisher-z macro-r.

## Primary test

Define the relative value of long versus short ocular history at target horizon (H):

[
D(H)=r_{60s,H}-r_{2s,H}.
]

The preregistered interaction is

[
\Delta = D(60s)-D(0s).
]

### Confirmatory prediction

Temporal Alignment receives direct within-dataset support if:

1. (Delta>0), and
2. a paired subject bootstrap 95% interval for (Delta) lies entirely above zero.

Bootstrap:

- 10,000 paired subject resamples;
- seed 20260929.

The claim does **not** require 60 s to become the best absolute sensor duration. It requires only that broadening target support makes the longer sensing history relatively more useful.

## Secondary analyses

After the primary result:

- full 5 × 4 duration/horizon matrix;
- (D(15)) and (D(30));
- best-performing sensing duration at each target horizon;
- 15 s, 30 s, and 60 s versus 2 s interactions.

These are secondary and do not replace the primary test.

## Failure

A null or negative interaction is retained.

If the prediction fails, cross-dataset duration differences cannot be presented as direct evidence that target temporal support caused the sign reversal.

## Claim boundary

Even a positive result would establish only a temporal-alignment effect in a public PVT/eyelid dataset.

It would not validate:

- APST-5 active probing;
- smartphone pupil measurement;
- a 2- or 3-second fatigue diagnostic;
- clinical use;
- causal neurophysiology.
