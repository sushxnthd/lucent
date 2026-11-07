# E002-539 FROZEN | Joint velocity-acceleration observability law and instrument decision reversal

Date: 2026-10-30. Primary E002-371 kernel. Branch `research/observability-human-boundary`; draft PR #26. **Evidence tier: exact conditional mathematics, independent discrete optimization, and synthetic adversarial validation. Not physical shutter timing, new human eyelid measurement, or a product certificate.**

## Question, new prediction, and kill criterion

E002-371 bounds hidden closure using a **hard continuous-time** normalized-aperture speed ceiling V; E002-538 separately bounds it using a **hard continuous-time** acceleration ceiling A. Neither standalone bound is necessary for exclusion when both independent physical ceilings hold simultaneously. Test a sharper joint law, with an experimentally consequential regime in which **both standalone tests abstain but their intersection excludes a hidden closure**.

Let a:[0,D]->[0,1] be C^{1,1} (continuously differentiable with Lipschitz derivative), a(0)=a(D)=b>c, |a'(t)|<=V and |a''(t)|<=A almost everywhere. D must be a conservative, independently authenticated **fully unobserved pointwise** anatomical interval, not nominal inverse FPS or a camera exposure mean. Define h=D/2 and

`F(h;V,A) = integral_0^h min(V,A*s) ds`.

If A=0 or V=0, F=0. Otherwise F=A*h*h/2 for V>=A*h, and F=V*h-V*V/(2*A) for V<A*h. **Frozen prediction:** every admissible a satisfies min a >= b-F. This is sharp for C^{1,1} paths, up to physical-range saturation; for any threshold c in [0,b), hidden a<=c is excluded exactly when F<b-c. At equality, contact is possible and must not be called excluded. The extremal trajectory uses a'(t)=-min(V,A*(h-t)) before h and its time-reversed positive counterpart after h. For F>b-c, scale that trajectory by (b-c)/F to construct a valid [0,1] touching witness, without increasing V or A. For A=0 the equal-endpoint trajectory is constant.

## Preregistered exact rational cases

Freeze b=9/10, c=1/5, D=1/30 s, A=6000 s^-2.
- V=45 s^-1: speed-only dip V*D/2=3/4 > 7/10, acceleration-only dip A*D^2/8=5/6 > 7/10. **Both alone fail to exclude**. Joint F=93/160, joint ratio F/(b-c)=93/112 <1, minimum b-F=51/160 > c: **jointly excluded**.
- V=60 s^-1: joint F=7/10, ratio=1, minimum=c. **Threshold contact possible; no exclusion**.
- V=65 s^-1: joint F=117/160, ratio=117/112 >1, minimum=27/160 < c. **Crossing feasible**.
- V=45, A=6000, D=1/240 s: V>=A*D/2; F=25/1920 (=5/384), joint ratio=25/1344 <1; recover acceleration-only regime.
- At D=1/15 s with V=45 and A=6000, joint F exceeds 7/10; **no exclusion**. The unscaled extremal may violate the aperture floor; require a scaled [0,1] touching witness.

The exact 240-fps value is F=A*D^2/8=5/384, ratio=(5/384)/(7/10)=25/1344.

## Independent empirical/synthetic checks

1. Exact Python Fraction evaluator and independent Node.js BigInt rational replay must agree on all five frozen cases and strict equality semantics.
2. Independently discretized linear-programming adversary (SciPy HiGHS) minimizes center aperture under |finite-difference speed|<=V and |finite-difference acceleration|<=A, endpoints b and physical range [0,1]. For N=120,240 uniform intervals, it must find an admissible path and approximate the analytic bound within **0.025 normalized aperture units** for V=45 and V=60. Discretization is a synthetic instrument/optimization surrogate, not independent physiological evidence.
3. Perturbations: increase conservative blind gap; increase either ceiling; use unknown timestamps, missing native frames, uncalibrated exposure-average endpoints, cohort-mean/sampled-peak ceilings, geometry/gaze/glasses/blur/brightness failures, and unsigned attestation claims. Such inputs must never produce a physical or product certificate.
4. No fitted threshold or changes to E002-534/535 rejected pixel-return observable. If LP disagrees beyond frozen tolerance, preserve failure, do not tune parameters after observation.

## Product and human-validation consequence

The *conditional* acquisition region is the joint phase diagram F(D/2;V,A)/(b-c)<1. It is potentially less conservative than checking the speed and acceleration ceilings separately. **No current human evidence authenticates either hard ceiling**, so Lucent must remain `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. To validate this law empirically, independently obtain physical exposure/clock measurements and same-geometry pointwise anatomical endpoint intervals, use two blinded native-frame raters, independently constrain both between-frame derivative ceilings (not sampled maxima), freeze predicted exclusion/abstention before reference review, and evaluate participant-disjoint prospective records including adverse nuisance strata. A high-rate reference without a positive witness is censored, not proof of no hidden closure. Preserve the E002-537 minimum 19 participant-level calibration requirement for nontrivial exchangeable 95% conformal calibration, and do not treat it as shift-robust.

Hush PR #45 is a separate secondary workstream and must not be modified during this primary experiment.
