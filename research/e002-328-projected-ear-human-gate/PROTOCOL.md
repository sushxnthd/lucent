# Frozen prospective human evaluation (2026-10-20)

1. SIGNAL/REFERENCE: RGB six-landmark EAR, per-participant open-eye normalized, versus independently manually adjudicated NIR/EEG-assisted blink-event labels from synchronized 30-fps capture (candidate mEBAL2). Event labels are NOT continuous aperture or millisecond timing truth.
2. FRONTIER: Soukupova & Cech (2016) EAR; Fogelton & Benesova (2016, 2018) blink/completeness; Daza et al. (2024) mEBAL2; Zhao et al. (2025) RGBE-Gaze. No novelty claim.
3. METRIC: CLOSED/OPEN/ABSTAIN coverage at closure-proxy threshold theta=0.30; event-level F1, recall, no-blink FPR, abstention and landmark-ball coverage. Participant-level bootstrap CIs.
4. CONFOUND: gaze/head pose, glasses, auto-exposure, blur, occlusion, illumination, reference timing, device shift.
5. MODEL: I_j=Q_j[integral w_j(t)*(L_j(t)*R(c(t),g(t),pose(t),glasses,person)+B_j(t))dt+noise]. Projected landmarks p_hat_jk=p_jk+delta_jk, ||delta_jk||<=eps_j. NIR/EEG/manual event label z_j is an annotation functional, not continuous anatomical truth.
6. FALSIFICATION: any unseen failure of calibrated landmark error coverage, timing eligibility, strong nuisance controls, or second-device transfer defeats anatomical/clinical claims.
7. FROZEN MECHANISM PREDICTION: For a=b=6 px, w=30 px, open EAR=0.30, theta=0.30, strict closure certificate changes at eps=15/121 px; this is a synthetic instrument prediction, not human evidence.
8. UNTOUCHED HUMAN TEST: prefreeze dataset checksums, subject IDs and annotations; deterministic participant 60/20/20 calibration/validation/test split by salted subject hash. Train/calibrate only on calibration subjects; leave test untouched until protocol frozen. Report glasses and illumination strata. If only one acquisition device, cross-device holdout is NOT POSSIBLE and must use a second independent dataset.
9. PUBLICATION GATES: verified synchronized reference, >=95% unseen empirical landmark-ball coverage, >=90% event recall, >=0.85 event F1, <=5% no-blink FPR, <=30% abstention, <=0.10 F1 gap for glasses/lighting, independently replicated second-device boundary crossing. These are prospective targets, NOT achieved results.
10. PRODUCT: permit only research-grade interval EAR with abstention; reject unrestricted pupil-waveform, blink timing, PERCLOS and five-second fatigue inference.

MANDATORY CONTROLS: geometry-only eye width/pose; brightness-only crop intensity/exposure; missingness-only mask/occlusion; temporal-smoothness-only previous-state/interpolation. Compare raw EAR, normalized EAR and interval EAR. Black-box secondary only. Stratify glasses, lighting, gaze, blur, missingness, participant and device.

FREEZE: use native timestamps and exposure durations, verify clock offset and drift, record every exclusion and file SHA256. Human landmark annotations must be independent of detector training. Never use test data to choose epsilon or thresholds. Only evaluate event labels within +/- one RGB frame for frame-level event scoring; no subframe physiological-lag claims.

HUMAN RESULTS: NOT RUN. Participant holdout: NOT RUN. Device holdout: NOT RUN. Prospective human boundary: NOT RUN.
