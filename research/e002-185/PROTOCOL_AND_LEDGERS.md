# E002-185: independent paired-source eligibility, frozen before inspection
2026-10-14 UTC

**One active question:** Can ordinary frontal RGB pupil/iris log-radius waveforms recover simultaneous native-time Tobii pupil diameter on unseen participants, devices, lighting, and glasses, with prospective rejection of photometric/geometry failure?

**Exact pair:** unprocessed webcam frame exposure timestamps and RGB eye pixels versus same-eye native Tobii Pro Spectrum diameter (mm), validity and device timestamps. The Zenodo record describes 10 people measured by both systems but does NOT yet establish availability of face video, pupil diameter or synchronization.

**Frontier:** Brown EOTT raw pairing is documented but original archive access blocked; EOTT's WebGazer-derived CSV omits pupil diameter. EyeDentify labels fold tracker samples across seconds. js-mEye and MEYE demonstrate prior webcam pupillometry; no first-ever webcam claim.

**Scalar:** 95% participant-bootstrap lower bound of Pearson correlation for held-out five-second waveform windows. Lag search must use frozen, calibration-only alignment; no optimizing lag on test waveforms.

**Strongest confound:** target-local photometric response and blur, head/gaze foreshortening, and unbounded webcam-to-Tobii clock offset.

**Decisive falsification:** calibrated normalized RGB pupil signal does not beat geometry-only/brightness-only controls by >0.10 held-out r, or misses other frozen gates, after eligibility confirmed. Missing files or access failure is NOT physiological falsification.

**Publishable threshold (unchanged):** >=8 untouched participants and >=3 windows each; participant-bootstrap lower r>0.30; nuisance-control advantage >0.10; |lag|<=100 ms; amplitude ratio 0.5..1.5; NRMSE<=0.75; >=75% accepted coverage; independent checker, held-out device/lighting/glasses, and mechanism-predicted failure boundary. If only one webcam device, device-holdout gate is NOT CLEARED.

**Product threshold:** independently calibrated selective measurement, >=75% accepted coverage under held-out nuisance conditions; otherwise reject measurement. Never infer fatigue before these gates.

**Dataset eligibility:** original RGB face frames (not stimulus/screen videos), native-time pupil diameter with validity, same-participant pairing, documented synchronization, >=8 people, at least two devices or explicit device-holdout unavailable. Fail closed when missing.

**Kill/switch:** two blocked acquisition routes for this candidate require source switch. Three non-discriminating runs require kernel reformulation. No synthetic result substitutes for original-human validation.

SCIENCE ledger: new public candidate, not yet source-byte eligible. No waveform inference.
PRODUCT ledger: only a genuinely native-time paired source could unlock the measurement experiment. Until verified, no new Lucent build.
