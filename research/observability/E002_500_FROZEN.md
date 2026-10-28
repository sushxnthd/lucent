# E002-500 | Frozen source-to-annotation provenance falsifier

Frozen 2026-10-28 before implementation. Primary E002-371 human-validation kernel. **This is an evidence-chain falsification, not a new physical theorem or a human anatomical measurement.**

## Hypothesis

E002-496 checks the checksum of the S01 source archive during packet creation, but its *separate* packet integrity checker verifies only image filenames, counts, 320x288 PNG headers and private permissions. It does not compare the 260 image pixels to the independently checksum-verified source. Thus a packet whose frames were substituted *after extraction* may still return `TECHNICAL_PACKET_INTEGRITY_PASS` and be incorrectly attributed to S01.

## Prespecified attack

1. Construct a complete synthetic private packet with the actual frozen E002-492 manifest and blank A/B templates. Supply 260 distinct filenames with PNG headers declaring 320x288 but with arbitrary non-source payloads of length >=100 bytes. The existing E002-496 validator is predicted to accept this forged packet. **No human imagery is needed.**
2. Change exactly one private PNG byte in an otherwise valid source-derived packet. The existing checker is predicted to remain oblivious if the PNG header and file size stay valid.
3. Independently re-extract the frozen 260 frames from the pinned MD5-verified S01.zip into a fresh private directory, compare exact PNG bytes to the packet at all 260 names, and reject a single substitution. No frame, image hash, source index or per-rater rating is printed or uploaded.
4. A positive authentic-data test must execute on the GitHub runner, which downloads the pinned S01 archive; local synthetic tests establish only the negative cases. Source-replay verification must be explicit in the product/evidence gate and never silently inferred from the old E002-496 status.

## Kill criteria and evidence tier

- If the old checker rejects the forged synthetic packet, report the prediction falsified and do not claim the vulnerability.
- If a single altered frame passes the new source-replay gate, reject the gate.
- If authentic source replay is not independently verified in hosted CI, label the new gate `UNVERIFIED` and retain the release blocker.
- Even if provenance passes, there are zero human ratings, no authenticated physical acquisition clock, no certified velocity envelope and no held-out closure test. E002-371 remains `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.

No images or private hashes in GitHub artifacts; no change to Hush, existing branches or hourly schedule.
