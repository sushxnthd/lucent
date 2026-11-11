# E002-453 — frozen external human peak-velocity cap transfer test

Frozen 2026-10-26 **before inspecting aggregate velocity statistics**. This is a new external *human measurement* falsification, not a physical proof of E002-371.

## Source and admissible evidence
Culemann et al. (2026), *Behavior Research Methods* 58, article 89, DOI 10.3758/s13428-026-02984-4; author-supplied OSF project https://osf.io/tud8a, public file `Blinks.csv` https://osf.io/m34qd, OSF sha256 `6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43`, 743520 bytes. Source provides per-blink **estimated** peak closing velocity, gaze target and participant; **not** raw high-frame-rate anatomical trajectories, authenticated exposure timing, or a population-wide hard speed bound. Do not commit participant-level data or the CSV.

## Locked analysis
- Parse the complete CSV using standard comma CSV parsing. Required fields: `subject`, `target_pos`, `peak_closing_velocity`, `peak_opening_velocity`, `closing_amplitude`, `duration`. Validate row count, participant count, nonfinite/missing and negative closing velocities. Report exclusions.
- Participant-disjoint split **before** observing velocity values: hold out subjects with numeric IDs `[3,6,9,12,15]`; remaining participants are calibration. Never refit after holdout inspection.
- Training-only candidate velocity caps (mm/s): (A) pooled observed maximum, (B) pooled nearest-rank 99th percentile, (C) each target-position-specific observed maximum. For (C), abstain if a holdout gaze condition was absent in training. Report holdout exceedance count and denominator, maximum exceedance ratio, by-gaze counts, and participant-level exceedance counts. A training maximum is *not* a physiological hard cap; this experiment tests only transfer to unseen people within this dataset.
- Independently report training/holdout pooled minima, median, maxima and by-gaze maxima, with data-quality warnings and missingness. Do not infer velocity from `time_peak_closing_velocity` (it is a timestamp).
- For an **illustrative** pair of instantaneous aperture endpoints a0=a1=3 mm and closure threshold c=2 mm, calculate critical gap `Tcrit=(a0+a1-2*c)/V` for the *training pooled maximum* only. Compare 30, 60, 240 fps nominal interframe gaps without claiming those are authenticated unsampled exposure gaps. Do not present this as an actual camera or physiology guarantee.
- **Kill criterion:** any holdout peak closing velocity > the corresponding training candidate cap falsifies that cap's *observed transfer coverage* for these people. Zero exceedances does not validate a deterministic universal bound. All product physical claims remain `ABSTAIN_UNCALIBRATED` regardless of results.

## Reproducibility and privacy
Commit source-specific stdlib analysis script, synthetic fixture tests, aggregate JSON and report. Read CSV from a caller-supplied path; do not download in CI or persist raw participant data. External analysis may be executed in a transient read-only web fetch and its aggregates independently reproduced using script against the hash-verified CSV. Record whether the original file hash was independently verified; if it was not, say so. Do not touch S21/S22. Preserve established branch and draft PR #26.
