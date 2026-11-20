# E002-432 — timestamp compression converts a missing frame into a false closure certificate

**Date:** 2026-10-25. **Primary kernel:** E002-371. **Evidence:** reproducible, preregistered **synthetic** boxcar-aperture experiment; no physical human validation. **Status:** six independent Python unittest groups passed in hosted GitHub Actions run [40160322976](https://github.com/sushxnthd/lucent/actions/runs/40160322976). **Protocol:** [E002_432_FROZEN.md](E002_432_FROZEN.md), committed before implementation and results.

## Research question

Can a frame dropped during a blink, followed by a pipeline that treats adjacent retained rows as adjacent *acquired frames*, reverse a mathematically conditional no-hidden-closure decision? This is distinct from the prior shutter-response, gaze-geometry, illumination and high-rate-reference ambiguities. It tests a concrete **missingness/timestamp failure mode**, not a new temporal theorem.

## Identical-observation counterexample

The idealized camera captures 2-ms uniform boxcar exposure means at 30 Hz. Set hypothetical physical speed cap V=4 mm/s, closure threshold 2.000 mm and open aperture 2.100 mm. This velocity is deliberately hypothetical, not a physiological hard bound.

World A is constantly 2.100 mm. World B has 2.100-mm flat shoulders spanning the two retained shutter windows, and a triangular dip to **1.980 mm** at the missing center frame (33.33 ms). Its maximum speed is **3.71134 mm/s**, below the stipulated cap. Both worlds yield the **same two surviving exposure means of 2.100 mm** at t=0 and t=66.67 ms and the same missingness mask. If the midpoint were retained, its exposure average would be **1.98185567 mm**, witnessing the closure.

For the deliberately conservative equal-endpoint surrogate lower bound L=y-V delta/2, the gap is decisive:

| Computation | Gap | Conditional lower (mm) | Study-only decision |
| --- | ---: | ---: | --- |
| Incorrect retained-row compression | 33.33 ms | **2.033333** | False no-closure candidate |
| Original acquisition timestamps | 66.67 ms | **1.966667** | Abstain |
| Actual gap, +/-0.005-mm aperture error, +/-0.5-ms endpoint clock error | up to 67.67 ms | **1.959667** | Abstain |

For equal means and a stipulated ideal-boxcar physical inversion, define the dimensionless gap ratio R=V delta/[2(y-theta)]. The nominal compressed gap has R=2/3, whereas the actual gap has R=4/3. Crossing R=1 reverses this restricted candidate decision. This is a direct consequence of classical Lipschitz bounds, not a novel universal law. If any required physical assumption is unauthenticated, neither candidate is a physical certificate.

## Frozen randomized falsification

Before observing the results, the protocol fixed seed 432 and 1,200 synthetic trials per missingness regime: 600 constantly open trajectories plus 600 dip trajectories with depth sampled uniformly in [0.08,0.125] mm. Exactly **336** trials have a continuous-time threshold crossing. The same precommitted trajectories were evaluated under MCAR (15% midpoint loss independent of truth) and MNAR (90% midpoint loss for closure, 5% otherwise). The trial outcome is whether an algorithm issues a conditional no-closure candidate over the full two-frame interval.

| Frozen regime | True closures | Dropped midpoint | Naive candidates | Naive false certificates | Timestamp-aware candidates | Timestamp-aware false |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MCAR | 336 | 200 | 709 | **60** | 509 | **0** |
| Closure-associated MNAR | 336 | 341 | 912 | **297** | 571 | **0** |

In this synthetic population, false-certificate fractions **among naive candidates** are 60/709 = **8.46%** (MCAR) and 297/912 = **32.57%** (MNAR). The timestamp-aware gate loses coverage rather than guessing: 509/1200 and 571/1200 total-interval candidates, respectively. The zero timestamp-aware false counts are conditional on the exact synthetic model, its fixed speed cap and perfect provenance; they are not confidence bounds or clinical/device reliability evidence. Correlated dropout is a deliberate stress intervention, not a measured prevalence estimate.

## Independent verification and falsification criteria

Six test groups passed on Python 3.11 in [GitHub Actions](https://github.com/sushxnthd/lucent/actions/runs/40160322976). They include: independent 20,000-subdivision midpoint quadrature versus exact piecewise-linear boxcar integration; dense continuous-time minimum and finite-difference velocity checks; exact equality of the two retained exposure means; the incorrect-gap counterexample and the retained-midpoint positive control; deterministic frozen MCAR/MNAR stress and negative counts; rejection of missing, reordered, duplicate, inconsistent and nonfinite frame metadata; and an explicit physical-product authorization lock. No real camera or human samples were used.

**Reproduce:** from research/observability, run Python 3.11 with no third-party dependencies: python -m unittest -v test_e002_432_missingness.py; python e002_432_missingness.py. Machine-readable outcomes: [E002_432_SYNTHETIC_AGGREGATE.json](E002_432_SYNTHETIC_AGGREGATE.json). Technical figure: [E002_432_MISSINGNESS_ALIAS.svg](E002_432_MISSINGNESS_ALIAS.svg).

## Prior literature and novelty boundary

Rubin, D. B. (1976), *Inference and missing data*, Biometrika 63(3):581–592, DOI [10.1093/biomet/63.3.581](https://doi.org/10.1093/biomet/63.3.581), establishes that whether a missing-data mechanism can be ignored depends on assumptions about the mechanism. This experiment is an application of established missing-data and Lipschitz-recovery principles to an eyelid-camera claim. It **does not** assert discovery of MNAR bias, the triangle counterexample as a general theorem, or an empirically measured blink failure rate. The novelty claim, if any, must ultimately rest on independently verified measurement-science results beyond these synthetic controls.

## Direct product consequence

1. Preserve raw sensor frame identifiers, monotonic hardware capture timestamps, explicit missingness masks, exposure windows, and independently measured clock-error bounds. Never replace elapsed acquisition time by retained-row adjacency.
2. When any frame is dropped, duplicated, reordered, timestamp-free or physically unauthenticated, either compute the correctly widened conditional gap with authenticated nuisance/velocity bounds or **abstain**. The reference annotation pipeline must also keep unresolved intervals unresolved.
3. Do not use a predicted dropout mechanism, interpolation, a fitted eye tracker, or a population-average velocity as a hard physical no-closure guarantee. The missingness mask can be statistically informative without identifying the physical trajectory.
4. Physical hidden-closure guarantees, blink duration, PERCLOS and fatigue remain **ABSTAIN_UNCALIBRATED**. No product capability is unlocked by this experiment.

## Prospective human experiment, not yet performed

Use authorized 400–600-fps human eyelid sequences (or independently calibrated equivalent) with original frame IDs, synchronized illumination and independently authenticated shutter/clock traces. Register physical eyelid aperture via multi-view or 3D calibration, obtain two independent blinded anatomical-rater sheets, and independently estimate a conservative velocity envelope on training participants only. Freeze predicted no-closure/abstention decisions and the error-budget parameters before evaluating participant-disjoint, unseen sequences. Randomly suppress reference-aligned ordinary-camera frames and separately test naturally blink-associated tracker dropout. Stratify by gaze, head pose, skin/lighting, glasses, blur, exposure, rolling shutter, geometry and timestamp errors. Evaluate participant-level false certificates, abstention, and unresolved reference intervals. Require independent instrument and analysis replication before any physical claim.

**Outstanding:** authorized individual human traces, independent physical-aperture geometry, shutter and clock measurements, defensible physiological speed bounds, two blinded raters, unseen-participant testing, and external review. E002-371 remains physically unvalidated.
