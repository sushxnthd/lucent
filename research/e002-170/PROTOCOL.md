# Lucent E002-170 — precommitted human five-second ocular-event observability check
Frozen 2026-10-14 **before** reading original Eyeblink8 annotation bytes. This is a secondary alternative-observable study; the primary pupil waveform kernel is unchanged. Prior E002-169 published video-level rates are already known. Do not call this untouched participant evaluation or novel mathematical theorem.

## Active primary kernel (unchanged)
Question: can a temporal ordinary-RGB pupil/full-anatomical-iris log-radius ratio recover independently timestamped valid eye-tracker pupil diameter (mm) in 5-second windows under unseen participant, device, lighting, and glasses conditions?
Exact pair: log(R_pupil/R_iris) from ordinary RGB frames vs synchronized left/right tracker pupil-mm waveform; demean and use predeclared bounded lag.
Frontier: original-human RGB masks and photometric stress evidence, but no qualified synchronized human waveform evaluation; EyeDentify folding and RGBE-Gaze source-schema risks unresolved for released records.
Scalar: participant-held-out Pearson r; secondary lag, amplitude ratio, NRMSE, coverage.
Strongest confounds: gaze/aperture/photometry and segmentation; clock drift, tracker schema/validity.
Decisive falsification: failure of frozen gates after participant/device/lighting/glasses holdout and nuisance-only controls.
Publishable threshold: >=8 unseen participants with >=3 eligible windows each; participant-bootstrap lower 95% r>0.30; >0.10 nuisance margin; |lag|<=100 ms, amplitude 0.5-1.5, NRMSE<=0.75, coverage>=75%, independent checker, mechanism prediction, prior-art audit.
Product threshold: >=75% accepted windows and calibrated abstention; no fatigue inference until reference gate clears.
Kill: repeated valid held-out failure at practical phone conditions; two blocked attempts on one data path => switch; three nondiscriminating runs => reformulate.

## This run's high-information alternate ocular test
Signal/reference: five-second RGB blink-event count (idealized detector) versus original human-annotated blink-ID onset events in EyeBlink8 (8 videos, 4 participants). We test the *reference event process*, not RGB detector performance.
Scalar: per-video Fano factor Var(N_5s)/E(N_5s), plus empirical zero-count window fraction versus Poisson exp(-mean count). Human annotations from the official author website; do not use paper summary rates as if they were new event observations.
Strongest confound: video-specific activity and correlated blink bursts, inaccurate 30fps assumption and missing/duplicated frame IDs. Blink-ID semantics and timestamps must be checked before computing metrics.
Decisive falsification: if annotations are missing, invalid, lack trustworthy frame/timestamp coverage, or cannot identify onsets, return NOT EVALUABLE; do not invent windows.
Data path: https://www.blinkingmatters.com/files/upload/research/eyeblink8.zip (official research page); license declared GPL3 at https://www.blinkingmatters.com/research. Download only on cloud CI, hash source bytes, inventory ZIP and parse original annotation files. Do not commit images/videos or redistribute dataset.
Eligibility: frame-ID based events require monotone integer frame IDs; positive blink IDs; a blink starts at first frame of a contiguous run with a positive blink ID. Preserve per-video frame counts, missing IDs, blink count and file hashes. Use original timestamp files when available and reliable; otherwise use 30fps only as explicitly conditional, reporting frame-index windows and uncertainty.
Frozen analysis: 150-frame nonoverlapping full windows starting from the first eligible frame of each video, onset-count assignment; compute mean count, population variance and Fano; per-video zero fraction, Poisson predicted zero fraction at that video's mean, pooled observed minus expected weighted by windows. Exclude partial windows; do not treat the eight videos as eight independent people. Sensitivity-only offsets of 30,60,90,120 frames, never as independent observations. No optimization of thresholds after outcomes.
Interpretation: descriptive deviation >0.10 in pooled zero fraction or Fano outside [0.67,1.50] is a *screening flag*, not formal statistical rejection. No valid population generalization with four people. Compare to E002-169 Poisson assumption; if non-Poisson, replace that assumption in product claims, not the general finite-window nonidentifiability.
Independent checker: separately recompute event counts from saved per-video onset lists, compare window totals and zero fractions. Save raw parsed events, derived windows, SHA256, full logs, negative/failed gates, both ledgers and CI status. Wildcard effort is bounded; do not contaminate primary frozen pupil-waveform evaluation.
