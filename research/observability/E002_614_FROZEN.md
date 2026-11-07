# E002-614 FROZEN | Cryptographic source-packet binding for blinded human eyelid review

Date: 2026-11-03. Parent: E002-371. Research branch: `research/observability-human-boundary`; draft PR #26. **Prospective instrument-validity attack, not human evidence or new observability mathematics.** Frozen before implementation.

## Concrete falsifier
The E002-598 offline reviewer accepts any decodable 640x480 PNG whose directory/name matches a blank blinded template. Two visually different frames with the same filename and dimensions can therefore be silently substituted without invalidating the exported annotations. Such annotations cannot be attributed to the owner's intended original frames. This is a **source-integrity** failure, not evidence of wrong anatomical ratings.

## Intervention
Owner privately freezes the actual SHA-256 of each PNG and a deterministic packet digest, without releasing participant/source mapping. An opt-in bound E002-598 template includes only blind clip/frame keys, individual PNG digests, and packet digest. The browser must compare the bytes of **every** selected PNG to the frozen digest *before* enabling any review; mismatch, missing WebCrypto, malformed digest, unexpected frame, or packet digest mismatch must fail closed. A reviewer export must state `source_integrity.status=SHA256_PACKET_MATCH` and packet digest. Legacy unbound templates remain usable only as `UNBOUND_DEMONSTRATION_ONLY` and must not be accepted as physical human-validation evidence.

Owner's private independent manifest and committed protocol SHA must be retained outside GitHub. A hash alone cannot authenticate the owner, prove the reviewer is independent, prevent someone from changing both images and template, or prove physical shutter/anatomical/velocity calibration. The reviewer's original images and individual ratings must not enter public CI.

## Preregistered tests
1. Same filenames, dimensions, counts and valid image decode, but one frame's bytes changed: **legacy interface accepts**, bound interface **REFUSES**.
2. Exact matching PNG bytes: bound interface loads all expected images and exports the packet digest.
3. A changed template digest, missing image digest, malformed digest, duplicate frame key or absent crypto API: **REFUSES**.
4. Unbound legacy templates: explicitly export `UNBOUND_DEMONSTRATION_ONLY`; no silent upgrade.
5. Independent Python packet builder/auditor and browser SHA-256 agree on the exact digest scheme. Adversarial tests run with synthetic, non-human PNG stubs; no real human annotation is fabricated.
6. No network, telemetry, persistent browser storage, identity mapping, or raw face images added.

## Digest canonicalization
For each expected key `clip_id::zero_based_frame_index` (clip ID already restricted to ASCII alphanumeric, underscore, dash), sorted lexicographically, concatenate `key + TAB + lowercase_64hex_sha256 + LF`; `packet_sha256` is SHA-256 of UTF-8 bytes of this concatenation. `frame_sha256` maps each key to the corresponding SHA-256 of the original PNG file bytes. The owner must precommit the packet SHA through an independent channel **before** rating.

## Evidence and release gates
A verified bound packet is only a prerequisite to an authentic two-rater study. It does not create human data, clock certificates, or an eyelid velocity ceiling. E002-371 remains unvalidated. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Preserve Hush's separate branch and draft PR #45.
