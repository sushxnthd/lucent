# APST5-HUMAN-CALIBRATION-001 Preregistration

**Status: frozen before inspecting any participant-level luminance-response outcome.**

## Objective

Replace Lucent's hand-specified pupil-parameter population with **human-calibrated dynamics** estimated from an independent public controlled-luminance experiment.

The question is:

> after fitting the existing Lucent delayed/asymmetric pupil surrogate to real human luminance responses, does the equal-exposure timing advantage survive on held-out people?

This is a bridge between APST5-SIM-001/005 and prospective E002. It is not a phone-camera experiment and it is not a fatigue-state validation study.

## Public dataset

PsPM-AOB_UW, Zenodo DOI:

https://doi.org/10.5281/zenodo.8239465

Associated protocol:

Abivardi et al. (2023), *Acceleration of inferred neural responses to oddball targets in an individual with bilateral amygdala lesion compared to healthy controls.*

The controlled illuminance task used:

- 23 healthy controls plus one lesion participant;
- EyeLink 1000 pupil recording;
- medium-gray background: 46.10 cd/m2;
- four five-second center-disc levels:
  - black: 33.50 cd/m2;
  - dark gray: 36.70 cd/m2;
  - light gray: 60.70 cd/m2;
  - white: 84.10 cd/m2;
- five sessions;
- 24 trials/session;
- five seconds disc-on followed by five seconds background.

Only healthy controls enter the primary analysis.

## Input signal

Use the paper/dataset's combined/preprocessed pupil series if such a series is explicitly supplied.

If only raw left/right pupil series are available, reproduce the paper's stated preprocessing without outcome-dependent tuning:

- invalid-pupil / implausible-change rejection;
- removal around gaps;
- low-pass filtering at 4 Hz;
- interpolation only across gaps <=250 ms;
- combine eyes as in the supplied/PsPM implementation.

This conditional choice is based only on data availability, not on probe-ranking results.

## Existing Lucent surrogate

Fit the same five-parameter family used in APST5-SIM-001:

[
	heta=(b,g,ell,	au_c,	au_d),
]

where:

- (b): baseline pupil size;
- (g): log-luminance gain;
- (ell): response latency;
- (	au_c): constriction time constant;
- (	au_d): dilation time constant.

For an actual luminance (L), the equilibrium response is

[
p^*(L)=mathrm{clip}{b-glog(L/20),2,8}.
]

The delayed equilibrium is then followed with separate constriction and dilation time constants exactly as in `src/lucent/active_probe.py`.

No new dynamic component may be added after seeing fit quality.

## Participant-level fitting

For each healthy control:

1. order illuminance-task sessions chronologically;
2. fit (	heta) on sessions 1–3;
3. evaluate waveform prediction on sessions 4–5;
4. report held-out RMSE and (R^2);
5. refit (	heta) on all five sessions only after the held-out fit metrics are frozen, for use in population probe-design analysis.

Do not exclude a participant because the surrogate fits poorly. Exclude only missing/corrupt participants for whom the required luminance event/pupil data cannot be reconstructed.

## Parameter bounds

Use the existing Lucent biological-surrogate bounds:

- baseline: [4.0, 6.5] mm;
- gain: [0.30, 1.30];
- latency: [0.12, 0.45] s;
- constriction tau: [0.20, 0.90] s;
- dilation tau: [0.60, 2.20] s.

If the public pupil series is normalized rather than millimeters, introduce exactly one participant-specific affine pupil-scale nuisance (offset + positive scale) during waveform fitting, but retain the same dynamic-parameter bounds. The nuisance parameters are not used as state parameters in probe ranking.

## Human design/test split

After healthy subject IDs are known:

1. sort IDs lexicographically;
2. shuffle them with NumPy RNG seed **20260930**;
3. assign the first floor(N/2) participants to the design set;
4. assign the remainder to the held-out test set.

The split is participant-level and does not depend on pupil dynamics or fit quality.

## Probe design space

Exactly the APST5-SIM-001 equal-exposure space:

- total duration: 5 s;
- ten 0.5 s segments;
- segment 0 fixed low;
- exactly three high segments among positions 1–9;
- 84 possible probes;
- low/high display levels unchanged from APST5-SIM-001 for ranking.

Comparators:

- best contiguous three-high-segment probe selected on the human design participants;
- evenly spaced (2,5,8);
- frozen E002 split sequence (1,2,8);
- APST5-SIM-005 robust-search sequence (1,2,9).

## Information metric

Estimate the empirical parameter covariance from **design participants only**.

For each fitted participant and probe:

1. compute the finite-difference Jacobian of the five-parameter surrogate;
2. form the Fisher information under the existing measurement-noise assumption;
3. combine with the design-set empirical parameter prior;
4. compute D-optimal information gain over dynamic parameters ((g,ell,	au_c,	au_d)).

No test participant is used to select a probe or covariance prior.

## Primary held-out tests

### H1 — human-calibrated design advantage

Choose the equal-exposure probe with maximum mean information gain on design participants.

On held-out participants compare it with the design-selected best contiguous probe.

Support requires:

1. mean held-out information gain is greater for the optimized probe;
2. paired participant bootstrap 95% CI for the difference is entirely above zero.

Bootstrap: 10,000 resamples, seed 20260930.

### H2 — frozen E002 survives human calibration

Without changing E002-v1, compare frozen (1,2,8) against the same design-selected contiguous control on held-out participants.

Support requires:

1. mean held-out information gain is greater for E002;
2. paired participant bootstrap 95% CI is entirely above zero.

## Secondary analyses

Only after H1/H2 are frozen:

- rank of (1,2,8) among all 84 probes;
- rank of (1,2,9);
- participant-level win fraction;
- sensitivity to measurement-noise SD;
- rerun on only participants with positive held-out waveform (R^2);
- compare human-fitted parameter distribution with the original synthetic population.

These do not replace H1/H2.

## Failure interpretation

If H1 fails, the original equal-exposure timing advantage is not robust to this human-calibrated dynamic population under the current model.

If H1 passes but H2 fails, probe timing matters but the frozen E002 sequence is not supported by this calibration dataset.

If the five-parameter surrogate predicts sessions 4–5 poorly for most participants, probe-ranking claims must be described as model-misspecified and exploratory even if H1/H2 are numerically positive.

## Claim boundary

A positive result would establish:

> Lucent's nontrivial equal-exposure timing advantage persists when its pupil-dynamic parameter population is estimated from independent human controlled-luminance data.

It would **not** establish:

- smartphone observability;
- fatigue/vigilance prediction;
- biological validity of the RGB pupil extractor;
- superiority of active probing over passive sensing in humans.
