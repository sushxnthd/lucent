# E002-403 — prospective shutter-kernel falsification (frozen before execution)

**Evidence tier:** synthetic instrument and source-level regression only. No human physiology, actual camera temporal response, or independent external calibration is claimed.

## Question
E002-399 uses the uniform-exposure first absolute moment e/4 to bound the difference between the instantaneous aperture at a nominal exposure center and the exposure-weighted aperture mean. E002-401 accepts calibrated rolling shutter with equal row exposure profiles, but does not separately require temporal **weight uniformity** or a measured first absolute moment. Can an admissible nonnegative nonuniform temporal response yield a false no-crossing certificate?

## Frozen instrument and predictions
Physical aperture: a(t) = 0.19 + 20 |t - 0.005|, with t in seconds, normalized aperture and threshold 0.20. Two nominal centers t0=0 and t1=0.010; both exposures last e=0.010 s. Each exposure integrates a narrow 0.0002-s rectangular shutter-weight pulse at the **outermost** edge of its exposure: the first pulse starts at -0.005; the second ends at 0.015. The two frame kernels differ (a nuisance currently unverified by the bridge). Velocity bound V=20/s is exact, clock error and all other nuisances are zero. Means are calculated analytically from the piecewise-linear trajectory. A reference oracle independently evaluates weighted integrals numerically.

**P1:** Naive uniform correction V e/4 makes E002-399 certify CONFIRMED_NO_CROSSING over [0,0.010], although the physical aperture reaches 0.19 at 0.005.

**P2:** Using each kernel's independently bounded first absolute temporal moment, V * E_w|t-t_i|, prevents that false certificate (UNRESOLVED).

**P3:** With uniform temporal kernels, E002-399 returns UNRESOLVED on the same physical trajectory.

**P4:** Across 1,000 seeded adversarial trajectories (V 10..40/s, exposure 5..20 ms, event minimum below threshold, edge-pulse width 1..3% of exposure, event center at midpoint of adjacent frame centers), the naive uniform assumption makes at least 90% incorrect no-crossing certificates; the moment-aware method makes zero incorrect certificates.

**P5:** A missing independent temporal-kernel bound forces ABSTAIN_UNCALIBRATED in the human annotation bridge even when all earlier Boolean gates and geometry/optical/row calibration objects are present. A valid independently calibrated first absolute moment fraction allows synthetic clean controls to retain correct certificates; increasing the bound must never strengthen a certificate.

**P6:** All E002-399 through E002-402 independent regression suites continue to pass after fixture calibration is updated.

## Mathematical contract
For nonnegative normalized temporal weights w_i(s) supported on [t_i-e_i/2,t_i+e_i/2], Lipschitz aperture |a(t)-a(s)|<=V|t-s| implies
|a(t_i)-integral a(s) w_i(s)ds| <= V integral |s-t_i| w_i(s)ds.
The first absolute moment equals e_i/4 only for uniform weights. For any unknown nonnegative kernel supported in the exposure, a safe generic upper bound is e_i/2. The code must never infer a uniform kernel from exposure duration alone. This is classical weighted-Lipschitz analysis, not a novelty claim.

## Claim and stopping rule
A wrong certificate under an unverified temporal kernel is a falsification of Lucent's measurement-input contract, not of the E002-371 physical theorem. Reject uncalibrated shutter-response certificates; preserve ABSTAIN_UNCALIBRATED. No blink, PERCLOS, fatigue, or human validation claim.
