# E002-034: first-session timestamp order, frozen before reading new raw files

Date: 2026-10-08. Dataset: public MCFW-Gaze v3 (Zenodo 20300972). Analysis is limited to tracker-recording integrity, not RGB or sleepiness.

**Already known before this protocol:** image_84_1 is a long-duration recording for 15/15 participants; 84_2/3 are normal; the first five seconds of 84_1 contain well-supported pupil data but have no verified stimulus onset.

**New hypothesis:** image 84 is first in the fixed first-session presentation order, and the abnormal recording is related to session initialization. Competing explanations: preamble, delayed stop, file-boundary overlap, wrong labels, multiple events, timestamp discontinuity.

**Frozen test:** For each of 15 participants, read the original first device timestamp of all 100 image_XX_1.tsv recordings (1,500 files). Rank image 84 among 100. Compute the first and second image IDs, start-time difference, the full image84 timestamp duration, whether the second file begins before image84 ends, and number of other image files beginning during image84. Report every participant, including reversals. Do not use sample count as a substitute for timestamp elapsed time. The 84_1 duration must reproduce the prior 29.059–230.297-second range.

**Prediction:** image84 is first in all 15; if its recording overlaps subsequent image files, acquisition/segmentation overlap is favored; if it ends before the next image begins, a preamble/long wait is favored. Either way acquisition timestamp is NOT stimulus onset. 013–015 are a new ordering confirmation stratum only; they were already inspected for image84 duration.

**Evaluation boundaries:** No threshold tuning, no excluding participants, no claiming untouched evidence for the already-discovered duration anomaly. The 100-image ordering is new, preregistered relative to this run. ZIP member CRC is verified only for fully read image84 files; first-row probes have no complete-member CRC check. Any missing member fails the run. No first-five-second image84 salvage without independent stimulus timing provenance.

**Adversarial roles:** Explorer proposed order hypothesis; Skeptic separates recording from stimulus; Experimentalist freezes 1,500 files; Analyst reads only post-freeze results; Anomaly Hunter checks order reversals and overlap; Prior-Art Auditor notes that timestamp QA is established practice; Replicator reruns independently; Theorist distinguishes signal support, interval provenance, waveform fidelity, and state validity.

**Status at freeze:** UNTESTED (new order/overlap question). Negative PupilSense scale finding preserved; ordinary RGB waveform fidelity and five-second fatigue inference remain UNTESTED.
