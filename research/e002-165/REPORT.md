# E002-165 — original-human RGB pixel provenance

Successful GitHub Actions run 38446057045, original Zenodo 20492528 source SHA256 `049df72454682c1c77c50c8236bb607919a6e333528bc2b89c567b625e459700` and upstream MD5 `a30eafe5e71cef9de1e08b91988f88b6` verified. Frozen E002-158 sample: 480 eligible original JPEG/mask pairs across 26 filename-defined recording groups. All 480 decode as RGB mode.

**Direct pixels:** 441/480 (91.875%) images have every decoded pixel exactly R=G=B; 39/480 (8.125%) have chromatic pixels. All 39 chromatic images are in groups `eye` (14), `eye 2` (4), `eye 3` (9), `eye 4` (12). The other 22 groups are wholly grayscale; no group mixes classes. The frozen >=95% monochrome gate **FAILED**, so do not call the whole dataset grayscale.

Cross-checked against the earlier 480-image E002-160 oracle-contrast results: 0/441 grayscale images have channel-dependent rank AUC; 3/39 chromatic images show any AUC difference; 36/39 chromatic images still have identical AUC across R,G,B,luminance. Descriptive median luminance AUC: 0.8946 grayscale vs 0.6954 chromatic; cannot interpret causally because recording groups are perfectly confounded with color class.

**Exact finite-sample identification law:** Let X be the 480x26 one-hot group matrix and c the color-class indicator. c equals the sum of the four indicator columns for the chromatic groups, so rank(X)=rank([X c])=26. A separate color effect is not identifiable from unrestricted recording-group fixed effects. This is a dataset design limitation, NOT a theorem about ocular physiology.

**SCIENCE:** The earlier pooled RGB-channel AUC equivalence cannot certify chromatic robustness. Source pixels and hashes are verified. Unresolved: camera sensor provenance, participant/device identities, physiological RGB/tracker waveform agreement.

**PRODUCT:** Remove claims of independent RGB color-channel or device transfer from this sample. Prioritize genuinely chromatic phone RGB paired with trustworthy timestamped eye-tracker recordings and held-out participant/device/lighting/glasses tests. No five-second fatigue claim.

**Kernel:** RGB pupil/full-iris log-ratio vs synchronized tracker pupil diameter; final scalar frozen correlation/lag/amplitude/NRMSE/coverage; strongest confounds photometry, eyelids, gaze, segmentation drift. Falsify via untouched held-out waveform failures under strongest nuisance controls. Publishable success requires independent checker, prior-art audit and unseen-condition prediction. Product threshold is calibrated useful accepted coverage. Kill or pivot after repeated valid held-out failure.

CI independent arithmetic checker PASS (480 images). Additional exact group-confounding checker PASS. CI artifact 11838745981, SHA256 `1d229f3fd8cf6dfe9fc08ae7a05a1ac68c3d699cc5db1e534fbf07f67a46cef8`; https://github.com/sushxnthd/lucent/actions/runs/38446057045. Original human images are not redistributed. No paired physiology or fatigue inference.
