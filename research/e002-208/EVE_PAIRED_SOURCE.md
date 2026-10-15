# E002-208 independent paired-RGB source collision: EVE (ECCV 2020)

**Date:** 2026-10-15. Source: https://github.com/swook/EVE/blob/master/DATASET.md ; https://ait.ethz.ch/eve . Dataset has 54 participants, four simultaneous views (`basler`, `webcam_l`, `webcam_c`, `webcam_r`), native camera MP4 and per-frame `.timestamps.txt`, and per-camera HDF5 containing Tobii-derived `left_p` and `right_p` pupil size in mm with validity. This is a materially better candidate than MCFW-Gaze for the active ordinary-RGB / tracker waveform pair.

**Critical timing limitation:** the official DATASET.md explicitly states reliable synchronization only between Basler and eye tracker. Webcam timestamps are based on Video4Linux host timestamps and may be imprecise. Thus the source does NOT establish that webcam pupil waveforms satisfy Lucent's 100-ms lag gate. Basler is a non-consumer camera, so success there cannot be advertised as ordinary webcam success.

**Access:** https://ait.ethz.ch/eve says dataset available on request via Google Form; no participant bytes downloaded or inspected. License CC BY-NC-SA 4.0 with additional conditions. Never fabricate human results. Data access is the outstanding user-action blocker; do not send a request without consent.

**SCIENCE:** A documented native camera/reference pair exists, but webcam clock uncertainty is not independently bounded. Distinguish geometry/photometry failure from timing failure with Basler reference and webcam clock calibration. This is provenance, not a new theorem.

**PRODUCT:** Next data priority is EVE, not further MCFW reference-only loops. Run source-verified per-camera timing audits first; use Basler for a controlled ceiling and ordinary webcams for deployment-relevant evaluation. If webcam lag is unbounded, reject time-sensitive measurement until independently synchronized.

**Active kernel:** RGB pupil/anatomical-iris waveform vs synchronized same-eye pupil mm; held-out lower correlation, lag/amplitude/NRMSE, nuisance controls, >=75% coverage, >=8 untouched participants and device/lighting/glasses holdouts. No five-second fatigue claim.
