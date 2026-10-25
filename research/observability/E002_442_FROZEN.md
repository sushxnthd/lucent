# E002-442 — preregistered S19 timebase reconciliation (frozen before sync-row inspection)

Parent: E002-371 / E002-441. Date: 2026-10-25. Evidence obtained before freezing: the 373,146,176-byte S19 archive passed its published MD5; a 320×288 MPEG-4 Phantom AVI decodes, has 56,911 frames, but **its container reports 1/1 fps and 56,911 seconds** despite the publication describing approximately 500-fps acquisition. The synchronization CSV contains headers `Time`, `PhanTime`, `RelTime`, `RecordingTimestamp`, `LocalTimeStamp`, `Blinks`. **No sync CSV data rows have been inspected** before this protocol.

## Frozen question and falsification
Does the independent synchronization table contain a numeric monotone clock compatible with ~2 ms spacing (500 Hz), or does the available archive fail to provide defensible per-frame time reconstruction? Treat the AVI 1-fps timebase as a candidate packaging artefact, NOT a proven error, until independently corroborated.

## Analysis locked before inspecting rows
1. Re-download S19 and verify archive byte count + published MD5; read only `*_sync.csv` inside the ZIP. Do not export images or absolute clock values.
2. For each named time column, compute row count, numeric coverage, count of nonpositive/positive adjacent deltas, median positive adjacent delta, p01/p99 positive delta, total relative span, and fractions of adjacent deltas compatible with 2 ms under units seconds, milliseconds, microseconds, or nanoseconds (tolerance ±20%). Include count of missing or unparsable values.
3. Require >=1000 adjacent valid deltas, >99.5% strictly increasing steps, >=95% 2-ms-compatible steps, and a table span within 5% of (video frame count-1)/500 s before describing a column as a *candidate frame clock*. Require sync row count to equal video frame count to even propose row-to-frame alignment. These are **exploratory instrument checks**, not independent exposure-clock authentication.
4. Record all failures, nonmatching columns, mismatched row counts, dropped rows, and uncertainty. Never silently substitute frame_index/500 or container 1fps as authenticated physical time.
5. No physiological velocity cap, physical scale, shutter integration, anatomical closure reference, or human no-closure certification is inferred. Keep `ABSTAIN_UNCALIBRATED`.

## Decision
If any column passes all checks, proceed only to a future blinded anatomical pilot on S19; S21 and S22 remain sealed. If none pass, explicitly reject native temporal calibration for E002-371 and request original hardware acquisition logs or prospective instrumented recordings. No release authorization under either outcome.
