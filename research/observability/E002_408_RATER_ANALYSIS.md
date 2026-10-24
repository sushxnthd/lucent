# E002-408 — full-event human two-rater analysis handoff

**Status:** The code and frozen synthetic adversarial protocol are committed. E002-407's **8 clips / 632 real human frames** were generated in ephemeral CI storage, but **no independent human landmark sheets exist**. The E002-408 tool is an analysis instrument, not a validation result.

## Local use, no uploads

Generate E002-407 rater packs locally following `E002_407_RATER_HANDOFF.md`, then have two independent raters complete the **same immutable** blinded pack. Keep raw eye images, private EEG arm mapping, rater sheets and framewise clock mapping on authorized local storage. Run:

```bash
python research/observability/e002_408_two_rater_adjudication.py \
  --manifest /private/S01-rater-pack/blinded_manifest.json \
  --rater-a /private/ratings/S01-rater-A.csv \
  --rater-b /private/ratings/S01-rater-B.csv
```

This reports total frames, number of usable pairwise ratings, excluded frames (nuisance and inverted signed geometry), and median/max absolute disagreement in **center-column vertical eyelid gap, pixels**. It rejects duplicate/missing entries, invalid landmarks, identical rater IDs and incomplete sheets. It does not output raw coordinates, blinded IDs or EEG event/control labels. Do not infer physical eyelid aperture, velocity, blink duration, PERCLOS or absence of hidden closures from pixel agreement.

## Optional independent camera calibration

Only an independently measured **camera-hardware** timing document, *not* the Eye-BCI EEG-synchronization clock, is admissible to the opt-in physical reference bridge. Its JSON object must contain:

- `clock_kind: "independent_camera_hardware"`, `camera_clock_verified: true`, and auditable `provenance` and `validity_domain` strings;
- `frames` with **exactly one** record for every `(clip_id, frame_in_clip)` in the blinded manifest, each containing finite `nominal_time_s`, positive `exposure_s`, and nonnegative `clock_error_s`;
- strictly increasing camera timestamps within every clip.

The physical calibration JSON must provide the complete E002-399/400/401/402/403/405 quantitative optical inversion, reference-column geometry, rolling-shutter per-landmark timing and speed, shutter temporal first-moment, synchronization, nuisance, and **deterministic physical** aperture-velocity gates. A finite observed human velocity maximum cannot satisfy the hard-speed gate. With both documents available:

```bash
python research/observability/e002_408_two_rater_adjudication.py \
  --manifest /private/S01-rater-pack/blinded_manifest.json \
  --rater-a /private/ratings/S01-rater-A.csv \
  --rater-b /private/ratings/S01-rater-B.csv \
  --external-camera-timing /private/calibration/S01-hardware-clock.json \
  --physical-calibration /private/calibration/S01-physical-aperture.json
```

**A provenance string or Boolean flag is not an independent calibration audit.** The tool reports that physical calibration is *asserted but not authenticated*. Its product field remains `ABSTAIN_UNCALIBRATED` even when a synthetic oracle produces conditional reference certificates. An independent physical metrology review and prospective untouched-device study are required before any product claim is unlocked.

## Next empirical experiment

1. Freeze two independent rater sheets for S01/S19 pilot packs, record adjudication of unusable frames, and publish only consent/license-compatible aggregate inter-rater results.
2. Quantify whether the independently calibrated camera clock exists. The currently available EEG-aligned timestamps do **not** establish exposure timing; if unavailable, stop at pixel-level agreement and do not retrofit the EEG clock.
3. Conduct a new synchronized high-speed/ordinary-camera physical acquisition with measured exposure/row timing, geometry, optics and a justified velocity envelope; preregister and score three-way predictions, abstentions, and false certificates on untouched participants and cameras.
4. If a deterministic human speed ceiling cannot be justified, use **statistical coverage statements** with explicit exchangeability/domain assumptions rather than deterministic no-hidden-closure certificates.

All missing evidence must remain missing, not filled with fabricated annotation or calibration data.
