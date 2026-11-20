# E002-720 — Velocity-ceiling misspecification is a certificate-safety failure

**Evidence tier:** executed deterministic synthetic exact-rational falsification, not human/physical validation. Date: 2026-11-08 UTC.

## Predefined test
Enumerate 8^4 = 4,096 positive rational configurations of endpoint apertures a0,a1, time gap Δ and actual Lipschitz velocity V, each drawn from {1/4, 2/4, ..., 8/4}. A complete closure/reopening trajectory exists exactly when VΔ >= a0+a1; the piecewise-linear path at speed at most V constructs the witness. The valid exclusion certificate is VΔ < a0+a1. Challenge the implementation with a velocity ceiling underestimated by 50% while keeping all other quantities exact. Equality must abstain.

## Executed results
Local Python run of e002_720_velocity_misspecification.py:
- Total configurations: **4,096**
- Correct velocity ceiling: **3,168 exclusions; 0 false exclusions**
- Underestimated velocity ceiling: **3,875 exclusions; 707 false exclusions**
- Example witness: a0=a1=1/4, Δ=1/4, actual V=2, claimed V=1. True motion can close and reopen exactly at the boundary (actual VΔ=1/2), but the falsely small ceiling certifies no closure (claimed VΔ=1/4).

These are deliberately constructed grid cases, **not estimates of human prevalence or clinical accuracy**. The test isolates a single invalid assumption; it is not an independent empirical verification of E002-371. The 707 cases are possible closure witnesses, not observed human blinks.

## Decision and next experiment
The velocity upper bound is safety-critical: it must come from independent continuous-time calibration with explicit sensor bandwidth and biomechanical assumptions. High-frame-rate sampled slopes, including OpenEDS at nominal 200 Hz, cannot supply a deterministic ceiling. If that gate is absent, return ABSTAIN_UNCALIBRATED, even when endpoint measurements and timestamps appear perfect. No product claim changes.

Next: independently timed mechanical occluder and calibrated velocity sensor with randomized shutter phase under E002-714; then participant-disjoint human replay. Do not substitute more synthetic parameter sweeps for acquisition.
