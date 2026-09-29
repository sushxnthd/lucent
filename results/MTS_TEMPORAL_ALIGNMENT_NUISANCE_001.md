# MTS-TEMPORAL-ALIGNMENT-NUISANCE-001: Time-on-Task Audit

**Status:** completed preregistered nuisance-adjusted audit.

**Original crossover survives frozen nuisance adjustment:** **YES**.

## Adjustment

Every duration model receives the same explicit nuisance vector: normalized time-on-task, squared normalized time-on-task, and PVT2/PVT3 session indicator.

## Adjusted duration x target-horizon matrix

| Target support | 2 s | 5 s | 15 s | 30 s | 60 s | nuisance only |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 s | 0.2672 | 0.1954 | 0.1253 | 0.1085 | 0.0892 | 0.0645 |
| 15 s | 0.2007 | 0.1753 | 0.1522 | 0.1549 | 0.1438 | 0.1054 |
| 30 s | 0.2007 | 0.1856 | 0.1906 | 0.1974 | 0.1954 | 0.1473 |
| 60 s | 0.2236 | 0.2246 | 0.2380 | 0.2533 | 0.2513 | 0.2177 |

## Preregistered adjusted interaction

- D(0 s) = r60-r2: **-0.1780**
- D(60 s) = r60-r2: **+0.0276**
- Delta = D(60)-D(0): **+0.2056**
- paired subject-bootstrap 95% CI: **[+0.1328, +0.2749]**
- paired subjects: **28**

The frozen robustness criterion requires a positive interaction with the entire interval above zero.

**Decision: survives.**

## Increment over nuisance-only

| Target support | 2 s ocular increment | 60 s ocular increment |
| ---: | ---: | ---: |
| 0 s | +0.2027 | +0.0248 |
| 15 s | +0.0953 | +0.0384 |
| 30 s | +0.0534 | +0.0481 |
| 60 s | +0.0060 | +0.0336 |

## Interpretation

The Massoz target-history crossover remains significant after all sensor-duration models are given the same explicit time-on-task and session identity covariates. The result is therefore not explained solely by this frozen temporal nuisance model, although it remains dataset-specific.

## Claim boundary

This audit controls a predeclared low-frequency nuisance model only. It neither proves nor excludes other physiological temporal effects.
