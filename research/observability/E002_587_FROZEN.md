# E002-587 | Frozen continuous-parameter optical phase inversion and grid-alias falsification

**Freeze:** 2026-11-01 UTC, before executing E002-587 solver or inspecting its numeric outputs. Parent E002-586; primary E002-371. Existing `research/observability-human-boundary` and draft PR #26. Synthetic/instrument evidence ONLY, not a physical shutter certificate.

## Scientific question

E002-586's 405-point grid was demonstrably insufficient to certify continuous physical shutter supports. Can the *entire* admissible continuous affine-rolling, rectangular-integration model be bounded with exact linear inequalities, and does the finite grid understate exposure uncertainty?

Let `x=(s0,E,d)`, `E>0`, row `r`, start `s=s0+r*d`, commanded optical phase `p`, normalized observed brightness `y`, phase uncertainty `delta`, and intensity uncertainty `epsilon`. The forward model is `clip((s+E-p_true)/E,0,1)`. Independent phase error per observation is in `[-delta,delta]`. For each observation set `lo=max(0,y-epsilon)`, `hi=min(1,y+epsilon)`. Existence of a phase and predicted brightness in the measured interval is equivalent to these linear inequalities:

* If `lo>0`: `s+(1-lo)*E >= p-delta`.
* If `hi<1`: `s+(1-hi)*E <= p+delta`.

Skip the respective constraint at saturation; do not treat a fully dark/bright sample as a partially integrated one. Restrict the physical model to the *continuous* rectangular domain `0<=s0<=4 ms`, `2<=E<=6 ms`, `0<=d<=0.2 ms/row`. Solve linear programs minimizing each row's `s` and maximizing each row's `s+E`. The extrema are **outer supports conditional on the model and assumed nuisance bounds**, not a certification of the camera. Compare directly to E002-586's 0.5/0.05-ms finite grid.

## Preregistered tests and kill criteria

1. Generate exactly the same 75 synthetic observations as E002-586: rows 0,20,40; phases 0,0.5,...,12 ms; truth `s0=2,E=4,d=0.1`. At `delta=epsilon=0`, recover row supports [2,6], [4,8], [6,10] ms within solver tolerance.
2. At `delta=0.5 ms`, `epsilon=0.1`, recover a nonempty continuous feasible region and supports at least as wide as E002-586's finite-grid supports. A strictly wider support falsifies treating the grid as an outer certificate.
3. Increasing either uncertainty may never narrow supports; the true synthetic model must remain feasible.
4. Saturated-only scans, missing rows, non-affine row shifts, contradictory intensity and missing optical/geometry/linearity controls must fail closed, not produce a physical certificate.
5. Perturb the true `s0` to an off-grid value (2.17 ms) and show a continuous solution exists at exact observations while the finite grid may have zero candidates. This is the decisive grid-miss control.
6. Independently replay linear constraints and primal solutions in JavaScript, including all observation-wise inequalities and parameter bounds; do not call a mere grid check a continuous proof.
7. Report solver feasibility and residuals, dependence on model assumptions, and uncalibrated release state. No physical data, human rater pairs, eyelid velocity certification or held-out physical closure predictions are claimed.

**Primary scientific consequence:** E002-371's effective unobserved gap must be computed using an outer shutter-support envelope; a finite-grid phase fit is insufficient. Fail closed on missing authenticated photodiode timing, unknown exposure/rolling model, nonlinear sensor transfer, unmodeled nuisance, or unbounded continuous parameter range. Product `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.
