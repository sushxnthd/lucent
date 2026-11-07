# E002-422 frozen protocol — unequal shutter means and full-horizon observability

**Frozen before implementation or outcome calculation, 2026-10-24.** Single active kernel E002-371. This is conditional measurement mathematics, **not human validation**. Preserve branch `research/observability-human-boundary` and draft PR #26. Do not requalify the rejected E002-417 optical proxies.

## Question and model

E002-421's equal-boxcar-mean law cannot be applied directly to realistic unequal camera observations. Determine a sharp rule for two **unequal, exact, independently calibrated physical-aperture** boxcar averages `a,b`, uniform exposure length `E`, centers `0,d`, `0<E<d`, a continuous `V`-Lipschitz trajectory `x(t) in [0,1]` over `[-E/2,d+E/2]`, and closure threshold `theta`. Predeclare the balanced-slope regime `abs(a-b) <= V*(d-E)`, `0<theta<min(a,b)`, `L=(a+b-V*d)/2 >= 0`, and `max(a,b)+V*E/2 <= 1`. Outside this restricted regime, return conditional `UNRESOLVED_MODEL`; never extrapolate the formula.

## Predictions frozen before running code

**P1:** For every feasible trajectory, the minimum physical aperture anywhere in the **entire two-exposure observation horizon**, including both exposure windows and their gap, is at least `L=(a+b-V*d)/2`. This bound is **sharp** and attained by `x_star(t)=L+V*abs(t-t_star)`, where `t_star=d/2+(a-b)/(2*V)`. The balanced-slope assumption places `t_star` in the unexposed gap. Both exact shutter averages of `x_star` equal `a,b`.

**P2:** The conditional full-horizon certificate `NO_CLOSURE` is sound iff `L>theta` in this model. If `L<=theta`, the V-valley reaches closure while a distinct piecewise-constant-over-each-shutter open trajectory, joined across the gap, reproduces the same two averages and stays above `theta`. The dimensionless ratio `Gamma_asym=V*d/(a+b-2*theta)` is <1 precisely in the no-closure regime.

**P3:** The tempting shortcut `max(a,b)-V*d/2>theta` is **unsafe**. Freeze `a=.4,b=.3,V=50/s,d=.006s,E=.002s,theta=.2`. Predict `t_star=.004s`, `L=.2`, a hidden threshold crossing, both measured means unchanged, while the unsafe max-mean shortcut falsely certifies because `.4-.15=.25>.2`. Include a no-crossing trajectory with the same means.

**P4:** A separately implemented numerical linear program on piecewise-linear trajectories, with **exact trapezoidal integration** over both exposures and Lipschitz constraints, will reproduce `L` within 1e-6 across at least 30 independently sampled admissible parameter sets. It must include both safe and ambiguous cases. An independent numerical quadrature checks the frozen witness. Invalid regimes, missing provenance, impossible physical feasibility, and nonfinite inputs must abstain; no real-world product certificate is authorized.

## Relevance, falsifiers and evidence tier

This extends E002-421 from equal means and the gap to unequal means and the full two-exposure horizon in a precisely restricted balanced-slope regime. It changes **which intervals** could be conditionally excluded, but never authorizes real camera outputs. Report any LP mismatch or invalid example rather than fitting thresholds. Outside the balanced-slope regime, use E002-389's general joint-integral LP, not this formula. A hard physiological V, physical aperture transfer, exposure timing, row timing, independent human lid annotations, and unseen-participant/device validation are absent. `ABSTAIN_UNCALIBRATED` remains mandatory for hidden-closure, blink-duration, PERCLOS and fatigue claims.

**Novelty boundary:** special-case optimal recovery under Lipschitz constraints is established mathematical literature; do not claim a new general theorem or physical breakthrough. Human-rater handoffs E002-407/E002-418 remain the decisive empirical dependency. No raw eye frames, participant identifiers, private annotations or simulated rater sheets in the repository.
