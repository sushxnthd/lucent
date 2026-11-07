# E002-551 FROZEN | Curvature-limited blind-gap exclusion (synthetic/instrument, no human claim)

Frozen 2026-10-31 before executable or simulation. Existing E002-371 Lucent kernel, branch `research/observability-human-boundary`, draft PR #26. No human recordings or authenticated physical calibration acquired.

## Falsifiable hypothesis and exact decision

A local acceleration ceiling may exclude a hidden eyelid closure between two calibrated instantaneous aperture samples **without first converting the samples into a global speed ceiling**. This is a conditional interpolation result, not a novel mathematical theorem, and it does not transfer directly to exposure-averaged camera frames.

Assume true normalized anatomical aperture f(t) has |f''(t)| <= A throughout an observed interval, A >= 0, with independently established hard A. Two independently calibrated *instantaneous* endpoint samples y0,y1 each have |y-f| <= e. Nominal timestamp separation d has per-endpoint error <= u, giving actual separation Delta in [d-2u,d+2u] with d>2u. Independently verified geometry, anatomy, transfer, clock and quality gates must hold. Let D=d+2u and s in [0,1]. The exact conservative lower envelope is

L(s) = (1-s)(y0-e) + s(y1-e) - (A*D*D/2)*s*(1-s).

The minimizer is s*=clamp(1/2 - (y1-y0)/(A*D*D),0,1) for A*D*D>0; otherwise use the lower endpoint. If min_s L(s) > threshold theta, return `CONDITIONAL_EXCLUSION_ONLY`. Otherwise return `POSSIBLE_CLOSURE_OR_UNRESOLVED`. Missing hard A/e/u, any nuisance failure, noninstantaneous or unverified optical response => `ABSTAIN`.

For equal endpoint observations y0=y1=a, exclusion requires a-e-A*D^2/8 > theta. Dimensionless curvature ratio R=A*D^2/[8*(a-e-theta)] (positive margin only): R<1 excludes; R>=1 cannot exclude. The envelope is sharp under the stated independent endpoint/error/time bounds: f(s)=(1-s)(y0-e)+s(y1-e)-(A*D^2/2)s(1-s) at Delta=D attains it. If the physical aperture must lie in [0,1], use a witness only when the constructed path satisfies that range; otherwise describe sharpness only in the unconstrained smooth-function class.

## Frozen tests and kill criteria

1. Exact equal-endpoint examples: a=.25, theta=.2, e=0, u=0, A=8000/s^2: 5-ms interval excludes (lower .225); 10-ms interval does not (lower .15). The 10-ms sharp witness reaches .15.
2. Compare against the E002-550 velocity ceiling and a conservative speed-only endpoint exclusion. For flat endpoints, curvature drop is A*D^2/8 vs speed-only drop A*D^2/4, a factor-two reduction. This is a conditional mathematical efficiency, not a measured sensitivity improvement.
3. Seeded Monte Carlo (10,000 trials) with independent bounded errors, random Delta within declared clock interval and parabolic trajectories |f''|<=A: count any falsely excluded true closure. Require zero in correctly specified synthetic trials. Preserve all counts and seed.
4. Adversarial underdeclared acceleration, clock error, localization error, exposure integration, missingness, geometry, gaze, glasses, brightness, blur and marker swaps: flag any false exclusion or abstention bypass. Underdeclared A must be explicitly labeled **model failure**, not hidden as a successful certificate.
5. Distinguish reference positives from negatives: high-rate reference negative is not continuous-time proof. Never use an uncalibrated camera mean as y0/y1.

## Product and evidence gates

This test can justify a **conditional instrument-geometry exclusion method** only. It cannot certify human A, anatomical transfer, or physical shutter support. No release until independent optical calibration, blinded human ratings and participant-disjoint physical predictions. Lucent stays `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.
