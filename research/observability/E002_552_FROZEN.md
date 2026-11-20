# E002-552 FROZEN | Exact boxcar-exposure curvature envelope

Frozen before executable, tests, or aggregate on the existing E002-371 kernel; branch `research/observability-human-boundary`, draft PR #26. Evidence tier is **mathematical instrument model plus constructed synthetic falsification**, not human evidence.

## Prediction and assumptions

E002-551's sharp interpolation envelope requires instantaneous anatomical endpoint samples. Predict that naively substituting exposure-averaged apertures can falsely exclude a true closure **even when** timestamps and a hard continuous-time acceleration ceiling are exact. Derive and test a sharp exposure-aware replacement, conditional on independent proof of linear boxcar integration of *anatomical aperture* (not merely RGB intensity), global shutter timing, bounded aperture error, hard continuous-time |f''| <= A, and valid geometry/quality.

Let two disjoint shutter intervals be `[-h0,0]` and `[d,d+h1]`, with `d>0`, `h0,h1>0`. Their exact linear means are `m0,m1`. Let exposure centers `c0=-h0/2`, `c1=d+h1/2`, and `s=(t-c0)/(c1-c0)` for `t in [0,d]`. With no mean error, predict the sharp lower envelope

`L(t)=(1-s)*m0+s*m1 - A/2*((t-c0)*(c1-t) + (1-s)*h0^2/12 + s*h1^2/12)`.

With independently certified mean errors `e0,e1`, subtract `(1-s)*e0+s*e1`. The envelope follows by setting `g(t)=f(t)-A*t^2/2`, concave because `f''<=A`; Jensen and concavity lower-bound g between the two exposure centers. Equality is achieved by quadratic f with f''=A and affine g. Minimize L over **only the dark gap [0,d]**. Return conditional exclusion iff `min L > theta`; otherwise possible closure/unresolved. This is a standard concavity/Jensen argument, not a new mathematical theorem.

For equal means m and equal exposures h, predict the exact central clearance `m - A*(d^2/8+d*h/4+h^2/6)`. Dimensionless exposure-aware ratio `R_box=A*(d^2/8+d*h/4+h^2/6)/(m-theta)` (only if m>theta); R_box<1 excludes, >=1 cannot exclude. Contrast naive `R_point=A*d^2/(8*(m-theta))`.

## Precommitted falsifier

Construct normalized anatomical aperture `f(t)=(t-1/2)^2`, `d=1`, `h0=h1=1/5`, `A=2`, `theta=1/10`, no timing or mean error. On the two exposures, predict exact means `m0=m1=109/300`; true minimum in dark gap is 0. The **incorrect** instantaneous substitution predicts `109/300-1/4=17/150>1/10` and falsely excludes. The **correct** boxcar envelope predicts minimum 0 and refuses exclusion. All f values over exposure-plus-gap lie in [0,1].

## Independent tests and kill gates

1. Exact rational proof-witness and independently implemented Node.js rational/closed-form oracle; equality at the quadratic witness.
2. Constant-aperture positive control with A=0 and authenticated model flags yields a *conditional* exclusion.
3. At least 5,000 seeded physically admissible quadratic trajectories with |f''|<=A, variable slopes, exposure durations and unequal means; zero false exclusions within the stipulated model. Preserve counts, seed, discarded cases and any false exclusions.
4. Vary exposure duration, aperture/clock error, missingness, geometry, blur, gaze, glasses, brightness, marker identity, rolling shutter, optical transfer and frame timing; require abstention when hard independent certificates fail.
5. Unknown shutter kernel, unverified radiometric-to-aperture transfer, rolling shutter, timestamp uncertainty without separately certified support, or human hard-A unavailable => `ABSTAIN_UNCALIBRATED`. Even valid synthetic results must not authorize production or imply physiological accuracy.

No new dataset search or provenance-tool work. This is a targeted falsification and instrument-law repair; the decisive next experiment remains photodiode-authenticated physical acquisition and blinded participant-disjoint human validation.
