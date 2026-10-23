# E002-388 — encoded-video phantom falsifies static aperture transfer under nuisance

**Evidence tier:** controlled software-instrument validation, not physical camera, human evidence, or a new physiological law. **Protocol frozen before execution:** E002_388_FROZEN.md at commit 1d4e7fa.

## Methods
Generated 240 separate 60-frame, 96×64 RGB eye-phantom videos: 20 shutter-onset phases × three event types (50-ms full-closure plateau; 8-ms plateau; always-open) × two H.264 compression settings (CRF 18/40) × clean/adverse optical conditions. Exposure-integrated each source frame at 30 fps with 10-ms shutter and ten sub-exposure samples, encoded with actual FFmpeg libx264, decoded with OpenCV, and estimated aperture from a two-point static phantom calibration. Adverse condition combines +18% brightness gain, fixed high-intensity glasses-like reflection, 17-pixel horizontal and 8-pixel vertical eye displacement, and Gaussian blur. These are intentionally constructed severe disturbances, not empirical camera nuisance distributions.

## Frozen predictions and outcomes
All four preregistered predictions passed.

| Event / condition | Source guaranteed 10-ms full exposure | Encoded detection CRF18 | Encoded detection CRF40 |
|---|---:|---:|---:|
| 50-ms plateau, clean | 20/20 | 20/20 | 20/20 |
| 8-ms plateau, clean | 0/20 | 3/20 | 3/20 |
| No closure, clean | n/a | 0/20 | 0/20 |
| 50-ms plateau, adverse | 20/20 | 20/20 | 20/20 |
| 8-ms plateau, adverse | 0/20 | 20/20 | 20/20 |
| No closure, adverse | n/a | **20/20 false positives** | **20/20 false positives** |

For the 8-ms plateau, only 6/20 phases have >=4-ms source overlap, but only 3/20 are detected after optical rendering and H.264. This discrepancy shows that temporal overlap alone does not imply optical observability.

Maximum absolute aperture-proxy error was 0.0265 (CRF18 clean) / 0.0311 (CRF40 clean), but reached 0.9391 / 0.9498 under the adverse condition. A clean static calibration is not a deterministic optical bound across unseen geometry/photometry/glare.

The source-interval calculation and MP4 metadata were independently checked in **726 checks across all 240 videos**. This is not independent human or physical-camera replication.

## What the result changes
The reference-camera exposure-erasure counterexample in E002-387 concerned extremely brief excursions. E002-388 establishes a different, more directly product-relevant failure: even when a sustained 50-ms closure necessarily occupies a full ordinary-camera exposure, encoded RGB can be non-diagnostic if the optical transfer changes. Conversely, severe glare and brightness/geometry shift can make a truly open eye look closed on every phase.

Therefore E002-371's aperture endpoint values must **not** be inferred from encoded RGB using a clean two-point calibration. H.264 bitstream integrity or FPS does not validate physiological aperture. The product must require qualified intermediate-aperture calibration and nuisance bounds or return ABSTAIN. Detection under the clean phantom is not a clinical blink, PERCLOS or fatigue validation.

## Limitations and priority
This is a deliberately simple synthetic rectangular eye patch with one combined adverse condition, not a human face, calibrated optical bench, physical camera, or population test. Compression CRF is not equivalent to device bitrate. A 50-ms plateau is illustrative; Kwon et al. (2013) reported a 58±4-ms mean closed phase for *voluntary* human blinks, not a universal minimum. Existing image formation, shutter aliasing and selective-prediction literature establishes the underlying principles; publication-level novelty is **not** demonstrated.

## Reproduction
```bash
python -m pip install numpy opencv-python-headless
# ffmpeg and ffprobe must be installed
python research/observability/e002_388_codec_instrument.py --output /tmp/e002_388_out
python research/observability/e002_388_independent_check.py /tmp/e002_388_out
```
See E002_388_HUMAN_PROTOCOL.md for a physical-camera phantom and synchronized human protocol. Preserve the entire result including negative findings; do not promote this result into a product claim.
