> **Repository-priority correction, 2026-10-30.** E002-421 (2026-10-24) had **already proved the sharp equal-boxcar speed boundary** under the interior-headroom condition `b+VE/2<=1`, and E002-495 independently replayed that result before explicitly correcting its duplicate claim. E002-540 must **not** be described as discovering exposure-average aliasing, the general boxcar bound, or the need to abstain on uncalibrated pixel means. Its narrower incremental result is the **physical aperture upper-cap saturation case omitted by E002-421's interior theorem**: for `b=.9,V=45,E=.01`, `b+VE/2=1.125>1`, so the old interior theorem is inapplicable. The cap-aware sharp floor is `0.175`, versus `0.15` from an **invalid extrapolation** of the old formula. At exploratory threshold `c=.16`, the invalid extrapolation would fail to exclude while the cap-aware bound conditionally excludes. This post-hoc comparison is not a preregistered human result or a novel general optimal-recovery theorem; the repository's E002-389 general integral LP already addresses bounded physical ranges numerically. The preregistered c=.2 false point-sample witness remains valid, but is an illustration of **previously established** exposure aliasing, not a new phenomenon. No further equal-boxcar theorem iterations are justified without physical evidence. The test suite now has 19 local mathematical/evidence controls including this post-hoc regression case.\n\n# E002-540 RESULT | Finite exposure can reverse a velocity-based hidden-closure exclusion

Date: 2026-10-30. Lucent primary E002-371 kernel. Existing branch `research/observability-human-boundary` and draft PR #26. The [protocol](E002_540_FROZEN.md) was committed first at `ba993524`, before executing the new synthetic experiment. **Evidence tier: exact counterexample under a deliberately idealized linear exposure model, independent numerical optimization, and adversarial software tests. NOT human physiology, a measured camera, or a valid product certification.**

## Question

E002-371 requires pointwise anatomical apertures at both sides of a fully blind shutter gap. Ordinary camera pixels are exposure integrals. Even if frame time and exposure length are exactly known, can replacing an *exposure mean* with a *pointwise endpoint aperture* incorrectly exclude a hidden closure?

**Yes.** The error survives perfect clock timing, ideal global shutter, no sensor noise, no image blur, and a hard V-Lipschitz aperture trajectory. Those assumptions are more favorable than a real camera. The result does not require a real eyelid or imply that real pixel values equal normalized anatomical aperture.

## Sharp idealized mean-to-endpoint law

Let `a:[0,T+E] -> [0,1]` be V-Lipschitz, `V>=0`. Suppose a frame reports the exact *linear* exposure average `b=(1/E) int_0^E a(t)dt` over `E>0`. If `x=a(E)`, then the largest possible average for that x is

`M(x)=(1/E) int_0^E min(1,x+V(E-t))dt`.

The pointwise upper envelope follows directly from the speed ceiling and the physical aperture cap. The least possible x compatible with average b is the inverse of this monotone envelope, clipped at zero:

- Define `z=VE` and `M(0)=z/2` if `z<=1`, otherwise `1-1/(2z)`. If `b<=M(0)`, `x_min=0`.
- Otherwise, if `z<=1` and `b<=1-z/2`, `x_min=b-z/2`.
- Otherwise `x_min=1-sqrt(2z(1-b))`.

For E=0 the limiting observation is pointwise. With **two equal averages** b over non-overlapping exposures `[0,E]` and `[T,T+E]`, `D=T-E`, the sharp speed-only hidden-aperture floor is `max(0,x_min-VD/2)`. A time-reversed pair of maximum-average exposure profiles and a symmetric V-shaped blind-gap trajectory attain this bound (up to physical-floor saturation). This is a standard Lipschitz envelope construction, **not** claimed as a novel mathematical theorem or human blink law.

## Frozen exact-rational counterexample

All values below are **hypothetical**: global shutter period `T=1/30 s`, exposure `E=1/100 s`, blind gap `D=7/300 s`, V=45 normalized-aperture/s, two exposure means `b=9/10`, closure threshold `c=1/5`.

| Interpretation | Inferred exposure-edge aperture | Lowest admissible blind aperture | Exclude hidden closure? |
| --- | ---: | ---: | --- |
| **Invalid**: frame mean treated as pointwise | 9/10 | 3/8 = 0.375 | **Yes, falsely** |
| **Correct**: exposure integral with physical cap | 7/10 | 7/40 = 0.175 | **No** |

A seven-vertex piecewise-linear aperture trajectory has exact exposure averages `9/10` at both frames, obeys `0<=a<=1` and `|a'|<=45/s` everywhere it is differentiable, and dips below `c=1/5` for **exactly `1/900 s` (1.111... ms)**. The trajectory is continuous and Lipschitz, but has a cusp at the hidden minimum; it is not claimed to satisfy an independent acceleration ceiling. This is a counterexample to **speed-only** point-sample substitution, not to the properly premised E002-539 joint-derivative theorem.

