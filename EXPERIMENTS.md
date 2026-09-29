# Experimental Plan

This document defines the current evaluation logic for Lucent. Exact sample sizes and model families may change as data collection develops, but the anti-leakage structure should remain fixed.

## A. Data unit

Each observation should contain:

- a short front-camera video clip;
- timestamp and session identifier;
- psychomotor reaction-time measurement collected near the clip;
- subjective sleepiness score;
- recent sleep-history variables;
- device/environment metadata needed for robustness analysis.

## B. Split design

Random frame-level or clip-level splits are not acceptable as the main result.

Primary splits should include:

- **subject-held-out:** no identity overlap between train and test;
- **session-held-out:** later sessions are unseen during training;
- **device-held-out:** where collection permits;
- **environment-held-out:** lighting/location shifts where collection permits.

A within-person setting can be evaluated separately, but must be clearly distinguished from cross-person generalization.

## C. Baselines

Before using complex video models, compare against:

1. mean/median prediction;
2. time-of-day and sleep-history-only predictors;
3. simple static image features;
4. a single-frame vision model;
5. handcrafted temporal summaries where appropriate.

A video model is only useful if it adds signal beyond these baselines.

## D. Ablations

Planned ablations include:

- temporal order shuffled;
- reduced frame rate;
- cropped eye region versus full face;
- static frame versus full clip;
- removal of blink-related features;
- removal of head-motion information;
- personalized versus population-level normalization.

## E. Evaluation

Depending on the target:

- MAE / RMSE for continuous outcomes;
- rank correlation for monotonic association;
- AUROC / AUPRC for thresholded states;
- calibration error and reliability plots for probabilistic outputs;
- confidence intervals via participant-level resampling.

All metrics should be reported on held-out participants where applicable.

## F. Failure tests

Any promising model should be challenged with:

- lighting shifts;
- camera quality degradation;
- partial occlusion;
- glasses;
- altered viewing distance;
- head-pose variation;
- repeated sessions on the same participant.

## G. Evidence threshold

The working thesis is not considered supported by a single high validation score. The stronger evidence is a result that remains useful across held-out people and conditions, beats non-visual and static baselines, and reproduces on a fresh dataset.
