# EHINGER-DEVICE-TRANSFER-001 Secondary Specificity Plan

**Status:** written after the preregistered primary device-transfer result. This is secondary and cannot replace or strengthen the primary criterion retroactively.

## Question

The primary held-out EyeLink/Pupil Labs waveform correlations are extremely high. Because both devices observe the same luminance stimulus, high correlation could be dominated by a generic stimulus-locked group waveform rather than preservation of person-specific response structure.

This diagnostic asks whether **within-person deviations from the group waveform** transfer across devices.

## Frozen held-out data

Use exactly the primary EHINGER-DEVICE-TRANSFER-001 held-out set:

- participants passing the primary fixed cell rules;
- blocks 4–6 only;
- luminance codes 0,64,128,192,255;
- 0–2.8 s post-onset window;
- released `pa_norm`;
- exact paired binned time support.

No calibration refit.

## Leave-one-person-out residualization

For each held-out row identified by block × luminance × time:

1. for EyeLink, subtract the mean EyeLink value of all **other** participants at that same block/luminance/time;
2. for Pupil Labs, subtract the mean Pupil Labs value of all **other** participants at the same block/luminance/time.

This yields participant-specific residual waveforms without using that participant in the reference mean.

For each participant, concatenate all held-out residual rows and compute Pearson correlation:

[
r_i^{resid}=corr(e_{EL,i},e_{PL,i}).
]

Aggregate with Fisher-z macro-r.

## Mismatched-participant negative control

Use NumPy RNG seed 20260930.

For 10,000 permutations, randomly permute Pupil Labs participant labels while rejecting fixed points. Pair each participant's EyeLink residual with another participant's Pupil Labs residual on identical block/luminance/time rows.

Compute the Fisher-z macro-r for every permutation.

Report:

- observed same-person residual macro-r;
- permutation median and 95% interval;
- one-sided empirical p-value = fraction of permuted macro-r >= observed.

## Interpretation

Evidence for person-specific cross-device transfer is present only if:

1. observed residual macro-r > 0; and
2. empirical permutation p < 0.05.

This is an exploratory specificity diagnostic, not a confirmatory Lucent breakthrough criterion.

## Claim boundary

Even a strong residual result concerns dedicated EyeLink/Pupil Labs systems under laboratory screen stimulation. It does not establish ordinary RGB phone pupil tracking or state prediction.
