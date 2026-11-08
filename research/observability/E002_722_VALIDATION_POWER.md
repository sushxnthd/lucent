# E002-722 — Zero-failure human-validation evidence budget

**Tier:** prospective statistical design / exact binomial calculation. No new human or physical recordings.

## Falsifiable decision consequence

E002-714 proposes >=20 participants and >=30 blinks each. Even if all 600 events yielded *eligible certified exclusions*, and no exclusion was false, the **one-sided 95% Clopper–Pearson upper bound** on a common independent-trial false-exclusion probability is **0.00498044 (0.498%)**. This is *not* a guarantee of safety, and in practice the denominator is only reference-valid **certified exclusions**, not all recorded blinks. Abstentions lower the denominator. If no exclusions are issued, there is no error-rate evidence.

Under independent Bernoulli trials with zero failures, the upper bound is `1 - 0.05**(1/n)`. Achieving a <1% bound requires at least **299** eligible zero-failure trials; <0.1% requires at least **2995**. These are mathematical sample-size calculations, not achieved observations.

## Dependence is decisive

Multiple blinks from one participant are not independent. For illustrative intraclass correlation rho=0.1 and 30 eligible trials per participant, design effect `1+(30-1)*0.1 = 3.9` gives a heuristic effective n ~154 from 600 observations. **Do not plug that heuristic effective n into an exact binomial interval or advertise it as a valid clustered confidence bound.** Use participant-resampled confidence intervals and a hierarchical sensitivity analysis, and report the number of participants with at least one certified exclusion. Cluster bootstrap cannot support an unconditional zero-risk claim.

## Frozen analysis rule before held-out labels

Report participant-disjoint counts of reference-valid certificates, false exclusions, reference-indeterminate events, and abstentions by nuisance condition. Compute the exact independent-binomial zero-failure bound *only as a labeled optimistic benchmark*, not the primary clustered inference. Primary inference should use participant-level failure indicators, with a one-sided exact bound across independent participants if justified; separately report conditional within-person results. Any confirmed false exclusion falsifies the combined calibration assumptions and blocks release. A zero-failure result never establishes a deterministic continuous-time velocity ceiling.

**Product:** Continue `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. E002-714 acquisition, independent speed calibration and human labels remain missing.

## Reproduction

`python research/observability/e002_722_validation_power.py --selftest`

`python research/observability/e002_722_validation_power.py --participants 20 --certified-per-participant 30 --icc 0.1`

The ICC scenario is a sensitivity illustration, not measured physiology. No synthetic configurations are presented as human evidence.
