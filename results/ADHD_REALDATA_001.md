# ADHD-REALDATA-001: Independent Temporal-Locality Test

**Status:** completed preregistered independent conceptual replication.

**Primary hypothesis:** **not supported; direction reversed.**

## Source

Rojas-Líbano et al. (2019), *A pupil size, eye-tracking and neuropsychological dataset from ADHD children during a cognitive task.*

- article: https://doi.org/10.1038/s41597-019-0037-2
- dataset: https://doi.org/10.6084/m9.figshare.7218725.v3
- license: CC BY 4.0
- EyeLink 1000, 1 kHz
- 50 participants represented in the analysis
- 67 sessions
- 5,973 common usable trials

Lucent does not redistribute the source participant data.

## Frozen design

The plan was committed before any duration-performance result was computed:

[experiments/registrations/ADHD_REALDATA_001.md](../experiments/registrations/ADHD_REALDATA_001.md)

Key choices:

- predictor windows end immediately before probe-array onset;
- durations fixed at 1, 2, 3, and 5 seconds;
- one common trial intersection across all durations;
- target = within-session reciprocal reaction-speed residual after removing load and distractor main effects;
- StandardScaler + Ridge(alpha=10);
- strict leave-one-participant-out evaluation;
- participants with two medication-state sessions remain in the same fold;
- no condition labels as predictors;
- primary contrast fixed at 2 s minus 5 s;
- paired participant bootstrap with 10,000 resamples.

## Result

Macro-r is the Fisher-z mean of held-out within-participant Pearson correlations.

| Pre-probe pupil window | Macro-r | Pooled-r | Participants | Trials |
| ---: | ---: | ---: | ---: | ---: |
| 1 s | 0.0101 | 0.0098 | 50 | 5,973 |
| 2 s | 0.0350 | 0.0309 | 50 | 5,973 |
| 3 s | 0.0549 | 0.0465 | 50 | 5,973 |
| **5 s** | **0.0749** | **0.0763** | 50 | 5,973 |

### Preregistered primary contrast

\[
r_{2s}-r_{5s}
=
-0.0400
\]

Paired participant-bootstrap 95% interval:

\[
[-0.0717,\ -0.0061].
\]

The entire interval is below zero.

Therefore the independent dataset does **not** replicate the MTS finding that 2 seconds outperforms 5 seconds.

It provides evidence in the **opposite direction under this task and feature family**.

### Other preregistered-duration contrasts

\[
r_{2s}-r_{3s}
=
-0.0200,
\qquad
95\%\ CI=[-0.0389,-0.0009].
\]

\[
r_{2s}-r_{1s}
=
+0.0249,
\qquad
95\%\ CI=[+0.0016,+0.0483].
\]

Within the available 1–5 second range, predictive correlation increased with history from 1 to 5 seconds.

## Why the failed replication matters

MTS-REALDATA-001 used eyelid behavior before an imminent psychomotor-vigilance stimulus during drowsiness experiments. In that dataset, 2 seconds outperformed every longer tested window.

ADHD-REALDATA-001 uses pupil dynamics during a structured working-memory trial. The five seconds before the probe contain the trial's fixation, memoranda, delays, and distractor sequence.

Even after removing load and distractor main effects from reaction speed, longer pre-probe history retained more held-out trial-level information.

The result therefore falsifies a stronger version of Lucent's earlier idea:

> **two seconds is not a universal optimal ocular-state window.**

That is scientifically useful.

## Revised interpretation

The combined evidence instead suggests a **target-dependent temporal receptive field**.

For a rapidly varying, state-proximal target, old history may dilute current information.

For a behavioral outcome integrating information over an extended task episode, the relevant ocular history may also extend over that episode.

Thus sensing duration should be optimized against the target's temporal support rather than fixed globally.

A cross-dataset interaction analysis is run separately and explicitly labeled post-hoc.

## What this establishes

Under the frozen analysis:

- pre-probe pupil history contains modest held-out information about trial-level reaction-speed residuals;
- 5 seconds significantly outperformed 2 seconds;
- the original 2-second temporal-locality observation did not generalize unchanged across tasks.

## What it does not establish

It does not establish:

- that 5 seconds is optimal beyond the tested range;
- that pupil dynamics diagnose ADHD;
- that these children constitute a fatigue cohort;
- that Lucent's active probe is validated;
- that the sign reversal is caused specifically by cognitive integration time.

Those are separate empirical questions.

## Reproduction

\`\`\`bash
pip install -e ".[dev]"
python experiments/adhd_realdata_temporal_locality.py
\`\`\`

The script downloads the public Figshare dataset directly and reproduces the frozen LOSO analysis.
