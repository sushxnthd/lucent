# E002-605 | Independent high-frame-rate human blink labels: preregistered assay and priority correction

Date: 2026-11-02. Parent E002-371. **Evidence tier: SOURCE-VERIFIED LITERATURE + LOCALLY VERIFIED INSTRUMENT, NO HUMAN-ANNOTATION OUTCOME YET.** The [frozen protocol](E002_605_FROZEN.md) was committed first at `15b21a5`, before source parsing or test implementation.

## New primary-literature finding, with immediate claim correction

Nassr Alsaeedi and Dieter Wloka, *Sensors* 19(5), 1121 (2019), https://doi.org/10.3390/s19051121, already describe **100–110-fps** eye-facing VR recordings from **12 participants** and discuss why a nominal **30-fps** camera can miss the brief pause/fully-closed portion of a blink. They cite **13.7 ± 3.3 ms** for the spontaneous pause and give a heuristic **73 fps** minimum based on the mean pause duration. Their associated public dataset, https://doi.org/10.17632/9yzdnng594.1, is published with CC BY 4.0 and advertises annotated participant videos.

This **removes any defensible Lucent novelty claim** for the generic proposition that 30-fps sampling can miss a closed-eye pause. Their heuristic is not a hard worst-case guarantee: the quoted ±3.3 ms is not a proven minimum closed dwell, the published recording rate is not an independently measured shutter/clock certificate, and event-level blink annotations cannot be silently interpreted as fully-closed intervals. E002-371 must be compared on its *specific sharp observability boundary*, not marketed as discovery of ordinary-camera blink aliasing.

## Frozen prospective empirical test

- Source: Alsaeedi 2019 dataset v1, 100–110 fps as reported by the original authors; no assertion that individual files have authenticated physical timestamps.
- Split: S1–S4 development; S5–S12 held out. Ignore S13 unless separately preregistered.
- Inputs: only unambiguous **native-frame-index** interval annotations explicitly typed as `blink_event` or `fully_closed`. Ambiguous rows, index origin, absent frame count or unlabeled closed phase => **ABSTAIN**. Video pixels and person-level labels must not be uploaded.
- Test: exact three-phase 3:1 index decimation. One native-frame event is missed in 2/3 phases; two frames in 1/3; three or more consecutive frames in none. A `blink_event` interval may measure event-index visibility, **never** actual closed-phase observability.
- Separate nuisance test: missing source frames cause unknown/abstention rather than negative evidence. No physical exposure simulation is implied by index decimation.

## Reproducibility and observed local verification

- [Python source](e002_605_human_blink_alias.py): strict schema, integer-frame bounds checked against the paper's per-video counts, duplicate rejection, subject-disjoint aggregation, fail-closed Mendeley public API attempt, aggregate-only output.
- [Eight adversarial tests](test_e002_605_human_blink_alias.py): **8/8 passed locally**, including phase law, missingness, class separation, split, malformed/ambiguous rows and duplicates.
- [Independent JavaScript enumerator](e002_605_independent.js): **500/500 independent integer phase checks passed locally**.
- [Dedicated CI workflow](../../.github/workflows/e002_605_human_blink_alias.yml): attempts public source acquisition and uploads only a sanitized aggregate; its hosted status and any actual source-annotation result are **not yet verified** at this report commit.

**No participant-level outcome, missed closure fraction, native-frame blink count, or physical shutter result is claimed from this run.** The Mendeley XLS workbook's schema has not been authenticated; the strict parser is intentionally allowed to abstain. This is the first independent-source **annotation-level** assay after repeated LPW/S01 instrument-only work, not a new round of dataset metadata archaeology.

## Completion gate

Still missing: independent human eyelid-margin adjudication or usable fully-closed labels on native high-rate sequences, verified physical shutter and clock timing, defensible physiological velocity ceilings, participant-disjoint held-out physical predictions, nuisance robustness, and external replication. E002-604's shutter-averaging counterexample was separately verified by hosted CI (run 41390859258); it remains a synthetic idealized model.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. Existing draft PR #26 and branch preserved. Hush PR #45 untouched.
