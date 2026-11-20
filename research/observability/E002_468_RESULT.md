# E002-468 — first independent development-video acquisition

Date: 2026-10-26. **Current evidence tier:** independently acquired public human-video archive, checksum-verified, with container-level signal diagnostics. No anatomical timing or closure labels.

## Change from E002-467
The independent 2026 Zenodo rehost of the original 2025 Eye-BCI recordings includes the Phantom AVI, Phantom XML and sync CSV, not merely EEG. Record: https://zenodo.org/records/18971758 ; preview: https://zenodo.org/records/18971758/preview/S19.zip?include_deleted=0 . E002-467's sealed split places S19 in calibration; S01 is holdout and is explicitly not accessed.

The rehost describes video as approximately **500 fps** whereas the primary dataset descriptor was recorded in E002-467 as **150 fps**. The difference is a prospective empirical measurement question, not a reason to silently relabel acquisition. The frozen test inspects real AVI frame-rate declarations, first 120 container timestamps and first 512 decoded-frame signal differences, after checking the published archive MD5. Neither frame metadata nor video decoding authenticates sensor shutter support.

## Hosted empirical result, 2026-10-27 (UTC run 2026-10-26)

The first hosted acquisition run [40368566214](https://github.com/sushxnthd/lucent/actions/runs/40368566214) failed **before download** because `ffmpeg` was absent on the runner. Commit `94b356f` explicitly provisions ffmpeg/ffprobe. The rerun [40378675346](https://github.com/sushxnthd/lucent/actions/runs/40378675346) then **passed all six synthetic tests, downloaded the actual S19 archive, verified the published MD5, extracted and SHA-256-hashed the original video/XML/sync files, decoded 512 real frames, and uploaded an aggregate**. Full nonidentifying aggregate: [E002_468_HUMAN_SIGNAL_AGGREGATE.json](E002_468_HUMAN_SIGNAL_AGGREGATE.json). This is the first independently acquired raw human eye video for this track; raw video was discarded in ephemeral CI and is not committed.

**Decisive negative timing result:** the actual `ME191_phantom.avi` declares `r_frame_rate=1/1`, `avg_frame_rate=1/1`, `nb_frames=52049`, duration `52049.000000` s, 320x288 MPEG-4. The first 120 decoded-frame presentation timestamps increase by exactly **1000 ms per frame**. This contradicts both the 150-fps primary-source claim and the rehost's approximately 500-fps statement **as container metadata**. It does *not* prove a physical acquisition rate of 1 fps: AVI timebases can be placeholders. Treating those timestamps as camera exposure times would be scientifically invalid. **No per-frame temporal eyelid velocity, hidden-closure test, or frame-to-millisecond inference is authorized.**

Observed first-512-frame video signal diagnostics (64x48 grayscale): mean brightness 73.155708/255; adjacent-frame mean absolute intensity change median 0.384440, p95 16.947917, maximum 29.466146. These establish that frames decode and exhibit variation, not anatomical aperture or actual frame rate. Source archive SHA-256 `da4281a4d77f95683f541452a0f5b6e56ad8d54139e3be9d7b64374d77a41c25`; AVI SHA-256 `0c75a359843694adc6eac1057d6c2aca6e94b31fea464c07d68d28a25b4ddbde`. Human participants newly annotated: **0**. Physical instrument acquisitions: **0**.

**Decision:** `TIMING_UNAUTHENTICATED`. A one-time decisive reconciliation using the downloaded sync CSV and Phantom XML is justified, but do not infer physical FPS from image dynamics or the video container. If the files lack an independent timestamp/frame correspondence, stop this dataset's temporal analysis and move to the previously frozen independently timed physical instrument protocol. Keep S01 and other holdout data sealed.

## Reproducible implementation
- [Frozen protocol](E002_468_FROZEN.md), [Python acquisition analyzer](e002_468_video_acquisition.py), [six adversarial synthetic tests](test_e002_468_video_acquisition.py), and [one-shot hosted acquisition workflow](../../.github/workflows/e002_468_human_video_acquisition.yml).
- Local synthetic 150-fps AVI fixture: 150 decodable frames, 120 available PTS, 0 nonpositive timestamp steps, median step 6.667 ms; physical release false. This is **not** human evidence.
- Local adversarial suite: 6/6 passed. It checks expected-rate and unexpected-rate video, checksum mismatch, unsafe ZIP paths, malformed rational FPS and percentile behavior.
- Hosted human download and signal audit: **completed** in [run 40378675346](https://github.com/sushxnthd/lucent/actions/runs/40378675346). Original video integrity and aggregate video-signal diagnostics are verified. **Physical timing and anatomical labels remain unresolved.**

## Falsification and product decision
If AVI rate differs from the declared 150 fps by >1%, flag NOMINAL_RATE_CONFLICT and keep E002-467's 150-fps preflight inapplicable to this recording until timestamps are reconciled. If rates agree, that establishes only video container timing, not physical shutter integration. Frame intensity differences are not anatomical aperture or closure witnesses.

E002-371 remains physically unvalidated; no universal speed bound, closure-exclusion guarantee, blink duration, PERCLOS, fatigue or medical claim. Product remains ABSTAIN_UNCALIBRATED. No raw human video or per-frame measurements are uploaded. PR #26 stays draft. Hush PR #45 unchanged.
