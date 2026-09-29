# Temporal Alignment Principle

Lucent originally treated scan duration mostly as a compression constraint.

The public-data results force a more precise view:

> **There is no universally optimal ocular history length. The useful sensing horizon depends on the temporal support of the behavioral state being predicted.**

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

The interval lies entirely above zero. This directly supports the prediction that broadening target temporal support increases the relative usefulness of longer sensing history.

## Second independent boundary dataset

COGBEACON-REALDATA-001 tested the earlier 2-second hypothesis on a separate WCST-like cognitive-fatigue dataset using 68-point facial landmarks and strict leave-one-person-out evaluation.

Macro correlations were:

\[
r_{2s}=0.1197,\qquad r_{5s}=0.1665.
\]

The 2 s - 5 s contrast was -0.0468 with 95% CI [-0.1046,+0.0101], while the secondary 3 s - 5 s contrast was -0.0796 with 95% CI [-0.1375,-0.0210].

This is again inconsistent with a universal ultra-short optimum.

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

1. **target dependence:** different behavioral targets can prefer different ocular history lengths;
2. **target smoothing:** deliberately smoothing an immediate behavioral target over a longer horizon should shift the useful sensor horizon longer;
3. **active compression:** a well-designed perturbation should increase information density and allow a shorter window than passive observation for the same target;
4. **personalization interaction:** removing stable nuisance with longitudinal history should reduce the observation duration required to reach a fixed target-information level;
5. **task-boundary sensitivity:** when a target depends on a bounded task episode, ocular samples from inside that episode should carry more useful information than equally old samples outside it.

Each prediction can fail independently.

## Claim boundary

Current evidence now includes a preregistered within-dataset manipulation: broadening the PVT target horizon produced the predicted positive long-versus-short sensing interaction. Two independent datasets also show that the ultra-short optimum does not generalize unchanged across tasks.

The remaining causal and deployment questions are whether active perturbation can further compress the target-matched sensing horizon, whether the effect survives prospective data collection, and whether commodity phones can measure the required ocular dynamics reliably.
