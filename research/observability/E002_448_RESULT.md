# E002-448 — a blinded human anatomical-reference collection instrument

**2026-10-26. Evidence tier: REPRODUCIBLE ANNOTATION INSTRUMENT + SYNTHETIC ADVERSARIAL TESTS; ZERO NEW HUMAN LANDMARK LABELS.** [Frozen protocol](E002_448_FROZEN.md) was committed at `2957e1ea` before the instrument was implemented. The later pre-implementation hardening `1c448f53` replaced publicly reversible deterministic view hashes with per-pack private-key HMAC IDs. [Code](e002_448_blind_annotation.py) · [Offline rater interface](e002_448_rater.html) · [Independent tests](test_e002_448_blind_annotation.py) · [Hosted human-pack readiness workflow](../../.github/workflows/e002_448_blind_annotation.yml).

## Why this is the next decisive scientific step

E002-446 showed that a fixed image-edge proxy recovered **0/3,000** usable anatomical candidates from S19. The previous optical associations cannot certify anatomy. E002-448 therefore **stops automatic proxy tuning** and creates a reproducible path to independent *human* anatomical margin annotations. This is a research-enabling artifact, not an empirical closure law or another theorem refinement.

## Frozen S19 pilot protocol implemented

Use only the previously checksum-verified S19 AVI and candidate sync event list. Within the first 12,000 frames, select up to 24 10–100-ms *candidate* event gaps, match the same number of <=10-ms control intervals by a fixed SHA256 ranking, and take three frames around each interval. Add 12 hidden repeat views to measure intra-rater consistency. Each pack gets a fresh private HMAC key. Raters see individually shuffled 320×288 grayscale frames and opaque IDs, **not** candidate event times, gap categories, sequence order, participant holdout frames, or index mappings. The private index mapping stays outside the rater pack. Public Actions may emit **only a nonidentifying aggregate**, never human images or the private master.

The offline HTML interface asks two independent raters to mark left/right canthi and upper/lower anatomical eyelid margins or explicitly abstain for ambiguous anatomy, occlusion/glasses, illumination, blur, gaze, or other nuisances. The adjudicator computes a **dimensionless 2-D image-space aperture** using the perpendicular separation of upper/lower marks divided by canthal length. This does **not** estimate mm, physical shutter time, or true anatomical depth. An observation is eligible only when both raters mark valid anatomy, the canthal geometry passes, between-rater discrepancy is <=0.03, and all hidden repeat views agree within <=0.03. Missing labels, inconsistent repeats, or nuisance flags yield **ABSTAIN_REFERENCE_UNRESOLVED**. Neither unresolved frames nor unresolved pairs count as witnessed open intervals.

## Verification and honest negative control

Fifteen independent synthetic/adversarial test cases passed **locally** before publication. They cover deterministic control selection, private-key HMAC blinding, nonmonotone/nonfinite candidate events, absent positive stratum, actual PNG encoding, offline manifest secrecy, normalized aperture geometry, two-rater consensus, missing raters, duplicate/unknown IDs, nuisance abstention, and hidden-repeat disagreement. Synthetic rater coordinates are fixtures, **not real human annotations**.

The dedicated hosted workflow checks the real S19 archive hash, attempts to construct the private pack, runs the same 15 tests, computes a no-label abstention result, removes images/master from the ephemeral runner, and uploads only counts. **Do not claim successful S19 pack generation until hosted execution completes.** Its successful execution would still establish only data-collection readiness, not new anatomical evidence. If the job fails, preserve the failure and repair before further scientific inference.

## Offline human study handoff

With authorized local access to the published S19 archive, run:

```bash
python -m pip install numpy==2.2.6
python research/observability/e002_448_blind_annotation.py prepare --zip /private/S19.zip --output-root /private/e002448_s19 --summary /private/e002448_readiness.json
```

Give **only** `/private/e002448_s19/rater_pack` to each of two independent blinded annotators. Open `rater.html` in a browser, select the pack folder, mark all views, and export separate JSON files. Do not share `PRIVATE_MASTER_DO_NOT_SHARE.json` with raters. After independent completion:

```bash
python research/observability/e002_448_blind_annotation.py score --master /private/e002448_s19/PRIVATE_MASTER_DO_NOT_SHARE.json --rater1 /private/raterA.json --rater2 /private/raterB.json --summary /private/e002448_consensus.json
```

Only deidentified, participant-level aggregate counts and calibration-eligible statistics should be published. Obtain the appropriate human-subjects/privacy approvals for the annotation workflow and keep raw eye imagery in controlled storage. S21/S22 remain untouched until a separately frozen, genuinely prospective prediction instrument exists.

## What this does *not* validate

Even two perfectly agreeing raters on S19 would not authenticate the physical exposure schedule (the AVI nominal 1-fps metadata and 7-ms candidate events already disagree with a claimed ~500-fps acquisition), independently calibrate mm per pixel, prove an upper human eyelid-velocity bound, or demonstrate unseen-participant no-hidden-closure prediction. The canthus-normalized image aperture is also susceptible to perspective/gaze and landmark bias. E002-371 is **NOT PHYSICALLY VALIDATED**. No product claim is upgraded: hidden-closure guarantees, blink duration, PERCLOS, fatigue and medical use remain `ABSTAIN_UNCALIBRATED`. Keep PR #26 draft/unmerged.

**Next stop condition:** prioritize obtaining two real independent rater sheets and external shutter/scale evidence. If they cannot be obtained, record the precise blocker; do not keep substituting synthetic lemmas for human measurements. Hush PR #45 and its separate branch are unchanged.
