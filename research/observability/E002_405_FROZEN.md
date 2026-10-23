# E002-405 — finite-sample velocity ceiling is not a physical hard bound (frozen before testing)

Date: 2026-10-24. Primary E002-371 kernel. Evidence tier: **distribution-free rank law + synthetic physical-aperture counterexample**, not human velocity measurements or a novel order-statistics theorem.

## New falsifiable question
The E002-399 human annotation bridge accepts `independent_velocity: true` and a numeric `speed_upper` without distinguishing a **physically justified deterministic upper bound** from the maximum observed speed in a finite human calibration sample. Can the latter create an invalid hidden-closure exclusion, even when camera, geometry, optical response, nuisance and timing are perfect?

## Frozen mathematical prediction
For n calibration velocities and m future velocities jointly exchangeable with distinct values, the probability that **at least one future speed exceeds the calibration maximum** is exactly m/(n+m). This is a rank statement, not a deterministic speed guarantee. It does not assert that every exceedance causes a false closure certificate. For n=20,m=10, n=100,m=100 and n=1000,m=100, test this against 5,000 seeded independent Monte Carlo replicates using continuous uniform and exponential speed distributions. Absolute discrepancy must be <0.03 in every cohort. Report the analytical risk and the observed frequency for all six cohorts. Distribution shift has no such guarantee.

## Frozen physical counterexample
Two perfectly calibrated instantaneous-like exposures of width 1 microsecond, centered at t=0 and t=0.04 s, observe a triangular normalized aperture with a(0)=a(.04)=0.30 and a(.02)=0.18. The closure threshold is 0.20. Actual speed magnitude is 6/s; a finite-sample ceiling of 4/s is incorrectly asserted as the hard speed bound. Predict: the existing `certify` issues **CONFIRMED_NO_CROSSING** under the incorrect speed, even though a real crossing occurs. Replacing the bound with the true hard 6/s must prevent that false certificate. An independent analytical oracle must check the triangular trajectory, exposure means and decisions.

## Frozen enforcement consequences
1. A new structured `velocity_bound_calibration` record must be required in the **human annotation bridge**, not merely the old `independent_velocity` Boolean.
2. Missing record, `sample_maximum`, `empirical_quantile`, `conformal_marginal` or unknown evidence types must return **ABSTAIN_UNCALIBRATED** even when the old Boolean is true.
3. Only explicitly documented `deterministic_physical_upper` evidence with an auditable provenance string and defined validity domain may enable the existing independent-velocity gate. Strings are NOT independently authenticated; independent external review is still required.
4. All previous E002-399–404 independent/synthetic regression suites must pass after the bridge change. Never rewrite earlier evidence.
5. No human physical-aperture validation, statistical population coverage, fatigue diagnosis, PERCLOS or unconditional blink-duration claims.

## Priority and prior art
The rank law is standard distribution-free order statistics / nonparametric tolerance-bound theory, related to conformal prediction. The scientific contribution in this run is a **specific falsifiable measurement-chain counterexample** and fail-closed enforcement of the hard-bound versus sampled-maximum distinction. Do not claim a novel general theorem. Keep PR #25 draft; Hush PR #45 untouched during this primary run.
