# E002-553 RESULT | Shutter-support duration is not a shutter kernel

2026-10-31. Primary E002-371 human-observability kernel. Frozen first at commit `18249609ef7d2d2ce0fc2a325f74f418321671e1`. **Evidence tier: exact mathematical/synthetic instrument falsification. No physical camera, shutter photodiode, or human physiological validation.**

## A new decisive negative control for E002-552

E002-552's boxcar curvature exclusion requires a *uniform temporal exposure response*, not merely known exposure start/end times. We constructed an admissible shutter response with two finite-width pulses, the same nominal exposure support and center of mass as a uniform boxcar, and a perfectly known anatomical aperture trajectory. Substituting its measured means into E002-552's boxcar formula **falsely excludes a real hidden closure**.

Frozen dimensionless configuration:
- Dark gap `[0,1]`; exposure supports `[-1/2,0]` and `[1,3/2]`.
- Actual aperture `f(t)=(t-1/2)^2`, continuously in `[0,1]` over the full acquisition window; exact acceleration bound `A=2`; actual minimum `0` at `t=1/2`.
- Each shutter has half its sensitivity uniformly over its first `1/20` interval and half over its last `1/20` interval. Its effective center matches the uniform boxcar's.
- Both measured aperture means are exactly `46/75`; shutter temporal variance is `61/1200`, whereas uniform boxcar variance is `1/48`.
- Frozen closure threshold `theta=1/50`.

| Method applied to the **same synthetic measurements** | Exact lower bound | Decision at theta=1/50 |
|---|---:|---|
| Incorrect nominal-duration **boxcar** assumption | `3/100` | **False exclusion** (0.03 > 0.02) |
| Correct known two-pulse shutter kernel | `0` | **Abstain** (closure remains possible) |
| True anatomical trajectory | `0` | Closure actually occurs |

The 0.03 margin is an exact shutter-weight misspecification artifact. It is not a real-camera effect size or physiological sensitivity.

## Kernel-aware sharp envelope and proof

Let each exposure have a nonnegative normalized temporal kernel `K_i`, known temporal mean `c_i`, variance `v_i`, and calibrated mean anatomical aperture `m_i` with one-sided error `e_i`. Let `D=c_1-c_0>0`, `s=(t-c_0)/D`, and a **hard, independently justified continuous-time** `|f''|<=A`. For any dark-gap `t` between the kernel centers,

```
f(t) >= (1-s)*(m0-e0-A*v0/2)
      + s*(m1-e1-A*v1/2)
      - A*D^2*s*(1-s)/2.
```

Proof: `g(t)=f(t)-A*t^2/2` is concave. Jensen's inequality gives `g(c_i)>=E_Ki[g]`, and concavity between the two centers gives `g(t)>=(1-s)g(c0)+s*g(c1)`. Substitute the exact kernel second moments. The bound is attained by quadratic `f(t)=A*t^2/2+b*t+c` wherever that witness satisfies physical aperture bounds. With uniform boxcar `v_i=h_i^2/12`, this reduces to E002-552. These are standard Jensen/curvature facts, **not a new general theorem**.

This is an experimentally testable **kernel-shape observability boundary**: measured shutter support, rate and nominal exposure duration are insufficient to justify boxcar exclusion unless temporal weights are calibrated. With only support and *independently known* center `c`, the distribution-free variance ceiling `v<=(c-a)(b-c)` is available, but is weaker. Without even a certified center, the kernel-center interpolation cannot be invoked.

## Executable falsification and independent check

- [Exact Python instrument](e002_553_kernel_curvature.py): rational piecewise-uniform shutter weights, moment computation, general-kernel lower envelope, exact gap minimization, fail-closed nuisance gates and synthetic demo.
- [18 adversarial Python tests](test_e002_553_kernel_curvature.py): frozen witness, invalid weights/overlap/support, absent gates, asymmetric kernels/errors, loose acceleration and **1,000 seeded quadratic equality cases** (five exact gap points per case).
- [Independent Node.js BigInt oracle](e002_553_independent.cjs): separately integrates both pulse shutters and checks the frozen fractions plus five further quadratic equality points.
- [Dedicated hosted workflow](../../.github/workflows/e002_553_kernel.yml).

**Local execution before GitHub commit:** 18/18 Python test methods passed, including 5,000 exact seeded equality checks; independent Node.js oracle passed. Hosted CI status must be verified separately. The randomized equality test exercises the unrestricted quadratic class; it is not a physiological ensemble, and no held-out human sequences were used.

## Concrete physical falsifier (next external acquisition)

1. Use an independently driven LED/photodiode optical reference and an adjustable moving-aperture target with a measured mechanical/optical trajectory. Log hardware clock, sensor row and exposure settings; reject unsynchronized clock or unknown rolling-shutter row.
2. Characterize **the shutter temporal sensitivity kernel**, not only its nominal support, using brief light pulses at randomized within-exposure offsets, independent repeated calibration blocks, dark frames and camera RAW/linear output where possible. Recover kernel mean and variance with uncertainty bounds. Check saturation, ISP nonlinearity, auto-exposure, gamma, brightness drift and blur.
3. Pre-register two predicted exclusion decisions for identical target motion: (a) naive boxcar and (b) measured-kernel envelope. Alternate randomized shutter pulse patterns/conditions, with matched dark controls and clock uncertainty. The primary falsifier is an independently witnessed threshold crossing in a gap that the *calibrated* envelope excludes.
4. Hold out shutter timing/exposure settings, geometry, brightness, focus, gaze-like occlusion, glasses-like reflections, missing frames and motion blur. Any missing calibration or transfer condition yields `ABSTAIN_UNCALIBRATED`, not a negative label.
5. Only after the physical transfer is verified, proceed to the existing E002-548/549 participant-disjoint blinded anatomical review and E002-550 independently bounded high-speed kinematics. A reference-negative high-speed frame is never a continuous-time absence certificate.

## Product and novelty boundary

**Kill:** Any claim that frame rate, nominal shutter width, or exposure support alone supports a boxcar curvature exclusion. A measured shutter *kernel* (or conservative certified moment bounds), calibrated linear anatomy-to-sensor transfer, hard acceleration bound, and timing/nuisance evidence are necessary. A supplied boolean gate is not independent physical authentication. Do not expose the conditional exclusion as a real-world blink-negative result.

Prior work E002-421/422 covered velocity-boxcar limits, E002-547 exposure integration and E002-552 the uniform boxcar curvature boundary. E002-553 adds a **finite-pulse shutter falsifier** and exact kernel-moment generalization; do not claim novelty for Jensen's inequality, generic sampling theory, or exposure response characterization.

**Evidence ledger:** authenticated physical shutter captures 0; independently rated human anatomical sequences 0; certified continuous-time human acceleration/velocity bounds 0; participant-disjoint physical predictions 0. Scientific status `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Keep PR #26 draft/unmerged. Hush remains separate.
