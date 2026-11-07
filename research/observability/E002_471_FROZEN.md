# E002-471 FROZEN — reference crossing must be inside an authenticated unexposed gap

**Frozen:** 2026-10-27, before editing E002-456 or running the new regression. **Evidence tier:** deterministic synthetic adversarial classification; no new human anatomical reference, shutter calibration or physical acquisition. Preserve E002-470's completed hosted result and do not reopen S19 timing archaeology.

## Scientific question

E002-456's prospective protocol requires the *entire temporal support* of an independently measured positive anatomical crossing to be inside the ordinary camera's **unexposed** interval, after camera and reference clock errors. The current evaluator checks only whether the reference lies between the ordinary frame **centers**. Does it incorrectly count a crossing during an ordinary-camera exposure as a hidden-gap witness?

## Frozen counterexample and predictions

Ordinary camera centers: 0 and 10 ms. Symmetric ordinary exposure: 4 ms. Its first exposure ends at 2 ms, second begins at 8 ms. Independent reference exposure: 0.2 ms. Camera clock uncertainty: 0.1 ms; reference clock uncertainty: 0.1 ms. The required strict reference-center margin from either ordinary center is

`g = ordinary_exposure/2 + camera_clock_error + reference_clock_error + reference_exposure/2 = 2.3 ms`.

For a reference report with `aperture+uncertainty <= threshold`, freeze the following predictions:

1. At 1.0 ms, the reference support intersects the first ordinary exposure. It is **not** a witnessed *dark-gap* crossing; label `REFERENCE_INCOMPLETE` even if the research endpoint evaluator returns `EXCLUDED_CONDITIONALLY`. Never label `joint_falsification=true` based solely on this out-of-gap reference.
2. At 5.0 ms, the same positive reference is strictly inside the dark gap; label `WITNESSED_CROSSING`. If conditional exclusion holds, label `joint_falsification=true`, meaning joint model assumptions are inconsistent, not that a physiological law has been disproved.
3. At exactly 2.3 or 7.7 ms, strict support containment fails and the reference must be incomplete. An increase in either exposure width or clock uncertainty must not turn an incomplete reference into a valid gap witness.
4. If ordinary exposure plus twice the camera clock uncertainty reaches the center separation, there is no guaranteed unexposed gap; abstain. If reference support cannot fit strictly in the guaranteed gap, abstain from reference-witness evaluation.
5. Preserve all existing research-only product restrictions: `physical_release_authorized=false`, `ABSTAIN_UNCALIBRATED`; reject missing/invalid nuisance and calibration declarations.

## Kill criteria and independent checks

The pre-edit E002-456 evaluator is expected to accept the 1.0-ms witness because its guard omits ordinary exposure. Confirm that failure against the actual evaluator before changing it. Then change only the support-containment checks, add boundary/monotonicity and zero-gap regression tests, and run the existing E002-456 plus E002-470 suites on hosted CI. Any 1.0-ms positive witness accepted as an *unexposed-gap* crossing, any equality boundary accepted, or any accidental product release is a failure.

This fixes a **reference-label semantics and study-adjudication error**. It does not change E002-371's theorem, supply physiological speed limits, or establish physical human validation. Next decisive evidence remains independently timed optical shutter/encoder acquisition and blinded anatomical human reference labels.
