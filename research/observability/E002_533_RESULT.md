# E002-533 RESULT | A real video codec does not rescue uncalibrated photometry

2026-10-30. Primary E002-371 kernel, established branch `research/observability-human-boundary`, draft PR #26. Frozen protocol committed first at `f8523e804033bf0115811ef9e6f48183b4c462f7`. This is **an encoded synthetic optical scene processed through real FFV1/H.264 codecs and actual OpenCV/ffmpeg decoding**, not physical shutter calibration, human validation, or a new theorem.

## Empirical software/instrument result

Generated twenty 96x96 synthetic optical frames with three vertically separated LED-duty-fraction patches and dark/bright references. Actual ffmpeg encoding, file I/O and decoding were exercised. E002-532's fixed 36-candidate exposure/clock/row-delay model was then fitted to the **decoded pixel intensities**, not the ideal synthetic intensities. Training and held-out frames remained frozen (10 each). No parameter tuning on held-out data.

| Preregistered condition | Training-feasible models | Held-out max normalized residual | Result |
| --- | ---: | ---: | --- |
| FFV1 lossless, linear photometry | 1/36 | 0.001961 | Unique grid candidate, **not** physical calibration |
| H.264 CRF 23, linear photometry | 1/36 | 0.009395 | Unique grid candidate, **not** physical calibration |
| H.264, unknown gamma 2.2 | 0/36 | Not evaluated | **MODEL_FALSIFIED** |
| H.264, separately specified inverse gamma | 1/36 | 0.015146 | Recovers frozen grid candidate |
| H.264, held-out ROI glare | 1/36 | 1.000000 | **FALSIFIED_HELDOUT**; training candidate unchanged |
| H.264, one missing held-out native ROI | 1/36 | 0.009395 over valid rows | 29/30 held-out rows; one **censored**, not imputed |

All four non-falsified conditions recover the *frozen discrete-grid* synthetic truth (offset 1 ms, exposure 2 ms, row delay 0.5 ms per ROI unit). The preregistered predictions were met in this environment. The uncorrected gamma condition deviated by up to 0.287255 in normalized brightness. This is a **direct failure of the linear-photometry assumption** under a camera-like response curve, not an eyelid or human finding. H.264 compression alone was tolerated in this one simple high-contrast synthetic scene; this does not establish robustness across cameras, codecs, auto-exposure, clipping or real motion.

The same files were decoded through OpenCV VideoCapture and a separate ffmpeg CLI raw-RGB path. Extracted ROI values agreed exactly in this environment (max difference 0). **Independence limitation:** OpenCV's decoder may use the same FFmpeg/libavcodec implementation, so this is independent extraction entry points, *not* independent codec implementations or independent physical verification.

## Verification and reproduction

- Local environment: FFmpeg 7.1.5, OpenCV 4.13.0, NumPy 2.3.5; 8/8 adversarial Python tests passed.
- [Executable](e002_533_codec_falsifier.py), [tests](test_e002_533_codec_falsifier.py), [frozen protocol](E002_533_FROZEN.md) and [dedicated workflow](../../.github/workflows/e002_533_codec_falsifier.yml).
- Reproduce: `python -m unittest -v test_e002_533_codec_falsifier.py` from `research/observability`; `python research/observability/e002_533_codec_falsifier.py --output e002_533_local.json` from repository root. Requires ffmpeg with libx264/FFV1 and Python NumPy/OpenCV.
- No subject video is generated or committed. Generated encoded files are ephemeral unless `--retain-videos` is explicitly used. The workflow uploads a reproducible JSON aggregate, not human material.
- Hosted GitHub Actions was running when this report was committed; hosted success is **not** claimed here. File hashes depend on encoder builds and are reported in the generated JSON, not used as cross-platform equality certificates.

## Scientific and product consequence

The same synthetic optical pulse schedule can support a unique, apparently precise shutter fit under a calibrated linear response and **no fit at all** under a nonlinear but plausible camera response. Therefore an E002-532 optical calibration must **reject** raw camera pixel duty fractions unless an independent response/linearity calibration is supplied. The gamma correction in this experiment was specified from the synthetic renderer, not estimated or authenticated on a camera. This cannot be promoted to a real calibration.

This is an application-specific real-codec falsification of an instrument assumption, not a novel gamma/rolling-shutter result. Existing optical calibration prior art remains acknowledged in E002-532. There is **no evidence** that real hardware follows the synthetic response or that actual anatomical closure is observed. No new independent human ratings, photodiode-timed captures, participant-disjoint physical predictions or continuous-time physiological velocity ceilings were obtained.

**Decision:** Lucent `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. No deterministic hidden-closure exclusions, fatigue scores, PERCLOS accuracy or medical claims are authorized. Next meaningful work requires physical LED/photodiode capture and blinded S01 anatomical ratings; no further synthetic codec sweeps without new physical evidence.

Hush branch and PR #45 untouched. No merge, force-push or deployment.
