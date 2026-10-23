# E002-393: frozen independent acquisition-clock and blink-marker audit (2026-10-23)

## Scientific question
E002-392 acquired real CC0 human eye video (53,680 frames) but the AVI time base falsely reports 1 fps. The same verified source archive contains `SSVEP011_sync.csv` (8,620,968 bytes) with columns `Time,Cues,PhanFrame,PhanTime,RelTime,RecordingTimestamp,LocalTimeStamp,Blinks`, plus a Phantom camera XML file. Can an **independent synchronization channel** establish the actual frame cadence and permit reproducible blink-event targeting without pretending EEG markers or RGB pixels are physical aperture ground truth?

## Frozen predictions and rejection criteria (before reading sync rows)
1. The number of distinct `PhanFrame` IDs will be substantial and monotonically increasing, with the median acquisition cadence inferred from `Time`/ `PhanTime` close to the paper's **150 fps** (inter-frame ~6.667 ms), not AVI 1 fps or mirror ~500 fps. Report both pass/fail and exact denominators; no cherry-picking.
2. `Time` will increment approximately 1 ms over a substantial part of the EEG sidecar. Reject inference if units cannot be independently established or frame-to-EEG correspondence is sparse.
3. The `Blinks` column may contain EEG-derived markers, not duration-resolved physical closures. Characterize marker values, counts, run lengths and temporal co-occurrence with frame indices. Do **not** equate a one-sample blink pulse with a 1-ms eyelid closure.
4. If the marker stream is informative, freeze first six non-overlapping candidate marker windows in chronological order and extract a small eye-region contact sheet at corresponding `PhanFrame` IDs. This is an **exploratory event-alignment check**, not a held-out model test. If not informative, preserve negative result.
5. Reconcile `PhanTime`, `Time`, XML camera metadata and the published rate; if sources conflict, explicitly report. No inferred acquisition FPS alone proves exposure start/end, optical transfer or physical aperture.
6. Do not publish participant-identifying raw video or full sync files in Git; output only aggregate timing statistics, sanitized samples, and a limited technical contact sheet. Source archive must pass its frozen MD5.

## World-class and product boundary
This is **actual human multimodal instrument evidence**, not validation of E002-371's sharp no-hidden-closure certificate. It can qualify a reference stream and expose timing pitfalls. Independent physiological velocity bounds, exposure timing, physical aperture labels, RGB transfer and untouched participants/devices are still required. Product decision remains `ABSTAIN_UNCALIBRATED`. Do not turn exploratory blink markers into fatigue, PERCLOS or clinical claims.
