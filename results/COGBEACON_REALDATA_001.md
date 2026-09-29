# COGBEACON-REALDATA-001: Independent Temporal-Locality Test

**Status:** completed independent public-human-data analysis.

**Preregistered 2 s > 5 s hypothesis:** **NOT SUPPORTED**.

## Dataset

CogBeacon (Papakostas, Rajavenkatanarayanan & Makedon, 2019), using published 68-point facial landmarks and per-round WCST response times.

- eligible correct rounds with >=10 facial frames: **1,892**
- unique people: **20**
- sessions represented: **77**
- facial sampling rate: **2 FPS**
- generalization: **strict leave-one-person-out**

## Frozen duration comparison

| Final facial window | Full model macro-r | Task-only macro-r | Increment over task-only |
| ---: | ---: | ---: | ---: |
| 1 s | **0.0468** | 0.1436 | -0.0968 |
| 2 s | **0.1197** | 0.1436 | -0.0238 |
| 3 s | **0.0869** | 0.1436 | -0.0567 |
| 4 s | **0.1176** | 0.1436 | -0.0260 |
| 5 s | **0.1665** | 0.1436 | +0.0229 |

Macro-r is the Fisher-z average of within-session Pearson correlations on held-out people.

## Preregistered primary contrast

2 s - 5 s macro-r difference: **-0.0468**

Paired session bootstrap (10,000 resamples; 67 paired sessions):

**95% CI [-0.1046, +0.0101]**

The confirmatory criterion required both a positive point difference and a confidence interval entirely above zero.

**Decision: not supported.**

## Secondary 3 s contrast

3 s - 5 s macro-r difference: **-0.0796**, 95% CI **[-0.1375, -0.0210]** across 67 paired sessions.

## Interpretation

The independent dataset does not confirm the preregistered 2-second temporal-locality hypothesis. This result is retained rather than replaced with a post-hoc duration claim.

CogBeacon differs materially from the earlier MTS analysis: it uses a WCST-like cognitive task, 68-point facial landmarks at 2 FPS, and per-round response time rather than PVT-linked eyelid distance. Agreement would therefore be cross-task evidence; disagreement bounds the hypothesis.

## Claim boundary

This analysis does **not** validate APST-5 active probing or a smartphone fatigue diagnostic. It tests only whether very recent passive facial dynamics can dominate a longer within-round history for an immediate performance target.

## Reproduction

The source dataset is not redistributed. The workflow downloads the public CogBeacon facial-keypoint and performance archives, runs the frozen script, and writes this report.
