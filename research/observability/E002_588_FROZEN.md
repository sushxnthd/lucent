# E002-588 | Frozen nonlinear-response optical shutter nonidentifiability

**Freeze:** 2026-11-01, before implementing or executing E002-588. Primary E002-371, parent E002-587. Evidence tier: exact synthetic camera-response counterexample only. Existing branch `research/observability-human-boundary`, draft PR #26.

## Question and falsification target

Can an optical step-phase scan, even with zero phase/brightness noise and three calibrated rolling-shutter rows, identify the physical exposure support when the camera's intensity-transfer function is *unknown but strictly increasing*, instead of authenticated linear?

Freeze 75 samples: rows `r in {0,20,40}`; phases `p=0,0.5,...,12` ms. Use a common rolling delay `d=0.1 ms/row`. Forward model: raw integration fraction `f=clip((s0+r*d+E-p)/E,0,1)`, observed brightness `y=h(f)`. Require `h(0)=0`, `h(1)=1`, continuous strictly increasing, shared across every phase and row (not per-sample fitting).

Two frozen worlds:

- **A (linear):** `s0=2.1 ms, E=4 ms, d=0.1 ms/row, h_A(f)=f`.
- **B (nonlinear):** `s0=2 ms, E=4.5 ms, d=0.1 ms/row`; `h_B` is continuous piecewise-linear interpolation through `(0,0),(1/9,1/40),(8/9,9/10),(1,1)`. Segment slopes are `9/40,9/8,9/10`, all strictly positive.

## Preregistered predictions and kill criteria

1. All 75 observed brightness values must agree exactly as rational numbers across A and B, including saturated observations and every row. Any mismatch kills the counterexample.
2. Exposure supports differ: row 0 A [2.1,6.1] ms versus B [2,6.5] ms; row 20 A [4.1,8.1] versus B [4,8.5]; row 40 A [6.1,10.1] versus B [6,10.5].
3. At 30 Hz periodic sampling, assuming the three rows' union is the full relevant sensor support, the uncovered interframe gap is `T-(40*d+E)`: A `T-8` ms, B `T-8.5` ms, a 0.5-ms difference. This is a synthetic illustrative model, not a physical-camera claim.
4. Independent Python exact-rational and Node BigInt rational implementations must agree on the 75 observations and gap difference. Include controls: one swapped phase, invalid/nonmonotone LUT, identity-only B, changed rolling delay, and an additional off-grid probe phase that distinguishes the worlds.
5. Freeze a prospective discrimination phase `p=6.25 ms` for row 0. Predict A `0`; B `h_B(1/18)=1/80` (verify exact). The probe must distinguish the worlds without using any previously observed sample to tune the LUT. A negative or zero difference kills the unseen-phase prediction.

## Interpretation

This attacks the **linearity assumption**, not E002-587's correct conditional LP arithmetic. Without independently verified response linearization, the same perfect phase scan can correspond to different physical shutter supports and hence different hidden-closure certificates. A held-out phase probe can falsify this particular two-world ambiguity, but a single extra probe does not certify arbitrary unknown transfer functions. Do not claim human or physical calibration, velocity bounds, priority over optical metrology, or product readiness. Fail closed (`ABSTAIN_UNCALIBRATED`, release `BLOCKED`) until response linearity and physical shutter/clock are independently measured.
