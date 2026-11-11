# E002-594 | Can finite high-speed frames certify a continuous-time eyelid speed ceiling?

Date: 2026-11-02. Primary kernel E002-371. Evidence tier: exact synthetic instrument and mathematical falsification, **not human or physical-camera validation**. This plan was explored locally before repository persistence, so it is a frozen reproduction protocol, **not a preregistered empirical experiment**.

## Scientific question
E002-593's shutter-gap exclusion presumes an independently certified hard continuous-time velocity ceiling V. Does a high-frame-rate sequence alone supply V? If not, which *additional independently authenticated* dynamical premise permits a conservative conversion?

## Predefined model and predictions
Let a(t) be a normalized anatomical aperture, with measurements y_i at exact spacing h and |y_i-a(t_i)| <= epsilon. Under the extra hard assumption |a''(t)| <= A for every interval, derive and independently check:

V_upper = max_i (|y_(i+1)-y_i|+2 epsilon)/h + A*h/2.

The inequality is conditional on genuine continuous differentiability with Lipschitz derivative, authenticated clock, anatomy, geometry, complete coverage and a **hard** A ceiling. A maximum sampled finite difference is not itself a hard V ceiling. A physical source cannot certify A merely by measuring finite differences or fitting a curve.

Test 1: h=1/100 s, y0=y1=1/2, epsilon=0, A=200/s^2. Predicted bound 1/s, attained by a quadratic with a''=-A.

Test 2: same h and A, epsilon=1/500 aperture. Predicted bound 7/5 per second, attained by a(t)=249/500+(7/5)t-100t^2, with endpoints 249/500 and 251/500 but both observed as 1/2.

Test 3: without an authenticated hard A, the smooth functions a_k(t)=1/2+(1/20)sin(2 pi k t/h), k=1,10,100,..., all have identical endpoint samples but arbitrarily large peak speed. This is a mathematical counterexample, not a physiological construction.

Test 4: missing any independent premise, nonphysical aperture, invalid h/epsilon/A or missing coverage must return ABSTAIN_UNCALIBRATED. Independently implement exact arithmetic in Python Fraction and JavaScript BigInt. The synthetic fixtures cannot verify the provenance flags supplied to software.

## Product gate and prospective physical test
The result can at most enable **MODEL_CONDITIONAL_VELOCITY_BOUND**. It cannot enable a physical no-hidden-closure certificate. Independently measure shutter/clock and anatomical aperture, obtain two blinded rater streams and a defensible hard acceleration/velocity envelope from a separate instrument or validated physical model. Freeze participant-disjoint holdout, nuisance strata and exclusion predictions before labels. If A or any premise is unauthenticated, abstain. A held-out reference-confirmed closure inside a certified-exclusion gap falsifies the physical model or implementation.

No human rater pairs, physical shutter calibrations, independently certified A/V, or held-out physical predictions are supplied by E002-594. Production remains BLOCKED.