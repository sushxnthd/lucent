# Lucent E002-256 — pooled covariance is not rapid waveform observability

**Active question:** Can ordinary RGB, with geometry/photometry normalization and independently certified exposure time, recover a same-eye pupil waveform above frozen correlation/lag/amplitude/NRMSE gates on unseen participants/devices/lighting/glasses?

- **Signal/reference:** prospective Lucent pupil-to-iris normalized RGB radius vs same-eye native-time Tobii pupil diameter. This secondary run analyzes a third-party RGB pupil regressor vs Tobii labels, aggregated by participant.
- **Frontier:** E002-255 established that high pooled r hides lower per-participant r; E002-254 found exposure-clock certification missing. No prospective five-second waveform.
- **Scalar:** primary held-out participant-bootstrap lower 95% Pearson r with frozen lag, amplitude, NRMSE, rejection and nuisance gates. This run: participant-centered r and fraction of pooled covariance from between-participant means.
- **Strongest confound:** participant identity and eye scale; stimulus-driven illumination/pupil co-variation, gaze and exposure timing.
- **Decisive falsification:** synchronized untouched human waveform fails gates or brightness/geometry placebos match ocular signal.
- **Publishable threshold:** untouched >=8-participant feasibility with powered participant/device/lighting/glasses holdouts, independent replay, nuisance controls and mechanism-derived prediction; NOT MET.
- **Product threshold:** >=75% prospectively accepted accurate quantitative windows with calibrated uncertainty; NOT MET.
- **Kill:** two blocked dataset attempts force switch; three nondiscriminating primary runs or prospective failure reformulate/kill. No fatigue claim.

Exact identity (standard covariance decomposition): total cross-deviation sum equals sum_g (n_g-1)r_g s_xg s_yg plus sum_g n_g (xmean_g-xmean)(ymean_g-ymean). Sample SDs use n_g-1. This is established statistics, not a new theorem.

This is an audit of published human-derived aggregates, not untouched raw RGB, not a within-session test, not an independently synchronized physiological result.
