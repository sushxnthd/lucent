# E002-148 EyeDentify source-to-release provenance

Frozen protocol SHA256: 6262ff8139b72ee2a49aabf2cc5cd3d95848c14ef5cf70281e573e44dddafeec.

Published alignment code converts Tobii timestamps to whole-second strings, groups three timestamp bins, averages corresponding row positions, repeats a common timestamp, and pairs the resulting rows to webcam frames by ordinal index. The 3-to-1 averaging map is noninjective: rank N, nullity 2N for N complete rows.

Original-human audit of previously unused left-eye participants 30,31, sessions 11,21: 4/4 public CSVs retrieved; row counts 88,89,89,89; all have exactly one timestamp and a distinct frame path for each row. This does not establish that the current source code generated every released file.

Original Tobii subsecond timestamps and webcam frame clock are required for valid waveform reconstruction. Not recovered in this run. No physiological waveform scoring was performed. Pivot to RGBE-Gaze raw paired-data validation. Prior PupilSense scale failure remains negative evidence.
