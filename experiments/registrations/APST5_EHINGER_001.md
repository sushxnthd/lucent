# APST5-EHINGER-001 Preregistration

**Status: frozen before computing any APST-5 sequence-separation outcome from the Ehinger et al. luminance benchmark.**

## Objective

Independently test whether the asymmetric response structure that favored frozen E002 timing in the PsPM secondary analysis appears in a second public controlled-luminance dataset.

This test changes:

- participants;
- laboratory;
- luminance protocol;
- preprocessing pipeline;
- eye-tracking hardware.

It therefore cannot be a clean replication of APST5-HUMAN-PRF-001, but it can test whether an equal-exposure split sequence remains distinguishable when response kernels are estimated from independent human luminance dynamics.

## Dataset

Ehinger, Groß, Ibs & König (2019), public Figshare collection:

https://doi.org/10.6084/m9.figshare.c.4379810.v2

Primary table:

`lum_binned.csv`, DOI record `10.6084/m9.figshare.7635806.v1`.

The table contains event-locked normalized pupil responses for:

- 15 participants;
- EyeLink 1000 (`el`);
- Pupil Labs mobile eye tracker (`pl`);
- six experiment blocks;
- display levels 0, 64, 128, 192, 255;
- 100 binned time samples per condition.

The experiment code shows that the luminance task alternates black (0) with one of the four nonzero levels. Nonzero transitions remain for approximately 3 s; black periods remain approximately 7 s.

## Primary tracker

EyeLink 1000 only.

Pupil Labs is a secondary cross-device analysis.

## Fixed fit/validation split

For every subject and tracker:

- blocks 1–3: response-kernel estimation;
- blocks 4–6: held-out validation.

No block is reassigned based on response quality.

## Response kernels

### Brightening kernel

Use condition `lum=255`.

For each block:

1. baseline-center `pa_norm` by the median over (-0.9 le t <0) s;
2. retain (0 le t le 2.8) s, before the programmed return to black;
3. interpolate to a common 20 Hz grid.

The participant brightening kernel is the pointwise median of blocks 1–3.

### Darkening kernel

Use condition `lum=0`.

Because each block contains four returns to black and the released binned table averages those same-luminance events within block, the black response is treated as an empirical **average darkening kernel**.

For each block:

1. baseline-center over (-0.9 le t <0) s;
2. retain (0 le t le 4.5) s;
3. interpolate to the same 20 Hz grid.

The participant darkening kernel is the pointwise median of blocks 1–3.

This asymmetry is fixed before sequence analysis.

## Held-out response noise

On blocks 4–6, compare each brightening and darkening curve with its corresponding fit kernel over the available fixed support.

For subject (i), define

[
sigma_i
]

as the median held-out curve RMSE across the six validation curves (three brightening + three darkening).

Do not exclude a participant for poor fit.

## Five-second sequence prediction

Use the same 84 equal-exposure binary sequences as Lucent:

- ten 0.5 s segments;
- segment 0 fixed low;
- exactly three high segments among positions 1–9.

Every low→high transition adds the empirical brightening kernel.

Every high→low transition adds the empirical darkening kernel.

Because the brightening kernel is observed only to 2.8 s, its contribution is set to zero after 2.8 s rather than extrapolated.

All predicted waveforms are baseline-centered over the first 0.4 s.

## Separation score

Against contiguous comparator ((4,5,6)):

[
S_i(u)=
rac{mathrm{RMSE}(y_i(t;u),y_i(t;u_{contig}))}
{sigma_i}.
]

## Human design/test split

Sort participant IDs lexicographically, shuffle with NumPy RNG seed **20260930**, then:

- first floor(N/2): design participants;
- remainder: held-out participants.

The split is independent of response quality.

## Primary tests

### H1 — independent optimized timing

Select the sequence maximizing design-set P10 (S_i).

Support requires on held-out EyeLink participants:

- P10 (S>1.25);
- at least 90% with (S_i>1.25).

### H2 — frozen E002 timing

Evaluate ((1,2,8)) without modification.

Same support criterion:

- held-out P10 (S>1.25);
- at least 90% with (S_i>1.25).

## Secondary cross-device test

Without re-optimizing the sequence, evaluate the EyeLink-selected sequence and frozen E002 on the Pupil Labs responses using the same block split.

Report:

- P10/median (S);
- fraction (S>1.25);
- participant-wise correlation between EyeLink and Pupil Labs (S_i).

This is a mobile eye-tracker transfer test, not a smartphone-RGB test.

## Failure interpretation

If H2 fails, the positive PsPM directional secondary result does not independently replicate under this response-kernel construction.

If H2 passes but Pupil Labs fails, biological timing separation may be present while mobile-eye-camera measurement is insufficient.

If both EyeLink and Pupil Labs show strong separation, this is independent support that E002 timing can create human ocular waveforms distinguishable above repeat-response noise under controlled eye-tracking conditions.

## Claim boundary

Even a positive result does not validate:

- RGB front-camera pupil extraction;
- ordinary smartphone observability;
- fatigue/vigilance inference;
- linear superposition under E002.

Real E002 phone captures remain required.
