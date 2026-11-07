# E002-566 | Frozen authentic S01 two-rater handoff acceptance test

Frozen 2026-10-31 **before running E002-566 on the public human source**. Kernel: E002-371 shutter-gap/eyelid-velocity observability. Reuse the existing `research/observability-human-boundary` branch and draft PR #26. No new anatomical threshold, camera-rate inference, video event selection, or optical proxy.

## Hypothesis and material

The existing E002-502 private handoff has passed synthetic tests but has **not been demonstrated end-to-end on the checksum-pinned original human S01 archive**. Test whether its full production path, including E002-492 native-frame extraction, E002-496 integrity checks, E002-500 independent source replay and two E002-502 private rater bundles, can complete on the original Motor Imagery S01 ZIP (Zenodo record 18970793; published archive MD5 `fb56109542a13aa7879778833fe4cbaa`).

Use the **existing frozen 20 clips x 13 frames = 260 native source frames**, including 19 controls. No reselection, candidate scoring, frame-rate conversion, physiological labels, or adjustment based on what images look like. Preserve original S01 and paradigm binding. Do not use the distinct Motor Execution S01.

## Acceptance criteria (fixed before the source run)

1. Source archive MD5 and E002-492 frame selection verify; E002-500 independently re-extracts and byte-compares all 260 frames. This is a *same-decoder replay*, not independent sensor authentication.
2. E002-502 produces exactly two separate private rater bundles, each with 260 PNGs, its own blank A/B template, the offline rater HTML and instructions. Each frame must byte-match its owner-only source counterpart. A and B templates must be distinct and unpopulated.
3. Neither bundle contains owner mapping, native source frame indices, candidate/control labels, source archive, extra files, or symlinks. Output must remain outside the Git checkout.
4. Run existing E002-502 synthetic adversarial tests and a separate E002-566 auditor with missing/altered/extra-frame and cross-rater-template negative controls.
5. In GitHub Actions, download privately into `$RUNNER_TEMP`; never upload images, original video, archive, raw template contents, per-frame hashes, source indices, reviewer identities or reviewer ratings. Delete source and private packet on exit. The only permitted artifact is a sanitized aggregate with fixed keys and counts. The runner is an *ephemeral technical test*, **not** a way to deliver private media to reviewers.
6. Any source, packaging, provenance or privacy failure returns `FAILED_OR_ABSTAINED`, with zero physiological claims. Even success is `AUTHENTIC_RATER_BUNDLES_VERIFIED`, **not** human annotation or a shutter/clock certificate.

## Falsification and hard stop

Failure means the previously claimed rater handoff is not yet operational on actual human media; preserve the failure and fix the instrument, not the anatomical threshold. Success establishes that real source-bound review packets can be prepared privately, but still requires **two actual independent blinded people** to annotate the private bundles on an authorized local machine. Neither the automation nor a CI runner is a human rater.

Do not repeat dataset metadata archaeology or optical-motion proxy tuning. No additional synthetic theory pass follows success. Next evidence is independent anatomical review and physical shutter/clock calibration.

Human rater pairs = 0; authenticated physical shutter captures = 0; hard continuous-time human velocity ceilings = 0; held-out physical closure predictions = 0. Product `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Hush stays untouched.
