# APST5-HUMAN-PRF-001 Secondary Adequacy/Sampling Plan

**Status:** written after the failed preregistered primary and after the directional-kernel secondary result. This is a diagnostic completion of analyses already listed in the original preregistration; it cannot convert the primary H1/H2 failure into a confirmatory success.

## A. Two-transition superposition diagnostic

### Purpose

The directional secondary model predicts an APST sequence by linearly superposing brightening and darkening kernels. The public PsPM luminance trials contain an actual five-second disc presentation followed by a return to background, so they provide a direct held-out two-transition check.

### Frozen split

Use exactly the existing first-three / last-three presentation split per disc level.

Directional kernels are estimated from **fit** transitions only.

Only **validation** disc presentations are used for this diagnostic.

### Observed validation waveform

For each validation disc presentation:

1. extract combined-eye pupil diameter from -0.4 s before disc onset through +9.5 s;
2. baseline by the median from -0.4 to 0 s;
3. require >=80% finite/interpolated support;
4. retain the waveform in millimeters.

### Predicted waveform

Let the disc-on signed log-luminance step be

[
a=log(L_{disc}/L_{background}).
]

Predict

[
hat y(t)=a h_{dir(a)}(t) - a h_{dir(-a)}(t-5s),
]

where the second term is active only after the return-to-background transition and each directional kernel is the participant-specific fit-set kernel from APST5-HUMAN-PRF-001 Secondary.

No parameter is refit on validation trials.

### Metrics

Per validation trial:

- RMSE in mm;
- R2 against the baseline-centered observed waveform.

Per participant:

- pooled validation R2;
- median trial R2;
- median trial RMSE.

Aggregate:

- median participant pooled R2;
- fraction of participants with pooled R2 > 0;
- median participant trial R2.

These are model-adequacy diagnostics, not an APST5 success criterion.

## B. Camera-rate sensitivity

Using the already computed directional participant kernels and frozen design/test participant split, evaluate the frozen E002 sequence (1,2,8) at:

- 50 Hz reference;
- 30 Hz;
- 24 Hz.

For each rate, linearly sample the five-second candidate/control predicted waveforms on a uniform camera grid and compute the same participant separation score

[
S_i=mathrm{RMSE}(candidate,control)/sigma_i^{dir}.
]

The held-out outputs are:

- P10 S;
- median S;
- fraction S>1.25.

No sequence re-optimization is performed at 30 or 24 Hz.

## Interpretation

A positive superposition diagnostic would strengthen the directional LTI bridge. A failure would make the directional E002 separation result substantially less persuasive.

Camera-rate stability only addresses sampling cadence under the EyeLink-derived model; it does not establish RGB-phone pupil observability.
