# E002-578 | Frozen authentic LPW development-video blinded-packet execution

Date: 2026-11-01. Primary kernel: E002-371. This is **real human-video instrument execution**, not anatomical human validation or a change to E002-573's frozen participant-held-out design. The E002-573 11/11 split, 19-frame windows, ten-window cap, SHA-256 window ranking, reviewer blindness, and product abstention remain unchanged.

## Question and predeclared success/failure

Can the E002-575 source-bound, native-geometry, two-rater packet generator actually produce **190 complete frames per reviewer** from a source-linked 95-fps LPW human recording, with verified frame identity and private blinded packets, rather than just from a synthetic FFmpeg fixture?

The E002-577 predetermined source `LPW/1/1.avi` (participant 1, video 1) is in the **development** half of the frozen E002-573 participant hash split (development IDs sorted by SHA-256 of `E002-573-LPW-v1|participant_id`). This run must not inspect or access any held-out participant. Do not optimize selection by blink likelihood or image content.

### Frozen protocol

1. Use the E002-577 range-only original-archive reader against https://datasets.d2.mpi-inf.mpg.de/tonsen/LPW.zip; reject full-archive fallback, missing byte-range support, archive integrity failure, altered selected member, or any change from source SHA-256 `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86`. Use the already verified `LPW/1/1.avi`, reported 2,000 frames, 640 x 480, 95/1 fps; reject a mismatch. No source imagery may leave the ephemeral runner.
2. Enumerate all nonoverlapping complete 19-frame windows beginning at frame 0, 19, 38, etc. Rank by ascending SHA-256(`E002-573-window-v1|video_sha256|start_frame`), with numeric start as a tie breaker, and select exactly ten. Do not inspect any frame before selection. Create an owner-only mapping with ten `clip_0000`... IDs and two independent blank reviewer templates. Use the existing E002-575 `build_packet`, not a duplicate decoder.
3. Require a strict native-frame timestamp ordering check, source SHA before/after decode, native PNG dimensions, 190 frames per reviewer, identical source-frame PNG digests between A and B, zero prefilled anatomical labels, and exactly 190 owner-only frame-audit entries. Reject any missing or mismatched frame. Explicitly verify source identities are absent from the rater-facing templates.
4. Emit **aggregate-only** JSON: source SHA, 95/1 reported stream rate, source frame count, windows, frames per reviewer, audit checks, and success/failure. No image bytes, pixel statistics, frame-index mapping, candidate events, eye landmarks, human labels, source packet, or private video as logs/artifacts/caches/commits. Delete temporary video and packets on completion. No GitHub Actions upload-artifact step.
5. Run a local synthetic schema/integrity self-test before remote acquisition; if the source or FFmpeg is unavailable, preserve a bounded explicit failure. Run only on this one development video. Do not repeatedly fetch the archive on every hourly research cycle.

### Prediction

The authentic 2,000-frame development video will yield 105 complete disjoint 19-frame windows and ten selected windows; E002-575 will produce 190 PNG frames in each reviewer packet, all source-bound and blank, without source metadata leakage into reviewer templates. Any failure is an actual human-video instrument falsification requiring repair, not a nuisance to suppress.

### Evidence limits and release gate

A success establishes only a functioning **real-human-source blinded-review instrument**. It does not create human anatomical ratings, certify camera shutter/clock, estimate continuous-time eyelid velocity, establish closure events, or validate E002-371's physical exclusion bound. Physical-camera study E002-567 and two genuinely independent blinded human raters remain mandatory. LPW noncommercial research-only use applies. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
