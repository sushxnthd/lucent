# E002-406 — frozen real-human full-event temporal-coverage experiment

Date: 2026-10-24. Freeze this protocol **before** examining full-event results.

## Question and primary hypothesis
The E002-398/E002-404 packets contain only seven consecutive frames per event/control clip. They may be usable for local eyelid annotation but cannot, without more evidence, support whole-blink onset/offset, physical velocity envelopes or 0.5-second trajectory validation. Test this acquisition limitation on the **already checksum-verified** S01 and S19 human high-speed EEG/video frame synchronization. No new EEG-to-aperture label interpretation is allowed.

**H1 (preregistered):** At least 90% of the selected 40 clips per participant span **less than 0.100 s** between first and last annotated frame. If false, preserve failure.
**H2 (preregistered):** At least one selected center per participant has contiguous synchronized video coverage of **±0.250 s** (minimum 0.500 s total), using source EEG-clock frame timestamps rather than nominal AVI fps. If false, preserve failure and do not silently shorten windows.
**H3 (safety invariant):** A candidate full-event window must be rejected if its maximal adjacent frame timestamp gap exceeds 0.020 s, its endpoint coverage falls short of ±0.250 s, or its frame indices are noncontiguous. A missing interval is not imputed.
**H4 (privacy invariant):** Public result contains only per-participant aggregate coverage, no clip IDs, individual event/control labels, EEG marker times, or identifiable eye imagery.

## Analysis
Recompute the same deterministic E002-398 pair selection (20 event/control pairs; 40 centers per participant) with unchanged S01/S19 checksum and prior exclusions. For each center, compute the actual time span of indices k-3..k+3. For full-event coverage find the nearest frame at or before t_center-0.250 and at or after t_center+0.250; require both endpoints and all adjacent frames in the interval to be contiguous, monotone and <=20ms apart. Report 7-frame span p10/p50/p90, count of eligible full windows, full-window frame counts and longest internal gaps. Avoid any claim that an EEG event timestamp measures physical eyelid aperture.

## Decision consequence
If H1 holds, do **not** use seven-frame packets to validate whole-blink duration or maximum eyelid velocity. If H2 holds, full-event private image packs become technically possible, but human annotations and independent shutter/geometry/velocity calibration remain outstanding. Regardless of H1/H2, keep `ABSTAIN_UNCALIBRATED` for closure exclusion, PERCLOS, blink duration and fatigue diagnosis. This is a **real-human acquisition-window adequacy test**, not E002-371 physiological validation.

## Independent reproduction
Source archives: CC0 Eye-BCI S01 (Zenodo 18978288, MD5 fef02cb7ebf62e4f3efb6303284fd6cb), S19 (Zenodo 21905748, MD5 8a16cf12526f7558b4e49926c4bc5e8e). Code must contain a separate synthetic timestamp oracle testing normal 150-Hz cadence, a 100-ms pause, incomplete boundaries and a nonmonotone clock. GitHub Actions must checksum source before executing. Public artifacts contain aggregate JSON only; raw video and private mappings remain ephemeral.
