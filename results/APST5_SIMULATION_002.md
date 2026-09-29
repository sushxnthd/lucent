# APST5-SIM-002: Personalization as Temporal Compression

**Status:** reproducible in-silico design result; no human-state claim is made.

## Question

Can a longitudinal personal baseline substitute for measurement time?

Lucent's original five-second framing implicitly asks every scan to solve two problems at once:

1. infer stable person/device characteristics;
2. infer the transient state change of interest.

A longitudinal system should already know something about (1).

The experiment therefore asks whether reducing uncertainty about stable nuisance parameters can let a much shorter active scan preserve the information relevant to transient state.

## State-targeted information

For a response model with scalar state \(s\) and nuisance vector \(\nu\), partition the Fisher information matrix as

\[
F =
\begin{bmatrix}
F_{ss} & F_{s\nu}\\
F_{\nu s} & F_{\nu\nu}
\end{bmatrix}.
\]

Let \(\Lambda_h\) be nuisance prior precision supplied by personal history.

The effective information about state after projecting out nuisance is

\[
J_s(\Lambda_h)
=
F_{ss}
-
F_{s\nu}
(F_{\nu\nu}+\Lambda_h)^{-1}
F_{\nu s}.
\]

The corresponding local Gaussian state-information gain is

\[
IG_s
=
\frac12
\log(1+\sigma_s^2 J_s).
\]

### Baseline-compression principle

If one longitudinal baseline is more informative than another,

\[
\Lambda_2 \succeq \Lambda_1,
\]

then

\[
J_s(\Lambda_2) \ge J_s(\Lambda_1).
\]

The reason is that positive-semidefinite ordering reverses under matrix inversion:

\[
(F_{\nu\nu}+\Lambda_2)^{-1}
\preceq
(F_{\nu\nu}+\Lambda_1)^{-1}.
\]

Therefore better knowledge of stable nuisance factors can only reduce the nuisance penalty on local state information.

This is not a new matrix theorem. Its significance for Lucent is architectural: **personalization is not merely a prediction feature; it is a way to buy back sensing time.**

## Surrogate experiment

The pupil-response surrogate contains stable nuisance parameters for:

- baseline diameter;
- luminance gain;
- response latency;
- constriction time constant;
- redilation time constant.

A latent reduced-alertness state perturbs those dynamics.

The state-effect prior deliberately allows luminance gain to move in either direction because the literature does not support one universal phasic-amplitude direction across all fatigue paradigms.

### Design / test separation

Probe design:

- 10 nuisance draws;
- 6 independent state-effect draws.

Held-out evaluation:

- 30 new nuisance draws;
- 10 new state-effect draws.

A five-second population probe is optimized with the full population nuisance prior.

Two-second probes are then optimized with progressively tighter nuisance priors. A nuisance-prior scale of 0.75 means the standard deviation of stable nuisance uncertainty is 25% smaller than the population prior.

## Primary held-out result

The optimized five-second population probe achieved:

\[
IG_{5s,\ population}=0.3402\ \text{nats}.
\]

The two-second probe produced:

| Two-second nuisance-prior scale | Held-out mean state IG | Ratio vs 5 s population |
| ---: | ---: | ---: |
| 1.00 | 0.2745 | 0.807x |
| 0.85 | 0.3424 | **1.007x** |
| 0.75 | 0.4023 | **1.183x** |
| 0.50 | 0.6405 | **1.883x** |

Under this surrogate, only a modest reduction in nuisance uncertainty is needed for a two-second active observation to approach the state information of a five-second population-level observation.

## Independent replication stress test

The stronger 0.75-prior case was evaluated on ten additional held-out synthetic populations.

For each replication:

- 25 fresh nuisance draws;
- 8 fresh state-effect draws;
- identical frozen two-second and five-second probe designs.

The two-second personalized-information condition beat the five-second population condition in **10/10 replications**.

Mean information ratio:

\[
\frac{IG_{2s,\ 0.75\ prior}}{IG_{5s,\ population}}
=
\mathbf{1.175}.
\]

Across the ten replications, the ratio ranged approximately from **1.105x to 1.241x**.

## Interpretation

The most important result is not the exact number 2 seconds.

It is the direction of the design principle:

> **Do not spend every scan re-identifying the person. Use history to absorb stable nuisance uncertainty, then spend the short active probe on what changed.**

This changes the Lucent architecture.

The measurement problem becomes:

\[
\text{state deviation}
\mid
\text{active response + personal prior},
\]

not:

\[
\text{absolute state}
\mid
\text{five seconds of raw face video}.
\]

## What this does not establish

The result does not prove that:

- a real personal baseline will reduce nuisance uncertainty by exactly 25%;
- two seconds is enough for real fatigue inference;
- the literature-inspired state-effect prior is quantitatively correct;
- ordinary front cameras will recover all required pupil dynamics;
- personalization will transfer across devices and long time gaps.

Those are empirical questions.

## Falsifiable prediction

If APST-5 is correct, a human study should show a **measurement-time / baseline-quality tradeoff**:

1. collect a stable personal ocular baseline across sessions;
2. estimate how much nuisance variance it removes;
3. compare 2 s, 3 s, and 5 s active probes;
4. test whether better baseline precision shifts the duration-performance curve leftward.

The critical result is not a better training score. It is a shorter held-out measurement window at equal predictive state information.
