# E002-440 — frozen participant-cluster false-reassurance test

**Frozen 2026-10-25 before implementation.** Evidence target: synthetic falsification of interval-level pseudoreplication, an exact participant-level statistical gate, and an executable human-study ledger validator. This does **not** establish E002-371 physical validity or any physiological cap.

## Scientific hypothesis and estimand
Ordinary-camera intervals from the same person are not independent replicates. The primary estimand is the probability that a *new independently sampled participant*, under the preregistered acquisition distribution, experiences at least one witnessed false no-hidden-closure certificate during a fixed 40-candidate challenge. It is **not** the probability that a randomly selected video frame is wrong, and it is not a deterministic physical guarantee.

## Frozen experiment
1. Generate 20,000 independent study replicates with seed 440. Each has 30 participants and 40 candidate intervals per participant. Each participant is independently in a latent failure-prone class with probability 0.05; in that class, all 40 candidate intervals fail; otherwise all pass. This is a deliberately extreme but admissible within-person dependence countermodel, not a fitted human distribution.
2. Measure the fraction of replicates with zero witnessed failures. Prediction: (1-0.05)^30 = 0.2146387639. Check simulation within ±0.012 of the exact probability.
3. For a zero-failure study, compare exact one-sided 95% Clopper–Pearson upper bounds calculated using n=30 independent participants versus the invalid n=1,200 pseudo-independent frames. Predictions: approximately 0.0950 versus 0.002493.
4. Derive the smallest zero-failure independent-participant sample with one-sided 95% upper risk bound strictly below 1%: 299 participants. Repeated frames do not replace participants.
5. Adversarial ledger tests must reject reference-unresolved candidates as successes, reject missing participant provenance and unlocked predictions, block participant duplication, and never treat abstentions as independent successes. A participant with any witnessed false certificate is a failure; one with unresolved candidates is not an eligible success and blocks release. No observationally conditioned censoring is permitted for a population claim.

## Product consequence
The statistical gate can only support a **distribution-conditional participant-level risk statement** after independently audited prospective human acquisition, authenticated physical timing/geometry/velocity premises, blinded reference adjudication, fixed challenge length, independently sampled participants, and nuisance-specific transportability review. It never upgrades E002-371 to a universal deterministic certificate. All existing physical product claims remain `ABSTAIN_UNCALIBRATED`.

## Prior art / priority
Clopper & Pearson (1934), https://doi.org/10.1093/biomet/26.4.404; Hurlbert (1984), https://doi.org/10.2307/1942661. This is application and falsification, not a new statistical theorem. Preserve all negative outcomes and report sample-size feasibility candidly.
