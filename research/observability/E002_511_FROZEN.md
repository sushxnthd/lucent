# E002-511 | Preregistered coverage-selection falsification of E002-509

Frozen 2026-10-29 **before changing the existing E002-509 evaluator**. Primary E002-371 workstream, branch `research/observability-human-boundary`, draft PR #26. This is a statistical measurement-claim falsification using **synthetic cohort counts only**. It is not human physiology, shutter calibration, or a new theorem.

## Question and estimands

E002-509 computes its zero-failure Clopper-Pearson upper bound with `n = all enrolled participants`, even when only a subset receive any no-hidden-closure certificates. Is this an appropriate denominator for **failure probability conditional on the product issuing at least one certificate**?

Two distinct estimands must not be conflated:

- **Unconditional participant-session false-exclusion probability**: `P(at least one false exclusion)` over all independently sampled participant-sessions, including sessions with zero certificates. With zero observed failures, the all-enrolled denominator is valid *under the stated exchangeability assumption*, but may describe a practically useless abstaining product.
- **Conditional false-exclusion probability among certificate-bearing participant-sessions**: `P(at least one false exclusion | >=1 certificate)`. With zero observed failures among `k` independently sampled, fully adjudicated certificate-bearing participants, the one-sided 95% upper bound is `1 - 0.05**(1/k)`. No conditional risk estimate exists at `k=0`. This is conditional on exchangeability **within the covered subgroup**, fixed selection rule, and resolved reference truth. It is not a per-window or universal risk bound.

## Frozen adversarial cases (n=299, no observed failures)

| k participants with >=1 certificate | Prepatch expected risk_gate | Independent 95% conditional upper bound | Required corrected interpretation |
| ---: | --- | ---: | --- |
| 0 | NO_USEFUL_COVERAGE | undefined | Abstain |
| 1 | PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY | 0.95 | Insufficient covered participants |
| 8 | PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY | 0.31234397806636793 | Insufficient covered participants |
| 298 | PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY | ~0.0100024 | Insufficient covered participants |
| 299 | PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY | ~0.0099691 | Conditional statistical gate only, never product release |

All-enrolled zero-event bound remains ~0.0099691 in each row, and is **not mathematically wrong** for the unconditional estimand. The falsification is of its use as evidence of **conditional safety given a non-abstaining certificate**.

## Frozen kill criteria and implementation

1. Demonstrate the 1/299 and 8/299 false conditional clearance against the original E002-509 executable, before modifying it. Preserve a link to exact-head hosted CI if available.
2. Add an independent-language arithmetic cross-check for 1/8/298/299 covered participants, without reusing the evaluator's denominator.
3. Repair the evaluator to report **both** unconditional and conditional bounds with explicit denominator labels. A conditional gate must use `k`, never `n`. For `k=0`, no finite conditional bound. A nonzero failure must not be run through the zero-event formula. Preserve old full-coverage behavior and input validation.
4. Preserve a separate measured certificate coverage fraction and the absence of a preregistered minimum utility target. Do not manufacture a utility target post hoc or count individual windows as independent people.
5. Verify the corrected 0/1/8/298/299 cases and all previous regression tests. Product must remain `ABSTAIN_UNCALIBRATED`; release `BLOCKED` for all cases.

This fixes a **measurement interpretation and software gate**, not E002-371's missing human evidence. No independent anatomical ratings, physical camera calibration, continuous-time velocity envelope, or participant-disjoint physical predictions are acquired. Stop after the correction passes and return to real blinded S01 reviews and physical timing.
