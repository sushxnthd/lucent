# E002-552 RESULT | Exact curvature boundary for exposure-averaged aperture

2026-10-31. E002-371 primary kernel. [Protocol frozen before implementation](E002_552_FROZEN.md) at `a4f7e8ff1a22f990ec13bbb6b9b3f735bdffa305`. **Evidence: exact mathematical instrument model, adversarial constructed witness, seeded synthetic tests, independent arithmetic. NOT human evidence, physical shutter calibration, or physiological certification.**

## Scientific advance: close the instantaneous-to-integrated gap

E002-551 correctly derived a sharp bound for two *instantaneous* anatomical endpoint samples, but an ordinary camera typically integrates light over exposure windows. E002-547 already showed reference negatives can be erased by integration. Here we derive the sharp replacement when each observation is independently certified to be a **linear boxcar mean of anatomical aperture**. This is a stringent idealization, not a property of raw webcam RGB.

Let the shutter exposures be `[-h0,0]` and `[d,d+h1]`, dark gap `[0,d]`, `d,h0,h1>0`. Let their calibrated mean apertures be `m0,m1`, independently bounded mean errors `e0,e1`, and a hard continuous-time `|f''|<=A`. Put `c0=-h0/2`, `c1=d+h1/2`, `D=c1-c0`, `s=(t-c0)/D`. For every `t in [0,d]`, the exact conservative envelope is

```
f(t) >= (1-s)*(m0-e0-A*h0^2/24)
       + s*(m1-e1-A*h1^2/24)
       - A*D^2*s*(1-s)/2 .
```

**Proof:** `g(t)=f(t)-A*t^2/2` is concave. Jensen implies `g(ci)>=mean_exposure_i(g)`; concavity between the two exposure centers gives the interpolated lower bound. Replacing each mean by its worst-case error and simplifying yields the displayed formula. For a quadratic `f(t)=A*t^2/2+b*t+c`, `g` is affine, so every inequality is equality. This proves sharpness in the unrestricted smooth-function class, and in the physically bounded class whenever the witness remains within [0,1]. Minimize the displayed convex quadratic over **the dark gap**, not over both exposures. This is elementary concavity/interpolation mathematics, **not a new general theorem**.

For equal means m, equal exposure duration h and zero mean error, the exact minimum is

```
L_min = m - A*(d^2/8 + d*h/4 + h^2/6).
R_box = A*(d^2/8 + d*h/4 + h^2/6)/(m-theta).
```

For `m>theta`, `R_box<1` is a conditional exclusion, while `R_box>=1` cannot exclude hidden closure. In the instantaneous limit `h->0`, this reduces to E002-551. Exposure integration adds a **strictly positive correction** `A*(d*h/4+h^2/6)` to the worst-case aperture drop.

## Frozen falsifier: false exclusion with perfect acceleration and timing

Take `f(t)=(t-1/2)^2`, dark gap `[0,1]`, two exposures `[-1/5,0]` and `[1,6/5]`, `A=2`, `theta=1/10`. The true gap minimum is **0** at `t=1/2`; over the complete instrument window, f stays between 0 and 0.49. Both exact exposure means are `109/300`.

| Decision rule | Certified lower | Verdict |
|---|---:|---|
| **Invalid** E002-551 point-sample substitution | `17/150 = 0.113333...` | **False exclusion** |
| Correct E002-552 boxcar envelope | `0` | Correctly refuses exclusion |

Thus a perfect hard acceleration ceiling, exact shutter timing, zero sensor noise, and a valid anatomical aperture still **do not** justify substituting frame means into the instantaneous theorem. The counterexample is exact and fully in the physical normalized range.

## Adversarial tests and independent verification

Seed 552, 10,000 generated variable-slope, variable-curvature quadratic trajectories with 2–20-ms dark gaps, 1–8-ms exposure windows, asymmetric mean errors and exact rational arithmetic:

| Count | Result |
|---|---:|
| Physically admissible synthetic trajectories | 5,221 |
| Discarded out of [0,1] | 4,779 |
| True threshold crossings | 397 |
| Conditional exclusions | 3,398 |
| False exclusions within stipulated model | **0** |
| Envelope violations | **0** |

The 3,398 exclusions are **not** a measured sensitivity or performance improvement. Fifteen Python adversarial test methods passed locally; a separate Node.js BigInt oracle independently integrated the quadratic exposures and verified the exact witness and five unequal-exposure equality checks. [Executable](e002_552_boxcar_curvature.py) · [Tests](test_e002_552_boxcar_curvature.py) · [Independent oracle](e002_552_independent.cjs) · [Aggregate](E002_552_SYNTHETIC_AGGREGATE.json). Hosted CI success must be verified separately.

The implementation rejects inexact floats, invalid ranges, any nonzero uncertified clock uncertainty, and failed/missing independent nuisance, optical, anatomy, boxcar, hard-A, or timing gates. These are **caller-supplied conditional assertions**, not cryptographic authentication of real calibration. Even when all gates are true, output is only `CONDITIONAL_INSTRUMENT_EXCLUSION_ONLY`; no physiological or product release is authorized.

## Novelty, falsification and next decisive experiment

The interpolation/Jensen mathematics is standard. The new Lucent-specific result is an exact **exposure-aware observability boundary** plus a constructive counterexample that kills naive use of E002-551 on camera frame averages. E002-547 previously established integration-induced reference misses; E002-552 specifically repairs the curvature-exclusion calculation for ideal calibrated boxcar means. Do not claim priority for generic sampling or convexity theorems.

This does not establish that webcam brightness is linear in anatomical aperture, that its shutter support is a global boxcar, that hard human acceleration ceilings exist, or that the anatomical geometry survives gaze/glasses/blur. Real rolling shutters, nonlinear ISP, unknown shutter kernels, unsynchronized clocks and segmentation errors remain **ABSTAIN_UNCALIBRATED**.

**Next physical falsifier:** photodiode-time a controlled moving aperture with a calibrated optical target; collect two shutter-integrated measurements and an independently timed reference; pre-register E002-552's predicted lower envelope; vary exposure duration and nuisance conditions while holding true trajectory fixed. After transfer validation, acquire independently rated human trajectories and test participant-disjoint exclusions. A reference-negative sequence is not continuous-time ground truth.

**Authenticated physical captures: 0. Independent human anatomical ratings: 0. Certified continuous-time human A/V bounds: 0. Held-out human physical predictions: 0.** Lucent production remains **BLOCKED**, scientific status **ABSTAIN_UNCALIBRATED**. Keep PR #26 draft/unmerged. Hush workstream untouched.
