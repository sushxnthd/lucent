# E002-492 | First authentic human-content result and blinded anatomical review handoff

**2026-10-28. E002-371 primary kernel. Evidence tier: authentic S01 image-content measurement + locally tested human-review tooling; no anatomical labels and no physical shutter calibration.**

## Verified E002-491 outcome (not a blink detection result)

[Hosted run 40563647913](https://github.com/sushxnthd/lucent/actions/runs/40563647913) **completed successfully** on 2026-10-27, with checksum-verified S01 human video, 10 frozen synthetic nuisance tests, actual FFmpeg frame decoding, and a 661-byte aggregate-only artifact [12765309314](https://github.com/sushxnthd/lucent/actions/runs/40563647913/artifacts/12765309314).

Prespecified image-content screen on the first 12,000 native frames:
- 11,999 consecutive frame pairs analyzed; 0 exact duplicate pairs.
- 1,427 pairs photometric/contrast-confounded (**11.89%** of all pairs), below the frozen >20% instability threshold.
- 10,572 eligible pairs; **1 localized-motion candidate** (**0.00946%** of eligible pairs), at native frame index **5356**.
- Eligible center mean-absolute-difference quantiles (median / p90 / p99): **0.0063225 / 0.0155633 / 0.0201618** (normalized by 255).
- Eligible border quantiles: **0.0104199 / 0.0246399 / 0.0314919**.

The single candidate meets the *precommitted image-motion* screen, not an anatomical blink criterion. It is unknown whether the candidate is a blink, gaze movement, occlusion, lighting artifact or something else. **Zero** anatomical closure labels, authenticated frame intervals, calibrated eyelid velocities or physical shutter acquisitions were obtained. This screen's extremely low candidate yield **does not establish sensitivity**; it should not be used as a blink event detector. Do not retune its thresholds post hoc.

The apparent AVI 1-fps rate, paper 150-fps rate and rehost ~500-fps description are **not independent hardware-clock measurements**. No time-axis or physical E002-371 exclusion may be inferred.

## New E002-492 human-evidence bridge

[Frozen protocol](E002_492_FROZEN.md) was committed first at `2ca1de11`, after inspecting the above aggregate but before any anatomy labels. Implemented a **private, local-only blinded review packet**:
- 20 clips of 13 consecutive native frames: the single prespecified motion candidate centered at 5356, plus 19 SHA256-selected controls, deterministically shuffled and concealed from raters.
- 260 native frame review positions. Two independent raters provide upper/lower eyelid coordinates, iris-diameter reference, landmark uncertainty and nuisance flags. Raw frames, crops and per-frame anatomy never enter GitHub.
- An executable interval adjudicator refuses missing/invalid landmarks, flagged gaze/glasses/blur/lighting/occlusion/geometry, and nonoverlapping rater uncertainty intervals. It never averages away disagreement.
- Disagreement >20% among dual-measurable positions is a precommitted falsifier of this annotation method. A motion candidate that cannot be anatomically interpreted is **not** promoted to a closure event.
- This tool reports agreement intervals only, **not** certified physical uncertainty or ground truth. No frame-index-to-seconds conversion.

[Executable local-only packet and adjudicator](e002_492_anatomical_review.py) · [13 adversarial tests](test_e002_492_anatomical_review.py) · [Hosted CI workflow](../../.github/workflows/e002_492_anatomical_review.yml).

Local Python 3.11 tests: **13/13 passed**; a no-label dry run produced 20 clips, 260 unreviewed positions, zero measurable intervals, and fail-closed product/release status. Actual S01 packet frame extraction and independent human ratings **were not executed** in this environment; the S01 ZIP remains available only to the hosted acquisition workflow. Hosted E002-492 CI was not yet verified when this report was committed.

## Reproduction and next decisive experiment

On an authorized local machine with FFmpeg and the published checksum-matching S01.zip:

```bash
python research/observability/e002_492_anatomical_review.py packet --archive S01.zip --outdir private_s01_review
# Keep OWNER_ONLY_MAPPING.json private; two independent raters complete separate templates.
python research/observability/e002_492_anatomical_review.py adjudicate \
  --manifest private_s01_review/OWNER_ONLY_MAPPING.json \
  --rater-a private_s01_review/RATER_A_TEMPLATE.json \
  --rater-b private_s01_review/RATER_B_TEMPLATE.json \
  --aggregate private_s01_review/aggregate.json
```

The next empirical milestone is **two genuinely independent anatomical ratings** of this frozen packet and independent acquisition-time provenance. Until both exist, do not claim that E002-371's physical shutter-gap/velocity bound has been validated, and do not touch held-out S21-S31 anatomy.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. **Physical shutter acquisitions:** 0. **Human anatomical labels:** 0. **No merge, deployment or new product claim.**
