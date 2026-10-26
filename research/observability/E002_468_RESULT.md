# E002-468 — first independent development-video acquisition

Date: 2026-10-26. **Current evidence tier:** frozen human-data acquisition protocol, executable integrity-gated video signal audit and synthetic fixture tests. **Do not infer real human results until the hosted acquisition succeeds.**

## Change from E002-467
The independent 2026 Zenodo rehost of the original 2025 Eye-BCI recordings includes the Phantom AVI, Phantom XML and sync CSV, not merely EEG. Record: https://zenodo.org/records/18971758 ; preview: https://zenodo.org/records/18971758/preview/S19.zip?include_deleted=0 . E002-467's sealed split places S19 in calibration; S01 is holdout and is explicitly not accessed.

The rehost describes video as approximately **500 fps** whereas the primary dataset descriptor was recorded in E002-467 as **150 fps**. The difference is a prospective empirical measurement question, not a reason to silently relabel acquisition. The frozen test inspects real AVI frame-rate declarations, first 120 container timestamps and first 512 decoded-frame signal differences, after checking the published archive MD5. Neither frame metadata nor video decoding authenticates sensor shutter support.

## Reproducible implementation
- [Frozen protocol](E002_468_FROZEN.md), [Python acquisition analyzer](e002_468_video_acquisition.py), [six adversarial synthetic tests](test_e002_468_video_acquisition.py), and [one-shot hosted acquisition workflow](../../.github/workflows/e002_468_human_video_acquisition.yml).
- Local synthetic 150-fps AVI fixture: 150 decodable frames, 120 available PTS, 0 nonpositive timestamp steps, median step 6.667 ms; physical release false. This is **not** human evidence.
- Local adversarial suite: 6/6 passed. It checks expected-rate and unexpected-rate video, checksum mismatch, unsafe ZIP paths, malformed rational FPS and percentile behavior.
- Hosted human download and signal audit: **pending**, no human frame, anatomical label, or physical measurement yet claimed. Hosted workflow must be checked before updating this status.

## Falsification and product decision
If AVI rate differs from the declared 150 fps by >1%, flag NOMINAL_RATE_CONFLICT and keep E002-467's 150-fps preflight inapplicable to this recording until timestamps are reconciled. If rates agree, that establishes only video container timing, not physical shutter integration. Frame intensity differences are not anatomical aperture or closure witnesses.

E002-371 remains physically unvalidated; no universal speed bound, closure-exclusion guarantee, blink duration, PERCLOS, fatigue or medical claim. Product remains ABSTAIN_UNCALIBRATED. No raw human video or per-frame measurements are uploaded. PR #26 stays draft. Hush PR #45 unchanged.
