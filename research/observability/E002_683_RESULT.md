# E002-683 | Conditional acceleration-to-speed observability law

**Evidence tier:** analytic conditional result with locally executed numerical witness (12 parameter pairs plus zero-acceleration case); not human/physical evidence, independent review, or authenticated calibration.

## Sharp global law
Suppose an aperture trajectory x(t) is defined for all real t, twice differentiable (or has absolutely continuous velocity), confined to an interval of width R, and has |x''(t)| <= A almost everywhere. Then **|x'(t)| <= sqrt(A R)** at every t. For A=0, bounded global affine motion forces x'=0.

Proof: fix t=0 with v=x'(0)>0. The acceleration bound gives x'(s)>=v-A|s| for |s|<=v/A. Therefore forward displacement on [0,v/A] is at least v²/(2A), and backward displacement on [-v/A,0] is also at least v²/(2A). The aperture range must accommodate their sum v²/A, so v²<=AR. Reverse signs for v<0. A bang-bang trajectory accelerating at +A over half the range then decelerating at -A over half attains sqrt(AR), with rest before and after; it has Lipschitz velocity and acceleration bounded almost everywhere. Smooth approximations approach the bound. Thus the constant is sharp in that function class.

**Scope and adversarial caveat:** This is not a free empirical eyelid-velocity ceiling. The global range R and *independent hard acceleration bound A* must be authenticated in consistent physical units. A finite capture interval without pre/post extension cannot use this bound at its boundaries: a trajectory entering the interval at arbitrary speed is not constrained by a finite-window acceleration bound alone. Pixel-space aperture with moving head/gaze is not automatically an anatomical aperture. Exposure integration, geometry, clock error, occlusion and missingness remain separate nuisances. The earlier E002-681/682 finite-measurement nonidentifiability remains valid when A is unknown.

## Reproduction and consequence
Run `python research/observability/e002_683_acceleration_envelope.py`. Locally passed 12 exact-parameter sharp envelope comparisons and one A=0 case. These check algebra and a constructed bang-bang witness, **not** a differential-equation proof checker or empirical validation.

A conditional product certificate may replace a separately measured speed ceiling V by sqrt(AR) **only** if an independently justified hard A and anatomical R, global-trajectory assumptions, and conservative camera timing/geometry are validated. Otherwise abstain. No human measurements were acquired; E002-671 physical shutter/photodiode and blinded held-out human study remain decisive. Production BLOCKED. This is a classical bounded-acceleration kinematic consequence; no novelty or priority claim before literature audit.
