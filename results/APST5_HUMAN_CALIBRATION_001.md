# APST5-HUMAN-CALIBRATION-001: Human Response and Device-Transfer Audit

**Status:** completed public-human evidence bridge. The confirmatory human probe test failed; secondary asymmetric-response and independent device-transfer analyses are retained with their original evidence levels.

## Executive result

Lucent now has public-human evidence for two pieces of the APST-5 measurement stack:

1. **Controlled luminance produces structured pupil dynamics whose direction matters.**
2. **A lower-cost dedicated video eye tracker can preserve those luminance-evoked dynamics relative to a concurrent EyeLink system, including person-specific residual structure.**

It still does **not** have the decisive evidence that an ordinary RGB phone front camera can resolve the E002 waveform, or that the waveform predicts vigilance/fatigue.

## 1. Confirmatory human-calibrated probe test — failed

APST5-HUMAN-PRF-001 used the public PsPM-AOB_UW controlled-luminance EyeLink dataset.

- 22 usable participants;
- participant-level design/held-out split;
- first-three / last-three repeated luminance presentations used for within-person fit/validation;
- 84 equal-exposure five-second timing patterns;
- frozen E002 sequence: **(1,2,8)**;
- comparator: contiguous **(4,5,6)**.

The preregistered primary model used one signed-normalized empirical response kernel for both brightening and darkening.

### Frozen E002 held-out result

- held-out P10 separation (S): **0.824**
- held-out median (S): **1.059**
- participants with (S>1.25): **27.3%**
- preregistered criterion: **NOT SUPPORTED**

The human-design-set winner, (1,2,3), also failed the same held-out criterion.

This failure is retained.

## 2. Directional pupil-response model — secondary positive result

The original preregistration explicitly listed a post-primary analysis separating brightening and darkening response functions. Its implementation was frozen after the primary failure and before computing the secondary result.

That change matters physiologically: pupil constriction and redilation are not assumed to be one symmetric signed kernel.

### Held-out result

The directional design-set search selected **exactly the frozen E002 sequence (1,2,8)**.

| Probe | held-out P10 S | held-out median S | participants S>1.25 | design rank |
| --- | ---: | ---: | ---: | ---: |
| **E002 (1,2,8)** | **1.264** | **1.836** | **90.9%** | **1** |
| SIM-005 (1,2,9) | 1.238 | 1.844 | 81.8% | 8 |
| evenly spaced (2,5,8) | 1.099 | 1.543 | 72.7% | 43 |

Under linear amplitude scaling, the held-out P10 threshold (S=1.25) corresponds to a modeled high/low luminance ratio of approximately **2.69×** for E002.

This is **secondary evidence**, not a rescue of the failed primary test.

## 3. Directional-model adequacy and camera-rate diagnostic

A second predeclared secondary audit tested whether the directional kernels could predict complete held-out two-transition trials: five seconds at the disc luminance followed by a return to background.

- participants with pooled held-out (R^2>0): **17/22 (77.3%)**
- median participant pooled (R^2): **0.3147**
- median participant median-trial (R^2): **0.0422**

The model is therefore useful but visibly imperfect.

When the frozen E002 waveform from this human-calibrated directional model was sampled at lower camera rates:

| Sampling rate | held-out P10 S | median S | S>1.25 |
| ---: | ---: | ---: | ---: |
| 50 Hz | **1.264** | 1.840 | 90.9% |
| 30 Hz | **1.263** | 1.838 | 90.9% |
| 24 Hz | **1.263** | 1.837 | 90.9% |

Thus simple temporal downsampling from 50 Hz to ordinary video rates does not erase the predicted waveform separation. RGB segmentation and auto-exposure are separate problems.

## 4. Independent lower-cost eye-tracker transfer — preregistered positive result

EHINGER-DEVICE-TRANSFER-001 used the public Ehinger et al. dataset with **concurrent EyeLink 1000 and Pupil Labs** recordings during controlled screen-luminance changes.

Frozen design:

