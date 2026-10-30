# E002-549 RESULT | Prospective validation provenance can be misclassified

Date: 2026-10-30. Primary kernel E002-371. Existing branch `research/observability-human-boundary`, draft PR #26. Frozen first in [E002_549_FROZEN.md](E002_549_FROZEN.md).

## New methodological falsification

The existing E002-548 one-sided exposure witness parser is **intentionally** a syntactic checker. It does not encode the precommitted 15/16 participant split, and `lock_sha256` is checked for shape, not checked against an independently retained prediction manifest. A constructed human-*origin-tagged* record for **exploratory S-24** therefore produces `HUMAN_WITNESS_CANDIDATE_EXTERNAL_REVIEW=1` in the original parser. That output is not itself incorrect: it says only candidate. However, an evaluator who treats every such candidate as a held-out result would make an invalid prospective claim. A fabricated 64-hex `lock_sha256` similarly does not establish prediction precedence. **These are synthetic methodological counterexamples, not human observations or forged real-world participant records.**

## Implemented claim gate

[e002_549_split_lock.py](e002_549_split_lock.py) composes the unchanged E002-548 exposure-aware witness check with a frozen-partition gate:

- Requires the exact 15 exploratory / 16 held-out IDs from E002-548, with all sessions of one participant remaining in one partition.
- Requires a caller-supplied, independently retained SHA-256 digest over the *entire* canonical ordered prediction manifest. Any post-lock change to a prediction, participant, threshold or time interval changes the digest and is rejected.
- Rejects unknown participant IDs, duplicate gap IDs and cross-participant/session/eye/ROI frame contamination instead of silently counting those records.
- Reports separate exploratory and held-out participant denominators, witness candidates, censored reference negatives and abstentions, without exposing participant identities or source frames.
- Explicitly returns `EXTERNAL_PRECOMMIT_TIMESTAMP_UNVERIFIED` even after a digest match. **This software cannot authenticate the existence, independence or date of the external precommit.** It also cannot authenticate rater identities, shutter certificates or anatomical transfer.

### Frozen constructed outcomes

| Constructed input | Original E002-548 output | New E002-549 output |
| --- | --- | --- |
| S-24 exploratory candidate | 1 human-origin candidate (split not distinguished) | 1 exploratory candidate; **0 held-out candidates** |
| S-08 held-out candidate | 1 human-origin candidate | 0 exploratory; 1 held-out candidate, still unauthenticated |
| Change `EXCLUDE` to `ABSTAIN` after lock | Arbitrary 64-hex lock accepted as syntax | **Rejected** against previously supplied expected manifest digest |
| Reference mean upper bound above threshold | Censored | **Censored**, never a closure-free label |
| Unknown S-99 participant | Not checked against frozen split | **Rejected** |

The S-24 and S-08 examples are constructed fixtures, **not** real participant data.

## Verification

- **19/19 local Python adversarial tests passed** against a local copy of the repository's fetched E002-548 witness implementation; [committed tests](test_e002_549_split_lock.py) run against the actual checked-out implementation on GitHub Actions.
- Independent Node.js SHA-256 canonicalization and partition replay passed locally: [e002_549_independent.cjs](e002_549_independent.cjs).
- Dedicated [hosted workflow](../../.github/workflows/e002_549_split_lock.yml) committed. **Hosted CI result not confirmed at report time**; no hosted pass claimed.

## Concrete prospective use

1. Independently publish or timestamp the expected digest of the complete held-out `predictions` array **before** accessing held-out imagery, and preserve a verifiable receipt separate from the analyzed bundle. The CLI `--expected-prediction-sha256` must come from that receipt, not be recomputed from the submitted results.
2. Acquire authorized native Phantom video, independently bound the actual exposure support/clock and anatomical-transfer uncertainty, and obtain two independent blinded anatomical raters. If any certificate cannot be independently authenticated, abstain.
3. Run E002-548's one-sided positive witness check and E002-549's partition/lock gate. A positive candidate still requires independent external adjudication; a negative reference is censored. Report participant-level denominators, nuisance strata, all failures and abstentions.
4. Do not claim 1% population false-exclusion risk from a 16-person holdout; E002-509 already established that such a guarantee is statistically unavailable.

## Scientific and product boundary

This is a reproducible **prospective-validation integrity correction**, not a new observability theorem, real blink measurement or a physical test of E002-371. No authenticated shutter captures, anatomical rater pairs, hard human motion ceilings or participant-disjoint physical predictions were obtained. Further provenance tooling should not displace physical acquisition. `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Hush PR #45 untouched.
