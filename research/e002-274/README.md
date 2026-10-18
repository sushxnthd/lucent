# E002-274 — EVE published loader is 10 Hz, not a 60-Hz physiological waveform stream

## Decisive primary-source provenance
Pinned EVE authors' commit `82757eb2ffb4dd198db36dbfea71601098b597f0`. In `src/core/config_default.py`, `assumed_frame_rate = 10`; `src/datasources/eve_sequences.py` declares `basler: 60` and uses `index_interval = int(fps / config.assumed_frame_rate)`, then `range(start_index,end_index,index_interval)`. Therefore its **published default model loader keeps only 1 of 6 Basler frames**. It does not imply the underlying EVE recordings were acquired at 10 Hz: author documentation says native Basler 60 Hz and webcam 30 Hz. EVE source uses frame-index selection, not a newly measured exposure-clock calibration.

## SCIENCE
Question: Can the EVE published default loader serve as a 60-Hz reference-aligned visible-RGB waveform evaluator? **No.** A 10-Hz stream has a 5-Hz Nyquist limit, and 83.33% of Basler frames are skipped. Synthetic 40-ms blink-like aperture event centered at 50 ms is present at 60-Hz samples but absent at every 10-Hz selected sample. This is a deterministic sampling counterexample, not evidence that real blinks or pupil waveforms were missed in EVE recordings. For pupil diameter specifically, human temporal bandwidth remains unknown. Source files were inspected through the connected GitHub API; `RESULTS.json` is offline-fixture output, NOT a completed independent remote byte replay.

## PRODUCT
**Reject reuse of EVE's published 10-Hz training loader for Lucent's native-rate temporal certification.** On acquiring EVE, read original `basler.mp4`, `basler.timestamps.txt`, and `basler.h5` at their native 60-Hz frame indices, verify exposure-to-reference timing and `left_p/right_p` validity. Run a reference-blind RGB-only admission rule. A 10-Hz model may remain a nuisance/static baseline, never the rapid ocular measurement ground truth. Do not claim a human pupil waveform result.

## Frozen active kernel
- Exact pair: visible RGB Basler full-frame apparent pupil/iris waveform vs same-eye Tobii `left_p/right_p` in mm with validity and clock verification.
- Frontier: Basler/eye-tracker synchronization documented, EVE access gated; published model loader downsampling now proven at source-code level.
- Scalar observability: participant-held-out lower confidence bound of within-window Pearson correlation, jointly with lag <=67 ms, amplitude ratio 0.75–1.25 and NRMSE <=0.70.
- Strongest confound: optical magnification, brightness-dependent contour bias, gaze geometry, and uncertain reference timestamp/label interpolation.
- Decisive falsification: native-frame, untouched human windows fail frozen gates or do not outperform nuisance-only controls.
- Publishable threshold: >=8 untouched participants, independent replay, device/lighting/glasses holdouts, mechanism-predicted unseen failure boundary and limitations.
- Product threshold: >=75% accurate accepted windows at >=50% reference-blind RGB-only coverage.
- Kill/reformulate: three nondiscriminating experiments, or prospective human failure without useful calibrated admission. No inference from lack of data access.

## Executable evidence
`python3 research/e002-274/audit.py --output /tmp/eve274.json` runs explicit **offline fixture**. `python3 research/e002-274/check.py /tmp/eve274.json` independently checks sampling and three mutations. `python3 research/e002-274/audit.py --online --output /tmp/eve274_verified.json` downloads the three exact author-source files from pinned commit, independently verifies their Git blob SHA-1s and parses real source. No dataset bytes are fetched by the audit. The initial offline fixture and checker passed; online replay requires a networked runner. `RESULTS.json` is an offline result.

## Controlled wildcard (~10% of cheap effort)
`src/datasources/common.py` has a `_face.mp4` timestamp branch that replaces `_eyes.mp4` rather than `_face.mp4`; likely points at video bytes instead of the `.timestamps.txt` sidecar. This is an author-code inspection finding, not a run of the full EVE loader, and does not affect the selected `_eyes.mp4` path. Avoid using normalized face patches as temporal proof without testing.

## Negative gates
EVE data access pending; original RGB bytes, native Tobii samples, reference timing, human waveform correlation, nuisance holdouts, independent external checker, and online source replay all pending. The prior Zenodo 17046553 archive path was attempted twice and blocked; do not retry as active dataset path.
