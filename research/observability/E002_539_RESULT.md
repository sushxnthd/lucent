# E002-539 RESULT | Two individually inconclusive motion ceilings can jointly exclude a hidden closure

Date: 2026-10-30. Lucent E002-371 primary research kernel. Established `research/observability-human-boundary` branch and draft PR #26. Frozen [protocol](E002_539_FROZEN.md) committed first at `220d83f` before the evaluator, independent optimizer, and tests. **Evidence tier: exact conditional mathematical law and numerical synthetic adversarial optimization. Not measured human physiology, authenticated physical shutter, or a release certificate.**

## New sharp joint law

Assume a normalized **pointwise anatomical aperture** a(t) in [0,1] over a truly unobserved interval [0,D], a(0)=a(D)=b>c, a continuously differentiable derivative with |a'|<=V and |a''|<=A almost everywhere, where V and A are independently justified **hard continuous-time** bounds. Let h=D/2 and

`F(h;V,A) = integral_0^h min(V,A*s) ds`.

For A=0 or V=0, F=0. For V>=A*h, F=A*h^2/2. For 0<V<A*h, F=V*h-V^2/(2A). Every such path satisfies

`min_[0,D] a(t) >= b - F(D/2;V,A)`.

**Proof:** If a attains an interior minimum at t*, then a'(t*)=0. The speed and acceleration ceilings jointly give |a'(s)|<=min(V,A*|s-t*|). Integrating toward the left endpoint yields b-a(t*)<=F(t*); integrating toward the right yields b-a(t*)<=F(D-t*). At least one of t*,D-t* is <=D/2, so b-a(t*)<=F(D/2). The endpoints themselves equal b. Equality is attained by the symmetric C^{1,1} trajectory whose derivative is -min(V,A*(h-t)) on the first half and +min(V,A*(t-h)) on the second. If its minimum falls below the physical floor, uniformly scale its excursion to touch the positive threshold c; this preserves both ceilings and [0,1]. Thus the strict **conditional** exclusion test F<b-c is sharp; equality permits contact.

This is a standard optimal-control/bounded-derivative construction applied to Lucent's measurement problem. **No claim of priority over classical interpolation, optimal control or bang-bang acceleration results.** Its novel-to-this-work consequence is the intersection-of-constraints acquisition decision, not a new physiological law.

## Frozen synthetic reversal

All parameters are hypothetical: b=0.9, c=0.2, D=1/30 s, A=6000 s^-2. Neither speed nor acceleration ceiling is established for a human.

| V (s^-1) | Speed-only dip | Acceleration-only dip | Joint dip F | F/(b-c) | Conditional joint result |
| ---: | ---: | ---: | ---: | ---: | --- |
| 45 | 3/4 | 5/6 | 93/160 | 93/112 | EXCLUDE if hard ceilings truly hold |
| 60 | 1 | 5/6 | 7/10 | 1 | Touch feasible; no exclusion |
| 65 | 13/12 | 5/6 | 117/160 | 117/112 | Crossing feasible; no exclusion |

For V=45, **both standalone tests fail**, yet the joint constraint yields a minimum aperture of 51/160 = 0.31875, strictly above the 0.2 closure threshold. This is the decisive prediction. The frozen 240-fps hypothetical case returns F=5/384 and ratio 25/1344, the acceleration-limited regime; doubling the 30-fps gap to 1/15 s removes exclusion.

For fixed A=6000, D=1/30 and b-c=0.7, the joint critical speed is **V=60/s**, versus the speed-only critical speed 42/s. This is a 42.9% relaxation of the hypothetical speed requirement when a hard acceleration ceiling is independently available. For fixed V=45/s, the joint critical acceleration is **A=20250/s^2**, versus acceleration-only critical A=5040/s^2. These are parameter-specific instrument-design calculations, not physiological estimates.

## Independent numerical falsification attempt

An independently written SciPy HiGHS linear program, not importing the exact evaluator, minimized the midpoint aperture subject to physical range [0,1], endpoint equality, discrete speed bounds, and discrete second-difference acceleration bounds. Two frozen grids produced the following **locally executed synthetic** values:

| V | Grid intervals | LP minimum | Analytic prediction | Absolute discrepancy |
| ---: | ---: | ---: | ---: | ---: |
| 45 | 120 | 0.3187500000 | 0.3187500000 | < 1e-10 |
| 45 | 240 | 0.3187500000 | 0.3187500000 | < 1e-10 |
| 60 | 120 | 0.2000000000 | 0.2000000000 | < 1e-10 |
| 60 | 240 | 0.2000000000 | 0.2000000000 | < 1e-10 |

The frozen acceptance tolerance was 0.025 aperture units; the LP observations agree more tightly for these aligned discretizations. This is independent **numerical optimization**, not independent human measurement. The discretized slope and second-difference constraints are not a substitute for physical continuous-time bounds.

The committed [exact evaluator](e002_539_joint_boundary.py), [20-case adversarial test suite](test_e002_539_joint_boundary.py), [independent Node BigInt replay](e002_539_independent_replay.cjs), [LP adversary](e002_539_lp_adversary.py), and [CI workflow](../../.github/workflows/e002_539_joint_boundary.yml) are intended to test equality, scaled physical witnesses, conservative timing, unsupported evidence and exact rational arithmetic. **Hosted CI success must not be claimed until a completed workflow is inspected.**

## Physical falsification and product consequence

A real validation would first use a borrowed high-speed camera plus an ordinary camera, independently photodiode-authenticated illumination/exposure/clock, and a controlled mechanical aperture or eyelid phantom with separately measured motion limits. The phantom can test shutter-gap predictions but cannot establish human eyelid limits. A human study then needs blinded independent native-frame anatomical raters, independently defensible continuous-time derivative envelopes, precommitted predictions, participant-disjoint prospective evaluation and adverse gaze/glasses/lighting/blur/missingness strata. Sampled peaks, cohort means, self-asserted attestation booleans and nominal FPS do **not** satisfy the premises. High-rate reference non-observation remains censored; only a qualified positive witness can falsify a frozen exclusion.

**Current real evidence: 0 independently certified human speed ceilings, 0 acceleration ceilings, 0 photodiode-authenticated camera captures, 0 independent anatomical reviews, 0 participant-disjoint human validations.** E002-539 is not an empirical validation of E002-371. It improves a conditional acquisition/abstention rule while preserving `ABSTAIN_UNCALIBRATED` and release `BLOCKED`. Do not resume tuning E002-534/535's rejected pixel-return observable. Hush PR #45 remains a separate workstream.
