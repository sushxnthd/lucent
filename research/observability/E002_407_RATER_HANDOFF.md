# E002-407 — blinded full-event human eyelid annotation pilot

**Evidence tier:** instrument under verification. E002-406 established real-human temporal coverage, **not** aperture ground truth. This pilot does not turn video into physical eyelid measurements without independent calibration.

## Why the pilot exists

E002-406 verified that all 80 previous seven-frame annotation clips span <100 ms (median 39 ms), whereas **36/40 S01** and **26/40 S19** selected centers have gap-free ±250-ms windows with about 79 frames. The seven-frame packs cannot measure whole-blink duration or velocity. The new local-only E002-407 pilot selects the **first two event/control pairs where both arms have eligible windows** for each participant, preserving the E002-398 deterministic pair order. No image appearance, marker strength or inferred closure is used to select pairs.

## Run locally

Install `numpy` and `opencv-python-headless`. Use the exact MD5-verified S01 and S19 archives already specified in E002-406. **Do not put raw eye images, event/control linkage or rater sheets in public GitHub, CI artifacts or public cloud storage.** In a local checkout of the existing Lucent research branch:

```bash
python research/observability/test_e002_407_full_event_pilot.py

python research/observability/e002_407_full_event_pilot.py generate \
  --archive /private/data/S01.zip --participant S01 \
  --public-dir /private/work/S01-blinded \
  --private-dir /private/work/S01-private

python research/observability/e002_407_full_event_pilot.py pack \
  --public-dir /private/work/S01-blinded \
  --private-dir /private/work/S01-private \
  --output-dir /private/work/S01-rater-pack
```

Repeat with S19. The generator refuses to overwrite existing output directories. Keep the **same immutable blinded pack** for both raters; regenerating changes cryptographic clip IDs. The private directory includes `PRIVATE_DO_NOT_UPLOAD_linkage.json`, which must never accompany the rater pack. The pack contains only blinded 190×130 PNGs, SHA-256 manifest, blank sheet and an offline HTML annotator. The manifest intentionally omits event/control labels, source frame IDs, source clock times and participant identity.

Open `annotate_offline.html` locally and load the manifest and images. Two raters independently annotate upper/lower eyelid margins at left/center/right columns, flag glare, blur, gaze, glasses and occlusion, or mark unresolved. Raters must not see each other's sheets or private event/control mapping until both are frozen.

After each rater exports a completed CSV:

```bash
python research/observability/e002_407_full_event_pilot.py check \
  --manifest /private/work/S01-rater-pack/blinded_manifest.json \
  --sheet /private/ratings/S01-rater-A.csv
```

The validator enforces frame completeness, a single rater ID, finite in-bounds coordinates and explicit unresolved states. It does **not** establish rater accuracy or inter-rater agreement. Keep source video, private linkage and sheets immutable for adjudication. Do not use the `check` subcommand on the **blank** sheet; it intentionally requires a completed rater ID.

## Evidence and limitations

The dedicated CI workflow tests synthetic manifest integrity, PNG hashes, filename/path safety, sheet completeness, geometry and offline JavaScript syntax. It also performs ephemeral generation against checksum-verified real-human archives, printing aggregate counts only and **uploading no artifacts**. A green CI job establishes instrument execution and synthetic integrity, not completed human ratings.

Before any E002-371 physical no-hidden-closure certificate, independently calibrate exposure-response weighting, rolling-shutter row timing, optical inversion, physical aperture geometry, clock uncertainty and a justified **hard** eyelid velocity bound. The finite-sample maximum is not a hard bound (E002-405). Use untouched participants/devices for prospective prediction and report abstention/false certificates. Until then, retain `ABSTAIN_UNCALIBRATED` for hidden-closure guarantees, blink duration, PERCLOS and fatigue diagnosis.
