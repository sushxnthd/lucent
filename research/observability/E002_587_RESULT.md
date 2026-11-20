# E002-587 | Continuous shutter inversion falsifies finite-grid outer support

**Protocol frozen before implementation:** [E002_587_FROZEN.md](E002_587_FROZEN.md) at commit `c8cd677`. **Evidence tier:** synthetic continuous-parameter LP under a deliberately restrictive affine rolling-shutter and rectangular-exposure model. This is **not** a physical calibration, an independently bounded human eyelid speed, or a new priority claim in optical camera metrology.

## New result (locally executed, 2026-11-01)

The E002-586 405-point grid reported [1,7], [3,9], [5,11] ms as outer exposure supports with ±0.5 ms phase and ±0.1 normalized-intensity uncertainty. That result **does not cover the continuous feasible parameter set**. E002-587 reformulates each saturated/unsaturated phase observation as linear inequalities and globally minimizes row exposure starts and maximizes row exposure ends over the *continuous* bounded model `s0∈[0,4]`, `E∈[2,6]`, `d∈[0,0.2]`.

| Row | Exact continuous support (ms) | Relaxed E002-586 finite grid (ms) | Relaxed E002-587 continuous support (ms) |
| --- | --- | --- | --- |
| 0 | [2,6] | [1,7] | **[0.9,7.1]** |
| 20 | [4,8] | [3,9] | **[2.9,9.1]** |
| 40 | [6,10] | [5,11] | **[4.9,11.1]** |

The finite grid understated both extremes by 0.1 ms, an aggregate 0.2 ms overstatement of the uncovered gap. Under a hypothetical periodic 30-Hz all-three-row exposure model, the conservative between-frame uncovered interval becomes **23.133 ms** instead of the grid's **23.333 ms**, and instead of a naive point-sample 33.333 ms. These are mathematical outputs from synthetic observations and assumed bounds, not physical sensor measurements.

**Decisive off-grid falsifier:** Replacing synthetic start `s0=2` ms by `s0=2.17` ms yields **zero** feasible candidates on E002-586's grid under zero noise, despite a unique feasible continuous model. Its exact row supports are [2.17,6.17], [4.17,8.17], [6.17,10.17] ms. Thus `MODEL_FALSIFIED_OR_GRID_MISSES_TRUTH` in E002-586 cannot distinguish a genuinely false physical model from a discretization miss.

## Independent verification and controls

The Python instrument uses SciPy HiGHS linear programming to obtain all six extrema and returns primal/dual witnesses. A **separately implemented Node.js verifier reconstructs every linear constraint from the synthetic observations**, checks all primal feasibility inequalities, dual sign, dual stationarity, and primal-dual objective equality. **18 independent primal-dual certificate checks passed locally** across exact, uncertain and off-grid cases. The Python self-test passed 17 declared synthetic controls, including saturated-only, insufficient-row, non-affine, inconsistent-intensity, all eight calibration assertion flags, uncertainty monotonicity, and finite-grid miss. The prior E002-586 hosted workflow #41296366425 completed successfully; E002-587 hosted CI is committed and must be verified separately. Local execution is not hosted verification.

**Analytic equivalence:** for observation `y`, `lo=max(0,y-epsilon)`, `hi=min(1,y+epsilon)`, and independently bounded true optical phase `p±delta`, the rectangular forward model admits a compatible observation iff `s+(1-lo)E≥p-delta` when `lo>0`, and `s+(1-hi)E≤p+delta` when `hi<1`. Saturated endpoints impose no inequality on their already-uninformative side. Because all remaining inequalities and parameter bounds are linear, primal-dual certificates verify global extrema **within this mathematical model**.

## What this does NOT establish

The LP's globally valid bounds are conditional on the asserted rectangular integration, linear intensity transfer, independent phase uncertainty, affine rolling delay, fixed exposure settings, and the *assumed* parameter box. They are not unconditional physical certificates. The calibration flags remain unauthenticated booleans. Model mismatch, auto-HDR, nonlinear tone mapping, missingness, finite LED rise time, motion blur, gaze/ROI changes, glasses, clock drift, and unknown row response can all invalidate the model. Numerical LP tolerances also require outward rounding or verified interval arithmetic before any future certified claim. Three rows do not establish the complete frame sensor model. The 23.133-ms calculation uses a synthetic 30-Hz period, not measured timestamps.

**Priority:** LP inversion is standard optimization, not claimed as novel; optical rolling-shutter metrology has established literature, including Huai et al. (2023), DOI 10.1364/OL.474375, and Kurosawa et al. (2024), DOI 10.3408/jafst.875. The novel target remains the prospective coupling of independently calibrated shutter supports with independently bounded continuous-time human eyelid motion.

## Consequence and next decisive experiment

E002-586's finite-grid supports must **not** be treated as physical outer envelopes. Even the continuous-LP supports are *model-conditional*, and no certificate may be promoted until authenticated photodiode-timed captures, model checks, and numerical outward rounding. Use [E002-585 human-study handoff](E002_585_HUMAN_HANDOFF.md) to collect synchronized ordinary/high-speed recordings and two independently blinded anatomical rater tracks, participant-disjoint holdout, and independently justified eyelid-velocity ceilings. Freeze no-hidden-closure predictions before unsealing high-speed reference. Any physical closure in a certified exclusion gap falsifies the proposed certificate or its assumptions.

**Evidence counts:** independently blinded human rater pairs 0; physically calibrated shutter captures 0; independently justified hard continuous-time eyelid-velocity ceilings 0; held-out physical closure predictions 0. **Product** `ABSTAIN_UNCALIBRATED`; **release** `BLOCKED`. Hush not modified in this primary run.
