# E002-559 FROZEN | Browser decoder as a human-evidence acquisition nuisance

Date: 2026-10-31. Kernel: E002-371 human validation. Frozen before reviewing the replacement hosted browser run.

## Observed falsification that motivated this protocol

Hosted E002-557 run [41155599319](https://github.com/sushxnthd/lucent/actions/runs/41155599319) completed with failure. Chromium reported `canPlayType('video/mp4; codecs=avc1.42E01E') == ''`, `MEDIA_ERR_SRC_NOT_SUPPORTED` (error 4), `DEMUXER_ERROR_NO_SUPPORTED_STREAMS`, and videoWidth=0 for the locally hashed H.264 fixture. The prior loopback-origin fix did not fix decoding. A cryptographic video hash certifies source bytes, **not decodability, frame correctness, anatomical annotation, or acquisition timing**.

## Prespecified repair and test

Use a 320x240, 30-Hz, two-second **synthetic** VP8/WebM fixture instead of H.264/MP4; do not alter the rater's anatomical adjudicators. Keep the same two independently labeled synthetic packets, source-byte SHA-256, local-only network guard, 260 native-frame nuisance-abstention cases, two video landmarks, and JSON export/audit. Check that `videoWidth == 320`, the source hash agrees, exports have the expected structure, and off-loopback traffic is zero. Report any failures rather than weakening checks.

This is a browser-instrument test, not a physiological result. A VP8/WebM pass is **not** evidence that arbitrary human H.264, HEVC, variable-frame-rate, smartphone, or high-frame-rate videos will decode correctly. A separate cross-decoder/physical-clock test is mandatory before human acquisition can be treated as instrument-verified. The 30-Hz fixture is not an independently clocked 30-Hz measurement.

## Explicit falsification criteria

- If Chromium cannot decode the VP8 fixture, or hash, export, audit, or network checks fail, the synthetic video-rater end-to-end validation **fails**.
- If any rater/export produces a physical closure certificate from synthetic frames, the human-evidence gate **fails**.
- If the browser succeeds, classify only as `SYNTHETIC_BROWSER_E2E_PASS`, with **zero** real raters, authenticated shutter captures, certified motion bounds, and held-out physical predictions.

## Human-study follow-through

Acquire permissioned high-rate native video with documented sensor acquisition times, exposure/shutter response and synchronized clock. Preserve original bytes and an independently decoded frame-index/time map; compare two decoder implementations or explicitly abstain on disagreements. Obtain blinded independent anatomical ratings, record geometry/brightness/blur/gaze/glasses/missingness, and freeze participant-disjoint ordinary-camera predictions before inspecting the high-rate reference. Never promote sampled peak speeds or accelerations to certified continuous-time ceilings. Until independent calibration and held-out physical testing, Lucent remains `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
