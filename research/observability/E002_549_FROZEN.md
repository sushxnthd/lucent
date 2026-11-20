# E002-549 | Frozen prospective participant-split and prediction-lock falsification

Frozen 2026-10-30 before the new adjudicator and adversarial tests. Primary E002-371 human-validation kernel; same branch and draft PR #26.

## Concrete failure hypothesis

E002-548's one-sided witness parser is deliberately an evidence **syntax** check. It does not enforce the published S-01...S-31 participant split and only checks that each `lock_sha256` looks like a SHA-256 digest. Consequently a syntactically valid **exploratory** S-24 candidate could be misreported downstream as prospective held-out evidence, and an after-the-fact `EXCLUDE` record with arbitrary 64-hex lock would be accepted. These are methodological falsifications, not physiological observations.

## Frozen test matrix

1. Construct an E002-548 syntactically valid *human-origin* witness for exploratory participant S-24 and show that the original parser reports a human candidate without indicating exploratory status. Do not call it real human evidence.
2. Freeze a canonical SHA-256 over the complete prediction array, with domain separator `lucent-e002-549-v1\n`, JSON sorted keys and compact separators, UTF-8, order preserved. A caller must supply an **independently recorded** expected digest. Mutating prediction, timing, participant or threshold after that digest must fail.
3. Enforce the exact E002-548 split: 15 exploratory and 16 held-out participants. All sessions from a participant remain in the same split. Unknown subjects and reference-frame participant mismatches fail closed.
4. Emit separate exploratory and held-out counts and denominators, with no participant IDs, frames, time points or private labels. Zero positives and reference negatives remain censored; never turn them into proof of nonclosure.
5. A digest match does **not** authenticate that a precommit existed before data inspection. Output must explicitly say `EXTERNAL_PRECOMMIT_TIMESTAMP_UNVERIFIED`, with `certified_exclusions=0`, `human_physical_validation=false`, `release=BLOCKED`.

## Kill criteria

Any exploratory witness counted as held-out, any post-lock mutation accepted, any unknown subject admitted, any negative reference promoted to nonclosure, or any synthetic record called a validated human result fails this method. No retuning on held-out observations.

## Evidence boundaries

This tests scientific provenance and participant-disjoint inference, not shutter timing, eyelid anatomy or physiology. No new human videos, independent rater pairs, physical optical captures or certified velocity ceilings are available in this run. Actual physical shutter/clock calibration and two blinded anatomical reviewers remain the decisive bottlenecks. Product stays `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. Hush unchanged.
