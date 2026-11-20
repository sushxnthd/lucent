# E002-697 — Exposure-mean certificate can be materially conservative

**Evidence tier:** independently formulated finite-grid synthetic optimization, not a physical experiment. 2026-11-07 UTC.

## Test and result

For aperture a(t) in [0,1], speed |a'|<=1, exposure windows [-1,0] and [1,2], blind gap [0,1], and *true calibrated anatomical exposure means* 0.9 and 0.9, the E002-694 lower certificate is max(0,(0.9+0.9-2)/2)=0. A separate linear program minimizes the aperture over every blind-gap grid point while enforcing exposure integrals and the motion bound. The executable tests spacings 0.1, 0.05, 0.025; it checks feasibility and prints the attained minima. A local exploratory discretization using uniform sample means at 0.05 found minimum about 0.0667, but that exploratory number is **not** a result of the committed trapezoidal script and should not be quoted as its output.

This establishes a testable **finite-grid non-sharpness diagnostic**, not a continuous-time sharp theorem. Discrete admissibility does not by itself prove a strictly positive continuous-time lower bound between nodes; piecewise-linear interpolants have minima at nodes, but the global continuous feasible class may have narrower extrema. Do not issue new certificates from this diagnostic.

## Scientific consequence

A bounded aperture range and exposure-integral constraints contain information discarded by the conservative E002-694 formula. Future work can derive a continuous-time optimal-control bound, independently prove it, and test against held-out physical instrument traces. The prospective E002-690 human protocol and E002-695 blinded prediction remain the release-critical priorities; no additional dataset archaeology is justified.

**Release:** ABSTAIN_UNCALIBRATED / BLOCKED. No calibrated camera, independent eyelid speed ceiling, physical occluder or held-out human evidence. This is not a product authorization.
