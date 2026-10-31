# E002-469 FROZEN — one decisive S19 timing reconciliation, not repeated dataset archaeology

Frozen on 2026-10-27 **after** E002-468's unexpected actual 1/1 AVI timebase and **before** inspecting any Phantom XML or sync CSV fields. The source remains the checksum-verified S19 calibration archive from Zenodo 18971758 (expected MD5 `022dc7770d62b258ce2dd5a9a7b3df6c`). S01 and all other holdout participants remain sealed. This is a one-shot temporal provenance experiment; do not optimize an inferred frame rate against blink appearance.

## Question and competing predictions

Does the independently supplied Phantom XML or sync CSV contain an explicit, usable correspondence between physical acquisition time and video frame index, contradicting the 1/1 AVI presentation timebase?

- H0: AVI timestamps are the only decodable frame timebase, or XML/CSV clocks cannot be unambiguously mapped to frames. Outcome: **TIMING_UNAUTHENTICATED**; no per-millisecond eyelid speed or E002-371 human test.
- H1: XML/CSV contains an explicit frame index plus physical-acquisition clock, documented units, and a monotonically increasing near-affine mapping. Outcome: **CANDIDATE_FRAME_CLOCK** with independently reproducible slope, residual, dropouts, and caveats; never automatically `HARDWARE_SHUTTER_AUTHENTICATED`.

## Frozen gates

1. Download exactly S19.zip in ephemeral CI and verify MD5. Extract only `ME191_phantom.xml` and `ME191_sync.csv` via the existing safe extractor. No image data, private rows, raw sync samples, or identifying metadata leave the runner.
2. Parse XML/CSV with standard-library streaming readers. Report only sanitized field/key names related to `frame|fps|rate|clock|time|timestamp|tick|trigger|sample|frequency|interval|duration`, structural counts, numeric summary ranges and monotonicity. Never publish raw timestamps or raw text values.
3. A candidate frame-clock rate requires **explicit frame-number and timestamp columns in the same CSV**, explicit time units (seconds, milliseconds, microseconds or nanoseconds) in the field name, at least 1000 valid unique paired rows, strictly increasing frame and time values, positive slope, median relative interval deviation <1%, and maximum residual <0.5 inferred frame after affine fitting. Units and clock identity must be independently documented before any scientific use. Do not infer units by selecting whichever yields 150 or 500 fps.
4. A scalar XML `fps` or `frame_rate` is only a **nominal device declaration**, not authenticated timing. If no eligible frame-clock pair exists, classify `NO_EXPLICIT_FRAME_CLOCK`; stop searching this archive and move to the already frozen physical instrument protocol.
5. Negative results, unsupported units, parse errors, dropped rows, and conflict with AVI's 1 fps must remain visible. Always output `hardware_exposure_timing_authenticated=false`, `anatomical_reference_authenticated=false`, `product_release_authorized=false`, and `physical_hidden_closure_exclusion=ABSTAIN_UNCALIBRATED`.

## Independence and falsification

No S19 imagery, eyelid annotation or blink dynamics may influence rate selection. No frame-rate guess from video duration or visual rhythm counts as evidence. A real timestamp-frame mapping is only a candidate clock: rolling shutter, shutter support, clock drift, synchronization and anatomical reference remain separate unresolved gates.

One attempt only. If XML/CSV do not establish an independent clock mapping, no more S19 metadata audits; proceed to moving-aperture instrument validation or acquire another independently timestamped human recording.
