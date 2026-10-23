# E002-398 — two-participant blinded human aperture annotation instrument completed

**Date:** 2026-10-23. **Evidence tier:** human video, checksum-verified source and independently verified annotation-packet generation; **zero actual eyelid landmark annotations** and **zero physically calibrated shutter-gap certificates**. E002-371 human observability remains unvalidated.

## Prospective execution and independent checks
- Frozen selection/annotation protocol committed `7028ed2` before running the new instrument. Public-seed blinding flaw was identified and prospectively corrected in `E002_398_PREEXECUTION_BLINDING_CORRECTION.md` before any E002-398 video analysis. HMAC IDs use a secret generated locally, not a public deterministic seed.
- Generator `research/observability/e002_398_blinded_annotation.py`, independent checker `e002_398_independent_check.py`, CI workflow `.github/workflows/e002_398_human.yml`.
- [Hosted GitHub Actions run 39981621645](https://github.com/sushxnthd/lucent/actions/runs/39981621645): **both S01 and S19 completed successfully**, with separate independent image hash, geometry, 40-clip/280-frame and public-label-leakage checks.
- S01 source MD5 `fef02cb7ebf62e4f3efb6303284fd6cb`; S19 `8a16cf12526f7558b4e49926c4bc5e8e`, from the previously verified public Eye-BCI recordings. These participants were previously used in E002-395–397 and **are not untouched holdouts**.

## Observed descriptive image-quality distributions

| Source | Eligible EEG/control pairs | Selected pairs | Blinded clips | PNG frames | Laplacian variance p10 / median / p90 | Grayscale p95-p05 contrast p10 / median / p90 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| S01 | 86 | 20 | 40 | 280 | 18.55 / 55.80 / 110.02 | 64 / **73** / 84 |
| S19 | 36 | 20 | 40 | 280 | 21.45 / 54.74 / 111.51 | 31 / **35** / 42.14 |
| **Total** | 122 | 40 | **80** | **560** | — | — |

Median grayscale contrast differed by a factor of about **2.09** across these selected crops. This is a descriptive cross-recording optical difference, not a statistical estimate of nuisance prevalence, human eyelid kinematics or rater performance. Neither image-quality statistic establishes that a margin can be annotated correctly.

All 560 crops passed independent decoding, size (190×130 pixels), content SHA256 and seven-frame continuity checks. The 80 clip identifiers are HMAC-blinded and their event/control linkage was kept out of public outputs. The private linkage and cropped human frames existed only in ephemeral CI working directories and were not uploaded. CI artifacts contain **only** label-free manifests, blank annotation sheets and descriptive summaries:
- S01 manifest artifact `12513623261`.
- S19 manifest artifact `12513952277`.

## Scientific interpretation and limitations
This is a concrete, reproducible **human-validation handoff** replacing another EEG-proxy AUC optimization cycle. It enables independent upper/lower eyelid landmark annotation on fixed human frames without disclosing EEG marker status. The human-video source has no independently calibrated shutter exposure or pixel-to-physical-aperture mapping. The two raters have **not** annotated the 560 frames. No measured physiological maximum eyelid speed, independent timing bound, real ordinary-camera paired stream, adjudicated reference labels, or new untouched participants/devices were obtained. A high-speed negative frame remains potentially unresolved due to exposure erasure and between-frame events.

**Do not interpret a successful computational pipeline as validation of the shutter-gap theorem.** The next required step is two blinded rater sheets, adjudication, independent physical exposure/time/geometry/velocity calibration and prospective E002-371 predictions on untouched participants/devices. The rater protocol is `E002_398_RATER_INSTRUCTIONS.md`.

## Product and paper decision
The optical-flow and dark-pixel proxies remain rejected for general physical-aperture claims. Keep `ABSTAIN_UNCALIBRATED` for hidden-closure exclusion, blink duration, PERCLOS and fatigue diagnosis. This result can support a reproducible methods/validation section, but is **not** a world-class measurement-science result or publication-level novelty by itself.
