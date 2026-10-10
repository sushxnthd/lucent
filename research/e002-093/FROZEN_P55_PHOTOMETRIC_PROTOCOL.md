# Lucent E002-093 P_55 cross-modal photometric replication lock

Locked 2026-10-11 UTC, before original P_55 paired RGB/Tobii outcome. P_55 was previously inspected for separate RGB-onset and reference-only questions; the RGB/reference correlation is the prospective endpoint, not a wholly untouched subject.

Use Brown Eye of the Typer ETRA 2018 P_55 initial dot-test webcam video, browser video-start event and validity-positive Tobii true_time pupil diameters. Frame indices 81,89,..., <=520; no outcome-based frame filtering. RGB: mean whole-frame brightness (0..1), not pupil/iris. Use container presentation FrameDurations relative to video start, match nearest valid reference within 75 ms, mean both valid eyes (or one valid eye). Windows [0,5), [5,10), [10,15), [15,20) seconds. Eligible if >=10 pairs and both signals nonconstant. Pearson r per window. **Frozen warning** if at least 2 eligible windows have |r|>=0.50; record all results regardless. No lag or threshold tuning. Do not inspect P_01/P_02/P_07 waveform holdouts.

Hypothesis: a non-anatomical photometric nuisance may correlate with the tracker reference; a plausible competing prediction is P_55 has weaker confounding because its webcam startup brightness was previously stable. Report negative and positive results. Post-primary diagnostics: detrending, first differences, circular shifts, amplitude and timestamp missingness. No fatigue or physiological inference from nuisance correlation.

If original data cannot be evaluated, report NOT_RUN. No claim of external preregistration.
