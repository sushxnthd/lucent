# E002-551 RESULT | Direct curvature envelope improves conditional blind-gap exclusion

2026-10-31. Primary E002-371 Lucent kernel. [Frozen before executable](E002_551_FROZEN.md) at commit `34b9d398ee5d667c9bd135e32a99863c1b87b671`. **Evidence tier: mathematical interpolation bound plus synthetic falsification only. No human kinematics, no physical camera data, no authenticated hard acceleration ceiling.**

## New falsifiable scientific distinction

E002-550 converted sparse 400-Hz samples into a *conditional* global speed upper bound, requiring a separately certified acceleration ceiling. E002-551 asks a narrower question: can a particular hidden closure be excluded locally without first bounding every instantaneous velocity? Under independently hard |f''|<=A, independently bounded endpoint errors e, clock errors u, and truly instantaneous anatomical aperture samples, the standard sharp bounded-curvature interpolation inequality yields:

`f(t0+s*Delta) >= (1-s)*(y0-e) + s*(y1-e) - (A*(d+2u)^2/2)*s*(1-s)` for 0<=s<=1.

Taking the minimum of this quadratic gives a conservative, and in the stated smooth-function class sharp, local exclusion. The sharpness witness is itself a parabola. This is **not a novel interpolation theorem**. The potential research contribution is its experimentally testable observability consequence under real optical and anatomical transfer.

For equal endpoints a and positive clearance m=a-e-theta, define `R=A*(d+2u)^2/(8*m)`. The interval excludes a hidden closure only if R<1. With R>=1 the data cannot exclude it. When m<=0, no exclusion. This is a dimensionless law with an explicit physical failure mode.

## Frozen exact counterexample

Stipulated A=8000/s^2, y0=y1=0.25, e=u=0, closure threshold theta=0.2:

| Gap | Exact minimum lower envelope | Decision |
|---|---:|---|
| 5 ms | 0.225 | Conditional exclusion |
| 10 ms | 0.150 | Cannot exclude |
| 10 ms, **incorrectly declared** A=1000/s² | 0.2375 | **False exclusion under model misspecification** |

The 10-ms parabola `f(t)=0.25-4000*t*(0.01-t)` has actual minimum 0.15, satisfies |f''|=8000/s² and remains in [0,1]. Thus the correctly specified 10-ms exclusion would be false; the method appropriately refuses it. If A is underdeclared, it incorrectly excludes. This is an explicit kill criterion for any product that substitutes sampled acceleration maxima for a hard independent ceiling.

For equal endpoints, the earlier speed ceiling gives V=A*D/2; the optimal two-endpoint Lipschitz lower envelope then drops A*D²/4, while the direct curvature envelope drops A*D²/8. This factor-two *bound* difference is exact, not a physiological performance claim.

## Reproducible seeded synthetic experiment

Seed 551, 10,000 generated bounded-curvature parabolic intervals; 46 rejected because their true aperture trajectory or observed endpoints left [0,1]. The 9,954 accepted intervals include random nominal intervals, clock uncertainty, bounded endpoint error, curvature and anatomy-compatible trajectories.

| Outcome | Count |
|---|---:|
| Physically in-range synthetic trials | 9,954 |
| True threshold-crossing intervals | 79 |
| Direct curvature exclusions | **9,203** |
| Tight two-endpoint speed-envelope exclusions | **5,951** |
| False exclusions with correct stipulated assumptions | **0** |

The 3,252 additional conditional exclusions are a synthetic comparison against a precisely defined speed-only baseline, **not a measured clinical sensitivity improvement**. Zero observed false exclusions across these synthetic trials does not prove robustness outside the model. The constructed underdeclared-A witness explicitly falsifies that robustness.

Twelve local Python adversarial test methods passed, covering exact witnesses, 10,000 seeded trials, monotonic clock/error effects, missing hard A, exposure averaging, all 11 nuisance gates and invalid inputs. A separately implemented Node.js BigInt rational oracle reproduced 0.225, 0.150 and 0.2375. Dedicated GitHub Actions verification was committed; hosted success must be checked separately.

[Python executable](e002_551_curvature_exclusion.py) · [Adversarial tests](test_e002_551_curvature_exclusion.py) · [Independent oracle](e002_551_independent.cjs) · [Frozen aggregate](E002_551_SYNTHETIC_AGGREGATE.json)

## Product consequence and priority

This does **not** authorize ordinary-camera blink exclusion: a 30-fps frame is typically an exposure-integrated optical observation, not the certified instantaneous anatomical endpoint required here. Marker motion in a 3D lab dataset also cannot automatically be transferred to a scalar webcam aperture. Missing independent A, e, u, optical response, anatomy or any nuisance gate => `ABSTAIN`. Valid synthetic output is `CONDITIONAL_EXCLUSION_ONLY`, never a physiological certificate.

The next decisive step is an actual independently timed optical/aperture acquisition and blinded participant-disjoint anatomical testing. Use the controlled-access FaceBase 400-fps dataset only after authorization, and treat sampled speed/acceleration as **lower-bound evidence** until a hard continuous-time ceiling is independently justified. Avoid another round of provenance tooling or synthetic threshold polishing.

**Authenticated physical shutter captures: 0. Independent anatomical ratings: 0. Certified continuous-time human acceleration/velocity ceilings: 0. Held-out human predictions: 0.** Lucent remains `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
