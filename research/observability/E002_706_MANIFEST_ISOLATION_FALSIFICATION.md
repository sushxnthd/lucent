# E002-706 | Adversarial acquisition-gate falsification (2026-11-07 UTC)

## New finding from source-level inspection
The E002-705 manifest gate is **not yet a secure prediction/reference isolation boundary**. Its forbidden-field check is applied only to each record's top-level keys, and it does not inspect the envelope or nested dictionaries. A manifest can therefore carry a top-level `reference_labels` field or `metadata: {"ground_truth": ...}` while returning `STRUCTURE_ONLY_PASS`, provided all required record fields are otherwise valid. This is a logical counterexample derived from the committed implementation, **not an executed exploit test**.

Additional failure cases:
1. A valid interval `aperture_scale_interval: [0, 0]` passes the nonnegative interval predicate, although zero anatomical scale cannot support aperture inference.
2. `json.loads` accepts duplicate object keys by retaining the last value, defeating an unambiguous signed manifest interpretation.
3. Non-string participant/session identifiers that are arrays or objects are rejected by `check`, but the later duplicate-key set construction may raise an unhandled `TypeError`, preventing a machine-readable fail-closed verdict.
4. Nested outcome-like keys are not recursively screened; even exhaustive keyword screening cannot establish noninterference for semantically disguised labels.

## Concrete falsification protocol
Freeze a valid E002-705 record; independently add each of the four mutations above. Require a nonzero exit, a machine-readable `ABSTAIN_INVALID_MANIFEST` verdict, and no raw reference labels in logs. Run these against the unmodified version to establish baseline failures, then against a patched version. Also fuzz nested arrays, JSON duplicate keys, Unicode keys, NaN/Infinity, large manifests, and identifier type confusion. Treat any crash as a failed gate test, not successful abstention.

## Correct enforcement boundary
Prediction execution must consume a **strictly allowlisted, versioned schema** rather than recursively trying to enumerate all possible outcome-bearing names. Store reference annotations in a separate inaccessible process/storage principal; bind both prediction and reference artifacts to a frozen manifest digest; release reference only after prediction digest is immutable. A JSON validator alone cannot guarantee blindness or provenance.

## Scientific and product consequence
E002-705 is a structural preflight only and should not be described as proof of prediction/reference isolation. No participant data, camera timing, velocity ceilings, physical shutter captures, or held-out outcomes were obtained in this run. Product remains `ABSTAIN_UNCALIBRATED`; release remains `BLOCKED`. Next work must implement the strict allowlist plus executable adversarial tests, then prioritize physical acquisition. Do not promote this source-level finding to a validated end-to-end isolation claim.
