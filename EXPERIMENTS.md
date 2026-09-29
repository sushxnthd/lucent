# Experimental Program

This document defines the experimental logic for Lucent. Model families and exact sample sizes may evolve, but the anti-leakage rules should remain stable.

## 1. Unit of observation

A paired observation should contain:

- one short front-camera video clip;
- participant identifier;
- session identifier;
- capture timestamp;
- device metadata;
- psychomotor / reaction-time measurement collected near the clip;
- subjective state-sleepiness score;
- recent sleep-history variables;
- environmental metadata required for robustness analysis.

Derived frames from the same source clip are never allowed to cross a train/test boundary.

## 2. Collection sequence

A candidate session:

1. quality check and standardized camera placement;
2. short front-camera clip;
3. state sleepiness rating;
4. psychomotor vigilance / reaction-time task;
5. recent sleep and contextual metadata;
6. optional repeated clip after the task for temporal stability analysis.

The allowed time interval between video and reference measurement must be pre-specified for each study.

## 3. Primary split design

Random frame-level or clip-level splits are **not** accepted as the primary result.

### A. Participant-held-out
No participant identity appears in both training and test sets.

### B. Session-held-out
Later or otherwise isolated sessions are held out when evaluating longitudinal generalization.

### C. Device-held-out
Where sample size permits, one or more device families are held out.

### D. Environment-held-out
Lighting, location, or recording-condition shifts are evaluated separately.

Within-person evaluation is useful but must be reported as a distinct task.

## 4. Baseline ladder

Before complex video models, compare against:

1. constant mean / median;
2. time-of-day only;
3. sleep-history only;
4. time + sleep-history + metadata;
5. static frame;
6. handcrafted ocular / motion summaries;
7. full temporal video representation.

The question is not "does the model predict?" It is "what information does video add?"

## 5. Ablation matrix

Planned ablations include:

- full clip vs single frame;
- temporal order preserved vs shuffled;
- full face vs eye region;
- high vs reduced frame rate;
- with vs without blink-related features;
- with vs without head-motion features;
- raw target vs person-centered target;
- metadata available vs removed;
- confidence-aware vs point prediction only.

## 6. Metrics

### Continuous targets
- MAE;
- RMSE;
- R²;
- rank correlation where relevant;
- participant-level bootstrap confidence intervals.

### Thresholded targets
- AUROC;
- AUPRC;
- sensitivity / specificity at pre-declared thresholds;
- calibration / reliability.

All aggregate metrics should be paired with participant-level distributions to expose subgroup or outlier effects.

## 7. Leakage audit

Before any result is accepted:

- verify participant sets are disjoint;
- verify source recordings are disjoint;
- inspect timestamps for accidental session leakage;
- train a participant-ID probe on the representation;
- train a device-ID probe where metadata permits;
- compare random-split and participant-held-out performance;
- inspect nearest neighbors in embedding space;
- check whether labels can be predicted from metadata alone.

## 8. Stress tests

Promising models should be challenged with:

- lighting shifts;
- compression and resolution degradation;
- partial occlusion;
- glasses;
- altered viewing distance;
- head-pose variation;
- camera movement;
- unseen devices;
- repeated sessions separated in time.

## 9. Statistical discipline

Before a confirmatory experiment:

- specify the primary target;
- specify the primary metric;
- specify participant inclusion / exclusion rules;
- specify the split seed or split-generation rule;
- specify which analyses are exploratory;
- freeze the model or model-selection rule before evaluating the final holdout.

The repository includes a [preregistration template](docs/PREREGISTRATION_TEMPLATE.md).

## 10. Publication rule

A result is not promoted as evidence for the central thesis because it scores well on one split.

The minimum interesting result is one that:

- beats non-visual and static baselines;
- survives participant-held-out evaluation;
- retains useful signal under at least one meaningful distribution shift;
- includes uncertainty;
- can be reproduced from a committed configuration.

The strongest result is a frozen pipeline that reproduces on a fresh cohort.
