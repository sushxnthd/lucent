# Concurrent Multimodal Information Principle

APST-5 can use the same display and camera frames to probe more than one ocular subsystem at once.

Suppose a scan produces two response channels:

- pupil dynamics \(y_p\) with modality-specific nuisance \(\nu_p\);
- pursuit / gaze dynamics \(y_g\) with modality-specific nuisance \(\nu_g\).

Both depend on the same transient state \(s\).

Assume, as a first approximation, conditionally independent measurement noise and independent nuisance priors across channels.

After nuisance projection, let the efficient Fisher information about state be

\[
J_p(s)
\]

for pupil and

\[
J_g(s)
\]

for gaze.

Because the joint log likelihood is the sum of channel log likelihoods and the nuisance blocks are independent, the efficient state information adds:

\[
J_{\mathrm{joint}} = J_p + J_g.
\]

Therefore

\[
J_{\mathrm{joint}} \ge J_p
\]

and

\[
J_{\mathrm{joint}} \ge J_g.
\]

For scalar state prior variance \(\sigma_s^2\), the local Gaussian information gain is

\[
IG_{\mathrm{joint}}
=
\frac12\log\left(1+\sigma_s^2(J_p+J_g)\right).
\]

## Why this matters for scan duration

If luminance modulation and a moving spatial target can be presented concurrently, adding the second response channel does not require adding a second serial test.

The scientific question is therefore not merely:

> which ocular feature is best?

It becomes:

> which combination of simultaneously excitable response systems gives the greatest nuisance-projected state information per second?

That is the temporal-compression objective.

## Boundary

The additivity result is conditional on the modeling assumptions.

Real pupil and pursuit channels are not perfectly independent. Shared arousal mechanisms, screen luminance, gaze direction, camera quality, and task engagement can create cross-channel covariance.

Human validation must therefore estimate the full joint covariance rather than assuming independence.

The theorem establishes a design reason to multiplex. It does not establish the size of the human gain.
