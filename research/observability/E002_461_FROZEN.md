# E002-461 — frozen quadratic-sensor shutter experiment (2026-10-26)

**Status:** preregistration, committed before implementation or evaluation. **Evidence:** synthetic/instrument-model falsification only; no new human trajectories or physical sensor measurements. **Parent:** E002-460 sharp *linear anatomical mean* dark-gap theorem. Preserve existing research branch and draft PR #26.

## Scientific question and kill rule

Does an exactly statically calibrated nonlinear sensor still permit false hidden-closure exclusions when a shutter integrates the sensor output before static inversion? If yes, kill the product assumption that "calibrated per-frame aperture" automatically equals the *linear anatomical aperture mean* required by E002-460. Require exposure-aware calibration or abstention. Do not claim physical human validation or mathematical novelty for Jensen/variance bounds.

## Frozen synthetic experiment

Two nonoverlapping, centered uniform shutters at t=0 and t=D, with D=1000/240 ms and width w=2.3 ms. Closure threshold c=2 mm; assumed closing cap C=567.103928/1000 mm/ms and opening cap O=274.616337/1000 mm/ms (published sample maxima used **hypothetically**, never universal physical limits). Place a genuine dark-gap closure a(tau)=c at tau=D/2, with a(t)=c+alpha*C*(tau-t) before tau and a(t)=c+alpha*O*(t-tau) after tau. Preselect alpha=0.99 for the primary falsification and alpha=0.95 as negative control. The shutter reads the exact time-average of g(a)=a^2 (units mm^2); static calibration is exact g^{-1}(q)=sqrt(q), but the aperture average is NOT sqrt(E[a^2]).

For a shutter fully on an affine side with slope magnitude s, m=E[a], q=E[a^2]=m^2+s^2*w^2/12. Pass sqrt(q) as if it were a linear aperture mean to the unchanged E002-460 rule. **Primary criterion:** a witnessed synthetic closure in the dark gap alongside E002-460's EXCLUDED_CONDITIONALLY is a counterexample to that *invalid observation model*, not to the theorem. Check that alpha=0.95 does not yield a naive false exclusion.

## Frozen repair and adversarial suite

For a nonnegative anatomical aperture with known directional velocity caps, let L=max(C,O). The exact shutter-time variance for a uniform shutter is w^2/12. The general Lipschitz variance inequality Var(a(T)) <= L^2 Var(T) implies m=E[a] >= sqrt(max(0, q - L^2*w^2/12)). This lower bound is conservative, not generally sharp with directional caps. Use it separately at both shutters, together with the necessary directional E002-460 dark-gap crossing condition. **Only** label EXCLUDED_CONDITIONALLY if every tau strictly inside the dark gap violates the necessary condition with the *lower* aperture means. Otherwise return NOT_EXCLUDED. Never return a positive POSSIBLE witness from lower bounds alone. Equality and numerical ambiguity are NOT_EXCLUDED.

Reject nonfinite or negative q, missing or unauthenticated shutter/clock/kernel, nonquadratic or uncalibrated transfer, unsupported units, unknown geometry/brightness/missingness/blur/gaze/glasses/sampling/rolling shutter, and unverified velocity-cap provenance with ABSTAIN_UNCALIBRATED. All outputs carry physical_certification=false. Sensor q uncertainty may be incorporated conservatively by replacing q with max(0,q-u) before lower-bounding m; if no certified uncertainty, abstain. In this synthetic experiment u=0 with explicitly synthetic provenance.

Run a seeded (461) independent randomized holdout of at least 10,000 valid affine hidden-closure trajectories with varied directional caps, shutter widths, gap lengths, threshold and slopes, using exact q formulas, and require **zero false exclusions** from the repaired evaluator. This tests implementation logic, not universal physical correctness. Report the naive false-exclusion count and abstention controls. Independently implement the witness and decision arithmetic in JavaScript, without importing Python.

## Interpretation and follow-through

If the primary counterexample occurs, withdraw any claim that static calibration alone licenses E002-460 on shutter-averaged image features. The corrected conditional instrument requires a verified nonlinear sensor model and shutter kernel, *plus* hard speed bounds; ordinary RGB cameras do not currently satisfy these prerequisites. If synthetic checks fail, preserve failure and debug without retuning alpha or replacing the preregistered case. No product release, no S21/S22 access. E002-371 physical validation remains NOT_ESTABLISHED and the release gate remains ABSTAIN_UNCALIBRATED.

For actual human validation, use the already frozen E002-456 prospective two-camera/two-rater protocol; separately calibrate the full dynamic feature-to-aperture mapping under shutter integration, not merely static still frames.
