# Temporal Locality Principle

MTS-REALDATA-001 produced an exploratory result that requires a different way of thinking about measurement duration.

For an **immediate** behavioral target, more historical sensor data need not be more informative.

## A minimal model

Let \(S(t)\) be a zero-mean stationary latent state and let the target be the current state

\[
Y=S(0).
\]

Suppose a sensor observes

\[
X(t)=S(t)+\varepsilon(t),
\]

where \(\varepsilon\) is independent measurement noise.

A simple duration-\(T\) summary is the backward average

\[
\bar X_T
=
\frac{1}{T}
\int_{0}^{T}X(-\tau)\,d\tau.
\]

Let the latent-state autocovariance be

\[
R(\tau)=\mathrm{Cov}(S(0),S(-\tau)).
\]

Then

\[
\mathrm{Cov}(\bar X_T,Y)
=
\frac{1}{T}
\int_0^T R(\tau)\,d\tau.
\]

As \(T\) grows, the average includes observations whose relevance to the current state is determined by increasingly old values of \(R(\tau)\).

If \(R(\tau)\) decays with lag, historical samples are not equally informative about \(Y\).

## Signal-to-noise tradeoff

Longer averaging can suppress high-frequency measurement noise.

But it can also dilute a transient state.

For white measurement noise with intensity \(\sigma_\varepsilon^2\),

\[
\mathrm{Var}(\bar X_T)
=
\frac{2}{T^2}
\int_0^T
(T-\tau)R(\tau)\,d\tau
+
\frac{\sigma_\varepsilon^2}{T}.
\]

Therefore

\[
\rho(T)
=
\mathrm{Corr}(\bar X_T,Y)
\]

depends on two opposing effects:

1. **noise reduction** from averaging longer;
2. **state dilution** as older observations become less correlated with the present target.

There is no general theorem requiring \(\rho(T)\) to increase with \(T\).

A finite optimum can exist.

## Exponential example

If

\[
R(\tau)=\sigma_S^2e^{-\tau/\tau_S},
\]

then

\[
\mathrm{Cov}(\bar X_T,Y)
=
\sigma_S^2
\frac{\tau_S}{T}
(1-e^{-T/\tau_S}).
\]

For \(T\gg\tau_S\), this covariance decays approximately as

\[
\frac{\sigma_S^2\tau_S}{T}.
\]

So once the averaging window greatly exceeds the state's correlation time, additional history can increasingly describe the **past** rather than the state being predicted now.

## Connection to MTS-REALDATA-001

Lucent tested the same immediate within-person reaction-speed target against pre-stimulus eyelid windows of:

\[
2,\ 5,\ 15,\ 30,\ 60\text{ s}.
\]

The 2-second window had the highest held-out macro correlation in both population-normalized and personalized analyses.

Post-hoc paired subject bootstraps found the 2-second advantage over every longer tested window to have intervals excluding zero.

That observation is consistent with, but does not prove, a short ocular-state correlation time.

## Design implication

This changes how Lucent should use a strict time budget.

A longer passive clip is not automatically a stronger sensor.

For state-proximal prediction, the objective should be:

\[
\max_{u,T}
I(S_0;Y_{[-T,0]}\mid u)
-
\lambda T,
\]

not simply "collect as many seconds as possible."

Active probing may improve this further by making the newest few seconds more informative instead of extending the window backward.

## Falsifiable prediction

If temporal locality is real rather than dataset-specific:

- independent data should show a duration-performance curve with a finite short optimum for immediate targets;
- smoothing the **target itself** over longer intervals should shift the optimal sensor window longer;
- active state-perturbation should increase information density in the short-window regime.

Those three predictions distinguish a true locality effect from a one-dataset feature artifact.
