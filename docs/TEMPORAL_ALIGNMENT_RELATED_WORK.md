# Temporal Alignment: Related Work and Novelty Boundary

Lucent's Temporal Alignment result should be positioned as a **controlled target-history interaction**, not as the first demonstration that temporal scale matters in physiological sensing.

A literature search completed after MTS-TARGET-SMOOTHING-001 found several close precedents.

## Closest precedent: matched multi-timescale drowsiness models

Massoz, Verly & Van Droogenbroeck (2018), *Multi-Timescale Drowsiness Characterization Based on a Video of a Driver's Face*, trained separate drowsiness classifiers at 5, 15, 30, and 60 second timescales using correspondingly multi-timescale PVT-derived ground truth.

DOI: https://doi.org/10.3390/s18092801

This work already established that drowsiness modeling has an accuracy-responsiveness trade-off across timescales.

The Lucent extension is narrower:

- predictor history and target aggregation are treated as **two separate axes** rather than matched together;
- one fixed human dataset, feature family, model family, validation protocol, and event set are used;
- the target horizon is deliberately changed while the sensor duration is crossed orthogonally;
- the primary statistic is the target-horizon x sensor-history interaction.

This factorization is what enables the observed reversal in MTS-TARGET-SMOOTHING-001 to be interpreted as a target-history interaction rather than simply "longer windows are more accurate."

## Performance-label smoothing

Gagnon et al. (2016), *A Systematic Assessment of Operational Metrics for Modeling Operator Functional State*, manipulated the smoothing window used to define performance labels and found that smoothing-window size affected classifier performance.

DOI: https://doi.org/10.5220/0005921600150023

Smith, Clark & Endsley (2025), *Balancing temporal dynamics with measurement noise in real-time situation awareness prediction*, reported that a three-trial moving-average situation-awareness target reduced measurement noise and was more predictable from single-trial physiology.

DOI: https://doi.org/10.1080/00140139.2025.2558703

These studies establish that target construction and smoothing matter. They do not, based on the available abstracts and metadata, jointly cross target horizon with physiological predictor-history length.

## Sensor-window optimization

Yamashita et al. (2021), *Pupillary fluctuation amplitude before target presentation reflects short-term vigilance level in Psychomotor Vigilance Tasks*, found that pupil fluctuations over roughly one to two seconds immediately before the target were most informative for trial-level PVT reaction time.

DOI: https://doi.org/10.1371/journal.pone.0256953

Cai & Demmans Epp (2024), *Exploring the Optimal Time Window for Predicting Cognitive Load Using Physiological Sensor Data*, compared physiological input windows from 60 to 210 seconds and found that longer windows were often preferable for cognitive-load prediction.

DOI: https://doi.org/10.48550/arXiv.2406.13793

These works optimize physiological history for a fixed target rather than manipulating target timescale.

## Resolution-dependent physiological features

Fernando, Robison & Maia (2024), *Analysis of goal, feedback and rewards on sustained attention via machine learning*, found that the machine-learning pipeline selected different physiological features when coarser, multi-trial feature representations were used.

DOI: https://doi.org/10.3389/fnbeh.2024.1386723

This is conceptually consistent with timescale-dependent information but does not isolate the target-history interaction.

## Recent theoretical overlap: the label defines the timescale

Xi-Zhe Zhang (2026), *The Label Defines the Timescale: Trait-State Limits of Temporal-Aggregate Learning*, derives protocol-conditioned limits for predicting long-horizon aggregate labels from temporally limited observations.

https://arxiv.org/abs/2608.01587

The paper makes a stronger theoretical point than Lucent can claim as novel: the useful observation protocol depends jointly on the label functional and latent temporal dynamics. It derives task-dependent effective temporal spans and shows that a snapshot can retain trait-level predictability while losing within-person state information as label horizon grows.

This substantially narrows Lucent's novelty boundary. Lucent should **not** claim to originate the general principle that "the label defines the relevant timescale."

The remaining empirical contribution is more specific:

- directly crossing sensor-history length and behavioral target horizon in public ocular-performance data;
- freezing the interaction statistic before analysis;
- retaining failed replications;
- testing explicit temporal nuisance baselines.

## What the literature search did not find

The search did **not** identify a directly equivalent prior result in which:

1. physiological history length is varied;
2. behavioral target horizon is varied independently;
3. all other pipeline components and the underlying human observations are held fixed;
4. a preregistered interaction tests whether changing target support changes the relative value of short versus long physiological history.

Absence from this search is not proof that no such paper exists.

## Conservative novelty claim

The strongest defensible claim is:

> **In MTS-TARGET-SMOOTHING-001, orthogonally separating physiological history length from behavioral target horizon revealed a preregistered crossover interaction: broadening the target changed which ocular history was most useful.**

This should be described as a **dataset- and pipeline-specific empirical interaction** that extends earlier multi-timescale physiological modeling.

It should **not** be described as:

- the first evidence that temporal scale matters;
- a universal law of physiological sensing;
- proof that target smoothing always favors longer sensor histories;
- proof that the same interaction generalizes across tasks or modalities.

## Independent replication status

COGBEACON-TARGET-ALIGNMENT-001 attempted the same directional interaction in a different task and signal family.

It did **not** replicate the positive interaction:

- D(H1) = +0.0358;
- D(H5) = -0.0288;
- interaction = -0.0645;
- paired-person bootstrap 95% CI = [-0.1665, +0.0313].

Therefore the current evidence supports a real interaction in the Massoz PVT dataset, but **not a universal target-smoothing rule**.

A second PVT/vigilance replication has now been completed on Martin, Whittaker & Johnston (2022), Experiment 2.

MARTIN-PVT-TARGET-ALIGNMENT-001 preserved the PVT target family while changing participants and ocular measurement:

- 25 participants;
- 2,330 common Block 2/3 anchors;
- 250 Hz EyeLink pupil area;
- strict leave-one-participant-out prediction;
- Block 1 used only for person-specific target normalization.

The preregistered interaction was **-0.0264**, 95% CI **[-0.0815,+0.0281]**. It did **not** replicate the Massoz crossover.

The Massoz crossover was then subjected to a preregistered explicit time-on-task/session nuisance audit. It remained positive:

- adjusted interaction **+0.2056**;
- 95% CI **[+0.1328,+0.2749]**.

So the current evidence is unusually asymmetric: the original Massoz/PVT crossover is robust to one simple temporal-confound model, but it fails to generalize to either an independent PVT/pupil cohort or CogBeacon.

The next empirical priority is no longer another passive window sweep. It is the prospective active-probe observability test, because passive temporal-scale effects are clearly measurement/protocol specific.
