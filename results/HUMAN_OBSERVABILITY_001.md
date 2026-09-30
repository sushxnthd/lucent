# HUMAN-OBSERVABILITY-001: Human-Calibrated APST-5 Timing

## Status

**Independent human-controlled-luminance support for the biological waveform-separation premise of APST-5.**

This is the strongest pre-phone evidence in Lucent so far.

It does **not** establish smartphone RGB observability or fatigue-state prediction.

## Evidence sequence

Lucent's original APST-5 timing was discovered in a hand-specified delayed/asymmetric pupil surrogate.

The next question was whether that timing survives when the response dynamics come from real humans rather than Lucent's synthetic population.

Three analyses now answer different parts of that question.

### 1. PsPM primary single-kernel model — failed

APST5-HUMAN-PRF-001 used public controlled-luminance EyeLink data from 22 usable participants.

A single signed-normalized pupil step-response kernel was estimated per participant and tested on held-out luminance transitions.

The preregistered human-calibrated observability criterion was **not supported**.

Frozen E002 (1,2,8):

- held-out P10 separation: **0.824**
- held-out median separation: **1.059**
- held-out participants above S=1.25: **27.3%**
- design rank: **2/84**

This result is retained.

The single-kernel approximation also fit held-out pupil transitions only modestly; 6/22 participants had non-positive held-out waveform R².

### 2. PsPM directional secondary — E002 selected

The preregistration had already identified constriction/dilation asymmetry as a secondary analysis.

A post-primary implementation froze separate empirical kernels for:

- brightening / constriction;
- darkening / redilation.

This substantially changed the result.

On the same fixed participant design/test split, the design-set search selected **exactly the frozen E002 sequence (1,2,8)** as rank **1/84**.

Held-out E002:

- P10 S: **1.264**
- median S: **1.836**
- participants with S>1.25: **90.9%**
- minimum log-luminance contrast implied by the P10 threshold: **0.989**
- corresponding high/low luminance ratio: **2.69×**

Because this directional analysis was secondary and followed the failed primary outcome, it is evidence about model structure rather than a confirmatory rescue.

### 3. Independent Ehinger replication — preregistered positive

APST5-EHINGER-001 was frozen before sequence outcomes were computed on an independent controlled-luminance dataset.

It changed the:

- participants;
- laboratory;
- luminance protocol;
- preprocessing pipeline;
- eye-tracking hardware.

Primary tracker: EyeLink.

Usable EyeLink participants: **13**
- design: 6
- held-out: 7

The independently optimized design was **(1,3,4)**.

Frozen E002 was rank **5/84** on the design set.

On held-out EyeLink participants:

| Probe | Held-out P10 S | Median S | S>1.25 |
| --- | ---: | ---: | ---: |
| independently selected (1,3,4) | **6.301** | 10.624 | 100% |
| **frozen E002 (1,2,8)** | **5.395** | **9.180** | **100%** |
| SIM-005 (1,2,9) | 5.713 | 9.479 | 100% |
| evenly spaced (2,5,8) | 3.001 | 5.699 | 100% |

Both preregistered H1 and H2 were **SUPPORTED**.

## Cross-device transfer

The Ehinger experiment simultaneously recorded Pupil Labs, a mobile infrared eye tracker.

The EyeLink-selected sequence and frozen E002 were transferred to Pupil Labs without reoptimization.

Frozen E002 on held-out Pupil Labs participants:

- P10 S: **5.615**
- median S: **9.544**
- S>1.25: **100%**
- participant-wise EyeLink↔Pupil-Labs separation correlation: **r=0.859**

This is useful evidence that the timing structure is not specific to one laboratory eye tracker.

It is **not** equivalent to an ordinary RGB smartphone front camera.

## What changed scientifically

The human data indicate that **constriction and redilation asymmetry matters**.

A single symmetric/signed-normalized response kernel did not support frozen E002 strongly enough.

When brightening and darkening dynamics were modeled separately:

- E002 became the best of 84 sequences in the PsPM design data;
- it crossed the held-out PsPM engineering separation threshold;
- it independently passed a preregistered held-out test in Ehinger;
- the same Ehinger timing transferred strongly to a second simultaneous eye tracker.

This converges with Lucent's original mechanistic model, which already used separate constriction and dilation time constants.

## Strongest defensible claim

> **Across two independent public human controlled-luminance datasets, modeling pupil constriction and redilation separately makes Lucent's frozen equal-exposure E002 split timing highly competitive; in an independently preregistered Ehinger analysis, E002 produced held-out waveform separation well above repeat-response noise and transferred to a simultaneous mobile eye tracker without reoptimization.**

This is a measurement-design result.

## What it does not prove

It does not prove that:

- a normal front-facing RGB phone camera can resolve the same waveform;
- the E002 RGB48/RGB176 display contrast creates the same retinal luminance transitions as laboratory displays;
- the pupil extractor is free of exposure/segmentation artifacts;
- active responses predict fatigue or vigilance;
- E002 outperforms passive video for cognitive-state prediction.

The merged E002 photometric/geometry audit is designed specifically for the next phone step.

## Current bottleneck

The remaining non-substitutable experiment is now narrower than before:

> **Can one ordinary phone reproduce the condition-specific biological waveform separation implied by the human EyeLink/Pupil-Labs data while passing the predeclared photometric and geometry negative controls?**

The software, condition order, technical gates, pupil extraction, and confound audit are already frozen.

## Reproduction

The committed manual workflow

`.github/workflows/reproduce_human_observability.yml`

downloads the public datasets and verifies that all three result files reproduce exactly.

Primary PsPM:

`results/APST5_HUMAN_PRF_001.md`

Directional PsPM secondary:

`results/APST5_HUMAN_PRF_001_SECONDARY.md`

Independent Ehinger replication:

`results/APST5_EHINGER_001.md`
