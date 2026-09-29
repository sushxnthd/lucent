# Temporal Alignment Principle

Lucent originally treated scan duration mostly as a compression constraint.

The public-data results force a more precise view:

> **There is no universally optimal ocular history length. In at least one controlled public-data setting, the relative value of short versus long ocular history changed when the behavioral target's temporal support was changed.**

This is a design principle, not a claim of a new mathematical theorem.

## Empirical motivation

Two independent public datasets now give opposite 2 s versus 5 s results under held-out-participant evaluation.

### Immediate psychomotor vigilance

In MTS-REALDATA-001, the target was the **next PVT reaction-speed deviation** and the ocular signal was pre-stimulus eyelid behavior.

Population-normalized macro correlations were:

\[
r_{2s}=0.2742,
\qquad
r_{5s}=0.2033.
\]

The exploratory paired difference was:

\[
r_{2s}-r_{5s}
=
+0.0709,
\]

with paired subject-bootstrap interval

\[
[+0.0424,+0.1010].
\]

Older history progressively reduced predictive correlation through 60 s.

### Structured working-memory trial

ADHD-REALDATA-001 was frozen before duration outcomes were computed on an independent EyeLink dataset.

The target was trial-level reciprocal reaction-speed residual after removing load and distractor main effects. Pupil windows ended before the probe array.

Macro correlations were:

\[
r_{1s}=0.0101,
\quad
r_{2s}=0.0350,
\quad
r_{3s}=0.0549,
\quad
r_{5s}=0.0749.
\]

The preregistered contrast reversed direction:

\[
r_{2s}-r_{5s}
=
-0.0400,
\]

with 95% paired participant-bootstrap interval

\[
[-0.0717,-0.0061].
\]

Thus the earlier "2 seconds is better" observation does not generalize as a universal duration rule.

## Direct preregistered manipulation

Cross-dataset disagreement alone cannot establish why the useful duration changes.

MTS-TARGET-SMOOTHING-001 therefore manipulated target timescale **inside the same Massoz dataset** while holding the participants, ocular data, feature map, model family, LOSO evaluation, and common event set fixed.

For the immediate target:

\[
r_{2s}=0.2700,\qquad r_{60s}=0.0744.
\]

For a target defined as mean reciprocal PVT speed over the next 60 seconds:

\[
r_{2s}=0.1559,\qquad r_{60s}=0.2042.
\]

Define

\[
D(H)=r_{60s,H}-r_{2s,H}.
\]

The preregistered interaction was

\[
\Delta=D(60s)-D(0s)=+0.2439,
\]

with paired subject-bootstrap 95% interval

\[
[+0.1647,+0.3191]
\]

across 28 subjects.

The interval lies entirely above zero. Within this Massoz/PVT pipeline, broadening target temporal support increased the relative usefulness of longer sensing history.

## Second independent boundary dataset

COGBEACON-REALDATA-001 tested the earlier 2-second hypothesis on a separate WCST-like cognitive-fatigue dataset using 68-point facial landmarks and strict leave-one-person-out evaluation.

Macro correlations were:

\[
r_{2s}=0.1197,\qquad r_{5s}=0.1665.
\]

The 2 s - 5 s contrast was -0.0468 with 95% CI [-0.1046,+0.0101], while the secondary 3 s - 5 s contrast was -0.0796 with 95% CI [-0.1375,-0.0210].

This is again inconsistent with a universal ultra-short optimum.

## Preregistered independent interaction replication

COGBEACON-TARGET-ALIGNMENT-001 then tested the **interaction itself** on a different human dataset rather than merely comparing fixed target durations.

Using 1,786 common anchor rounds from 20 people, the same 2-second and 5-second facial histories were evaluated against:

- H1: current log response time;
- H3: mean log response time over the current + next 2 correct rounds;
- H5: mean log response time over the current + next 4 correct rounds.

The preregistered long-history advantage was

\[
D(H1)=+0.0358,
\qquad
D(H5)=-0.0288.
\]

Therefore

\[
\Delta=D(H5)-D(H1)=-0.0645,
\]

with paired person-bootstrap 95% interval

\[
[-0.1665,+0.0313].
\]

The positive Temporal Alignment interaction **did not replicate** in CogBeacon.

This matters for interpretation: target smoothing is not, by itself, a universal mechanism that makes longer sensing histories more useful. The Massoz/PVT crossover is a real within-dataset interaction, but its generality remains open.

## Independent PVT replication

MARTIN-PVT-TARGET-ALIGNMENT-001 preserved the PVT target family while changing the participants and ocular measurement system.

The public Martin et al. Experiment 2 dataset provided 25 participants, 250 Hz EyeLink pupil area, three PVT blocks per participant, and 2,330 common Block 2/3 anchors after the frozen quality rules.

The preregistered long-history advantage was

\[
D(H0)=+0.0077,
\qquad
D(H60)=-0.0187.
\]

Therefore

\[
\Delta=D(H60)-D(H0)=-0.0264,
\]

with paired participant-bootstrap 95% interval

\[
[-0.0815,+0.0281].
\]

The positive interaction did **not** replicate even when the behavioral task remained PVT.

This rules out a simple claim that target smoothing alone determines the preferred ocular history across PVT datasets.

## Time-on-task nuisance audit

A failed independent replication raises a second question: was the original Massoz crossover only a slow time-on-task artifact?

