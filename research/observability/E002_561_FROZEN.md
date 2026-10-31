# E002-561 FROZEN | Timestamp-preserving repeat of E002-560 after Matroska quantization

Frozen 2026-10-31 after discovering the **E002-560 frozen exact-PTS acceptance condition fails** for FFV1/Matroska: FFmpeg's MKV stream timestamps are quantized to 1-ms ticks, producing alternating 4-ms and 5-ms increments at nominal 240 fps. This failure must remain recorded; do not silently reclassify E002-560 as an exact-PTS pass.

## Corrected instrument test
Keep the E002-560 surrogate, all eight acquisition phases, event indices 3/4, lossless FFV1, raw decoded frame comparison and prediction **exactly unchanged**. Change only container from MKV to NUT to preserve a 1/240-second frame timebase. Compare actual FFprobe frame timestamps to i/240 within 0.51 microseconds (FFprobe prints six decimals). Require all nine streams report 240 fps, 240 frames and monotonically increasing PTS. Require the authentic stream to show two closed frames; phase-derived streams must show 8 closed frames for phases 3 and 4 and zero for six other phases.

## Additional falsification and release boundary
Produce an MKV negative-control run from the identical raw frames; record its nonuniform frame-PTS increments and maximum quantization error. Do not treat either NUT PTS or MKV PTS as physical camera acquisition timestamps. Report video-container and decoder measurements only. The product stays `ABSTAIN_UNCALIBRATED` and release `BLOCKED`. No human evidence, no physiology and no optical shutter calibration are asserted.

## Consequence
A high-frame-rate reference file must carry independently authenticated acquisition provenance and no temporal resampling; a high declared frame rate, uniform container PTS or even independently decoded frames cannot alone certify reference-camera closure sensitivity. A sample can be absent from a 30-Hz acquisition and cannot be recovered by re-encoding at 240 fps.