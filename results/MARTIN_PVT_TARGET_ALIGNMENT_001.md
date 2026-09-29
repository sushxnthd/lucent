# MARTIN-PVT-TARGET-ALIGNMENT-001: Independent PVT Replication

**Status:** completed preregistered independent public-human-data analysis.

**Primary Temporal Alignment interaction:** **NOT SUPPORTED**.

## Dataset and frozen protocol

Martin, Whittaker & Johnston (2022), Experiment 2; 250 Hz EyeLink pupil area during a psychomotor-vigilance task.

- participant folders seen: **25**
- participants included after frozen Block-1/evaluation QC: **25**
- common Block 2/3 anchors: **2,330**
- strict leave-one-participant-out prediction; held-out Block 1 used only for that person's target normalization
- predictors end immediately before target onset; no target-evoked pupil samples are used

## Duration x target-horizon matrix

| Target horizon | 2 s pupil history | 5 s pupil history | D(H)=5 s - 2 s |
| ---: | ---: | ---: | ---: |
| H0 | **0.0892** | **0.0968** | +0.0077 |
| H15 | **0.1367** | **0.1202** | -0.0165 |
| H30 | **0.1753** | **0.1498** | -0.0255 |
| H60 | **0.1995** | **0.1808** | -0.0187 |

Macro-r is the Fisher-z average of held-out participant scores; Block 2 and Block 3 correlations are first combined within person.

## Preregistered primary interaction

- D(H0): **+0.0077**
- D(H60): **-0.0187**
- Delta = D(H60) - D(H0): **-0.0264**
- paired participant-bootstrap 95% CI: **[-0.0815, +0.0281]**
- paired participants: **25**

The frozen criterion requires a positive interaction and a 95% interval entirely above zero.

**Decision: not supported.**

## Nuisance-only baseline

The nuisance model uses only actual foreperiod and normalized block progress.

| Target horizon | nuisance-only macro-r |
| ---: | ---: |
| H0 | 0.1227 |
| H15 | 0.1679 |
| H30 | 0.2143 |
| H60 | 0.2959 |

## Secondary 1-second history

| Target horizon | 1 s macro-r |
| ---: | ---: |
| H0 | 0.0531 |
| H15 | 0.1378 |
| H30 | 0.1626 |
| H60 | 0.1984 |

## Block-count sensitivity

| Minimum anchors/block | unbootstrapped interaction |
| ---: | ---: |
| 15 | -0.0246 |
| 20 | -0.0238 |

## Interpretation

The independent PVT cohort did not satisfy the preregistered positive interaction criterion. The Massoz crossover therefore remains dataset-specific under the current evidence.

## Claim boundary

This analysis concerns pre-target pupil history and PVT performance. It does not validate APST-5 active probing, smartphone pupillometry, fatigue diagnosis, or a universal temporal-alignment law.

## Reproduction

The workflow downloads the public CC BY 4.0 Figshare archive, extracts only the published ASCII event/sample files, and runs this committed analysis. Participant data are not redistributed by Lucent.
