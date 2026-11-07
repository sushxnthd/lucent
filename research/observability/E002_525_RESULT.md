# E002-525 | Prospective exclusion-lock falsification and owner-private replay

Date: 2026-10-29. Primary E002-371 workstream, existing branch and draft PR #26. [Frozen protocol](E002_525_FROZEN.md) committed first at `e870d5f215ecfc504fcd1fec14c2591d24c6a0ec`. **Evidence tier:** prospective study-integrity attack and software enforcement, not human anatomy, physical shutter calibration, independent reviewer completion, or a new measurement law.

## Scientific-inference failure exposed

E002-519 receives both the ordinary-camera `prediction` and subsequent high-speed `references` in one mutable JSON. Its correct one-sided reference-censoring logic does **not** establish that exclusions were actually frozen before reference review. A study owner can inadvertently or deliberately replace a contradicted `EXCLUDE` with `ABSTAIN`, omit that window, or alter its timing interval after inspecting outcomes. The historical evaluator accepts such otherwise valid inputs; its duplicate-ID check cannot detect post-hoc selection.

Frozen artificial two-gap attack (no real participants or measurements):

| Replay | Syntactically qualified synthetic E002-519 label | E002-519 falsifications | E002-519 not-testable |
| --- | --- | ---: | ---: |
| Original, g1 EXCLUDE + g2 EXCLUDE | g1 | 1 | 0 |
| Posthoc g1 changed to ABSTAIN | g1 | 0 | 1 |
| Posthoc g1 omitted entirely | g1 removed from submission | 0 | 0 |

These are deterministic consequences of the existing evaluator's public input contract, not allegations of actual data manipulation. The artificial E002-519 categorical witness does not establish E002-520's separate quantitative cross-camera transport, so even the unedited synthetic falsification is not a physical closure observation. They mean that an **unlocked** zero-falsification report cannot support a prospective product-risk estimate, even if the reference adjudicator itself is mathematically correct.

## Correction

[e002_525_prediction_lock.py](e002_525_prediction_lock.py) introduces an owner-private manifest of *every* prespecified window, including abstentions, with opaque participant/session IDs, exact predictions and conservative blind-gap endpoints. A random 32-byte private nonce and canonical JSON produce a SHA-256 digest with an explicit domain separator. Publish **only** that digest in a timestamped GitHub commit **before** reviewers access reference anatomy. After review, the gate checks the pinned digest, exact gap set, frozen prediction, participant/session attribution and timing bounds before calling the unchanged E002-519 evaluator.

Any changed or omitted prespecified gap, extra gap, posthoc EXCLUDE/ABSTAIN change, changed bound, malformed digest or changed frozen attribution fails closed. The gate prints only aggregate counts. No raw eye images, source-frame indices, individual ratings, manifest, private nonce or reference evidence are committed.

A self-supplied digest **without independently verifiable pre-label publication is not a prospective lock**. The tool cannot authenticate GitHub timestamps, independent human raters, participant identity, native-frame provenance, exposure truth, or whether a reference was assigned to the correct participant. Those are separate release blockers. The new manifest has not yet been created for any actual human study.

## Owner-private execution

Prepare a private JSON manifest outside the Git repository with `version: "E002-525-v1"`, a securely generated 64-character lowercase hex nonce, and `gaps` containing every prespecified gap. Each gap must contain exactly `id`, `participant`, `session`, `prediction`, `left_end_max_ms`, `right_start_min_ms`. Do not publish it. Generate the nonce with `python -c "import secrets; print(secrets.token_hex(32))"`.

Before anyone opens the reference labels:

```bash
python research/observability/e002_525_prediction_lock.py digest \
  --manifest /secure/private_frozen_gaps.json
```

Commit the returned digest only, in a timestamped study-specific preregistration. After independent reference review, create a private E002-519-v1 evidence JSON with **exactly the frozen gaps** and with each gap's matching `participant` and `session` fields alongside the existing E002-519 reference fields. Verify using the *previously published* digest, not a newly computed replacement:

```bash
python research/observability/e002_525_prediction_lock.py verify \
  --manifest /secure/private_frozen_gaps.json \
  --published-digest <prelabel_committed_sha256_digest> \
  --evidence /secure/private_reference_evidence.json
```

The CLI outputs aggregate counts and blocked product state, never a no-hidden-closure certificate. Retain the private manifest, nonce and raw evidence for authorized independent audit. Keep participant identifiers pseudonymous and images/ratings outside GitHub.

## Verification status

[16 adversarial Python test groups](test_e002_525_prediction_lock.py) were committed, including an executable **prepatch** post-hoc-selection demonstration, commitment mismatch, denominator edits, timestamp-bound edits, attribution changes, malformed nonce, duplicate gaps, reference censoring and canonicalization. [Dedicated hosted workflow](../../.github/workflows/e002_525_prediction_lock.yml), [run 40852051733](https://github.com/sushxnthd/lucent/actions/runs/40852051733) **completed successfully** on commit \`c5d5ce81fb4b3feb2a86db3e2742c7a00ec468fd\`. GitHub Actions independently executed all 16 adversarial Python test groups and syntax validation. This is software verification, not a prospective human study or instrument calibration.

## Product and evidence gates

No E002-519 or E002-520 intake can support a *prospective* false-exclusion-rate claim unless its ordinary-camera predictions, all eligible-window denominators and participant assignments were frozen and independently timestamped before reference labels. This new lock is necessary but insufficient: an authentic physical shutter/clock reference, quantitative same-predicate anatomy transport, two genuine independent blinded reviewers and fully accounted-for reference censoring remain mandatory.

**Actual independent human ratings: 0; authenticated physical shutter measurements: 0; certified continuous-time human speed ceilings: 0; held-out physical predictions: 0.** Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. No merge, deployment, new dataset search, simulated reviewer, or Hush branch write.
