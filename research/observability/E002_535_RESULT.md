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

## Hosted independent human replay: 2026-10-30 UTC (verified)

**Evidence tier: checksum-pinned real-human-video, independent software replay of a frozen image-space null. This is not independently rated anatomy, physical camera timing, participant-disjoint validation, or a new physiological law.**

The first E002-535 hosted attempt, [run 40983540709](https://github.com/sushxnthd/lucent/actions/runs/40983540709), **failed** after successfully downloading and verifying both source archives. Both human jobs stopped before video analysis because `ffprobe` was absent from the runner (`FileNotFoundError`). The original integrity job passed, but its optional codec roundtrip was not sufficient evidence that the CLI was installed. The workflow was repaired at commit [a12bfe5](https://github.com/sushxnthd/lucent/commit/a12bfe5c44f176c17f6e7fa57d290290586daf4c) by explicitly installing and verifying FFmpeg and ffprobe in both jobs, before human source download.

The repaired [run 40988238089](https://github.com/sushxnthd/lucent/actions/runs/40988238089) **completed successfully across all three jobs**. Its integrity job verified FFmpeg 6.1.1-3ubuntu5 and ran all **12/12 adversarial tests**, including an actual FFV1 command-line encode/decode roundtrip. The two human jobs each downloaded and MD5-verified their authentic source archives and ran the independent FFmpeg CLI grayscale decoder and separate float64 ROI implementation.

| Participant | Phase | Eligible | Rejected time/ID | Eye-return | Eye-specific | Background-return | Frozen replay decision |
|---|---:|---:|---:|---:|---:|---:|---:|
| S01 | 0 | 2,379 | 22 | 0 | 0 | 0 | Agreement |
| S01 | 2 | 2,378 | 22 | 0 | 0 | 0 | Agreement |
| S19 | 0 | 2,380 | 21 | 0 | 0 | 0 | Agreement |
| S19 | 2 | 2,379 | 21 | 0 | 0 | 0 | Agreement |
| **Total** | both | **9,516** | **86** | **0** | **0** | **0** | **Agreement** |

These are **observed E002-535 outputs**, not copied predicted counts. Both human jobs emitted `original_frozen_counts_reproduced: true` and `decision: REPLAY_AGREEMENT`. The original E002-534 null therefore **replicates at the aggregate level across the two software implementations**. This supports the narrow decision to **keep the frozen image-return observable rejected** rather than retune it.

**Independence limits:** Both pipelines read the same previously studied participants and source metadata parser; FFmpeg CLI and OpenCV may share libavcodec internally. The grayscale conversion and float precision differ, but the zero aggregate agreement is not proof of bitwise identity, independent physiological measurement, or that no true eyelid closure occurred. No frame-level agreement statistics were exported, by design. Phase windows are dependent, and the two participants do not support a population false-negative confidence claim.

**Stop decision:** Close E002-534/535 image-return investigation at these frozen thresholds. Do not retune S01/S19, relabel null image events as anatomical absence, or promote the pixel observable. Future primary work must use independently timed physical camera exposures, native-frame anatomical aperture with two blinded raters, explicit missing/unknown intervals, and participant-disjoint prospective gap predictions under a defensible velocity envelope. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush PR #45 was not modified.
