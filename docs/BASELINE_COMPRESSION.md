# Baseline Compression Principle

Lucent treats personal history as part of the measurement system, not merely as an extra feature.

## Setup

Suppose a short active response \(y\) depends on:

- transient state \(s\);
- stable nuisance parameters \(\nu\) such as pupil gain, latency, device response, and personal morphology;
- chosen probe \(u\).

For a local Gaussian approximation, write the Fisher information as

\[
F(u)=
\begin{bmatrix}
F_{ss} & F_{s\nu}\\
F_{\nu s} & F_{\nu\nu}
\end{bmatrix}.
\]

Let longitudinal history \(h\) induce nuisance prior precision \(\Lambda_h\).

After nuisance is marginalized, the efficient information about state is

\[
J_s(u,h)
=
F_{ss}
-
F_{s\nu}
(F_{\nu\nu}+\Lambda_h)^{-1}
F_{\nu s}.
\]

## Monotonicity

If history \(h_2\) produces at least as much nuisance precision as \(h_1\),

\[
\Lambda_{h_2}\succeq\Lambda_{h_1},
\]

then

\[
F_{\nu\nu}+\Lambda_{h_2}
\succeq
F_{\nu\nu}+\Lambda_{h_1}.
\]

For positive-definite matrices, inversion reverses Loewner order, hence

\[
(F_{\nu\nu}+\Lambda_{h_2})^{-1}
\preceq
(F_{\nu\nu}+\Lambda_{h_1})^{-1}.
\]

Multiplying by \(F_{s\nu}\) and \(F_{\nu s}\) preserves the scalar inequality:

\[
F_{s\nu}
(F_{\nu\nu}+\Lambda_{h_2})^{-1}
F_{\nu s}
\le
F_{s\nu}
(F_{\nu\nu}+\Lambda_{h_1})^{-1}
F_{\nu s}.
\]

Therefore

\[
J_s(u,h_2)\ge J_s(u,h_1).
\]

## Design consequence

A better personal baseline cannot hurt local state identifiability under the model.

That means duration and baseline precision can be traded against each other.

Define the minimum duration needed to reach a target state-information level \(J^*\):

\[
T^*(\Lambda_h)
=
\inf\{
T:
\max_{u\in\mathcal U_T}
J_s(u,\Lambda_h)\ge J^*
\}.
\]

As nuisance prior precision improves, \(T^*\) is non-increasing provided the shorter-duration probe family is nested appropriately.

This is the mathematical reason Lucent should be designed longitudinally from the beginning.
