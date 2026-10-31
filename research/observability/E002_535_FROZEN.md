# E002-535 FROZEN | Independent decoder/measurement replay of the E002-534 human null

Date: 2026-10-30. Primary E002-371 kernel. Existing branch `research/observability-human-boundary`, draft PR #26. Freeze this *before* writing the independent replay executable or inspecting new replay counts. No new physiological observable is proposed. The aim is to test whether the published zero-count E002-534 human-video result is reproducible outside its OpenCV decoding and score implementation.

## Fixed evidence and exact prediction

Use precisely the previously authenticated E002-534 human sources and first 12,006 native frames: S01 ZIP MD5 `fef02cb7ebf62e4f3efb6303284fd6cb`, S19 ZIP MD5 `8a16cf12526f7558b4e49926c4bc5e8e`. Retain the original E002-534 source-frame ID/time parser only (the sole shared metadata dependency); do not call its OpenCV decoder, `measurements`, `candidate`, `accumulate`, `quality_ok` or any scoring function. Decode the actual AVI through standalone FFmpeg CLI to native 320x288 8-bit grayscale, stream without writing decoded human frames. Check decoded frame count against synchronization record count. Use a separately written NumPy float64 implementation of the E002-534 photometric normalization, eye/background ROIs, six-frame linear endpoint interpolation, and the frozen threshold predicates.

The exact frozen thresholds remain: eye ROI rows 118:190, cols 100:230; background rows 20:100, cols 30:290. Normalize each frame by adding (median background of first frame minus its own background median), clipping to [0,255]. For each six-frame window, eye-return iff endpoint eye mean absolute difference <=8 and max interior mean absolute deviation from endpoint-linear interpolation >=18. Eye-specific iff eye-return and background excursion <=8. Background-return iff background endpoint difference <=8 and background excursion >=18. Analyze k=0,5,... and k=2,7,..., with native IDs consecutive, each synchronization delta in [0.002,0.020] seconds, total duration in [0.020,0.050] seconds. No phase, ROI, threshold or eligibility retuning.

**Prediction:** the independent replay returns E002-534's four aggregate rows exactly, including zero eye-return, eye-specific and background-return candidates: S01 phase 0 eligible 2379 rejected 22, phase 2 eligible 2378 rejected 22; S19 phase 0 eligible 2380 rejected 21, phase 2 eligible 2379 rejected 21. If any discrepancy arises, mark `REPLAY_DISAGREEMENT`, preserve both outputs and investigate before citing the human null. Do not alter thresholds to force agreement. An FFmpeg/OpenCV grayscale conversion difference is a possible genuine decoder discrepancy and must be reported, not hidden.

## Independent implementation controls

Before human replay, synthetic tests must cover an eye-localized transient accepted, a global flash vetoed, a linear ramp rejected, missing/nonmonotone native IDs/timestamps rejected, and a six-frame score implementation independently matching hand-computed small arrays. Assert no image bytes, native frame indices, clip linkage or per-window scores appear in printed results or GitHub artifacts. The runner must fail closed on source checksum mismatch, bad geometry, malformed frame byte counts, invalid metadata and decoder nonzero exit.

## Interpretation and kill decision

Agreement supports **software-level independent replay of a frozen negative image-space result** only. Both decoders may use FFmpeg/libavcodec internally; source synchronization parser is shared. Neither agreement nor disagreement measures anatomical closure, validates the E002-371 continuous-time speed assumption, authenticates a shutter/clock, or supplies an unseen participant. Zero image-return candidates remain a rejection of that particular optical proxy, not evidence of zero hidden blinks. No new optical detector is to be tuned on S01/S19. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.

If source download fails, report `NO_HUMAN_REPLAY`, keep the synthetic integrity result separately and do not claim human verification. No S01/S19 frames or participant-level linkage may be uploaded.
