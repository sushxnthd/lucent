# APST5-HUMAN-PRF-001 Preregistration

**Status: frozen before any participant-level probe-separation outcome is computed.**

## Objective

Test APST-5's most basic biological-observability prediction using independent human controlled-luminance data **without relying on Lucent's hand-specified pupil surrogate**.

Question:

> if each person's pupil step response is estimated directly from real EyeLink luminance transitions, should the frozen E002 split sequence produce a waveform distinguishable from a matched-exposure contiguous pulse by more than ordinary within-person response noise?

This is not a state/fatigue analysis. It is a human-calibrated waveform-observability test.

## Dataset

PsPM-AOB_UW:

https://doi.org/10.5281/zenodo.8239465

Released luminance data:

- 500 Hz left/right pupil diameter in mm;
- 24 five-second disc presentations per available subject;
- five-second return to medium-gray background after each disc;
- four disc luminance levels, six presentations each;
- subject 06 luminance pupil file missing due documented technical failure.

## Luminance values

Use the associated paper's measured luminances:

- background: 46.10 cd/m2;
- black disc: 33.50 cd/m2;
- dark-gray disc: 36.70 cd/m2;
- light-gray disc: 60.70 cd/m2;
- white disc: 84.10 cd/m2.

Released Cogent stimulus codes and pupil event markers will be mapped mechanically from matching event order before analysis. No code may be relabeled based on pupil response direction.

## Pupil preprocessing

For each eye:

1. retain finite pupil diameter values >0;
2. linearly interpolate gaps no longer than 250 ms;
3. low-pass filter at 4 Hz;
4. downsample to 50 Hz.

Combine eyes by samplewise mean when both are available and use the available eye when only one is valid.

No outcome-driven filtering threshold may be introduced.

## Transition responses

For every non-initial luminance transition:

1. require at least 80% finite/interpolated pupil support from -0.5 s to +4.5 s;
2. baseline pupil by the median from -0.4 to 0 s;
3. define signed log-luminance step

[
a_j=log(L_{after}/L_{before});
]

4. define the normalized step response

[
r_j(t)=rac{p_j(t)-p_{baseline,j}}{a_j}.
]

Positive and negative luminance steps are therefore put on a common signed scale.

## Balanced within-person train/validation split

Each non-background disc level is presented six times.

For each subject and disc level:

- the first three disc presentations and their subsequent returns-to-background belong to **fit**;
- the final three presentations and returns belong to **held-out validation**.

This produces 24 training transitions and 24 validation transitions when all trials are usable.

## Empirical pupil step-response function

For each participant, estimate

[
hat h_i(t)
]

as the pointwise median of all usable normalized **fit** transition responses.

No parametric latency or time-constant model is fitted in the primary analysis.

## Held-out waveform adequacy

For every held-out transition (j), predict:

[
hat p_j(t)-p_{baseline,j}
=
a_j hat h_i(t).
]

Report:

- held-out waveform RMSE;
- held-out waveform (R^2);
- median per-transition RMSE.

Do not exclude a participant because held-out prediction is poor.

## Equal-exposure APST probe space

Exactly the existing APST5 design space:

- 5 s total;
- ten 0.5 s segments;
- initial segment fixed low;
- exactly three high segments among positions 1–9;
- 84 possible sequences.

For this empirical-PRF analysis, use a two-level luminance step defined by the E002 screen-content design only through **log-luminance contrast**. The absolute low/high pair is common to every candidate, so sequence ranking depends on timing rather than exposure magnitude.

The primary waveform calculation uses a normalized low/high log-luminance step of ±1. Results therefore report separation in units of empirical response noise rather than millimeters.

## Predicting a sequence from the empirical step response

Every change in binary probe level is treated as a signed luminance step.

For participant (i):

[
y_i(t;u)=
sum_k
Delta log L_k,
hat h_i(t-t_k).
]

Superposition is an explicit LTI approximation.

The five-second predicted waveform is baseline-centered over the first 0.4 s.

## Participant-level noise scale

For participant (i), define

[
sigma_i
]

as the median RMSE of held-out normalized transition responses around their predicted waveform.

This is estimated only from held-out real human transitions and is not tuned per candidate probe.

## Human-calibrated separation score

Against the same matched-exposure contiguous control used by E002, define

[
S_i(u)=
rac{mathrm{RMSE}(y_i(t;u),y_i(t;u_{contig}))}
{sigma_i}.
]

Higher values mean the timing-induced waveform difference is larger than ordinary held-out transition-response error.

## Human design/test split

After subject IDs are known:

1. sort IDs lexicographically;
2. shuffle with NumPy RNG seed **20260930**;
3. first floor(N/2) = probe-design participants;
4. remainder = held-out participants.

Subject 06 is absent by documented technical failure and is not imputed.

## Primary tests

### H1 — empirically optimized timing survives held-out people

Select the sequence maximizing **P10 (S_i)** on design participants.

On held-out participants, support requires:

- held-out P10 (S>1.25); and
- at least 90% of held-out participants have (S_i>1.25).

### H2 — frozen E002 timing survives held-out people

Evaluate frozen E002 sequence (1,2,8) without modification.

Support requires the same frozen criterion:

- held-out P10 (S>1.25); and
- at least 90% of held-out participants have (S_i>1.25).

Comparator:

- contiguous high segments (4,5,6), exactly as E002.

## Secondary analyses

After H1/H2:

- rank of (1,2,8) among all 84 sequences;
- rank of APST5-SIM-005 sequence (1,2,9);
- evenly spaced (2,5,8);
- separate brightening-derived and darkening-derived empirical step responses;
- nonlinear-superposition diagnostic by comparing predicted two-transition trial waveforms with actual ten-second disc-on/off trials;
- sensitivity to 30 Hz and 24 Hz resampling.

These do not replace H1/H2.

## Failure rules

If held-out step-response prediction is poor for most participants, the LTI bridge is weak and sequence-separation results are exploratory.

If H1 passes but H2 fails, timing matters in human-calibrated dynamics but E002-v1 is not supported.

If H2 passes, the strongest allowed claim is:

> under an LTI approximation calibrated from independent human EyeLink luminance responses, E002's equal-exposure split timing is predicted to create a waveform difference larger than held-out within-person response error.

## Claim boundary

Even a positive H2 does not establish:

- that an RGB phone camera can resolve the waveform;
- fatigue or vigilance sensitivity;
- active-vs-passive state prediction;
- exact validity of linear superposition under the E002 stimulus.

Real E002 phone capture remains required.
