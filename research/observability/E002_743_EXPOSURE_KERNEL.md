# E002-743 — Exposure-kernel counterexample and calibrated replacement (2026-11-11 UTC)

## Claim and evidence tier
**Exact mathematical/instrument-model counterexample; not human or physical validation.** E002-741's uniform-exposure formula must **not** be applied to a nonuniform temporal integration kernel. For normalized nonnegative exposure weighting k(t) on [0,w], measured linear aperture mean M=∫k(t)a(t)dt, and a nonnegative L-Lipschitz aperture a, the universally valid pointwise inequality is

a(s) >= max(0, M - L∫k(t)|t-s|dt).

Proof: a(t) <= a(s)+L|t-s| for every t. Multiply by k(t), integrate, rearrange; nonnegativity supplies zero. The expression is sharp in the unconstrained-aperture Lipschitz class whenever a(t)=c+L|t-s| is feasible, since equality holds. If a is physically bounded above, sharpness additionally requires this witness to satisfy the bound.

## Explicit falsification of uniform-shutter substitution
Set w=L=1, k(t)=2(1-t), a(t)=1-t, t in [0,1]. This kernel is normalized (integral 1), the trajectory stays in [0,1], and |a'|=1. The actual exposure mean is M=∫2(1-t)^2dt=2/3. At the exposure endpoint s=1, a(1)=0. **Incorrectly** assuming uniform exposure gives M-Lw/2=1/6>0, falsely certifying that closure was impossible. The correct kernel moment ∫2(1-t)(1-t)dt=2/3 yields a(1)>=0, sharp.

## Reproduction (Python standard library only)
Run `python research/observability/e002_743_exposure_kernel.py`. All arithmetic is exact rational; no acquisition data or external packages. The executable checks the counterexample, kernel normalization, and the corrected endpoint bound for a family of beta-shaped polynomial shutter weights.

## Product consequence
For an exposure-integrated observation, accept a hidden-closure exclusion only if **(i)** the observable is calibrated as a linear aperture average with defensible error bounds, **(ii)** the *temporal weighting kernel* is independently measured or bounded, **(iii)** timing and rolling-shutter uncertainties are bounded, and **(iv)** a velocity ceiling has an independently defensible scope. A nominal exposure duration or frame timestamp alone does not establish a uniform temporal weighting. Otherwise `ABSTAIN_UNCALIBRATED`; production remains `BLOCKED`.

## Physical test
Use a synchronized photodiode or pulsed LED to map relative temporal response over the exposure interval, including auto-HDR and multi-frame computational capture modes. Measure aperture proxy linearity separately with a calibrated mechanical shutter/target. Freeze the inferred kernel before evaluating held-out closure trajectories. Stratify by exposure setting, brightness, motion, row, and device; fail closed on unbounded temporal weighting. This test is proposed, **not executed**.
