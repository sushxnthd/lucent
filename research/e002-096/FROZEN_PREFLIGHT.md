# E002-096 — MEYELens acquisition/label integrity preflight (frozen before archive inspection)
Date: 2026-10-11. Program: RGB-REFERENCE-OBSERVABILITY-002.
Classification: CAPABILITY-BUILDING / DISCRIMINATION.

## Scope and objective
Inspect the official Zenodo record 20492528 and its image/mask archive, with SHA/MD5 verification and no user hardware. Determine whether the dataset can legitimately calibrate a pupil-visibility/abstention gate for ordinary RGB. It has NO synchronized Tobii waveform or behavioral fatigue labels. A red pupil mask and green *whole-eye* mask do NOT define an iris-only denominator. Do not claim webcam or visible-spectrum acquisition merely because images are RGB JPEG.

## Frozen preflight procedure
1. Query https://zenodo.org/api/records/20492528, require an open-access file named human_eyeregion_pupil_segmentation_dataset.zip. Download it using standard HTTPS, verify size and MD5 against record metadata, then open ZIP safely (no traversal/extraction).
2. Inventory all filenames, extensions, CSV headers, subject/source counts, duplicate image stems and image/mask pairing, image dimensions, red/green mask semantics, and metadata provenance. Report ambiguity rather than silently guessing paths or treating different source images as independent subjects.
3. Inspect a deterministic sample of up to 64 image/mask pairs selected by SHA256(filename) sorting, before looking at any algorithm performance. Quantify pupil pixel area, eye-region area, pupil/eye-area fraction, connected-component count, and image contrast. Report all invalid masks and whether red is a subset of green.
4. If matching or decoding is ambiguous, STOP with an explicit blocker; do not fabricate segmentation results.
5. Only after this audit, freeze a source/subject-wise evaluation split and threshold/edge baselines in a NEW preregistration. This preflight is not a held-out evaluation and does not permit threshold tuning on a frozen test set.

## Prior negatives and claim boundary
Preserve RGB-SCALE-OBSERVABILITY-001 scale failure and E002-094/095 dark-core waveform failures unchanged. This archive cannot establish RGB-Tobii waveform fidelity, phone-domain validity, five-second active response, or fatigue-state inference. All exploratory dataset characteristics remain descriptive. GitHub Actions run status and archive integrity must be reported precisely.