## Independent falsification

The [exact Python Fraction construction](e002_540_exposure_average.py) was checked against a separately written [Node.js BigInt rational integration](e002_540_independent_replay.cjs), and an [independent SciPy HiGHS linear program](e002_540_independent_lp.py) with exposure-average constraints, physical aperture bounds, and speed-bounded adjacent differences. Local execution:

| V (/s) | LP grid intervals | LP minimum | Analytic minimum | Frozen decision |
| ---: | ---: | ---: | ---: | --- |
| 45 | 130 | 0.17500000000000004 | 0.175 | Hidden crossing feasible |
| 45 | 260 | 0.17500000000000104 | 0.175 | Hidden crossing feasible |
| 40 | 130 | 0.2505426356589159 | 0.2504906208587144 | Hidden crossing excluded conditionally |
| 40 | 260 | 0.2505098039215673 | 0.2504906208587144 | Hidden crossing excluded conditionally |

All four LP cases satisfy exposure means within numerical tolerance and speed constraints to floating-point precision. The **unseen V=40/s** prediction excludes closure while V=45/s does not. The preregistered 0.025 aperture tolerance was met without retuning. **19/19 local Python adversarial tests passed after the explicit cap-saturation regression was added**, including physical range, exact integrals, false point-sample exclusion, equality/invalid input handling, zero exposure, zero speed and no human-certification claim. Independent Node BigInt replay passed locally. The dedicated [hosted workflow](../../.github/workflows/e002_540_exposure_average.yml) was committed; hosted success must be verified separately before being claimed.

This is **synthetic model validation**, not independent physical measurement. Neither the LP nor the rational replay tests nonlinear image formation, anatomical labeling, real shutter phase or physiological speed limits.

## Product consequence

A camera frame reporting a high brightness/eyelid score cannot be treated as a pointwise anatomical aperture merely because its nominal FPS and shutter time are known. Even with perfect idealized exposure means, that shortcut can change the decision from **cannot exclude** to **exclude**. The correct evidence-gated product must require: authenticated exposure start/end and scanline timing; a validated image-to-anatomical-aperture observation model with uncertainty; independent endpoint geometry; a defensible *hard continuous-time* speed or acceleration ceiling; and nuisance coverage. Unknown transfer function, rolling shutter, gaze, glasses, blur, brightness shifts, missingness or clock uncertainty force abstention. A sampled peak, cohort average, or unsigned attestation does not provide the hard bound.

No production code is authorized to issue a hidden-closure exclusion from these synthetic inputs. Preserve `ABSTAIN_UNCALIBRATED` and release `BLOCKED`. Do not revive the E002-534/535 rejected pixel-return observable.

## Next physical/human experiment, not another synthetic threshold search

1. **Instrument bench:** borrow a phone/ordinary camera, an independently timed optical pulse or photodiode, and a moving opaque aperture/servo or linear translating shutter with a ruler/fiducial. Capture at multiple known exposure lengths and phase offsets. Record raw files, clock uncertainty, illumination profile, and a separate high-speed/encoder trajectory. Preregister predicted exclusion vs non-exclusion under the *measured* exposure integration and independently bounded motion. Include saturation, nonlinearity, rolling-shutter rows and light flicker as explicit failure/abstention conditions. A phantom validates the instrument pipeline only, never human speed ceilings.
2. **Human pilot:** collect consented high-rate native eyelid sequences with two independent blinded anatomical raters, per-frame aperture intervals and rater disagreement. Determine whether any defensible continuous-time speed envelope can be established with measurement and between-sample uncertainty; sampled peaks alone cannot. Freeze predictions before viewing held-out participant references. Require independently authenticated camera timing and participant-disjoint testing with adverse gaze/glasses/lighting/blur/missingness strata.
3. **Reference sensitivity:** report positive independently observed threshold crossings as falsifiers. A high-speed reference that misses a brief closure is *censored*, not evidence of no closure; the present witness lasts only 1.111 ms below threshold. Do not interpret an empty 240-fps reference as absence of a blink.
4. **Stop rule:** if no hard human motion envelope and independently validated image-to-aperture transfer can be established, retire real-world deterministic hidden-closure exclusion. Retain a bounded research measurement with abstention and empirically calibrated participant-level risk instead.

**Evidence still absent:** authenticated physical shutter measurements, independent native-frame anatomical ratings, hard human derivative ceilings, and prospective participant-disjoint human predictions. Hush draft PR #45 remains separate and untouched.
