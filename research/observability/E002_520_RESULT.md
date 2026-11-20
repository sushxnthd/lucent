# E002-520 | Cross-camera closure-predicate transport falsification

Date: 2026-10-29. Primary E002-371 kernel. Frozen protocol [E002_520_FROZEN.md](E002_520_FROZEN.md) was committed first at `ac3cf1ca8f3f583588b6832bdfc1345561a8a1c2`. Evidence tier: **analytic counterexample, independent arithmetic, prospective software regression**. No new human or instrument measurement.

## New scientific information: a categorical witness is not automatically a same-predicate witness

The historical E002-519 reference-censoring evaluator can emit `FALSIFIED_BY_REFERENCE_WITNESS` from a categorical `CLOSED_WITNESS` and five human-supplied boolean attestations, without a numerical cross-camera aperture transport or the ordinary camera's frozen closure threshold. That is insufficient when the two camera views use different uncertain iris/lid coordinate normalizations.

Freeze ordinary-camera closure as `a_o(t) <= 0.20`, guaranteed blind interior `(10,30) ms`, and a reference exposure within `[12,20] ms`. The same reference observation gives a calibrated upper bound on exposure-averaged reference aperture `U_r = 0.19` and the same qualitative closed label in two hypothetical worlds:

| World | Cross-camera upper scale | Upper ordinary exposure mean | Same-predicate closure established? |
|---|---:|---:|---|
| A | 1.0 | 0.190 | Conditionally yes |
| B | 1.2 | 0.228 | No, insufficient bound |

Independent JavaScript arithmetic reproduced `1.0*0.19=0.19` and `1.2*0.19=0.228`. In World B, a constant true ordinary aperture of 0.228 is compatible with the supplied upper bound and has **no ordinary-threshold closure**. The historical categorical witness would be insufficient to distinguish the worlds. This is a logical inference counterexample, **not an observed false positive**.

## Sufficient one-sided transport law

For nonnegative reference aperture `a_r(t)`, a linear, independently calibrated shutter integration establishes `mean_E(a_r) <= U_r`. A separately justified pointwise cross-camera transport inequality `a_o(t) <= K_max*a_r(t)+B_max` for every relevant time, with finite nonnegative `K_max, B_max`, gives

`mean_E(a_o) <= K_max*U_r+B_max.`

If `K_max*U_r+B_max <= theta`, at least one instant in the reference exposure satisfies the *ordinary-camera* closure predicate `a_o(t) <= theta`. With strict reference-exposure containment in the guaranteed ordinary blind interior, and independent anatomical, radiometric, timing, native provenance, and nuisance evidence, this contradicts a frozen EXCLUDE prediction. Failure of this sufficient test does not prove absence of closure.

This law requires the **same underlying physical aperture** to be transported across cameras; cross-camera scale and offset must be calibrated independently under gaze, perspective, glasses, blur, brightness, missingness, and anatomical landmark uncertainty. Merely setting `geometry_transport_valid=true` is not evidence of calibration. Nonlinear radiometry, unmatched scanlines or unsynchronized clocks invalidate the implication.

## Implemented product/evidence consequence

The versioned [E002-520 evaluator](e002_520_cross_camera.py) requires the frozen ordinary threshold, reference exposure-mean aperture upper bound, nonnegative cross-camera scale/offset upper bounds, strict timing containment and six explicit external attestations. It reports `FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS` only when all quantitative conditions hold; otherwise it returns UNKNOWN, REFERENCE_CENSORED_NOT_FALSIFIED or NOT_TESTABLE. The old E002-519 categorical output is **not admissible as a same-predicate falsification** without an E002-520 transport check.

The [22 adversarial tests](test_e002_520_cross_camera.py) cover two-world reversal, threshold equality, offset uncertainty, missing transport, geometry, radiometry, clock, raters, boundary timing, reference censoring, duplicate IDs, invalid scale, nonfinite values and explicit product abstention. [Established reference workflow](../../.github/workflows/e002_519_reference_censoring.yml) was expanded to run both historical and new tests; a separate [E002-520 workflow](../../.github/workflows/e002_520_cross_camera.yml) was added. **Hosted pass is not claimed until a completed successful run is observed.**

## Limitations and next decisive step

This is an analytic/synthetic measurement-inference correction, not a new physiological law. A validated high-rate image-to-physical-aperture model and independently bounded cross-camera transport are still absent. Two independent blinded S01 anatomical ratings: **0**. Authenticated physical shutter/clock measurements: **0**. Certified continuous-time human speed bounds: **0**. Participant-disjoint physical predictions: **0**.

Stop further synthetic aperture-factor sweeps. The decisive next experiment remains private independent S01 anatomical adjudication and synchronized optical capture with physical calibration of same-predicate aperture transport, shutter timing, and reference censoring. Lucent product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush PR #45 untouched.
