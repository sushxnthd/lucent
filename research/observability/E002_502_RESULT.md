# E002-502 | Source-verified local handoff to two independent anatomical reviewers

Date: 2026-10-28. Primary E002-371 human-validation kernel. **Evidence tier: reproducible local review handoff, not human physiological measurement.**

## Scientific bottleneck and concrete consequence

E002-496/500 successfully built and source-replayed the 260-frame authentic S01 review packet, but correctly deleted its private images on the ephemeral hosted runner. The verified aggregate cannot be used to obtain anatomical labels. E002-501 then yielded zero optical-alias candidates with 92.58% baseline nuisance abstention and 100% abstention under 1-pixel jitter. That optical proxy is retired. More synthetic detector retuning cannot close the actual anatomical-evidence gap.

E002-502 makes the existing frozen E002-492/499 anatomical protocol **deliverable to two independent human raters on an authorized local machine**, without publishing source frames, native frame indices, candidate status, archive bytes or individual ratings. It does not change clip selection, frame indices, anatomical thresholds or the E002-371 physical theorem.

## Reproducible private handoff

Prerequisites: an authorized local machine, Python 3.11+, FFmpeg on PATH, the unchanged repository branch, and the original [S01.zip](https://zenodo.org/records/18970793) downloaded locally in accordance with the dataset's terms. The existing E002-492 source extractor rejects archives whose MD5 is not `fb56109542a13aa7879778833fe4cbaa`. The source-replay verifier independently compares all 260 PNGs with a second extraction of that pinned archive, though both passes use FFmpeg. The ZIP is not downloaded or transferred by this automation.

From the repository root, with private output **outside any Git repository**:

```bash
python research/observability/e002_502_local_handoff.py \
  --archive /secure/source/S01.zip \
  --outdir /secure/LUCENT_E002_502_PRIVATE
```

The command builds and validates the frozen packet, replays all 260 source frames, then creates `REVIEWER_PACKETS/RATER_A_PRIVATE` and `REVIEWER_PACKETS/RATER_B_PRIVATE`. Each contains only 260 blinded `clip_XX_frame_YY.png` images, its own blank A/B JSON template, the existing offline E002-497 anatomical rater, and an instruction text. The owner-only native-index/candidate mapping remains exclusively in `OWNER_PRIVATE_DO_NOT_SHARE`. The program refuses a pre-existing output directory, archive symlinks, output inside a Git repository, malformed templates, extra or missing frame files, and frame symlinks. It sets private filesystem permissions where supported. Do not put the output in cloud sync, GitHub Actions artifacts, a public folder or a shared drive.

Give rater A only `RATER_A_PRIVATE` and rater B only `RATER_B_PRIVATE`. They must be separate people, independently blinded to the candidate, each other's ratings, and the owner mapping. Each opens the offline HTML file, loads its own template and 260 images, marks upper/lower eyelid landmarks at native x=160 with iris reference and uncertainty, or explicitly abstains on nuisance, then exports a private JSON. Do not exchange ratings before both are frozen. An A/B letter in JSON does **not** prove two independent humans; the study owner must separately document that fact without publishing identities.

After two actual completed reviews, adjudicate locally using the existing frozen E002-492 adjudicator:

```bash
python research/observability/e002_492_anatomical_review.py adjudicate \
  --manifest /secure/LUCENT_E002_502_PRIVATE/OWNER_PRIVATE_DO_NOT_SHARE/OWNER_ONLY_MAPPING.json \
  --rater-a /secure/private_ratings/E002_492_RATER_A_PRIVATE.json \
  --rater-b /secure/private_ratings/E002_492_RATER_B_PRIVATE.json \
  --aggregate /secure/private_ratings/E002_492_AGGREGATE_ONLY.json
```

Publish only privacy-reviewed aggregate counts, never individual frames, native source indices, identities, individual ratings or image hashes. If raters cannot identify anatomy, report abstention and stop. Even a perfect dual-rater agreement cannot authenticate camera acquisition timing, shutter exposure, inter-frame eyelid velocity, hidden closures or PERCLOS.

## Verification and limitations

Seven synthetic privacy/blinding adversaries passed locally before GitHub persistence: separate 260-frame bundles, missing frame, extra candidate-revealing file, prepopulated rating, symlink frame, existing output, and cross-rater template substitution. A dedicated GitHub Actions workflow reruns these tests without any human images or dataset downloads. **Hosted verification must be checked separately**; no real S01 local handoff or human annotation is claimed.

This is a human-validation **artifact**, not a new theorem, a new anatomical observation, or a completed human study. The decisive next external action is two actual independent blinded S01 ratings, followed by authenticated physical shutter/clock calibration and participant-disjoint high-rate held-out predictions. The E002-371 continuous-time velocity premise remains unverified.

**Anatomical ratings: 0. Authenticated clock/shutter: 0. Certified human speed upper bounds: 0. Held-out physical predictions: 0. Product: `ABSTAIN_UNCALIBRATED`. Release: `BLOCKED`.**

Hush remains a separate secondary workstream. No merge, force-push, deployment, or scheduling change.
