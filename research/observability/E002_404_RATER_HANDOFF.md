# E002-404 — local blinded human-eyelid annotation handoff

**Evidence tier:** usable annotation instrument + deterministic synthetic integrity tests. **Not** independent human ratings, physical eyelid aperture, or a validated E002-371 human shutter-gap law.

## What changed

The E002-398 generator already created 40 blinded seven-frame clips per participant (S01 and S19), but stored the 190×130 PNGs only in temporary private directories. Its CI artifacts contain manifests and blank sheets **without images**, so nobody could annotate them directly. E002-404 makes a complete **local-only** rater pack with image hashes, a standalone offline browser annotator and an independent CSV checker. The private event/control key is never copied.

## Reproduce a rater pack locally (do not upload human frames or linkage)

Use the exact already-checksummed E002-398 public source archives, dependencies and generator, with separate output folders. From the Lucent repository root:

```bash
python -m pip install numpy opencv-python-headless
python research/observability/e002_398_blinded_annotation.py \
  --archive /path/to/S01.zip --participant S01 \
  --public-dir /tmp/lucent-S01-public \
  --private-dir /tmp/lucent-S01-private

python research/observability/e002_404_rater_pack.py pack \
  --public-dir /tmp/lucent-S01-public \
  --private-dir /tmp/lucent-S01-private \
  --output-dir /tmp/lucent-S01-rater-pack
```

Repeat with S19 using its separately verified archive. The pack contains `annotate_offline.html`, `blinded_manifest.json`, `blank_annotation_sheet.csv` and the `images/` folder. It contains **no** source video, EEG marker status, source timestamps or `PRIVATE_DO_NOT_UPLOAD_linkage.json`. Never copy the private source directory to raters. The E002-398 generator uses a fresh random HMAC key, so rerunning it creates different blinded clip IDs; **do not mix sheets or manifests from separate runs**. Keep a single master pack for both raters per participant.

Open `annotate_offline.html` directly in a Chromium-based browser. Select `blinded_manifest.json` and the `images/` directory (or all its PNGs through the fallback file picker), enter a nonempty rater ID, then click **Load & validate manifest**. Every displayed PNG is SHA-256 verified. The page has no network dependencies, uses a restrictive content-security policy and sends nothing to a server.

Click six upper/lower eyelid margin landmarks in this order: left upper, left lower, center upper, center lower, right upper, right lower. Use native image coordinates, not screen coordinates. Mark **unresolved** if a required margin cannot be located; set optical nuisance flags for glare, occlusion, glasses, blur or gaze as appropriate. Navigation and undo are available. CSV export is blocked until every frame has either six points or an explicit unresolved flag. Export a separate CSV for each blinded independent rater; do not share the other rater's sheet until both are frozen.

Check each sheet independently:

```bash
python research/observability/e002_404_rater_pack.py check \
  --manifest /tmp/lucent-S01-rater-pack/blinded_manifest.json \
  --sheet /path/to/e002_404_rater_A_landmarks.csv
```

The checker rejects missing/duplicate frames, wrong columns, out-of-range/nonfinite landmarks, incomplete point pairs, missing rater IDs and invalid flags. **It does not certify annotation correctness**. A separate blinded adjudicator must inspect disagreement and missingness. Keep raw rater sheets immutable.

## Frozen tests and limitations

- Synthetic fixture suite: manifest/PNG hash and geometry, pack whitelist, no private linkage copy, output isolation, valid completed sheet, unresolved allowance, missing coordinates/rows, duplicate indices and out-of-bounds coordinates.
- Browser script: static no-network checks and Node syntax check. Browser UI has not undergone an independent human usability study; the next operational test is two raters on real clips.
- The E002-398 selection used previously studied participants and EEG event/control windows. It is **not** an untouched participant holdout.
- Landmark distances in 2D cropped video are **not** calibrated physical aperture. Exposure duration/kernel, independent clock, rolling-shutter row timing, geometry, optical inversion and independently measured velocity remain separate gates.
- Never use the private event/control mapping during annotation. After freezing both rater sheets and adjudication, compare prospective ordinary-camera certificates to independent physical reference where reference certainty is adequate; report unresolved rates and false certificates without relabeling unresolved cases as negatives.

**Product remains `ABSTAIN_UNCALIBRATED`** for hidden-closure exclusion, blink duration, PERCLOS and fatigue diagnosis. This is an enabling human-validation deliverable, not the world-class completion gate.
