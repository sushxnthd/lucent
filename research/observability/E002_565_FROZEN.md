# E002-565 FROZEN | Cross-paradigm human-reference provenance falsification

Frozen 2026-10-31 before writing the executable. E002-371 is the sole primary kernel. Existing branch `research/observability-human-boundary`, draft PR #26. This experiment is a **source-identity falsification and fail-closed validation guard**, not a physiological discovery or physical shutter calibration.

## Precommitted observation from independently published records

Two different 2026 Zenodo records both contain a file named `S01.zip` and a Phantom eye video, but they describe **different experimental paradigms** from the same 2025 paper:

| Record | Paradigm | Native video prefix | S01 archive MD5 | Previously reported AVI frames |
|---|---|---|---|---|
| https://zenodo.org/records/18970793 | Motor Imagery | `MI011_phantom.avi` | `fb56109542a13aa7879778833fe4cbaa` | 51,252 (E002-510 metadata only) |
| https://zenodo.org/records/18971758 | Motor Execution | `ME011_phantom.avi` | `bce89dd9fbb67e27a656623aa27927e0` | 48,756 (E002-563 metadata only) |

Both record pages were inspected 2026-10-31. Their frame-count difference **must not be called dropped frames, re-encoding or source-version divergence**, because they are distinct tasks/recordings. The same S01 participant label is not a globally unique video/sample key. No private imagery or raw frame hashes will be published.

## Falsifiable provenance rule

For a human reference positive to be joined to a previously sealed ordinary-camera prediction, require **exact equality** of the canonical identity tuple: Zenodo record, paradigm, source archive MD5, native video member, session, participant, original-video SHA256, and native frame namespace. Enforce the public MI/ME record-to-paradigm-to-filename binding, not merely equality of self-declared labels. Reject missing, malformed or contradictory fields; never use file basename `S01.zip`, participant `S01`, nominal FPS, container presentation timestamps or a shared paper DOI as an identity substitute.

A matching tuple is **necessary but insufficient**: absent independent sensor time, shutter, continuous-time motion bound, anatomical reference and blinded-rater evidence, the only permitted output is `SOURCE_MATCH_ONLY_UNCALIBRATED` with physical certification false. The guard cannot authenticate the declared hashes or independence of evidence.

## Locked adversarial predictions

1. MI and ME both labeled S01/Sess01 with identical nominal 1-fps AVI headers: **REJECT_CROSS_PARADIGM**.
2. Same record/paradigm/subject but distinct original video SHA256: **REJECT_VIDEO_IDENTITY**.
3. Same record/video digest but distinct session or frame namespace: **REJECT_SAMPLE_NAMESPACE**.
4. Same record with missing original-video SHA256, unknown record or mismatched archive MD5/prefix: **REJECT_INCOMPLETE_OR_CONTRADICTORY_SOURCE**.
5. Exactly matching complete identity: **SOURCE_MATCH_ONLY_UNCALIBRATED**, never certified closure.
6. Even when a caller asserts all physical certificate booleans, the guard must not promote unverified declarations into a physical claim.
7. Independent implementation must agree on all test vectors; preserve negative cases.

## Stop and release

No additional S01 metadata schema archaeology or cross-archive frame alignment. This is a one-time correction of an invalid potential cross-paradigm inference. Next eligible primary evidence must be actual independent blinded anatomical S01 annotations and externally timed physical optical acquisition. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Keep Hush separate.
