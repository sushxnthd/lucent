# E002-525 | Frozen prospective prediction-lock attack and human-validation integrity gate

Date: 2026-10-29. Same E002-371 kernel, branch `research/observability-human-boundary`, draft PR #26. Freeze this protocol **before** implementation or test execution. Evidence tier: adversarial study-inference software test, not human or physical validation.

## Predeclared falsification

The E002-519 reference-censoring evaluator accepts both `prediction` and reference annotations in one editable input. Its duplicate-ID checks do not authenticate that exclusions were frozen before reference review. Predeclare a valid contained `CLOSED_WITNESS` for an `EXCLUDE` gap; then (A) replace its prediction with `ABSTAIN`, (B) remove the gap from a multi-gap study, or (C) expand the blind interval after observing the reference. The old evaluator should accept these edited inputs, producing a different result or omitting a failure. This is **not** a claim that anyone altered actual human data. It is a pre-data threat model for outcome-dependent selection.

## Frozen correction and exact acceptance

Create a separate, owner-private, canonical `E002-525-v1` manifest of every prespecified gap, with unique opaque IDs, participant/session pseudonyms, prediction, and conservative timing bounds. Require nonempty 32-byte random nonce, exact field allowlists, finite time values, a positive gap only for `EXCLUDE`, and an explicit `ABSTAIN` record for every noncertified window. Canonicalize using sorted-key compact JSON and commit SHA-256 over a domain-separated prefix, nonce and canonical manifest. Only the digest is published in a timestamped GitHub commit **before** reviewers access reference labels. Keep the nonce, manifest and all participant identifiers private.

After adjudication, a separate program receives the immutable manifest, its previously published digest, and the E002-519 evidence JSON. Verify the digest and **exact** gap-ID set and all frozen predictions and timing bounds before invoking the existing E002-519 evaluator. Any omission, addition, change to EXCLUDE/ABSTAIN or bounds, invalid nonce, duplicate, or missing commitment fails closed. A valid qualified witness must remain a falsification. Reference censoring must never become a clean success. Do not add a `VERIFIED_NO_HIDDEN_CLOSURE` state.

## Predeclared adversarial tests

1. Demonstrate old E002-519 accepts post-hoc EXCLUDE->ABSTAIN and omission on a two-gap artificial fixture.
2. New gate rejects both edits, altered timing, changed participant/session attribution, uncommitted additions, digest mismatch, duplicate IDs, malformed numbers, and insufficient nonce.
3. Correctly locked two-gap fixture preserves one falsification and one censored outcome; no exposure or human facts are inferred.
4. Verify canonicalization is independent of JSON key insertion order, but not changes to record order (the study enrollment sequence is frozen).
5. Confirm no individual IDs, nonce, images, reference labels or private hashes are written to the repository by the test suite. All fixtures synthetic.
6. Local Python tests and hosted GitHub Actions must pass. A self-supplied digest without an independently timestamped pre-label publication is **not** proof of prospective locking.

## Product consequence

Historical E002-519/520 outputs are *unlocked intake* unless a separate prospective commitment exists. A zero-falsification rate without a verified locked denominator is inadmissible for a product-risk claim. No anatomical ratings or authenticated shutter/clock evidence currently exist; Lucent remains `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. No new source search, simulated reviewers, merge or deployment.
