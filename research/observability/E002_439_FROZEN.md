# E002-439 — frozen optical-clock witness instrument experiment

**Frozen:** 2026-10-25 before implementation and results. **Parent:** E002-371. **Branch:** `research/observability-human-boundary`; draft PR #26. **Evidence tier:** software instrument/encoder-decoder test using synthetic optical images; **not a physical clock, human eyelid experiment, or authenticated sensor exposure measurement**.

## Scientific question and predicted falsification

E002-435 showed that identical video frames can carry different presentation timestamps. Can an **independently authored, in-frame optical timecode** preserve an unmodified frame's *intended* acquisition tick through container retiming and frame loss, while failing closed on corrupt or duplicated codes? This is a candidate **instrument design for prospective human validation**, not a new law of nature.

A virtual external 1-kHz clock emits 16-bit Gray-coded tick values plus CRC-8 (polynomial 0x07, initial 0x00), laid out in 24 data cells, with eight optical black/white reference cells. The ticks are authored before encoding and **must not be reconstructed from FPS or container PTS**. Synthetic images are then encoded with FFV1 in Matroska and independently decoded using FFmpeg. Decode only if optical reference contrast, CRC and strict monotonicity pass.

## Preregistered outcomes

1. A 12-frame source with nonuniform ticks `[0,33,67,100,200,233,267,300,400,433,467,500]` at a stipulated 1-kHz virtual tick rate yields optical gaps including 100 ms. A naive 30-fps reconstruction misses that gap.
2. Remux/re-encode with video PTS doubled. Decoded image SHA-256 and optical ticks remain identical, while container PTS change. The optical clock **conditionally** recovers authored relative time independent of container PTS.
3. Deleting a frame preserves the gap between remaining optical ticks; duplication or reordering triggers nonmonotonic/repeated-tick rejection.
4. A single altered data cell triggers CRC rejection; insufficient reference contrast or saturation triggers abstention. All decisions include evidence tier and `ABSTAIN_UNCALIBRATED` for physical hidden-closure, blink duration, PERCLOS, fatigue.
5. Use an independent decoder/oracle that does not import the production decode function. Commit scripts, deterministic aggregate and CI. Preserve negative results.

## Hard limitations / prospective physical test

The tick emitter here is **virtual** and shares the host computer's generated schedule. It cannot establish that a physical LED panel was driven by an independent oscillator, that a camera sampled it during the exposure, that rolling-shutter rows saw the same tick, or that the optical code could not be forged/replayed. For real validation require hardware oscillator trace and photodiode, calibrated LED switching latency, exposure integration and rolling-shutter row characterization, robust optical decode under brightness/blur/glare/glasses, synchronized high-rate physical aperture reference and independent human ratings. A one-time in-frame counter alone is **not cryptographic authentication**. Any ambiguity is `ABSTAIN_UNCALIBRATED`.

This experiment must not be described as empirical human validation or a novel theorem. If it fails, retain failure traces and do not weaken the frozen criteria.
