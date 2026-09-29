# TEMPORAL-ALIGNMENT-001: Controlled Target-History Crossover

**Status:** preregistered positive result, nuisance-audited, with two preregistered failed interaction replications.

## Result in one sentence

In the Massoz PVT/eyelid dataset, changing only the behavioral target horizon produced a large reversal in which ocular history length was most predictive; that crossover survived an explicit time-on-task/session nuisance audit, but the same directional interaction did not replicate in either an independent PVT/pupil cohort or CogBeacon.

## Primary Massoz result

MTS-TARGET-SMOOTHING-001 held fixed:

- participants;
- public ocular data;
- feature family;
- Ridge model;
- leave-one-subject-out evaluation;
- common event intersection.

Only target temporal support was changed.

| Target support | 2 s sensor | 5 s | 15 s | 30 s | 60 s |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 s | **0.2700** | 0.1975 | 0.1199 | 0.0968 | 0.0744 |
| 15 s | **0.1868** | 0.1608 | 0.1339 | 0.1339 | 0.1209 |
| 30 s | **0.1678** | 0.1522 | 0.1547 | 0.1561 | 0.1592 |
| 60 s | 0.1559 | 0.1607 | 0.1712 | 0.1953 | **0.2042** |

Define

[
D(H)=r_{60s,H}-r_{2s,H}.
]

The preregistered interaction was

[
Delta=D(60)-D(0)=+0.2439,
]

with paired-subject bootstrap 95% CI

[
[+0.1647,+0.3191].
]

N = 28 paired subjects.

## Nuisance audit

MTS-TEMPORAL-ALIGNMENT-NUISANCE-001 was frozen after the independent replication failures but before recomputing the adjusted outcome.

Every duration model received the same explicit nuisance variables:

- normalized time-on-task;
- squared time-on-task;
- PVT2/PVT3 session identity.

The adjusted matrix still crossed:

| Target support | 2 s | 60 s | nuisance only |
| ---: | ---: | ---: | ---: |
| 0 s | **0.2672** | 0.0892 | 0.0645 |
| 60 s | 0.2236 | **0.2513** | 0.2177 |

Adjusted interaction:

[
Delta_{adjusted}=+0.2056,
]

95% CI

[
[+0.1328,+0.2749].
]

Thus the original crossover is not explained solely by this frozen low-frequency time/session nuisance model.

## Independent interaction replications

### Martin PVT / pupil area

MARTIN-PVT-TARGET-ALIGNMENT-001 preserved the psychomotor-vigilance target family while changing cohort and ocular measurement.

- 25/25 participants passed frozen participant-level QC;
- 2,330 common Block 2/3 anchors;
- 250 Hz EyeLink pupil area;
- strict leave-one-participant-out evaluation;
- Block 1 used only for participant-specific target normalization.

| Target | 2 s pupil | 5 s pupil | D(H)=5 s - 2 s |
| --- | ---: | ---: | ---: |
| H0 | 0.0892 | 0.0968 | +0.0077 |
| H15 | 0.1367 | 0.1202 | -0.0165 |
| H30 | 0.1753 | 0.1498 | -0.0255 |
| H60 | 0.1995 | 0.1808 | -0.0187 |

Primary interaction:

[
Delta=-0.0264,
]

95% CI

[
[-0.0815,+0.0281].
]

**Not supported.**

The nuisance-only model using foreperiod and block progress outperformed the pupil model at every horizon and reached macro-r 0.2959 at H60.

### CogBeacon / facial landmarks

COGBEACON-TARGET-ALIGNMENT-001 used:

- 20 people;
- 77 sessions;
- 1,786 common anchors;
- 2 s and 5 s facial-landmark histories;
- strict leave-one-person-out evaluation.

Primary interaction:

[
Delta=-0.0645,
]

95% CI

[
[-0.1665,+0.0313].
]

**Not supported.**

## Current scientific interpretation

The data reject two simple stories:

1. **shorter history is universally better** — false across the independent duration tests;
2. **broadening the target generally makes longer history better** — not replicated.

The strongest defensible empirical statement is:

> **sensor-history length and target aggregation horizon are separate design axes. Their interaction can be large enough to reverse the preferred sensing window in a specific signal × target × protocol system, but the sign of that interaction is not universal.**

That interpretation is also more consistent with recent theory in which label construction and latent temporal dynamics jointly determine the effective observation span.

## Relation to prior work

Massoz et al. (2018) already established multi-timescale drowsiness modeling and an accuracy-responsiveness trade-off using matched 5/15/30/60-second sensor/ground-truth branches.

Lucent's narrower empirical extension is:

- crossing sensor-history duration and target horizon **orthogonally**;
- holding the remaining analysis pipeline fixed;
- preregistering the interaction statistic;
- stress-testing it with independent datasets and a nuisance audit;
- retaining failed replications.

See [docs/TEMPORAL_ALIGNMENT_RELATED_WORK.md](../docs/TEMPORAL_ALIGNMENT_RELATED_WORK.md).

## Consequence for APST-5

The passive-data evidence does not justify choosing a universal 2-, 3-, 5-, or 60-second scan.

APST-5 should instead be evaluated target-by-target:

1. establish incremental observable information beyond trivial temporal/task context;
2. identify the relevant history under that target and measurement channel;
3. test whether a controlled active perturbation increases information density;
4. validate the result prospectively on unseen people/devices;
5. replicate before product claims.

## Claim boundary

None of these passive-data analyses validates:

- active phone-display probing;
- smartphone pupillometry;
- fatigue diagnosis;
- a universal temporal-alignment law;
- a specific physiological mechanism.

The next non-substitutable evidence is prospective synchronized phone data under the frozen E002 matched-exposure protocol.

## Reproduction

Primary crossover:

    python experiments/mts_target_smoothing.py

Nuisance audit:

    python experiments/mts_temporal_alignment_nuisance.py

Independent Martin PVT replication is reproducible through its committed GitHub workflow because it downloads the public Figshare raw-data archive.

See also:

- results/MTS_TARGET_SMOOTHING_001.md
- results/MTS_TEMPORAL_ALIGNMENT_NUISANCE_001.md
- results/MARTIN_PVT_TARGET_ALIGNMENT_001.md
- results/COGBEACON_TARGET_ALIGNMENT_001.md
- results/TEMPORAL_SCALE_AUDIT_001.md
