# E002-698 — Finite-grid exposure LP has a continuous-time quadrature gap

**Evidence tier:** exact-rational constructed falsification, not physical or human measurement. 2026-11-07 UTC.

E002-697's sampled LP uses trapezoidal integration for calibrated exposure averages. This is exact for piecewise-linear interpolants, not arbitrary Lipschitz trajectories compatible with the same nodes. A valid 1-Lipschitz aperture on [0,0.2], with values 0.9, 1, 0.9 at times 0, 0.1, 0.2, has true mean 0.95; endpoint trapezoid gives 0.90. Thus exact trapezoid equality can exclude feasible physical trajectories.

For L-Lipschitz aperture and grid cell widths d_i, absolute difference between true exposure mean and trapezoidal mean is at most L*sum(d_i^2)/(4*sum(d_i)). For uniform spacing d, this becomes Ld/4. Proof: on each cell integrate the upper/lower Lipschitz cones from the endpoint values and compare with linear interpolation; maximum integral deviation is L*d_i^2/4. Equal-endpoint symmetric tents attain the bound without aperture clipping. The exact-rational executable checks three saturating cases.

**Decision:** E002-697's uncorrected sampled LP optimum is not a continuous-time certificate. Correct exposure constraints by a proven quadrature envelope, cover off-grid minima, and independently calibrate anatomical aperture, velocity and shutter timing before claiming exclusion. The conservative conditional E002-694 bound is unaffected. E002-690 physical acquisition and E002-695 blinded prediction remain next.

**Release:** ABSTAIN_UNCALIBRATED / BLOCKED. No human recording, physical shutter measurement or certified physiological velocity ceiling was obtained. Independent replay of the committed executable remains pending.
