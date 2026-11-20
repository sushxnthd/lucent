# E002-510 | Frozen cross-source timebase falsification on authentic S01

Frozen 2026-10-28 before opening S01 Phantom XML or sync CSV. Existing E002-371 kernel, branch `research/observability-human-boundary`, draft PR #26. No human anatomy will be opened, labeled, uploaded or inferred. This is a **single bounded source-timebase experiment**, not a new dataset search or a physical shutter calibration.

## Predeclared hypothesis and falsification

The paper states 150 fps, the 2026 rehost advertises approximately 500 fps, and the AVI header has previously been reported to be unreliable (1 fps). A nominal FPS cannot be used as a physical acquisition period without cross-source timing evidence. Independently inspect **only** the already checksum-pinned S01 archive (MD5 `fb56109542a13aa7879778833fe4cbaa`), specifically its Phantom AVI, Phantom XML, and sync CSV. Never use S21–S31 held-out anatomy.

1. Confirm archive checksum and safe ZIP members. Read only metadata. The script must not decode, save or upload frames or individual event times.
2. Record the AVI nominal rate and frame count, plus a bounded packet-PTS cadence audit; these are container claims, not authenticated camera time.
3. Accept a source-derived Phantom frame-to-time mapping **only if** an explicit frame-index column and explicitly Phantom-associated timestamp column are found, unique, finite, strictly increasing, at least 100 distinct frames, and their time unit is unambiguous. Reject ambiguous column selection, other-device clocks, duplicate indices, unknown time units, and unverified offsets. If no such mapping exists, report `NO_VALID_PHANTOM_FRAME_TIME_MAP`.
4. If such mapping exists, calculate median frame period, 5th/95th percentile positive periods, gaps >1.5x median, and percent deviation from 1000/150 ms and 1000/500 ms. The fixed consistency criterion is within **2%** of the stated 150-fps period on median and at most **1%** large gaps. Any failure falsifies *using this map as a clean 150-Hz reference*, not the published study itself. A pass is `SOURCE_TIMEBASE_CONSISTENT_UNAUTHENTICATED`, never hardware clock authentication.
5. Inspect Phantom XML for explicit nominal FPS or shutter duration **only as reported metadata**. Do not infer shutter width from frame rate or container PTS. No XML or CSV data may silently override the physical clock/shutter requirements.
6. Publish a sanitized aggregate only: counts, source/parse tiers, statistics, contradiction flags, no per-frame times, source frame indices, image hashes or private participant content. The only allowed physical/product result remains `ABSTAIN_UNCALIBRATED` and `BLOCKED`.

## Fixed stop rules and expected outcomes

- If metadata cannot be unambiguously paired with Phantom frames, stop with `NO_VALID_PHANTOM_FRAME_TIME_MAP`; do not reinterpret other device clocks post hoc.
- If the 150-Hz consistency criterion fails, prohibit using nominal 150-fps as an observed shutter-gap bound. If it passes, it establishes **internal source consistency only**, not exposure start/end or a certified velocity envelope.
- Preserve all failures and the original threshold. No iterative heuristic column matching to obtain a pass.
- This is the **last S01 metadata-only attempt**; next primary evidence must be genuine independent blinded anatomical review and physically measured optical clock/exposure. A new XML/CSV schema inspection is not a substitute.

## Evidence and safety

The existing E002-507 private two-rater packet remains unchanged. No reviewer data exist at freeze. A verified rate is not a closure label, shutter duration, continuous-time eyelid-speed ceiling or held-out human validation. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. No Hush branch changes.
