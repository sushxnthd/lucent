# E002-410 — frozen unit-of-exchangeability experiment (2026-10-24)

**Status: PREREGISTERED BEFORE OUTCOME EXECUTION.** Research branch: `research/observability-human-boundary`; draft PR #25. E002-371 physical shutter-gap theorem remains the primary kernel.

## Question
Can a maximum observed over many highly correlated eyelid-velocity frames be treated as if every frame were an independent calibration unit when predicting a new participant's motion? E002-405 established the exact rank exceedance law under exchangeability; this experiment tests the *unit of exchangeability* under participant-level heterogeneity and its consequence for future-session closure certificates.

## Fixed simulation (numpy RandomState/Generator PCG64 seed 4102026)
- 40,000 independent Monte Carlo trials. 20 calibration participants, each with 100 velocity observations. One future participant, one velocity observation. All velocities in normalized aperture units/s, positive.
- **Clustered model:** for each participant independently draw `U ~ Uniform(0,1)`; for each of 100 frames draw `epsilon ~ Uniform(0,0.001)`, and set `v=U+epsilon`. Future participant draws independent `U` and `epsilon`.
- **Independent-frame control:** all 2,000 calibration frames and the future frame iid `Uniform(0,1)`, with the same nominal counts.
- **Shifted-participant negative control:** calibration as clustered; future `U ~ Uniform(0.25,1.25)` with independent `epsilon ~ Uniform(0,0.001)`.
- **Session-maximum control:** under clustered model, compare the maximum of 100 future frames with the maximum of 20 *calibration participant maxima*.
- Report per-condition number of exceedances and Monte Carlo rate; never call a velocity-bound exceedance a wrong eyelid certificate.

## Frozen predictions and thresholds
1. Clustered *single future frame* exceedance rate is within 0.006 of `1/(20+1)=0.047619` (small within-session noise). It exceeds the naive frame-count rate `1/(2000+1)=0.00049975` by at least a factor of 40.
2. IID-frame control is within 0.0007 of `1/2001`.
3. Session-max control is within 0.006 of `1/21` (exact exchangeable-rank probability for continuous participant maxima).
4. Shifted-participant rate is greater than 0.20, invalidating exchangeability-based deployment assurances under this domain shift.
5. A separate independent implementation using direct rank simulation (21 iid participant scores, one future maximum) reproduces `1/21` within 0.006; this is an *independent mathematical oracle*, not a human replication.
6. Release-gate unit tests must reject a calibration declaration that counts frames instead of independent participants; reject absent independent physical aperture, unknown participant exchangeability, insufficient participants for a prespecified alpha, and new-device shift. Conditional statistical-risk statements must never be promoted to deterministic E002-371 certificates.

## Mathematical target
For `n` exchangeable continuous participant-level maxima and `m` future participant maxima, `P(any future max exceeds calibration max) = m/(n+m)`. With ties the exceedance probability is at most this. This is a standard exchangeable-rank identity, not novel conformal theory. For a one-participant future guarantee of at most alpha, a maximum-based bound requires `n >= ceil(1/alpha)-1` *independent participant units*. A risk statement is marginal over calibration and future samples, not conditional on the observed calibration set and not a guarantee of no hidden blink.

## Evidence, limits and product consequence
Synthetic falsification of frame pseudoreplication; no human velocity ground truth, no authenticated physical shutter timing, and no physiological hard bound. Independent physical verification is required before any E002-371 guarantee. Human protocol: 20+ independently recruited participants with high-speed reference video and synchronized ordinary-camera exposures, independent two-rater aperture trajectories, participant-disjoint calibration/evaluation, and prespecified nuisance strata. For alpha=0.05 and *one* future participant, 19 independent calibration participant maxima are the theoretical minimum only under exchangeability; use more for uncertainty, strata, and rejection monitoring. Multiple future participants require `n >= m*(1/alpha-1)`. Until those data exist: `ABSTAIN_UNCALIBRATED`.

## Literature boundary
The exchangeability and cluster-level calibration requirement are known in conformal prediction, including the review https://doi.org/10.1145/3736575. Claim only the Lucent-specific failure demonstration and explicit release-gate consequence; no novelty claim for the rank theorem.
