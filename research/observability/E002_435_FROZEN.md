# E002-435 — frozen bitstream-identical media-clock intervention

**Date:** 2026-10-25. **Parent kernel:** E002-371. **Evidence tier:** FFmpeg/FFprobe stream-copy instrument test using synthetic image frames; not physical shutter, camera, or human validation.

## Question

Can two media files with **identical encoded video packets and decoded image sequence** carry incompatible frame presentation times solely through stream-copy container retiming? If so, neither an exact image match nor a plausible container PTS trace authenticates the physical acquisition clock.

## Predictions frozen before implementation

1. Encode exactly 13 distinguishable generated frames at 25 Hz with lossless FFV1 in Matroska; record the base frame-level PTS, compressed packet SHA-256 sequence and decoded raw frame SHA-256 sequence.
2. Make a **stream-copy** retimed file with FFmpeg input option `-itsscale 2` and a second stream-copy file with `-itsoffset 0.8`, without re-encoding. A stream-copy identity control without retiming is required.
3. All four files must have exactly the same ordered **compressed packet SHA-256** sequence and decoded-frame SHA-256 sequence. Fail the experiment if this is not true. Do not compare container-file hashes because container headers/timestamps differ by design.
4. For the scaled file, every inter-frame presentation interval must be twice the baseline within 1 ms; the last-frame absolute time shift must exceed 0.40 s. For the offset file, every frame PTS must shift by +0.80 s within 1 ms; its inter-frame intervals must match baseline within 1 ms. The identity control must match baseline PTS within 1 ms.
5. Every file must remain parseable by Lucent's existing E002-434 PTS instrument and must **not** authorize sensor timestamps or a physical closure certificate. Reject missing/nonmonotone frame times and packet/frame-count mismatches. Preserve exact command lines, versions, machine-readable results, and independent test assertions.

## Decision and interpretation

If stream-copy retiming changes packets or pixels, **report a failed identity control**, do not reinterpret the files as a valid witness. If the codec/container refuses retiming, record that negative result without changing the frozen thresholds. The experiment tests media provenance non-identifiability only: it cannot prove a particular real camera had wrong timestamps, establish physical eyelid velocity, or provide human closure reference labels.

**Product consequence:** encoded PTS is useful for quality diagnostics but cannot serve as authenticated sensor exposure-start/end timing even if pixel hashes match. Physical hidden-closure, blink duration, PERCLOS and fatigue remain `ABSTAIN_UNCALIBRATED`. The outstanding decisive experiment remains the independent, blinded, participant-disjoint physical study in E002-433.
