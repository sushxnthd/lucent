# E002-418 — offline observer qualification and blinded human-validation handoff

**Status:** Synthetic rater qualification instrument implemented; **zero actual human raters have been qualified**. Do not describe this as human physical eyelid validation. This is a separate prerequisite to the existing E002-407/E002-408 human-video experiment.

## Prepare one immutable local synthetic challenge

In a local checkout of the existing research branch, with Python 3.11+ (no extra dependencies for the synthetic challenge):

```bash
python research/observability/test_e002_418_rater_challenge.py
python research/observability/e002_418_rater_challenge.py generate \
  --pack-dir /private/lucent/qualify-blinded \
  --truth-dir /private/lucent/qualify-PRIVATE
```

The public-to-raters directory contains only `blinded_manifest.json`, 144 synthetic PNGs in `images/`, `blank_annotation_sheet.csv` and `annotate_offline.html`. The private truth directory contains `PRIVATE_DO_NOT_SHARE_truth.json`, which must be kept by the study coordinator and **never sent to raters**. Challenge case order and geometry use OS-backed unpredictable randomness by default; a fixed seed is available only to Python tests, not exposed by the command line.

Provide the **same immutable blinded pack** to two independent human raters. Each opens the offline HTML annotator, selects the manifest and PNG folder, annotates all frames, and exports a complete CSV under a distinct rater ID. For every synthetic frame, click six lid-margin points left/center/right, upper/lower. Mark `unresolved` and **clear all points** whenever a required margin is obscured. Keep raters blind to the private truth and each other's sheets until both are frozen. Do not use an AI model as a substitute for an independent human rater.

## Score only after both completed sheets are frozen

```bash
python research/observability/e002_418_rater_challenge.py score \
  --pack-dir /private/lucent/qualify-blinded \
  --truth-file /private/lucent/qualify-PRIVATE/PRIVATE_DO_NOT_SHARE_truth.json \
  --rater-a /private/lucent/ratings/rater_A.csv \
  --rater-b /private/lucent/ratings/rater_B.csv
```

Scoring reports 96 visible cases and 48 deliberately obscured cases per rater. All missing/unresolved visible cases count as incorrect. Obscured cases count as correct only with an unresolved flag **and no coordinate entries**. The frozen gate is at least 87/96 accurate visible cases, at least 12/16 in each of six visible nuisance conditions, and at least 46/48 correct abstentions. The scorer checks distinct rater IDs but cannot authenticate human identity or independence. Coordinator must separately attest independence and maintain an immutable hash of each completed sheet.

The `oracle` subcommand exists **only for automated test controls** and must never be used to manufacture apparent human annotations. Oracle results are synthetic, not measured rater performance. Do not upload any rater sheet or private challenge answer file to GitHub.

## Proceed to actual human recordings only after qualification

Regenerate E002-407 S01/S19 packs locally from the checksum-verified source archives, following `E002_407_RATER_HANDOFF.md`. Two qualified independent human raters must annotate the same blinded real-human pack and freeze their sheets before E002-408 adjudication. Keep source video, private EEG linkage, real-eye PNGs, and rater sheets on authorized local storage. Publish only consent/license-compatible aggregate metrics. E002-407/408 is **not** completed by passing this synthetic challenge.

Even successful synthetic qualification plus pixel-space human agreement cannot establish physical aperture, exposure response, camera clock, a physiological hard eyelid-velocity ceiling, or the E002-371 hidden-closure guarantee. Use E002-416 reference adequacy rules and external physical metrology; unresolved high-speed intervals remain unresolved. Product remains `ABSTAIN_UNCALIBRATED`.

## Reproducibility and release guard

The synthetic source generator and independent adversarial tests are in `e002_418_rater_challenge.py` and `test_e002_418_rater_challenge.py`. The CI workflow runs only synthetic challenge integrity and E002-407 regression; it deliberately uploads no images, linkage, truth or sheets. A green CI result is an **instrument test**, not proof that any human rater has completed the challenge. No automatic product unlock exists.
