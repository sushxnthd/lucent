# E002-409 — frozen untouched-participant transfer test (S06)

**Frozen before writing or executing E002-409 analysis.** Date: 2026-10-24. Primary outcome is **EEG-marker association of a fixed image-motion surrogate**, not physical eyelid aperture or validation of E002-371.

## Data and no-leakage boundary
- Previously analyzed S01 and S19 are excluded. Evaluate **S06 only**, selected in advance as the smallest-numbered previously unused participant with a modest-size SSVEP archive in the same CC0 Eye-BCI collection. No other participant may be substituted if S06 fails.
- Source: Guttmann-Flury et al., *Scientific Data* 12, 587 (2025), Zenodo SSVEP record 18978288; `S06.zip` MD5 **8217203472f7393b03aa56102dbc9adc**. URL: https://zenodo.org/records/18978288/files/S06.zip?download=1. Verify checksum before decoding.
- If multiple session pairs exist, select the **lexicographically first session containing exactly one _sync.csv and one _phantom.avi**; do not choose by outcome. No image or EEG timestamps leave ephemeral execution.
- Use the exact previously frozen E002-397 Farneback flow parameters, eye ROI, background median subtraction, p80 residual magnitude, seven-frame event/control maximum, and existing digital nuisance transforms. No training, score inversion, feature tuning, or new ROI.

## Deterministic pairing
- Sort EEG-marked blink times in source order. For each, choose the nearest frame within 10 ms, requiring seven contiguous frame IDs and all six internal synchronized-time gaps <=20 ms.
- Match the first valid control among offsets **(+0.55, -0.55, +0.75, -0.75, +1.05, -1.05) seconds**, requiring distance >=0.35 s from every EEG marker and nonoverlapping seven-frame windows. Reject invalid windows without replacement. Require at least **15** event/control pairs for an evaluable transfer; if fewer, report feasibility failure and do not claim hypothesis success.
- Image transformations must be applied to both frames of each flow pair: clean; gain x0.7/x1.3; Gaussian blur sigma 2; white rectangular glare; whole-frame translation (+8,+6) pixels. Use the same E002-397 functions.

## Frozen predictions, no post-hoc adjustment
- H1: clean participant-level paired rank AUC >= **0.70** (EEG-marker windows have higher image motion).
- H2: blur sigma 2 causes clean-to-perturbed AUC loss <= **0.10**.
- H3: glare causes AUC loss <= **0.10**.
- H4: both global gains cause AUC loss <= **0.10**.
- H5: translation causes AUC loss <= **0.10**.
- Record exact pair counts, rejected reasons, all AUCs, and each hypothesis PASS/FAIL; CI success is computational verification, not scientific success. No threshold adjustment if a hypothesis fails.
- Independent checker must recompute all AUCs and H1–H5 from anonymous per-pair scores without using the primary AUC implementation. Test with synthetic controls and corrupted results.

## Decision rule
If clean association or any realistic nuisance robustness fails, **reject the frozen E002-397 motion feature as a transferable product observable**. Even if all H1–H5 pass, EEG markers do not establish physical aperture, a hard velocity envelope, shutter timing, or ordinary-camera no-hidden-closure certificates. Keep `ABSTAIN_UNCALIBRATED` for blink duration, PERCLOS, fatigue and E002-371 closure guarantees. No face/eye images, raw video or event timestamps may be committed or uploaded.

## Independent physical validation still required
Two independent blinded rater sheets for E002-407, calibrated shutter timing and geometry, a justified velocity envelope (not a finite-sample maximum), and untouched-device paired ordinary/high-speed capture. This experiment does not replace that study.
