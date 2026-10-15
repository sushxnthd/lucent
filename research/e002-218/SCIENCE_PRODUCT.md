# Lucent E002-218 | SCIENCE / PRODUCT ledger (2026-10-15 UTC)

## SCIENCE — what is true?
Author-linked Kaggle ZIP's ZIP64 end-of-central-directory declares 5,197,947 entries and a 703,375,480-byte central directory. Its complete metadata inventory exceeds the 80-MB transfer budget. Four 200-entry public listing pages returned PNG entries only; they are not representative of the archive.

A fixed 16-window stratified central-directory sample (512 KiB per window; ~1.19% of directory bytes) parsed 62,532 valid entries: 57,761 PNG, 4,082 NPY, 688 CSV and 1 PKL. Session-level CSV files occur alongside eye crops and depth maps. This disproves an image-only characterization of the sampled release. It does NOT establish original unmodified tracker time-series, raw webcam video, native timestamps, or reliable synchronized waveform labels.

Two selective single-file API requests for distinct session_data.csv paths returned HTTP 404. This is an access-path failure, not a missing-file proof. Switch retrieval method or dataset. No human waveform evaluation was run.

## PRODUCT — capability consequence
Keep EyeDentify as a possible source of image crops and processed session labels, not a certified five-second physiological waveform reference. Do not relax the frozen correlation, lag, amplitude, NRMSE, nuisance or prospective coverage gates. Prefer native-time paired source retrieval; if unavailable, retain this negative provenance finding and move to a different dataset. No fatigue inference.

## Active kernel
Exact pair: geometry/photometry-normalized ordinary-RGB pupil/iris temporal waveform vs native-time same-eye tracker pupil diameter.
Current frontier: author-linked archive has session CSVs but their temporal lineage is unverified.
Scalar: held-out participant-bootstrap lower Pearson correlation bound.
Strongest confounds: timebase, defocus, contrast, illumination, gaze geometry and occlusion.
Falsification: untouched paired human waveform gates fail against nuisance controls.
Publishable success: at least eight untouched paired participants, independent checker and holdouts.
Product relevance: at least 75% prospective acceptance.
Kill: prospective waveform failure or three nondiscriminating primary runs.

## Evidence
Actions E002-218: https://github.com/sushxnthd/lucent/actions/runs/38800322535
Actions E002-218b: https://github.com/sushxnthd/lucent/actions/runs/38800692580
Actions E002-218c: https://github.com/sushxnthd/lucent/actions/runs/38800985520
SHA-256 and exact filenames are in immutable Actions artifacts. Sample windows are stratified byte intervals, not random representative human sessions.