- **15 participants**
- calibration blocks 1–3
- held-out blocks 4–6
- fixed common response window 0–2.8 s
- five luminance codes
- participant-specific affine calibration learned only on blocks 1–3

### Held-out primary result

- Fisher-z macro-r: **0.9974**
- participant-bootstrap 95% CI: **[0.9948, 0.9987]**
- participants with held-out (r>0.70): **15/15**
- median normalized RMSE: **0.0217**
- frozen criterion: **SUPPORTED**

Because Pearson correlation is invariant to positive affine calibration, the calibrated and uncalibrated correlations are essentially identical; the calibration primarily affects absolute error.

## 5. Person-specific negative control — secondary positive result

The primary cross-device correlation could be dominated by the generic luminance-locked waveform shared by everyone.

A post-primary secondary diagnostic therefore subtracted a **leave-one-person-out group waveform** separately for each device, then compared the remaining subject-specific residual dynamics.

Observed same-person residual transfer:

- Fisher-z macro-r: **+0.8910**

Mismatched-participant derangement null:

- median macro-r: **-0.0551**
- 95% interval: **[-0.1941, +0.0846]**
- one-sided empirical (p=0.000100) over 10,000 derangements

So the lower-cost-device agreement is not explained only by a generic stimulus-locked average waveform.

Again, this is secondary specificity evidence.

## Evidence ledger

| Claim | Evidence level | Status |
| --- | --- | --- |
| one symmetric human response kernel makes E002 clearly observable | preregistered held-out test | **failed** |
| brightening/darkening asymmetry materially changes sequence ranking | post-primary frozen secondary | **supported** |
| directional human-calibrated model favors frozen E002 timing | post-primary frozen secondary | **supported** |
| directional superposition predicts unseen repeated transitions well | secondary model-adequacy audit | **mixed/moderate** |
| predicted E002 separation survives 24/30 Hz sampling | secondary sampling diagnostic | **supported** |
| lower-cost dedicated video eye tracker preserves luminance pupil waveforms vs EyeLink | preregistered held-out test | **supported** |
| person-specific response deviations transfer across those dedicated devices | secondary permutation negative control | **supported** |
| ordinary RGB phone resolves E002 pupil dynamics | prospective E002 | **open** |
| E002 dynamics predict vigilance/fatigue | prospective human state study | **open** |

## What changed scientifically

The earlier APST-5 simulations assumed a delayed asymmetric pupil model. The new public-human analysis gives that modeling choice empirical support: collapsing brightening and darkening into one signed response kernel fails badly enough to reverse the engineering conclusion, while a direction-specific model recovers a held-out timing preference that independently lands on the already frozen E002 sequence.

That coincidence is interesting because **E002 was frozen before this dataset was analyzed**.

It is still not confirmatory evidence for E002. The directional analysis was secondary after the symmetric primary failed.

The independent Ehinger result strengthens a different part of the chain: luminance-evoked pupil waveforms and participant-specific deviations can survive a move from laboratory EyeLink measurement to a lower-cost dedicated video tracker.

## Current bottleneck

The evidence chain now reaches the final hardware gap:

[
	ext{controlled screen input}
ightarrow
	ext{human pupil dynamics}
ightarrow
	ext{lower-cost video eye tracking}
ightarrow
oxed{	ext{ordinary RGB phone?}}
]

E002 is the experiment that fills or kills that box.

Its synchronized phone instrument, frozen condition order, processing pipeline, manifest validation, and photometric/geometry negative controls are already implemented.

## Claim boundary

None of these results establishes:

- ordinary RGB smartphone pupil measurement;
- E002 biological specificity on a phone;
- fatigue/vigilance prediction;
- clinical use;
- a universal optimal probe timing.

The strongest allowed statement is:

> Public human controlled-luminance data support asymmetric pupil dynamics relevant to APST-5 sequence design, and independent concurrent measurements show that those luminance-evoked dynamics—including person-specific deviations—can transfer from EyeLink to a lower-cost dedicated video eye tracker. The ordinary-phone step remains prospectively untested.
