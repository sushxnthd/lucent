# E002-508 | Frozen source-to-rating binding falsification

Frozen 2026-10-28 before editing E002-507 evaluator. Primary E002-371 kernel, existing branch `research/observability-human-boundary`, draft PR #26. No human imagery or annotations are used.

## Decisive question
Can an attacker substitute a syntactically valid 20-clip E002-492 owner manifest that changes native source-frame provenance while preserving reviewer A/B labels, and still obtain an apparent E002-507 native-frame closure witness? The current evaluator checks subject, clip count, clip IDs, reviewer frame positions and delta, but does **not** compare the owner-only manifest to the deterministic, previously frozen E002-492 mapping. This is a provenance/measurement validity test, not an attack on camera physics.

## Frozen adversary
1. Construct the canonical `build_manifest()` and two *synthetic* A/B annotation files: all 260 frames OPEN except one CLOSED at local index 5 of `clip_00`; use positive delta=1 px and the already frozen 0.10 threshold. This produces exactly one **synthetic** witness under the canonical manifest. These are software fixtures, never human observations.
2. Keep both annotation files byte-for-byte unchanged. Alter only `clip_00.native_frames[5]` in the owner manifest by +1000, and separately alter the `candidate` bit, `center_native_frame`, or add an unauthorized key. These changes invalidate the frozen physical source-to-label correspondence while retaining schema-shaped clip IDs.
3. **Prepatch prediction:** E002-507 silently accepts each modified manifest and reports the same one-witness count. **Postpatch prediction:** every noncanonical owner manifest is rejected before classification, while the canonical manifest still produces the synthetic fixture witness. A manifest copy with identical canonical values must remain valid.
4. Preserve an executable prepatch/postpatch attack runner and independent regression tests. No retuning of closure threshold or window selection. Keep product `ABSTAIN_UNCALIBRATED`, release `BLOCKED` regardless of software outcomes.

## Hard limit
Canonical-manifest equality verifies **declared source-index provenance only**. It does not cryptographically bind image pixels to ratings, establish that two distinct humans rated them, authenticate the S01 camera clock, validate iris scale, or certify continuous-time velocity. E002-502 archive checksum/source replay and independent human/instrument checks remain mandatory. Do not treat passing synthetic tests as human evidence.

## Kill / continuation
If prepatch substitution does not survive current validation, preserve the negative result and do not patch. If it survives, enforce exact frozen manifest equality in the evaluator and verify the previously accepted forgery is rejected. If the fix rejects legitimate canonical input or fails hosted CI, preserve failure and keep research blocked.
