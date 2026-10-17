# E002-257 — Eye-specific absolute-scale bias and remote replay

**Single active question (unchanged):** Does geometry/photometry-normalized ordinary-RGB pupil/iris temporal ratio agree with independently synchronized same-eye Tobii pupil diameter under participant/device/lighting/glasses holdouts, with predictable failure?

- **Exact signal/reference:** Future Lucent RGB dimensionless pupil/iris waveform vs native-time same-eye Tobii diameter. This run uses only a third-party model's predicted diameter vs Tobii reference, released as participant aggregates.
- **Frontier:** E002-256 showed between-participant covariance dominates pooled r. Here test absolute-scale bias per eye and repair deterministic E002-256 CI output-path mismatch.
- **Primary scalar:** held-out participant-bootstrap lower Pearson waveform r, plus frozen lag/amplitude/NRMSE and nuisance gates. Secondary scalar: paired right-minus-left raw SD-normalized RMSE.
- **Strongest confound:** eye-specific checkpoint/label/crop bias, exposure and illumination, gaze geometry, glasses.
- **Decisive falsification:** independently synchronized untouched human waveform fails gates or does not outperform brightness/geometry placebo; eye asymmetry fails independent replication.
- **Publishable threshold:** >=8 untouched synchronized participants, participant/device/lighting/glasses holdouts, independent checker, mechanism prediction, prior-art audit. Not met.
- **Product threshold:** >=75% prospectively admitted accurate windows. Not met; exploratory NRMSE <=0.7 is not a product gate.
- **Kill:** two blocked attempts on a dataset path force switch; three nondiscriminating primary runs reformulate; prospective measurement failure kills quantitative pupil claim.

Exact finite-sample identity: RMSE² = bias² + (n-1)/n (sd_pred²+sd_ref²-2*r*sd_pred*sd_ref). This is established moment algebra, not a novel theorem. Offset oracle uses reference-informed calibration and is not deployable as-is. No fatigue inference.
