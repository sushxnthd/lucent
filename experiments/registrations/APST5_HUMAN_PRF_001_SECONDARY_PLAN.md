# APST5-HUMAN-PRF-001 Secondary Directional Analysis Plan

**Status:** written after the frozen primary APST5-HUMAN-PRF-001 result. This is explicitly secondary/exploratory and cannot replace the failed H1/H2 primary criteria.

## Motivation

The primary empirical PRF deliberately used one signed-normalized response kernel for both pupil constriction after brightening and pupil dilation after darkening.

That is a strong linear-time-invariant simplification. Lucent's original surrogate already models constriction and dilation with different time constants.

APST5-HUMAN-PRF-001 preregistered a secondary analysis using separate brightening-derived and darkening-derived response functions. This document fixes its implementation before computing that secondary result.

## Fixed data split

Use exactly the same:

- 22 available PsPM luminance participants;
- subject 06 source-data exclusion;
- first-three / last-three presentations per disc level;
- participant design/test split with seed 20260930;
- preprocessing;
- 84 equal-exposure probe set;
- comparator (4,5,6);
- E002 (1,2,8);
- threshold S>1.25.

No participant or transition is added or removed based on the primary result.

## Direction-specific kernels

For each participant:

- **brightening kernel**: pointwise median of normalized fit transitions with (a_j>0);
- **darkening kernel**: pointwise median of normalized fit transitions with (a_j<0).

The same normalization is retained:

[
r_j(t)=rac{p_j(t)-p_{baseline,j}}{log(L_{after}/L_{before})}.
]

Held-out brightening transitions are predicted only by the brightening kernel; held-out darkening transitions only by the darkening kernel.

## Secondary noise scale

Define directional-model noise (sigma_i^{dir}) as the median RMSE across all held-out normalized transitions against their corresponding directional kernel.

Report held-out waveform (R^2) under this directional model.

## Sequence prediction

For every binary probe transition:

- if (Delta log L>0), use the brightening kernel;
- if (Delta log L<0), use the darkening kernel;
- multiply the chosen normalized kernel by the signed log-luminance step.

For the normalized sequence comparison, use unit log-luminance contrast as in the primary test.

## Secondary outputs

Report:

1. directional held-out waveform adequacy;
2. design-set P10-optimal sequence;
3. held-out P10/median/pass fraction for:
   - directional selected sequence;
   - frozen E002 (1,2,8);
   - SIM-005 (1,2,9);
   - evenly spaced (2,5,8);
4. required log-luminance contrast and luminance ratio for each named probe to reach the engineering separation threshold under simple linear amplitude scaling.

## Interpretation

Any improvement over the failed primary result is evidence that constriction/dilation asymmetry matters for sequence design.

It is **not** a confirmatory rescue of APST5-HUMAN-PRF-001.

A positive secondary E002 result may motivate a future prospectively frozen asymmetric human-calibrated model, but E002 phone data remain required.
