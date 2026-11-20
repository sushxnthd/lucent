# E002-672 | Executed gap-boundary synthetic challenge (2026-11-06 UTC)

Evidence tier: **executed synthetic exact-rational challenge**, not independent validation, physical instrumentation, or human evidence. The frozen E002-671 prospective protocol remains unchanged.

## Executed checks
Local Python 3 stdlib Fraction calculations evaluated the sharp endpoint bound
`min a(t) = max(0, (a_0+a_1-V Δ)/2)` for a V-Lipschitz aperture on an interval, with closure threshold τ=3/10.

At equal open endpoints a0=a1=1, define dimensionless ratio R=VΔ/[2(1-τ)]. R=4/5 gives sharp minimum 11/25 and a conditional exclusion; R=1 gives 3/10 (equality, abstain); R=6/5 gives 4/25 (closure feasible, abstain). This is an assumption-conditional bound, not a physiological estimate.

A 135-case synthetic grid varied both endpoint apertures (3/4, 9/10, 1), R (1/4,1/2,3/4,1,5/4), and independent endpoint error budgets (0,1/100,1/20). The conservative rule produced 70 exclusions and 0 false exclusions **under the stipulated V-Lipschitz, exact timing and bounded endpoint-error assumptions**. These cases are not statistically independent human trials and do not estimate real-world false-exclusion risk.

**Adversarial negative control:** actual V=84, assumed V=42, Δ=1/50, a0=a1=1. The assumed bound certifies absence while the actual bound permits a hidden closure (minimum 4/25). Thus underestimated velocity can create a false certificate even with perfect endpoints and timestamps.

## Reproduction
Python stdlib: `fractions.Fraction`, `itertools.product`. For each combination compute `max(0,(a0+a1-V*dt)/2)` using pessimistic endpoints `max(0, observed-error)`; issue certificate only if strictly above 3/10. Assert 70/135 certified and 0 false under the assumed model, then assert the negative control produces a false certificate when actual V exceeds assumed V. No hardware or participant data used.

## Decision
This run does **not** meet the empirical-validation gate. Do not promote the 70/135 synthetic coverage to a product metric. Prioritize independently calibrated acquisition, held-out human reference sequences and externally verified velocity assumptions. Product remains `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. No Hush changes.