MTS-TEMPORAL-ALIGNMENT-NUISANCE-001 froze an explicit nuisance model before recomputing the interaction. Every sensor-duration model received the same:

- normalized time-on-task;
- squared normalized time-on-task;
- PVT2/PVT3 session indicator.

The adjusted interaction remained strongly positive:

\[
\Delta_{adjusted}=+0.2056,
\]

with 95% paired subject-bootstrap interval

\[
[+0.1328,+0.2749].
\]

Thus the Massoz crossover is not explained solely by that predeclared low-frequency nuisance model.

The combined evidence is therefore not "the effect disappeared" and not "the effect is universal." It is a robust result in one measurement/task system that failed two independent generalization tests.

## A target-weighted model

Let \(S(t)\) be a latent physiological / cognitive process and let an ocular sensor observe

\[
X(t)=g(S(t))+\varepsilon(t).
\]

A behavioral target need not depend only on instantaneous state.

Write a local linear approximation:

\[
Y
=
\int_0^\infty
q(\tau)S(-\tau)\,d\tau
+
\eta,
\]

where \(q(\tau)\) is the target's temporal support.

Examples:

- an imminent reflexive vigilance response may put most mass near \(\tau=0\);
- performance after a multi-second working-memory episode may depend on a broader history.

A sensor summary using temporal kernel \(w(\tau)\) is

\[
Z_w
=
\int_0^\infty
w(\tau)X(-\tau)\,d\tau.
\]

Its covariance with the target is

\[
\operatorname{Cov}(Z_w,Y)
=
\int
w(\tau)c_{XY}(\tau)\,d\tau,
\]

where

\[
c_{XY}(\tau)
=
\operatorname{Cov}(X(-\tau),Y).
\]

The optimal linear temporal weighting is therefore related to the **target-specific cross-covariance**, not to a universal window length.

In the full linear-Gaussian case, the Wiener solution has the form

\[
w^*
\propto
C_{XX}^{-1}c_{XY}.
\]

A fixed boxcar of length \(T\) is only a crude member of this much larger design space.

## Why the sign can reverse

Suppose the target is nearly instantaneous.

Then \(c_{XY}(\tau)\) can decay quickly with lag. Extending a boxcar adds increasingly stale samples. Noise reduction may eventually be outweighed by state dilution.

Now suppose the target integrates a multi-second task episode.

Then \(c_{XY}(\tau)\) can remain relevant over much of that episode. A longer window can contain information that a short terminal window necessarily discards.

Neither case implies that "more data is always better" or "shorter is always better."

The design problem is **temporal matching**.

## From duration selection to experimental design

For Lucent, the relevant objective becomes

\[
(u^*,T^*)
=
\arg\max_{u,T}
I(Y;\,X_{[-T,0]}
\mid u,h)
-
\lambda_T T
-
\lambda_C C(u),
\]

where:

- \(Y\) is the specific functional target;
- \(u\) is the active visual probe;
- \(h\) is longitudinal personal history;
- \(T\) is sensing duration;
- \(C(u)\) is a comfort / exposure cost.

The duration and probe should be optimized **jointly for the target**.

## Consequence for APST-5

"Five seconds" should not become dogma.

The stronger architecture is:

1. define the functional target;
2. estimate its state-relevant temporal support;
3. use personal history to remove stable nuisance;
4. design the active stimulus to concentrate information inside that support;
5. stop sensing when marginal target information falls below its time / friction cost.

In some domains this may yield two seconds.

In others it may require five seconds or more.

A research system that discovers that boundary honestly is more useful than one forced to make every target fit the same scan length.

## Falsifiable predictions

The Temporal Alignment Principle predicts:

1. **signal-target dependence:** the preferred history can change when either the observable or behavioral target changes;
2. **target smoothing under compatible dynamics:** broadening an immediate behavioral target can shift the useful sensor horizon in some systems, but both CogBeacon and Martin PVT show that this is not guaranteed;
3. **active compression:** a well-designed perturbation should increase information density and allow a shorter window than passive observation for the same target;
4. **personalization interaction:** removing stable nuisance with longitudinal history should reduce the observation duration required to reach a fixed target-information level;
5. **task-boundary sensitivity:** when a target depends on a bounded task episode, ocular samples from inside that episode should carry more useful information than equally old samples outside it.

Each prediction can fail independently.

## Claim boundary

Current evidence contains:

- one strong preregistered crossover in the Massoz/PVT eyelid data;
- the same crossover surviving a preregistered time-on-task/session nuisance adjustment;
- a preregistered failed interaction replication in an independent Martin PVT/pupil cohort;
- a preregistered failed interaction replication in CogBeacon;
- separate ADHD and CogBeacon duration tests showing that an ultra-short optimum does not generalize unchanged.

The defensible result is therefore narrower:

> **predictor-history length and behavioral target horizon are distinct design axes, and their interaction can be large enough to reverse the preferred sensing window in a specific signal × target × protocol system. The sign of that interaction is not universal.**

This framing also aligns with recent theory showing that label function and latent temporal dynamics jointly determine the effective observation span.

See [TEMPORAL_ALIGNMENT_RELATED_WORK.md](TEMPORAL_ALIGNMENT_RELATED_WORK.md) for the prior-art and novelty boundary and [TEMPORAL_SCALE_AUDIT_001](../results/TEMPORAL_SCALE_AUDIT_001.md) for the replication matrix.
