# E002-472 — FROZEN instrument-feasibility and product-claim design test
Date: 2026-10-27. Frozen before E002-472 implementation and output inspection. Evidence tier: algebraic instrument-design prediction plus synthetic adversarial controls; **not physical/human validation**.

## Question and non-goals
Given the already frozen E002-456 uniform-symmetric shutter lower envelope, what *measurable* shutter/timing/geometry precision is necessary for an ordinary camera to conditionally exclude a hidden threshold crossing? This is an engineering feasibility experiment, not another physiological theorem or dataset archaeology. It must change which camera configurations Lucent even attempts to validate. All velocities in this protocol are hypothetical sensitivity parameters, **not observed human velocity limits**.

## Locked model and prediction
Two identical ordinary-camera shutter means are `a=c+m` mm, each with absolute uncertainty `u` mm; inter-center spacing `T` ms; symmetric exposure `w` ms; ordinary clock bound `e` ms; and a *hypothesized* hard velocity cap `V` mm/s. Under a uniform shutter, the E002-456 lower envelope is
`L=c+m-u-V*(w/4+(T+2e)/2)/1000`.
Thus for this symmetric-endpoint design, strict exclusion `L>c` is feasible **iff** `m>u` and `V < Vcrit=1000*(m-u)/(w/4+(T+2e)/2)`. For a support-only symmetric shutter replace `w/4` by `w/2`. Equality must not be promoted. This is not a population-physiology statement or a necessary condition for asymmetric observed endpoints.

The guaranteed ordinary dark gap exists only when `w+2e<T`. A reference camera with exposure `r` and reference clock error `er` can place a strictly interior positive witness only if `w+r+2*(e+er)<T`. If either fails, the relevant outcome must be `ABSTAIN_DESIGN`, never `NO_CLOSURE`. Positive witness localization also requires E002-464 dynamic response checks and E002-471 support containment, not just this geometry inequality.

## Prespecified matrix
Evaluate nominal 30, 60, 120, 240 fps (T=1000/fps), exposures 1/4/8 ms when nonoverlapping, `m=1.0 mm`, `u=0.1 mm`, `e=0.1 ms`, `r=0.2 ms`, `er=0.1 ms`, uniform shutter. Independently test hypothetical `V=50,100,200,400 mm/s` (not human estimates). Output numerical Vcrit and the dark-gap/reference-feasibility gates. The simulator must not emit physical release authorization.

## Adversarial controls / kill criteria
- Strict equality at Vcrit must be NOT_EXCLUDED; values just below/above switch appropriately.
- Increasing shutter duration, clock error, aperture uncertainty or assumed V cannot improve exclusion; decreasing aperture margin cannot improve exclusion.
- Unknown shutter, zero/nonfinite/negative input, overlapping exposure, no dark gap or infeasible reference support => fail closed.
- Independently cross-check the computed threshold by constructing the exact E002-456 input and comparing decisions. Any mismatch kills this design evaluator.
- Preserve a negative result if ordinary 30-fps configurations cannot exclude at illustrative speeds; do not tune m/u/V post hoc.
- Quantify *only* instrument feasibility; do not turn zero witnessed closures, synthetic examples, or dataset timestamps into anatomical negatives.

## Human/instrument acquisition consequence
Freeze this design matrix before borrowing/using a physical camera. First authenticate real shutter integration with a phase-scanned optical pulse visible to the sensor (independent timing and detector sensitivity), then verify an independently encoded moving aperture with sensor response and clock uncertainty characterized. Record raw camera mode, exposure, actual per-frame time, pulse delay, gain, row timing, position-encoder transfer function, and nuisance flags. Two blinded raters must annotate independently timed human reference frames with millimeter geometry and uncertainty; split by participant, never frame. If authenticated measurements cannot meet a selected design's feasibility gate, report it as a **rejected measurement configuration** rather than collecting a misleading human exclusion count. Human data and any hard velocity limit remain unavailable.

Keep E002-371 **NOT PHYSICALLY VALIDATED** and all hidden-closure, blink-duration, PERCLOS, fatigue and medical claims `ABSTAIN_UNCALIBRATED`. Do not merge PR #26 or touch Hush PR #45.
