# E002-484 frozen falsification protocol (2026-10-27)

Kernel: E002-371; branch: research/observability-human-boundary. This protocol is a prospective test of the **closure claim**, not a retest of E002-483's narrower stationary-vs-moving classification. E002-483's comparison may remain valid while closure inference fails.

## Frozen hypothesis and decisive predictions
Use the exact E002-482/483 moving aperture a_C(t)=1+d(t) mm, with d(t) linear through (0,0),(5,1),(15,-1),(20,0), and a nonclosing counterpart a_N(t)=1+(1-epsilon)d(t). Both have a(0)=a(10)=a(20)=1 mm and speed <=0.2 mm/ms. The first closes at t=15 ms; the second has minimum epsilon mm >0.

The two ideal 10-ms gates are C=(1.5,0.5) mm and N=(1.5-epsilon/2,0.5+epsilon/2) mm. Independent per-gate gain in [1-delta,1+delta] and additive error in [-q,q] yield overlapping raw-gate observation sets iff epsilon <= 2(delta+2q)/(1-delta), for 0<epsilon<=1 and delta<1. Prediction at delta=.10 and q=.03 mm: epsilon=.35 mm admits an identical observed two-gate vector for closure and nonclosure. Prediction at delta=0 and q=.03: epsilon=.10 mm admits overlap; epsilon=.13 does not. Prediction at delta=q=0: these *endpoint-matched scaled* trajectories differ for every epsilon>0.

Separate exact/no-nuisance control without endpoint authentication: a_S(t)=1+(pi/4)cos(pi*t/20) mm for t in [0,20]. It never closes (minimum 1-pi/4 mm), obeys speed pi^2/80 mm/ms <0.2, and produces exactly (1.5,0.5) mm gate means. It does not match a_C's t=0,10,20 instantaneous apertures and must not be used as a counterexample if those endpoints are independently measured.

## Tests and kill criteria
1. Independent numerical integration of both trajectories and the exact cosine control.
2. Explicit common observation witness for epsilon=.35, delta=.1, q=.03.
3. Exact threshold negative control epsilon=.36 (no full raw-vector overlap), plus q-only epsilon=.10 positive and epsilon=.13 negative.
4. Verify geometry, speed and endpoint constraints, and phase=0 as an allowed case within the E002-483 +/-2-ms budget.
5. Reject any claim that two-gate contrast alone certifies physical eyelid closure, even if it separates a chosen stationary trajectory from a chosen moving one. Do not infer a population physiological velocity bound from the illustrative speed.
6. Preserve all negatives. Synthetic only: no new physical or human acquisition.

This protocol is frozen before the E002-484 implementation. No model fitting or post hoc threshold adjustment is permitted.
