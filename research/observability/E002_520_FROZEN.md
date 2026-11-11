# E002-520 | Frozen cross-camera closure-predicate transport falsification

Date: 2026-10-29. E002-371 primary kernel, existing branch and draft PR #26. Frozen **before** implementing E002-520. Evidence tier: analytic two-world falsification plus prospective software controls; **not human or physical measurement**.

## Target

E002-519's executable accepts a categorical `CLOSED_WITNESS` with generic photometry/nuisance booleans but does not encode the ordinary-camera closure threshold, a quantitative upper bound on the exposure-averaged reference aperture, or cross-camera geometry/iris-normalization transport. A categorical label alone is insufficient to establish that the **same prespecified scalar predicate** was violated. This experiment tests the missing condition without weakening the one-sided reference-censoring logic.

## Two-world kill test (hypothetical)

Freeze the ordinary-camera predicate `a_o(t) <= theta = 0.20`. A reference observation supports `mean(a_r) <= 0.19` and is labelled CLOSED_WITNESS, in an independently timed exposure strictly inside an ordinary-camera blind gap. World A has `a_o = 1.0 a_r`, so a witness can be certified. World B has `a_o = 1.2 a_r`, so the upper bound on ordinary aperture is 0.228 > 0.20 and the same categorical label is **not a certified witness**. The label and timing alone cannot distinguish worlds. Scale here represents uncertainty in cross-camera iris/lid coordinate transport, not a claimed physiological difference.

## Prespecified mathematical gate

For a nonnegative physical aperture `a_r(t)`, calibrated exposure integration yields a conservative upper bound `mean_E(a_r) <= U_r`. Independent calibration must establish for all relevant times `a_o(t) <= K_max * a_r(t) + B_max` with finite `K_max >= 0`. Therefore `mean_E(a_o) <= K_max*U_r+B_max`. If this upper bound is <= frozen ordinary threshold `theta`, then at least one instant within the reference exposure satisfies `a_o(t) <= theta`. With independently established strict timing containment in the ordinary blind interior, this is a one-sided contradiction of an EXCLUDE prediction. If the transport bound, linear exposure-integration premise, coordinate correspondence, or independently attested timing is missing, return UNKNOWN, never a falsification or clearance.

This bound is sufficient, not necessary. No reference observation can certify absence of closure between its own samples. Require separate explicit attestations for two independent blinded anatomical raters, radiometry/linearity, clock, native provenance, cross-camera geometry/iris scale, and nuisance controls. These attestations are not authenticated by the program.

## Frozen tests and decisions

Implement a versioned E002-520 intake separate from historical E002-519. Test World A -> FALSIFIED, World B -> UNKNOWN; equality at threshold -> FALSIFIED; uncertain offset -> UNKNOWN; missing geometry -> UNKNOWN; nonfinite/negative scale -> reject; timing boundary -> no witness; OPEN_OBSERVED -> reference-censored, never verified negative; duplicate IDs -> reject; ABSTAIN -> not testable. Preserve all prespecified windows and failure modes. Compare against legacy E002-519 to demonstrate the unsafe *logical inference*, not a real false-positive human event.

No code may claim a physical cross-camera calibration or anatomical rating was obtained. If controls fail, record the failure and retain product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Do not touch Hush or merge the PR.
