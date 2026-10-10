# Lucent E002-084 frozen protocol — original-video independent timing check and collision semantics
Frozen: 2026-10-10 before executing original-file Python/ffprobe on the target recordings.
Classification: DISCRIMINATION / CAPABILITY-BUILDING.
Source: Brown Eye of the Typer original ZIP. No original video redistribution.

Primary target: P_06 initial recording, central-directory ZIP member at byte 2542541874; method STORE, compressed length 3136910, CRC32 2419120984, local filename length 81.
Secondary targets: P_02 initial/final and P_07 initial from E002-083 reproduction script.

Hypothesis H1: corrected unknown-size-Cluster EBML parser and ffprobe agree on the full ordered video packet presentation-time sequence for P_06. Mechanistic prediction: 687 frames, 382 distinct PTS, 7 Clusters, CRC verified, and exact 687/687 ordered PTS match.
Primary gate G1: original CRC and size pass; G2: full EBML/ffprobe packet count and ordered timestamps match exactly; G3: independent decoder counts match 687/382. Any failure is retained, not retuned.

H2: exact repeated presentation timestamps do not necessarily mean duplicated image content. Preselect up to first 30 adjacent same-PTS frame pairs and first 30 adjacent different-PTS frame pairs from P_06; compare decoded pixel hashes and grayscale mean absolute difference. Do not claim camera exposure-time differences from visual difference alone. Gate: report exact identical-pair fractions in both groups; descriptive only.

Confounds: Matroska PTS are not exposure times; packet order vs display order, VP8 decode state, timing rounding, source ZIP central-directory correctness, ffprobe timebase and non-monotonic PTS.
Anomaly mine all failures: cluster truncation, repeated packets, timestamp splitting, within-recording regime changes.
Do not use pupil/reference data in any timestamp gate. No APST-5 physiological inference is supported by this audit.
