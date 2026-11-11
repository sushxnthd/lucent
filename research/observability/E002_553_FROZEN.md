# E002-553 FROZEN | Non-boxcar shutter falsification (2026-10-31)

Primary E002-371 observability kernel. Freeze before writing experiment code. Evidence target: **exact synthetic instrument falsifier**, not human blink data, camera calibration, or new general theorem.

## Hypothesis to kill
E002-552's sharp curvature lower envelope is only valid for **known uniform boxcar shutter weights**, not merely a shutter-support interval and nominal exposure length. An equal-duration two-pulse shutter with the same center of mass can cause E002-552 to falsely exclude a hidden closure despite perfect timing, anatomical transfer, acceleration, and noiseless measurements.

## Frozen rational witness (dimensionless time)
- Gap [0,1], exposures [-1/2,0] and [1,3/2].
- True aperture f(t)=(t-1/2)^2. Thus 0<=f<=1 on full acquisition span, |f''|=A=2, and true gap minimum f(1/2)=0.
- Shutter weights on each exposure: 1/2 uniform on the **first 1/20** of the exposure and 1/2 uniform on the **last 1/20**. All other exposure times have zero weight. The two-pulse center is exactly the nominal boxcar center, but its temporal variance is larger.
- Both observed means must equal **46/75**. Both actual kernel variances about their centers must equal **61/1200**; a uniform boxcar of width 1/2 would have variance **1/48**.
- Set closure threshold theta=1/50 (0.02). The **invalid boxcar** lower bound must be **3/100** (0.03), hence falsely exclude closure. The kernel-aware lower bound must be **0**, hence abstain. A known-support, unknown symmetric-kernel fallback must not claim a certified boxcar exclusion.

## Kernel-aware hypothesis
For normalized nonnegative known shutter kernels K_i with mass one, known means c_i, variances v_i, and measurements m_i with one-sided errors e_i, and a hard continuous-time |f''|<=A, define D=c1-c0, s=(t-c0)/D. For t in [0,d] lying between the two centers, the sharp lower envelope is
L(t)=(1-s)*(m0-e0-A*v0/2)+s*(m1-e1-A*v1/2)-A*D^2*s*(1-s)/2.
Proof attempt: g=f-A*t^2/2 is concave; Jensen gives g(c_i)>=E_Ki[g], then chord concavity bounds g(t). For quadratic f=A*t^2/2+b*t+c, equality holds at every t; verify exactly. When K is uniform, v=h^2/12 and the E002-552 envelope is recovered. A boxcar-shaped *support* does not imply boxcar *weight*.

## Tests frozen before execution
1. Exact Fraction arithmetic verifies all witness fractions, true min, and false-exclusion decision.
2. Independent JS BigInt rational integration verifies shutter-weighted means and variances, not by copying Python numerical results.
3. Nonuniform two-pulse kernels, boxcar kernels, asymmetric errors, unequal widths, varying acceleration and randomized admissible quadratic trajectories must produce zero kernel-envelope violations under the stipulated model.
4. Negative controls: a misdeclared boxcar kernel produces at least one false exclusion; incorrect center-of-mass, negative shutter weights, unnormalized kernels, absent hard-A or anatomy/optical/timing gates must force abstention.
5. Nonlinear brightness transfer, rolling shutter, blur, clock error, gaze, glasses, and geometry are **not** certified by this mathematical model; reject claims unless independently calibrated.

## Interpretation and stop rule
Any positive synthetic witness kills a product claim that nominal exposure width alone justifies boxcar curvature exclusion. This is an exact transfer-model falsification, **not** an observed camera failure. Do not promote synthetic results into physiological sensitivity. Product remains ABSTAIN_UNCALIBRATED and production BLOCKED pending photodiode-authenticated shutter-weight measurements and blinded held-out human anatomical validation. Do not run another dataset archaeology loop.
