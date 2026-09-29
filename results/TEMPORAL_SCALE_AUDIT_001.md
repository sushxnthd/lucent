# TEMPORAL-SCALE-AUDIT-001: What Survived Replication

## Executive result

Lucent's original Temporal Alignment story has survived one important falsification and failed two important generalization tests.

That is more informative than either a clean positive story or a discarded null.

### Evidence map

| Experiment | Dataset / signal | Preregistered target-history interaction | Result |
| --- | --- | ---: | --- |
| MTS-TARGET-SMOOTHING-001 | Massoz PVT / eyelid distance | Delta = D(60)-D(0) | **+0.2439**, 95% CI **[+0.1647,+0.3191]** |
| MTS-TEMPORAL-ALIGNMENT-NUISANCE-001 | same MTS data + explicit time/session nuisance | same | **+0.2056**, 95% CI **[+0.1328,+0.2749]** |
| MARTIN-PVT-TARGET-ALIGNMENT-001 | independent PVT / 250 Hz pupil area | same directional hypothesis | **-0.0264**, 95% CI **[-0.0815,+0.0281]** |
| COGBEACON-TARGET-ALIGNMENT-001 | WCST-like task / facial landmarks | H5-vs-H1 analogue | **-0.0645**, 95% CI **[-0.1665,+0.0313]** |

Here

[
D(H)=r_{mathrm{long},H}-r_{mathrm{short},H}.
]

The exact long/short durations and target-horizon units follow each frozen protocol.

## What survived

The Massoz/PVT crossover is not explained away by the preregistered nuisance vector consisting of:

- normalized time-on-task;
- squared time-on-task;
- PVT2/PVT3 session identity.

After that adjustment:

- immediate target: 2 s = 0.2672, 60 s = 0.0892;
- 60 s target: 2 s = 0.2236, 60 s = 0.2513;
- adjusted interaction = **+0.2056**;
- 95% CI = **[+0.1328,+0.2749]**.

Thus the original crossover is not merely a trivial linear/quadratic task-progress effect under this audit.

## What failed

The same directional interaction did not replicate in either independent dataset.

### Independent PVT/pupil cohort

Martin et al. Experiment 2 preserved the PVT target family but changed the participants and ocular measurement.

With 25/25 participants and 2,330 common Block 2/3 anchors:

| Target | 2 s pupil | 5 s pupil | 5 s - 2 s |
| --- | ---: | ---: | ---: |
| immediate | 0.0892 | 0.0968 | +0.0077 |
| 15 s | 0.1367 | 0.1202 | -0.0165 |
| 30 s | 0.1753 | 0.1498 | -0.0255 |
| 60 s | 0.1995 | 0.1808 | -0.0187 |

The preregistered interaction was **-0.0264**, 95% CI **[-0.0815,+0.0281]**.

A simple foreperiod + block-progress nuisance model was more predictive than the pupil model at every horizon, reaching macro-r **0.2959** at H60.

### CogBeacon

Broadening the target from current response time to the current + next four correct rounds also failed to make the 5-second facial history relatively more useful.

The preregistered interaction was **-0.0645**, 95% CI **[-0.1665,+0.0313]**.

## Revised scientific statement

The data do **not** support:

> longer target support generally implies that longer physiological history is more useful.

They support a narrower statement:

> **sensor-history length and target temporal aggregation are separate design axes, and their interaction can be large enough to reverse the preferred sensing window in some measurement/task systems. That interaction is not universal across ocular/facial modalities or tasks.**

The relevant timescale is therefore better treated as a property of the full **signal × target × task/protocol** system, not the label alone.

## Relation to prior work

This narrower conclusion is consistent with, but more empirical than, recent theoretical work arguing that the label and latent temporal dynamics jointly determine the useful observation protocol:

- Xi-Zhe Zhang (2026), *The Label Defines the Timescale: Trait-State Limits of Temporal-Aggregate Learning*: https://arxiv.org/abs/2608.01587

It also sits downstream of earlier multi-timescale drowsiness modeling:

- Massoz, Verly & Van Droogenbroeck (2018), DOI: https://doi.org/10.3390/s18092801

Massoz et al. matched four sensor timescales to four PVT-derived ground-truth timescales. Lucent's controlled contribution is the orthogonal crossing of sensor history and target horizon under a fixed pipeline, plus explicit preregistered replication attempts.

## Consequence for Lucent

This result changes how APST-5 should be developed.

The project should not search for a universal "best scan length."

Instead, for a specific functional target, Lucent should estimate:

1. whether the chosen observable actually contains incremental state information beyond trivial temporal/task context;
2. which temporal support of that observable is useful for that target;
3. whether an active perturbation increases information density enough to shorten that support;
4. whether the result survives a second cohort/device/protocol.

## Strongest remaining empirical bottleneck

The active-probe thesis is still untested prospectively.

The phone E002 instrument now exists and has a frozen observability protocol. The next non-substitutable evidence is therefore real synchronized phone capture showing that the split and contiguous matched-exposure probes create repeatable, distinguishable ocular dynamics on commodity hardware.

Until that happens, simulations remain design hypotheses.

## Claim boundary

TEMPORAL-SCALE-AUDIT-001 is a replication/falsification synthesis, not a universal theorem.

It does not establish:

- a causal physiological mechanism for the Massoz crossover;
- that eyelid signals are categorically superior to pupil signals;
- that active probing works;
- that smartphone fatigue inference is valid;
- that the same temporal interaction will appear in a fresh sleep-loss cohort.
