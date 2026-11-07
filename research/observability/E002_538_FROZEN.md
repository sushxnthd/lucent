# E002-538 FROZEN | Acceleration-limited hidden-closure boundary and sampled-velocity aliasing

Date: 2026-10-30. Lucent primary E002-371 kernel, established `research/observability-human-boundary` branch and draft PR #26. **Evidence tier: new conditional deterministic boundary and synthetic adversarial instrument-design test, NOT independently measured human acceleration, physical shutter calibration or a product certificate.**

## Question and falsifiable prediction

E002-536 rejected treating a sampled peak eyelid velocity as a hard continuous-time bound. Can an *independently established* hard bound on normalized aperture acceleration instead provide a sharp closure-exclusion law even if no trustworthy velocity bound exists? For a twice-differentiable normalized aperture a(t) with `|a''(t)| <= A`, independently known **pointwise** endpoint apertures `a(0)=b0>c`, `a(D)=b1>c`, and an authenticated fully unobserved interval of length D, predict that every admissible path obeys

`a(t) >= L(t) = b0 + (b1-b0)t/D - A*t*(D-t)/2`.

Consequently a hidden crossing `a(t)<=c` is impossible **if and only if** `min_[0,D] L(t) > c` (subject to the physical aperture range and the same fixed endpoints). The lower parabola is a sharp witness; if its minimum is below c, a scaled convex parabola with curvature at most A reaches exactly c while staying within [0,1]. Equality allows touching c and must NOT be certified as excluded.

For equal endpoints b0=b1=b, the dimensionless acceleration ratio `Q=A*D^2/[8*(b-c)]` predicts NO_HIDDEN_CROSSING only for Q<1. Q=1 permits touching; Q>1 permits crossing. Unlike the E002-371 speed ratio, this is an acceleration-only conditional boundary. It is not a new physiological measurement.

## Frozen exact-rational synthetic cases

Use exact Fraction arithmetic and no random calibration:
- Equal endpoints b=9/10, c=1/5, D=1/30 s: A=3000 s^-2 gives Q=25/42 (<1), **excluded conditionally**; A=5040 gives Q=1, **touch permitted**; A=6000 gives Q=25/21 (>1), **crossing feasible**.
- Same b,c and A=6000 at D=1/240 s gives Q=25/1344 (<1), **excluded conditionally**.
- Asymmetric endpoints b0=4/5, b1=9/10, c=1/5, D=1/30, A=6000: independently minimize L(t) at clamped vertex; test a witness and exact boundary, not a symmetric approximation.
- Sampled-velocity alias: construct `a(t)=b-(b-c)*sin^2(pi*t/D)`; the two endpoint aperture samples and endpoint derivatives are identical, yet a(D/2)=c. This establishes that sampled endpoints and sampled peak velocity alone cannot certify continuous-time absence. This sinusoid has a finite acceleration scale, which must be reported rather than suppressed.
- Timing nuisance: increase D to the authenticated worst-case gap, never nominal gap. Unknown/missing frame times or unknown pointwise apertures force abstention.

## Independent tests and kill criteria

Implement an exact-rational evaluator with a **strict** crossing/exclusion boundary; an independently implemented Node BigInt check of the equal-endpoint threshold; and >=10 Python adversarial tests covering equality, asymmetric endpoints, witness curvature, invalid geometry, invalid acceleration, missing frame timing, exposure-averaged pixels masquerading as endpoint aperture, unsupported acceleration evidence, sampled-velocity alias, and no product promotion. No data-dependent threshold tuning.

Fail and preserve evidence if any independently checked exact ratio disagrees, if a witness violates the curvature or [0,1] assumptions, if equality is labeled excluded, or if unsupported physical evidence yields a certified product claim. All outputs remain `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.

## Physical and human translation

The experiment predicts a **testable scaling law**: for independently measured acceleration envelopes and calibrated pointwise anatomical endpoints, doubling unobserved gap D multiplies Q by four. A human pilot must independently bound acceleration (sampled second differences are NOT a hard bound), physically authenticate shutter/clock and exposure integration, use two blinded anatomical raters, and test participant-disjoint predictions under gaze/glasses/lighting/blur/missingness nuisance strata. Without those, this study is a sharp synthetic boundary and an equipment-design calculation, not empirical validation of E002-371. No reopening rejected E002-534/535 pixel-return detector. Hush PR #45 remains untouched.
