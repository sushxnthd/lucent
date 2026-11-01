# E002-590 | Frozen full-duty velocity-aliasing threshold protocol

**Freeze date:** 2026-11-01 UTC. **Primary kernel:** E002-371. **Parent:** E002-589. **Evidence tier:** exact idealized observation-operator analysis, NOT human/physical validation.

## Preregistered question
E002-589 produced a closure-versus-no-closure alias at normalized speed L=V*T=4. Is this speed necessary? Find the **sharp** speed threshold for an ideal full-frame linear aperture-integrating sensor when BOTH trajectories have identical known endpoints c, the open control is constant c, the closure trajectory reaches zero, a(u) is continuous, 0<=a<=1, and |a'|<=L almost everywhere on u in [0,1].

Define Y=integral_0^1 a(u)du. Alias means a(0)=a(1)=c, min a=0, Y=c. No noise, shutter gaps, unknown clocks, radiometric nonlinearity or geometry nuisance is permitted in this narrow experiment.

## Frozen prediction (to be attacked)
For 0<c<1, a zero closure is feasible only if L>=2c. Subject to that, the **maximum** integrated aperture among zero-reaching paths is

M(L) = L/4 for 2c<=L<=2; and M(L)=1-1/L for L>=max(2,2c).

Thus the sharp alias threshold is

Lcrit(c)=4c when c<=1/2; and Lcrit(c)=1/(1-c) when c>=1/2.

Below Lcrit(c), no closure path can have the same full-frame average as the constant-open control c. At equality, a piecewise-linear extremizer should match exactly. This is a conditional mathematical boundary, not a physiological speed estimate. At c=1/2, Lcrit=2, **half** E002-589's example L=4.

## Frozen exact witnesses
1. c=1/5, L=4/5, knots (0,1/5),(1/4,0),(3/4,2/5),(1,1/5), expected mean 1/5.
2. c=1/2, L=2, knots (0,1/2),(1/4,0),(3/4,1),(1,1/2), expected mean 1/2.
3. c=4/5, L=5, knots (0,4/5),(4/25,0),(9/25,1),(24/25,1),(1,4/5), expected mean 4/5.

## Independent falsification checks
- Compute exact-rational slopes, endpoints, extrema, integrals and zero events for each witness.
- Verify the upper envelope at the boundary and at an exact-rational speed just below the threshold; reject any subthreshold equal-average zero closure.
- Independently implement the witness and integral checks in JavaScript BigInt fractions without trusting Python-produced results.
- Attack assumptions: changing the baseline, requiring finite-duration closure, changing the response operator, or losing exact endpoints must not be silently generalized.
- For a 30-fps illustrative frame, convert Lcrit to Vcrit=Lcrit/T only as a dimensionless model consequence, never as a human speed claim.

## Product decision
If confirmed, E002-589's witness is not speed-sharp. Reject full-duty integrated-video 'no hidden closure' claims whenever an authenticated L permits aliasing, and abstain if L or the image-formation model is not independently certified. This is a *necessary observability condition*, not an automatic sufficient clinical or fatigue measurement certificate.

**Hard boundary:** No new human subjects, independently certified continuous-time eyelid speed, real optical shutter calibration or held-out physical predictions are produced by this mathematical experiment. Human acquisition remains the priority after this single speed-sharpness test.
