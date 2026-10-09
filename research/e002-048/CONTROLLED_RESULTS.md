# E002-048 controlled results and next gate

Date: 2026-10-09. Classification: DISCRIMINATION and CAPABILITY-BUILDING. All numeric results below are synthetic; no human RGBE-Gaze recordings were accessed.

The published collector saves each TCP receive chunk as a line. The published converter accepts a line containing RPOGY and LPOGX without checking that it is one complete Gazepoint record. A source-equivalent fixture used 100 complete 750-byte records with 48 attributes.

| Partition | Exact rows | Accepted incomplete rows |
| --- | ---: | ---: |
| Unsplit | 100 | 0 |
| 512 bytes | 0 | 87 |
| 1024 bytes | 27 to 28 | 65 to 66 |
| 2048 bytes | 63 to 65 | 30 to 34 |

For 50 seeded random partitions with lengths 1 to 1024 bytes, mean exact recovery was 8.28 of 100. A stateful record parser recovered all 100 in every tested partition. These stress distributions do not estimate actual operating-system receive boundaries or released-data corruption.

The MATLAB reference code resets device time to the first retained valid record but uses a first-receive host epoch as the alignment anchor. The unknown difference between these anchors creates a potential constant offset. The actual offset has not been measured.

**Gate:** Before scoring waveform fidelity, validate raw record framing, named measurement units, pupil-specific validity, FLIR acquisition timestamps, Gazepoint device time, and independent clock offset/drift. Preserve frozen E002-044 participant-wise evaluation and the earlier PupilSense negative result. No physiological breakthrough or five-second fatigue/alertness validation is claimed.
