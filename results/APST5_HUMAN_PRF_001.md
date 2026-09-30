# APST5-HUMAN-PRF-001: Human-Calibrated Active-Probe Observability

**Status:** completed preregistered public-human controlled-luminance analysis.

**H1 human-optimized held-out criterion:** **NOT SUPPORTED**.

**H2 frozen E002 held-out criterion:** **NOT SUPPORTED**.

## Dataset

PsPM-AOB_UW public EyeLink controlled-luminance data (Zenodo 10.5281/zenodo.8239465).

- usable participants: **22**
- design participants: **11**
- held-out participants: **11**
- subject 06 luminance pupil recording is absent in the source archive.

## Empirical step-response adequacy

| subject | fit transitions | validation transitions | validation RMSE | validation R2 | noise scale sigma | split |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 01 | 17 | 17 | 1.0409 | 0.0455 | 0.9462 | design |
| 02 | 24 | 24 | 1.0140 | -0.0247 | 0.6144 | held-out |
| 03 | 11 | 14 | 1.1007 | 0.0413 | 0.7701 | held-out |
| 04 | 24 | 23 | 1.1990 | 0.0493 | 0.8682 | held-out |
| 05 | 24 | 24 | 1.2844 | 0.0718 | 1.1196 | held-out |
| 07 | 24 | 24 | 0.8079 | 0.1544 | 0.7466 | held-out |
| 08 | 24 | 23 | 1.4098 | -0.2155 | 0.7693 | design |
| 09 | 24 | 21 | 0.7755 | -0.0848 | 0.6133 | design |
| 10 | 24 | 24 | 1.0635 | 0.0498 | 0.8691 | held-out |
| 11 | 19 | 20 | 1.0686 | -0.0631 | 0.7368 | design |
| 12 | 24 | 24 | 1.0603 | 0.0066 | 0.5387 | design |
| 13 | 24 | 24 | 1.1800 | 0.1879 | 1.1303 | held-out |
| 14 | 12 | 16 | 0.8398 | 0.2133 | 0.7345 | design |
| 15 | 24 | 24 | 1.4297 | 0.1012 | 1.1736 | held-out |
| 16 | 24 | 24 | 1.0629 | 0.0476 | 0.9339 | held-out |
| 17 | 24 | 23 | 1.3621 | 0.1236 | 1.2130 | held-out |
| 18 | 24 | 24 | 1.0752 | 0.0599 | 0.9289 | design |
| 19 | 24 | 24 | 1.1380 | 0.1037 | 0.8397 | design |
| 20 | 24 | 23 | 1.2029 | 0.1096 | 0.9569 | design |
| 21 | 18 | 19 | 0.9474 | -0.0082 | 0.6635 | held-out |
| 22 | 23 | 23 | 1.2481 | 0.0666 | 1.1860 | design |
| 23 | 22 | 21 | 1.0458 | -0.3007 | 0.8802 | design |

## Equal-exposure sequence result

Human-design-set P10 search selected **(1, 2, 3)**.

| Probe | positions | design P10 S | held-out P10 S | held-out median S | held-out S>1.25 | design rank |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| human_selected | (1, 2, 3) | 0.875 | **0.859** | 1.115 | 27.3% | 1 |
| frozen_e002 | (1, 2, 8) | 0.822 | **0.824** | 1.059 | 27.3% | 2 |
| sim005 | (1, 2, 9) | 0.804 | **0.799** | 1.032 | 27.3% | 3 |
| evenly_spaced | (2, 5, 8) | 0.545 | **0.598** | 0.790 | 0.0% | 56 |

## Interpretation

The frozen E002 split timing does not satisfy the preregistered human-calibrated held-out observability criterion.

This analysis does not use the hand-specified Lucent pupil-parameter population for the primary waveform. Each participant's response function and noise scale are estimated from real controlled-luminance EyeLink transitions, with separate held-out transitions used to quantify response error.

## Model-adequacy warning

Participants with non-positive held-out step-response R2: **6/22** (02, 08, 09, 11, 21, 23).

## Source-data failures

- 06: missing luminance pupil file

## Claim boundary

A positive result predicts biological waveform observability under a human-calibrated LTI approximation. It does not show that an RGB phone camera resolves that waveform and does not validate fatigue or vigilance inference.
