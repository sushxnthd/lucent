# E002-535 RESULT | Independent replay launched; human comparison pending

Date: 2026-10-30. Lucent primary E002-371 kernel; established `research/observability-human-boundary` branch and draft PR #26.

## Scientific purpose

E002-534 produced zero image-return candidates across 9,516 eligible phase windows in two checksum-pinned real-human videos, but its source decoding and measurement implementation shared one OpenCV pipeline. E002-535 freezes an independent software replay of **the same null**, without changing the detector, thresholds, source participants, phases or inclusion criteria. It is a replication attempt, not a new detector or a search for favorable post-hoc thresholds.

The independent implementation streams native grayscale video through the **FFmpeg command-line decoder** rather than OpenCV VideoCapture, recomputes the photometric correction and ROI excursions in a separately written float64 NumPy implementation, and independently evaluates the frozen window predicate. It shares only the pre-existing source synchronization parser and may share FFmpeg/libavcodec internally. These limitations prevent a claim of independent hardware or fully independent codec verification.

## Frozen exact predictions

E002-534's original published aggregates are locked in `e002_535_independent_human_replay.py`:

| Participant | Phase | Expected eligible | Expected time/ID rejects | Expected eye-return / eye-specific / background-return |
|---|---:|---:|---:|---:|
| S01 | 0 | 2379 | 22 | 0 / 0 / 0 |
| S01 | 2 | 2378 | 22 | 0 / 0 / 0 |
| S19 | 0 | 2380 | 21 | 0 / 0 / 0 |
| S19 | 2 | 2379 | 21 | 0 / 0 / 0 |

Any difference produces `REPLAY_DISAGREEMENT` and a nonzero process exit, rather than rewriting the frozen expected values. No human-image artifact or per-window linkage is published. Source MD5, frame geometry, decoded frame count, timestamps and native IDs are checked before accepting the aggregate.

## Verification completed this run

The protocol was committed first at `21a9d47`, before the replay code at `592e7c0`. The independent executable, 12 adversarial tests and dedicated GitHub Actions workflow were then committed. **All 12 tests passed locally** with Python, NumPy and a real FFV1 encode/decode roundtrip. Tests cover localized transients, global-flash rejection, linear ramps, missing IDs, nonfinite/jumped clocks, exact hand-computed ROI scores, aggregate privacy, invalid source, geometry, truncation and lossless FFmpeg decoding.

A test-only initial negative-control assertion incorrectly expected background excursion to remain after the frozen global-median correction; the correction correctly removes uniform flashes. The assertion was repaired **before GitHub persistence** to check the actual frozen eye-specific predicate. No algorithm or threshold was changed.

The hosted workflow is [E002-535 independent frozen human-null replay](../../.github/workflows/e002_535_independent_human_replay.yml), triggered on the research branch. **No hosted human replay result has been independently verified at the time of this report.** The real-human predicted counts are not represented as observed E002-535 counts. If source download or CI fails, report failure and preserve E002-534's original result as unreplicated by this new pipeline.

## Consequence and stop rule

If both human replays match, E002-534's negative image-return finding gains an independent *software-level* replication. If they disagree, investigate decoder/normalization differences and withhold any stronger inference. In neither case does this prove absence of hidden anatomical closure, authenticate physical shutter timing or validate a hard continuous-time human speed ceiling. The killed E002-534 pixel-return observable stays rejected and **must not be retuned on S01/S19**.

**Human anatomical ratings: 0; independently timed physical camera captures: 0; certified human velocity ceilings: 0; participant-disjoint physical predictions: 0.** Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Next decisive experiment remains the existing E002-502 two-human blinded anatomical review and E002-532 photodiode-timed physical camera study. Hush PR #45 is unchanged.
