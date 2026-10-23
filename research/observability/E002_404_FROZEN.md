# E002-404 — blinded human landmark annotation: frozen usability and integrity protocol

Date: 2026-10-24. Evidence tier: human-validation *instrument*, not human ground truth. This protocol is frozen before implementation and testing. It does not change E002-398's fixed clip selection or its private EEG event/control mapping.

## Problem and primary test

E002-398 generated 560 checksum-verified human-eye frames and blank CSV sheets, but no usable local rater interface. Independent annotation remains the critical empirical bottleneck. Build a zero-cost, entirely offline browser annotator for the existing 190x130 PNG crops and blinded public manifest. Two raters must be able to independently mark left/center/right upper and lower eyelid margins on every frame, or explicitly mark a frame unresolved. Never expose the private event/control linkage or claim that pixel landmarks alone are calibrated physical aperture.

## Frozen predictions and acceptance tests

- **P1** A local-only packager copies exactly the manifest-listed PNG files, the public manifest and blank sheet into a separate output directory. It refuses missing files, modified image bytes, unsafe filenames, duplicates, incorrect PNG dimensions, mismatched clip/frame totals, and output-directory collisions with the private source. It NEVER copies `PRIVATE_DO_NOT_UPLOAD_linkage.json` or any other unlisted private file.
- **P2** The offline single-page annotator reads a manifest and image files selected by the rater; it has no network dependencies, no telemetry, no external scripts, and no code path that transmits frames or annotations. Each PNG is checked against the manifest SHA256 before display. A mismatch must block annotation/export.
- **P3** Six fixed landmarks per usable frame are required in this order: left upper/lower, center upper/lower, right upper/lower. Click coordinates must be native 190x130 pixels, not scaled canvas pixels. Undo, previous/next, keyboard shortcuts, per-frame nuisance flags, and explicit unresolved are available.
- **P4** CSV export uses E002-398's exact 22 columns and one row for every manifest frame; no silent frame omission. Missing six-point annotations are prohibited unless `unresolved` is true. A nonempty rater ID is mandatory. The two rater sheets must remain separate and not display event/control labels.
- **P5** A source-independent Python checker validates the exported CSV against the blinded manifest, including unique rows, complete coverage, finite/in-bounds coordinates, exact field names, and rater ID consistency. Deliberately corrupted sheets must fail. The checker must NOT require event/control linkage.
- **P6** CI runs deterministic packager and CSV integrity tests using synthetic PNG fixtures, without downloading human video or publishing human frames. It must not claim actual rater annotations or independent human E002-371 validation.

## Stopping and release

Stop building proxy classifiers or further theoretical nuisances in this run. Deliver an actionable human-rater handoff and reproducible local integrity tests. No person-identifying full-face images, no public CI frame uploads, no private event/control linkage in public artifacts. The local pack remains on the operator's computer. Actual human ratings, independent camera exposure/clock/velocity calibration and untouched participants remain future gates. Product continues `ABSTAIN_UNCALIBRATED`.
