# E002-686 — Independent exact-rational replay of the E002-685 conditional gap decision

Evidence tier: **synthetic model verification**; not an independent laboratory, camera or human validation.

## Executed result (2026-11-06 UTC)

Executed `python e002_686_independent.py` in a separate local Python runtime. Exhaustive grid: endpoint apertures a,b, velocity ceiling v, gap h and closure threshold c each from {0, 1/4, ..., 2}. **59,049 configurations; 32,769 feasible; zero oracle/implementation disagreements.** A separate monotonicity sweep visited 32,769 feasible configurations with zero violations: increasing the blind gap cannot turn a prior abstention into exclusion, holding the remaining inputs fixed.

The independent oracle explicitly minimizes the intersection of endpoint Lipschitz cones over time using exact rational arithmetic; the compared implementation uses the closed-form lower bound. This checks mathematical decision equivalence on the declared finite grid, not the authenticity or completeness of the E002-685 CSV pipeline. The code is self-contained and requires only Python stdlib.

## Falsification and limits

The oracle assumes instantaneous, exact, nonnegative scalar anatomical endpoints, a *hard independently valid* velocity ceiling throughout the blind interval, and a conservative effective gap. It cannot verify physiological velocity, shutter/row timing, exposure integration, reference truth, or chain of custody. E002-685's string `authenticated=external_verified` remains an external assertion, not a cryptographic or scientific verification. Correlated measurement errors, gaze, blur, glasses, occlusion, landmark failures and clock drift remain unvalidated.

**Product consequence:** No additional measurement claim is authorized. Preserve `ABSTAIN_UNCALIBRATED` and release `BLOCKED`. Next experiment is the frozen E002-671 synchronized occluder/photodiode acquisition followed by participant-disjoint human reference evaluation; do not replace it with more synthetic arithmetic.
