# E002-434 — frozen encoded-frame timing experiment

Date: 2026-10-25. Parent: E002-371. Evidence tier: **instrument/codec validation with generated video**, not a human or camera measurement. This experiment responds to E002-432's missingness alias with a real media-container test, rather than another idealized eyelid trajectory.

## Question and hypothesis

Can an ordinary encoded video have frame presentation times that diverge materially from the common shortcut `frame_index / reported_fps`, and can a reproducible instrument preserve the observed container timestamps without misrepresenting them as sensor exposure times?

**Frozen primary prediction:** In a deliberately variable-frame-rate (VFR) FFV1/Matroska video containing at least one injected 100-ms or longer presentation gap, the naive `frame_index / fps` reconstruction will differ from the actual encoded frame presentation timestamps by **more than 50 ms** at one or more frames. The new reader must preserve ordered PTS, identify long gaps and return `ABSTAIN_UNCALIBRATED` for physical shutter/eyelid claims. A constant-frame-rate (CFR) control will have much smaller reconstruction error. Do not change thresholds after observing outcomes.

## Frozen protocol

1. Generate 12 tiny synthetic PPM frames with distinct frame identifiers; encode using FFmpeg's concat demuxer, explicit per-frame durations and FFV1/Matroska with VFR preservation. Set nominal short intervals to 0.04 s and inject a 0.20-s interval and a 0.12-s interval. Include a separate CFR control with all intervals 0.04 s. The generator must preserve a local authored-time manifest and the exact FFmpeg/FFprobe command lines.
2. Extract frame-level `best_effort_timestamp_time` with FFprobe JSON `-show_frames`, not a guessed FPS or a packet-order index. Read stream-reported average/nominal frame rate for the naive baseline, explicitly labeling it metadata, not sensor timing.
3. Precommitted outcomes: all decoded frames have finite, strictly increasing PTS; max absolute naive reconstruction error for VFR exceeds 0.05 s; maximum gap is at least 0.10 s; CFR reconstruction error is at most 0.01 s after choosing its observed nominal rate. Encoded PTS agree with authored cumulative durations within 0.015 s (container timebase/rounding allowance). The instrument reports both PTS gaps and maximum naive timing error.
4. Adversarial unit tests inject duplicate, reversed, missing, NaN and nonnumeric PTS, invalid FPS and empty frames; these must fail closed. An incomplete/unauthenticated sensor manifest must not be upgraded to a physical capture certification.
5. The product consequence is a strict separation between **container presentation timestamps** and **hardware exposure-start/end timestamps**. Even perfect PTS agreement with authored media does not establish original sensor timestamps, shutter kernels, eyelid geometry, velocity bounds or reference truth. `ABSTAIN_UNCALIBRATED` remains mandatory.

## Decision rules

If FFmpeg cannot encode the intended VFR schedule or the source is non-decodable, preserve the failure and investigate the codec/timebase before scientific interpretation. A real negative finding (e.g. this codec normalizes timestamps) must be reported rather than modifying the preregistered gap criteria. No fabricated human subjects, physiological speed limits, or real-camera measurement claims. Preserve generated media locally; commit code, protocol, tests, commands and aggregate results only.
