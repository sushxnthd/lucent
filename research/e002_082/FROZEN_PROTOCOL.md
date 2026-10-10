# E002-082: independent original-video PTS replication — frozen before execution

Date: 2026-10-10. Classification: DISCRIMINATION / REPLICATION.

## Prior observations (not independent evidence)
E002-081 reported original WebM timing metrics from Wolfram Import on P_02 initial/final, P_06 initial, P_07 initial. These four recordings are **not untouched**. This experiment tests independent software agreement, not prospective population generalization.

## Source and immutable member specification
Brown Eye of the Typer 2018 public archive, `https://webgazer.cs.brown.edu/data/WebGazerETRA2018Dataset_Release20180420.zip`. The original ZIP member offsets, compressed sizes, original sizes, CRC32s, local filename lengths, and compression methods are in `research/e002_082/verify_original_timing.py`. Read only bounded HTTP byte ranges and check Content-Range, ZIP header, CRC32, and length before analysis. Do not redistribute face video.

## Frozen gates
G1: All four original WebM members pass byte-level ZIP provenance and CRC32 checks.
G2: For every member, an independent Python EBML parser and ffprobe agree on **the entire ordered per-packet video PTS array** after conversion to integer milliseconds, not merely collision totals.
G3: EBML-derived (frame count, unique PTS) equal E002-081's archived Wolfram observations: P_02 initial (857,792), P_02 final (783,463), P_06 initial (687,382), P_07 initial (535,350).
G4: P_02 within-session final-minus-initial collision fraction exceeds 0.20 (expected approximately 0.3328).

All four gates must pass for the claim of independent source-file timing replication. On errors or missing data, report NOT EVALUABLE rather than PASS. No adjustment of thresholds after seeing outcomes.

## Exploratory analyses (not gates)
Per-video multiplicity distribution, gap histograms, complementary-gap structure, 60ms epoch fractions, and packet duration flags. Any interpretation as exposure timing is prohibited. ffprobe and EBML parse the same container, so agreement validates parsing, **not independent physiological or camera-clock truth**.

## Negative-control and leakage notes
Preserve all prior RGB pupil-observability failures. No Tobii samples are used in this timing test; thus no waveform, participant-state, or APST-5 validation can be claimed. Public media presentation timestamps may not reflect actual exposure time.

## Reporting
Save machine-readable metrics, pass/fail/NE, exact commands, interpreter and ffprobe versions, and stderr. Run on GitHub-hosted runner with zero paid compute. Only publish aggregated timing statistics.