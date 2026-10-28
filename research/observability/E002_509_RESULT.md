# E002-509 | A prospective human holdout of eight cannot support a 1% population false-exclusion claim

2026-10-28. Same E002-371 research branch and draft PR #26. [Frozen before executable](E002_509_FROZEN.md). [Executable](e002_509_participant_power.py), [11 frozen controls](test_e002_509_participant_power.py), and [independent-language CI](../../.github/workflows/e002_509_participant_power.yml).

## New decision-relevant scientific information

The existing E002-373 physical human protocol called for at least **eight** participant-disjoint held-out participants. That is appropriate for pilot counterexample discovery, but **cannot** substantiate a strong population-level false-exclusion risk claim. Counting each gap as an independent trial would be pseudoreplication: many gaps from one person share anatomy, nuisance and device properties.

For a fixed, independently adjudicated participant-session protocol, define one Bernoulli failure if *any* claimed hidden-closure exclusion is contradicted by a synchronized high-rate anatomical reference or the predeclared speed envelope is violated. With `n` independent, exchangeable participants and **zero** failures, the exact one-sided 95% Clopper-Pearson upper confidence limit on the probability of at least one failure for a new participant-session is `1 - 0.05^(1/n)`. No distribution-free deterministic no-closure claim follows.

| Held-out participants, zero observed failures | One-sided 95% upper risk |
| ---: | ---: |
| 8 | 31.2344% |
| 24 | 11.7346% |
| 80 | 3.6754% |
| 298 | 1.00024% |
| 299 | 0.99691% |
| 300 | 0.99361% |

Therefore **299 independent fully adjudicated participants with zero failures** are minimally needed to clear the **statistical** 1%/95% participant-session risk criterion, assuming exchangeability and fixed session design. Even this cannot certify a hard continuous-time velocity maximum or a device-independent physical guarantee.

The published Lee, Seo and Hwang 2025 high-frame-rate study included 80 volunteers using mainly 240-fps acquisition (https://doi.org/10.1007/s13534-025-00522-3). Its volunteers were **not tested on Lucent's certificate**, so their data cannot be counted as successes. The 80-person row is only a hypothetical zero-failure design comparison, not an observed result.

## Executable falsification and fail-closed rules

Locally, all **11** standard-library adversarial controls passed. The executable refuses duplicate or missing participant IDs, invalid counts, unresolved reference labels and nonzero-failure misuse of the zero-event formula. A 299-participant all-abstain cohort returns `NO_USEFUL_COVERAGE`; a single participant failure returns `NONZERO_FAILURES_REQUIRE_EXACT_INTERVAL`, not a false zero-failure pass. The code does not authenticate real participant identities, independence, video timing, reference anatomy, or study preregistration.

[GitHub Actions hosted verification](https://github.com/sushxnthd/lucent/actions/runs/40722238384) was **queued** when this report was written; no hosted success is claimed. An independent Node calculation is included in that workflow to check the 8/298/299 boundary without importing Python code.

## Practical impact on the primary human study

Do **not** discard the E002-502 blinded S01 anatomical pilot or E002-373 eight-participant pilot. Their purposes are now explicitly **feasibility, nuisance failure discovery and physical counterexamples**, not certification of a 1% population risk. Before any larger study, fix the participant-session exposure, nuisance mixture, device, shutter and reference calibration, error definition, exclusion threshold and utility/coverage requirement. Separate the deterministic physical theorem (which requires an independently justified hard speed envelope) from a *statistical* empirical false-exclusion risk statement. A participant with unresolved truth cannot be counted as a clean success; no all-abstain product.

**Evidence tier:** mathematical/statistical study-design falsification, with synthetic count controls only. **New human anatomical ratings: 0. Authenticated camera timing: 0. Certified continuous-time human V: 0. Participant-disjoint physical predictions: 0.** Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. No new physiological discovery or release clearance. Further statistical threshold polishing should not displace actual human review and physical timing measurements.
