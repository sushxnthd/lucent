# E002-749 | Clustered validation falsifier (2026-11-11 UTC)

**Evidence tier:** T1 analytical counterexample. No human or instrument measurements. This is a validation-inference correction, not an additional eyelid observability theorem.

## Failure mode

E002-744 and E002-747 correctly define a zero-error one-sided upper bound `1 - 0.05**(1/n)` **only under independent Bernoulli validation units**. Consecutive intervals from one participant, camera session, or shutter program are not automatically independent. Reusing interval count `n` as though it were the number of independent participants can severely understate uncertainty.

Construct 100 intervals in one session with perfectly shared failure indicator `Z ~ Bernoulli(p)`. Every interval's error indicator equals Z. If all 100 intervals show no error, their joint probability is `1-p`, not `(1-p)^100`. Thus the exact 95% upper confidence limit for p is 0.95, whereas the invalid interval-iid calculation reports `1-0.05^(1/100) = 0.029513...`. The latter has only 2.9513% coverage at p=0.95 under this data-generating process, not 95%.

## Frozen correction to prospective validation

Preserve raw interval-level counts for detecting individual false exclusions. Separately report the number of independent **participant-level** and **session-level** units, with their actual per-unit denominators. The primary confirmatory analysis must specify the independent sampling unit before unblinding. For a conservative zero-failure bound under arbitrary within-cluster dependence, count only independently sampled clusters with at least one certified exclusion and no observed error, and apply `1-0.05^(1/K)` to the probability that an independently sampled eligible cluster contains >=1 false exclusion. **This is a cluster-level event-risk bound, not an interval-level error-risk bound.** Do not convert between these estimands without assumptions.

If there are any failures, retain them and use a preregistered cluster-level interval procedure; do not use the zero-failure shortcut. For heterogeneous clusters, convenience samples, adaptive enrollment, or dependence between participants, report descriptive results and abstain from a population-level guarantee unless the sampling model is justified. Stratify by participant, device and condition; do not present overlapping intervals as independent replicates. Holdout participant count >=10 is a feasibility target, not proof of rare-event safety.

## Product consequence

No production claim of low human false-exclusion probability can be licensed by a large number of temporally correlated, zero-error frames. E002-744 remains the frozen physical falsification protocol; this note adds a statistical release blocker: confirmatory uncertainty must be computed at a defensible independent unit. Product remains ABSTAIN_UNCALIBRATED; production BLOCKED.

## Reproduction

Python standard library:

```python
import math
n = 100
naive = 1 - 0.05 ** (1/n)
cluster = 1 - 0.05 ** (1/1)
assert 0.029 < naive < 0.030
assert abs(cluster - 0.95) < 1e-12
p = 0.95
assert abs((1-p) - 0.05) < 1e-12
assert (1-p) > (1-p)**n
print(f"naive interval-iid upper={naive:.9f}; valid cluster-event upper={cluster:.9f}")
```

No test execution or hosted CI is claimed in this note. Independent review of the sampling model is required before applying it to actual observations.
