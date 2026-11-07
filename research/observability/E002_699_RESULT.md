# E002-699 — Off-grid anatomical minima invalidate sampled-only closure exclusion

**Evidence tier:** exact-rational synthetic falsification, executed locally with Python 3 standard library on 2026-11-07 UTC. No human or physical instrument measurements.

**Question.** E002-697's finite-grid optimization and E002-698's quadrature correction do not by themselves establish that the *continuous-time minimum* of an eyelid-aperture trajectory stays above the closure threshold. Can an admissible Lipschitz trajectory cross the threshold between sampled nodes while every sampled node remains above it?

**Constructed attack.** On a cell of width d, take a(t)=b-L min(t,d-t), with b=theta+Ld/4 and closure threshold theta. Both sampled endpoints are b>theta, but the continuous midpoint is theta-Ld/4<theta. This trajectory is exactly L-Lipschitz and has a hidden closure. With d=1/5, L=1, theta=1/2, endpoint apertures are 11/20, while the midpoint is 9/20. Twelve exact-rational witnesses spanning four grid widths and three velocity ceilings passed local assertions.

**Sharp correction.** For an arbitrary L-Lipschitz trajectory and sampling grid with maximal spacing d_max, min_t a(t) >= min_i a(t_i)-L d_max/2. Proof: each point is at distance at most d_i/2 from a cell endpoint; Lipschitz continuity gives a(t)>=min(a_i,a_{i+1})-L d_i/2. Equal-endpoint V-shaped trajectories attain equality. Consequently a sampled minimum above theta is not a valid continuous-time exclusion unless it exceeds theta+L d_max/2 (or an equally strong interval-specific bound). This is a discretization certificate, not a physiological velocity calibration.

**Implication for E002-697/698.** A quadrature-error envelope corrects the exposure integral but does **not** correct an off-grid minimum. Both envelopes are necessary for a certified continuous-time LP. A sampled-grid optimum alone can overstate exclusion even if exposure integrals are represented correctly. The earlier conservative E002-694 analytical bound is unaffected.

**Reproduction:** `python3 research/observability/e002_699_offgrid.py`. Local stdout: `E002-699 PASS 12 exact-rational hidden-closure witnesses`. Independent execution of the committed file is pending.

**Product consequence:** Do not ship sampled-grid-only closure-exclusion logic. Apply a certified off-grid Lipschitz correction, verified aperture/timing envelopes, and independently justified speed bounds; otherwise abstain. E002-690 synchronized physical acquisition and E002-695 blinded predictions remain the next decisive validation. Status: `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.
