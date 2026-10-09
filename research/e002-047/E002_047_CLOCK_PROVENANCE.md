# Lucent E002-047: EOTT clock provenance audit (2026-10-09)

**Classification:** DISCRIMINATION / CAPABILITY-BUILDING. **No physiological result.**

## Code-derived provenance chain

The official EOTT extractor constructs frame epochs from **browser recording-start event epoch + WebM presentation timestamp (PTS)**, then selects the nearest Tobii sample by that derived epoch.

- `participant.py`: browser recording-start `epoch` is saved as the video start time.
- `webgazerExtractServer.py`: frame PTS comes from ffmpeg `showinfo`; missing values are reconstructed using nominal frame rate.
- `videoProcessing.py`: frame epoch is computed from recording start plus PTS.
- `webgazerExtractServer.py`: derived frame epoch is used to select a Tobii record.

The extractor does **not** independently validate per-frame camera exposure epochs. Its exported frame-epoch/nearest-Tobii CSV cannot independently confirm its own synchronization assumption.

Source code: https://github.com/brownhci/WebGazer/tree/master/www/data/src . The authors already document incorrect WebM frame timestamps; this is not claimed as novel.

## Synthetic counterexample

Five-second, 30-fps, noiseless identical sine waves evaluated with hypothetical clock offsets:

| Hz | offset | waveform r |
|---|---:|---:|
| 0.5 | 0.10 s | 0.9495 |
| 0.5 | 0.50 s | -0.0017 |
| 1.0 | 0.10 s | 0.8090 |
| 1.0 | 0.50 s | -1.0000 |
| 1.0 | 1.00 s | +1.0000 |
| 2.0 | 0.10 s | 0.3090 |

Perfect correlation can coexist with a one-period clock error. These are synthetic phase counterexamples, not measured EOTT errors.

## Evidence state

**KNOWN:** The official epoch is derived rather than independently exposure-measured. Previously analyzed E002-046 P_33 clips contained 192/1,749 duplicate WebM PTS. **BELIEVED:** EOTT may be unsuitable for strict rapid-waveform scoring without another exposure anchor. **CONFLICTING:** Dense tracker data but unreliable RGB timing. **FALSIFIED:** Official extracted epoch is independently camera-verified; correlation alone validates absolute alignment. **ANOMALOUS:** Prior clip-specific duplicate rates vary widely. **UNTESTED:** True acquisition offset, RGB pupil waveform fidelity, active response, sleepiness/fatigue inference.

The observed E002-046 browser-event-minus-video-duration difference of 0.477–0.551 seconds is **not** an estimated camera-to-tracker offset. Do not set an alignment correction using that number or optimize it against reference pupil dynamics.

**Next discriminator:** Audit original acquisition collector for hardware/frame exposure timestamps; otherwise prioritize RGBE-Gaze's documented FLIR hardware timestamps, subject to independent cross-device synchronization checks.

E002-044 frozen protocol unchanged (SHA256 `ab0e70a109a7ee6646fb7cda594c939a8f1184e0cbc401aea7e0dcdb9d537e6e`). Previous PupilSense scale-observability negative result preserved. No human RGB waveform scored, no physiological breakthrough or five-second state validity established. Cloud-only, zero spend.
