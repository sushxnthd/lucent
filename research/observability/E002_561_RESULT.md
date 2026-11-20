# E002-560/561 RESULT | 240-fps video metadata can hide 30-fps acquisition

Date: 2026-10-31. Primary kernel E002-371. Preregistration: [E002-560](E002_560_FROZEN.md) then [E002-561](E002_561_FROZEN.md). Evidence tier: **synthetic aperture frames processed by real FFmpeg FFV1 encoders/decoders and FFprobe**. No human physiology or physical shutter measurement.

## First frozen test failed, and that failure is preserved

E002-560 predicted FFV1/Matroska would preserve exact 1/240-second frame PTS. It did **not**. On the local FFmpeg/FFprobe instrument, every MKV stream declared 240 fps and contained 240 decoded frames, but timestamps were quantized to a 1-ms container timebase. Consecutive steps alternated between 4 and 5 ms, with a maximum discrepancy of **500 microseconds** relative to i/240 s. Therefore E002-560's exact-PTS acceptance condition is **FALSIFIED**. This is an instrumentation finding, not an eyelid theorem.

The separately frozen E002-561 correction changed **only the container** to NUT. NUT retained a 1/240-second timebase; FFprobe's six-decimal printed timestamps deviated from i/240 by at most **0.3333 microseconds**. The original raw frames, all eight phases and the predicted event were unchanged. E002-561 passed locally.

## Encoded/decoded phase experiment

A one-second 240-Hz **synthetic moving-aperture surrogate** contains two closed-state frames at indices 3 and 4. Eight 30-Hz acquisitions take every eighth high-rate sample with phase 0..7; each acquired frame is repeated eight times and losslessly encoded as nominal 240 fps. All nine files in each container report 240 fps, 240 frames, monotone PTS and exact lossless decoded pixels. These are generated frames, not camera images.

| Decoded stream | Closed-state frames | Distinct decoded images |
|---|---:|---:|
| Native synthetic 240-Hz source | 2 | 2 |
| Phase 0, 1, 2, 5, 6 or 7 (30->240) | 0 | 1 |
| Phase 3 or 4 (30->240) | 8 | 2 |

**6/8 phase offsets entirely miss the constructed event**, despite reporting 240 fps, 240 decoded frames and (in NUT) nearly exact uniform PTS. This is a phase-enumeration result for the frozen synthetic 2-frame event, **not a human blink miss rate**. The 8 closed frames in the other two files are duplicated evidence of one 30-Hz sample, not eight independent observations. The native synthetic stream has 237 identical-adjacent frame pairs; stationary frames themselves are not proof of a low sensor rate.

## Scientific falsification and direct enforcement consequence

**Killed shortcut:** accepting a high-frame-rate reference solely because the encoded file reports high nominal fps, regular PTS, or successfully decodes. An unverified 30-Hz source can be upsampled to apparently 240 Hz while losing a brief closure. Container PTS are presentation times, not authenticated acquisition/exposure times.

**Reference gate:** A held-out human video can be used as positive anatomical evidence only with independently authenticated original capture, per-frame acquisition timing (including missing/duplicated frames), shutter/exposure response, anatomical calibration and two blinded raters. Duplicate-frame heuristics may trigger review but cannot authenticate or disprove sensor timing. An ordinary-camera hidden-closure **exclusion** still requires independently justified continuous-time kinematic bounds, clock/geometry/blur/illumination/gaze/glasses/missingness controls, and frozen predictions. If any certificate is missing, abstain. Negative high-rate frames alone cannot certify no closure between exposures.

## Reproduction and human study handoff

Run `python research/observability/e002_561_media_provenance.py --output aggregate.json` with FFmpeg and FFprobe installed. The script creates all 18 lossless synthetic videos in a temporary directory, independently probes PTS and decodes raw bytes, compares exact SHA-256 of decoded pixels with generated source, checks the eight-phase predictions and removes videos. Run `cd research/observability && python -m unittest -v test_e002_561_media_provenance.py`. **Six local adversarial tests passed**, including invalid phase, corrupt video and truncated frame count. Hosted CI is committed at [e002_561_media_provenance.yml](../../.github/workflows/e002_561_media_provenance.yml); its outcome must be checked separately.

For physical human validation: collect consented native high-speed eye video and simultaneous ordinary-camera footage, with a hardware LED/photodiode sync signal, original unmodified sensor timestamps, independently recorded shutter/exposure configuration and an explicit frame-drop/transcoding log. Use participant-disjoint precommitted splits and independent A/B blinded anatomical raters, as in [E002-550](E002_550_FROZEN.md) and [E002-555](E002_555_FROZEN.md). Freeze predicted excluded/abstained 30-Hz gaps before inspecting held-out high-rate references. Stratify by gaze, geometry, illumination, blur, glasses, occlusion, missingness and clock error. If acquisition authenticity, independent hard velocity/acceleration bounds, or anatomical transfer cannot be established, **do not issue closure-negative certificates**; report coverage/abstention and any witnessed counterexamples. This instrument experiment does not replace human capture.

## Literature/dataset access boundary

The 2019 240-fps smartphone study (PMID [30893187](https://pubmed.ncbi.nlm.nih.gov/30893187/)) and Kwon et al.'s 2013 600-fps voluntary-blink study ([DOI 10.1098/rsif.2013.0227](https://doi.org/10.1098/rsif.2013.0227)) provide published physiological context, not an authenticated downloadable held-out video. The 2026 400-fps FaceBase eyelid dataset ([DOI 10.25550/88-28BJ](https://doi.org/10.25550/88-28BJ)) is restricted access. The public [MPEblink Zenodo release](https://zenodo.org/records/7754768) does not by itself establish the independently authenticated high-rate exposure/timestamp reference required here. No such participant-disjoint human reference was accessed in this run.

**Honest evidence counters:** authenticated physical shutter captures 0; independently blinded human anatomical rater pairs 0; certified continuous-time physiological motion ceilings 0; held-out physical predictions 0. Product `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. No clinical fatigue or blink-negative claim.
