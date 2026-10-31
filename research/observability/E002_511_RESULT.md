# E002-511 | Coverage-selection denominator falsification and correction

Date: 2026-10-29. Primary E002-371 workstream, same persistent research branch and draft PR #26. [Frozen before code modification](E002_511_FROZEN.md). Evidence tier: **synthetic cohort-count software falsification + independent arithmetic**, not human physiological validation.

## Newly isolated measurement-claim error

The previous E002-509 implementation applied the all-enrolled participant count `n` to the exact zero-failure bound even when most participants received **no certificates**. That is a valid bound on *unconditional per-session failure* (including all-abstention sessions), but not a bound on failure probability **conditional on at least one certificate being issued**. Its `PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY` label could therefore misleadingly imply conditional certificate safety when only 1 of 299 participants received a certificate.

For a fixed, preregistered certificate rule and independent, exchangeable, fully adjudicated participant-sessions, the one-sided 95% zero-failure Clopper-Pearson upper bound among the `k` certificate-bearing participants is `1 - 0.05**(1/k)`, not `1 - 0.05**(1/n)`. This conditional estimate is undefined for `k=0`; it does not imply a universal speed bound or per-window safety. Selection on unresolved truth, changes to the certificate rule, or nonexchangeable participants invalidate the simple inference.

| Enrolled n | Certificate-bearing k | Prepatch conditional-gate label | Corrected conditional 95% upper | Corrected conditional-gate label |
| ---: | ---: | --- | ---: | --- |
| 299 | 0 | NO_USEFUL_COVERAGE | undefined | NO_USEFUL_COVERAGE |
| 299 | 1 | PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY | 95.0000% | INSUFFICIENT_COVERED_PARTICIPANTS |
| 299 | 8 | PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY | 31.2344% | INSUFFICIENT_COVERED_PARTICIPANTS |
| 299 | 298 | PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY | 1.00024% | INSUFFICIENT_COVERED_PARTICIPANTS |
| 299 | 299 | PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY | 0.99691% | PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY |

The all-enrolled **unconditional** upper remains 0.99691% in every row. Both estimands must be disclosed. A strong unconditional bound with 0.33% coverage does not establish a useful measurement product. No post hoc minimum-coverage target was invented.

## Reproduction and code change

- [Frozen adversarial protocol](E002_511_FROZEN.md), committed at `30e1863` before modifying the original evaluator.
- [Synthetic 299-person adversary](e002_511_coverage_falsifier.py), committed at `f98a179`. Tests all 0/1/8/298/299 covered counts; no human records are read or published.
- Historical prepatch CI on `57d1d24`: [run 40750100688](https://github.com/sushxnthd/lucent/actions/runs/40750100688), **queued at report creation**. Do not claim its completion.
- Correction [`c8116dc`](https://github.com/sushxnthd/lucent/commit/c8116dc187fa024de6fdc2f526d7f0aa28a662c6): preserves `zero_failure_upper` as the legacy **unconditional** estimate, adds `unconditional_zero_failure_upper` and `conditional_zero_failure_upper`, labels both denominators, reports covered-participant fraction, and makes the conditional gate depend on `k`.
- [Regression additions](test_e002_509_participant_power.py) at `930b953`: sparse coverage, all-abstain, full coverage, nonzero failures, plus all existing E002-509 tests.
- [Postpatch CI](https://github.com/sushxnthd/lucent/actions/runs/40750208798) at `4182950`: **queued at report creation**. Runs the frozen adversary in corrected mode, previous regressions, and an independent Node.js denominator check.
- Independently calculated locally with Python and Node.js: k=1 0.95, k=8 0.3123439780663679, k=298 0.010002432437677695, k=299 0.00996914679289927. This verifies arithmetic, not physical measurement or hosted execution.

## What this does and does not establish

This is a **new falsification of an inference gate**. It does not establish human eyelid speed, anatomical classification, shutter timing, a validated continuous-time E002-371 boundary, or even one actual held-out false-exclusion outcome. No new human ratings were obtained. The existing S01 metadata-only track remains closed; do not repeat it. The next decisive evidence remains two independent blinded S01 anatomical reviews and authenticated physical acquisition/shutter measurements before any participant-disjoint prediction.

Product `ABSTAIN_UNCALIBRATED`. Release `BLOCKED`. No PR merge, no deployment, no Hush branch writes.
