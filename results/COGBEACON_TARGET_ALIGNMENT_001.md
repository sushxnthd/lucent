# COGBEACON-TARGET-ALIGNMENT-001: Independent Target-Horizon Replication

**Status:** completed preregistered independent public-human-data analysis.

**Primary Temporal Alignment prediction:** **NOT SUPPORTED**.

## Dataset and frozen design

CogBeacon facial landmarks and WCST-like response times; strict leave-one-person-out evaluation.

- common anchor rounds: **1,786**
- unique people: **20**
- sessions represented: **77**
- sensor histories: **2 s** and **5 s**
- targets: current log RT (H1), mean over current + next 2 correct rounds (H3), and mean over current + next 4 correct rounds (H5)

## Duration x target-horizon matrix

| Target horizon | 2 s facial history | 5 s facial history | D(H)=5 s - 2 s |
| ---: | ---: | ---: | ---: |
| H1 | **0.1271** | **0.1629** | +0.0358 |
| H3 | **0.0938** | **0.0455** | -0.0483 |
| H5 | **0.1110** | **0.0823** | -0.0288 |

Macro-r is the Fisher-z mean of person-level held-out correlations; each person's score first combines eligible session correlations in Fisher-z space.

## Preregistered primary interaction

- D(H1): **+0.0358**
- D(H5): **-0.0288**
- Delta = D(H5) - D(H1): **-0.0645**
- paired person-bootstrap 95% CI: **[-0.1665, +0.0313]**
- paired people: **20**

The frozen confirmatory criterion requires a positive interaction with the entire 95% interval above zero.

**Decision: not supported.**

## Secondary H3

D(H3) = r(5 s,H3) - r(2 s,H3) = **-0.0483**.

## Task-only baselines

| Target horizon | task-only macro-r |
| ---: | ---: |
| H1 | 0.1551 |
| H3 | 0.1679 |
| H5 | 0.2072 |

## Session-count sensitivity

| Minimum anchors/session | unbootstrapped interaction |
| ---: | ---: |
| 15 | -0.0495 |
| 20 | -0.0471 |

## Interpretation

Broadening the behavioral target did not produce the preregistered positive long-versus-short history interaction. The independent replication therefore does not confirm Temporal Alignment in this task, and the null/reversed result is retained.

## Claim boundary

The target horizon here is defined in future task rounds rather than wall-clock seconds. The result concerns predictive temporal alignment in this observational dataset. It does not establish an active-probe effect, smartphone pupil validity, fatigue diagnosis, or a neurophysiological mechanism.

## Reproduction

The source participant data are not redistributed. The workflow downloads CogBeacon's public facial-landmark and performance archives and executes this committed analysis.
