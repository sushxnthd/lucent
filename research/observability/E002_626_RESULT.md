# E002-626 | Time-local asymmetric shutter-gap budget (conditional synthetic result)

**Evidence tier:** mathematical extension with exact-rational synthetic witness. No human, camera, or independently calibrated velocity envelope obtained. Product remains `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.

## Question and result
E002-371 uses one global speed ceiling V. If independent calibration supplies *time-local*, direction-specific bounds v_down(t) and v_up(t), a hidden closure at candidate time tau in a dark gap [0,G] requires BOTH
`a-c <= integral_0^tau v_down(t) dt` and
`b-c <= integral_tau^G v_up(t) dt`.
Here a,b are **conservative lower endpoint-aperture bounds**, c is the independently frozen closure threshold, and all timing uncertainty must be propagated adversarially. If no tau in [0,G] satisfies both inequalities, hidden closure is excluded conditional on these envelopes. The global-V rule is a special case. A witness tau only establishes *kinematic possibility*, not that closure occurred. With integrable envelopes and no other dynamics, the criterion is sharp: construct a descending trajectory at no more than v_down until it reaches c, hold there if necessary, then ascend at no more than v_up. Additional physiology or minimum-dwell constraints may change sufficiency.

## Exact synthetic counterexample to global-envelope decision
Gap G=20ms; a=b=2mm; c=0mm. A valid but coarse global bound V=300mm/s does not exclude closure (each 10ms half permits 3mm travel). An independently certified local bound of 100mm/s over each half allows only 1mm per half and **excludes closure at the midpoint**. At 200mm/s per half, a piecewise-linear trajectory exactly reaches closure at the midpoint, establishing sharp equality for this example. **Caution:** exclusion at the midpoint alone does not exclude closure elsewhere; all candidate times must be considered. If the 100mm/s bound applies to the entire gap in both directions, all times are excluded because the total 20ms gap can supply only 2mm total travel versus 4mm required.

## Verification
`python research/observability/e002_626_local_velocity_budget.py` contains four exact-rational synthetic assertions. It tests candidate-time decisions and explicitly demonstrates why a single candidate cannot certify a whole gap. Assertions are committed but not yet independently or in hosted CI executed.

## Empirical falsification and product implication
Time-local bounds are **not** inferred from frame differences or the held-out participant. They require independent physical/dynamical validation including clock, geometry, acceleration, exposure integration, gaze, glasses, blur and missingness uncertainty. Before a product uses this improvement, preregister held-out human shutter-gap predictions and count any reference-confirmed closure inside an excluded gap as a certificate-family failure. If no validated time-local envelopes exist, use only defensible global bounds or abstain; do not substitute synthetic speeds.

This result offers a more discriminating *conditional* measurement design, not progress toward independently established physiological envelopes. Physical validation remains the immediate priority.
