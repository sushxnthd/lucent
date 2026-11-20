# E002-471 RESULT — dark-gap witness classification correction

**Date:** 2026-10-27. **Evidence tier:** source-level falsification plus synthetic, analytically checked aperture/reference controls; **not** a new human anatomical measurement, physical shutter acquisition, or E002-371 physiological validation. [Frozen protocol](E002_471_FROZEN.md) was committed first at `868509ef9998cede9727c0dd577c8d26c6c7b11a`.

## New falsification of the research measurement instrument

E002-456's frozen protocol requires the **entire** reference exposure to be inside the ordinary camera's **unexposed** interval after both clocks' uncertainties. Source inspection of the prior evaluator found that its positive-reference guard omitted the **ordinary exposure half-width**. It could therefore label an exposure-overlapping reference as `WITNESSED_CROSSING`, which is incorrect **as a hidden dark-gap witness**. This is an implementation/claim-semantics error, not a counterexample to E002-371's theorem.

For ordinary camera centers 0/10 ms, exposure 4 ms, ordinary clock error 0.1 ms, reference exposure 0.2 ms, and reference clock error 0.1 ms:

- Previous reference-center guard: `0.1 + 0.1 + 0.2/2 = 0.3 ms`.
- Required dark-gap guard: `4/2 + 0.1 + 0.1 + 0.2/2 = 2.3 ms`.
- A positive reference centered at **1.0 ms** lies inside the first ordinary exposure, so it must be `REFERENCE_INCOMPLETE` for the dark-gap claim, not `WITNESSED_CROSSING`.
- A positive reference centered at **5.0 ms** is strictly inside the guaranteed gap and remains a valid positive witness. Equality at 2.3/7.7 ms is deliberately not promoted.

With 3.0-mm declared shutter averages, a 2.0-mm closure threshold, and an **illustrative** 100-mm/s velocity cap, the research-only lower envelope is **2.39 mm**. The original code would combine `EXCLUDED_CONDITIONALLY` with a 1.0-ms `WITNESSED_CROSSING` and report joint falsification; the corrected code retains the conditional exclusion diagnostic but marks the reference incomplete. **This illustrative endpoint/witness combination is not asserted to be physically consistent with that speed cap.** It is a classification/schema counterexample, not a measured human contradiction.

An additional **exploratory, physically consistent synthetic control** uses a 1000-mm/s-Lipschitz continuous aperture `a(t)=2.5-max(0,0.7-|t-1|)` mm. It crosses below 2.0 mm **only inside the first exposure** (minimum 1.8 mm at 1 ms), stays at 2.5 mm throughout the dark gap [2,8] ms, has exact ordinary shutter means 2.3775/2.5 mm, and has a 0.2-ms reference boxcar mean of 1.85 mm at 1 ms. Thus an independently positive reference can be physically real **without** being a hidden-gap closure. The corrected evaluator must mark its reference incomplete; its ordinary-camera decision is `NOT_EXCLUDED`.

## Corrected decision boundary and tests

E002-456 now requires

`g = ordinary_exposure/2 + ordinary_clock_error + reference_clock_error + reference_exposure/2`

and accepts a dark-gap reference only for `t0+g < t_ref < t1-g`. It abstains if the ordinary exposure plus twice ordinary clock uncertainty eliminates the guaranteed dark gap, or if the complete reference support cannot fit strictly in that gap. This is a conservative **positive witness localization** gate. It does not certify absence between high-rate reference samples, and all nuisance flags/calibration IDs remain self-declarations.

[Regression tests](test_e002_471_reference_gap.py) cover exposure-only positives, an independent continuous-aperture control, valid interior positives, strict boundaries, exposure/clock monotonicity, zero gap, reference-support infeasibility, nuisance failure, and the unchanged `ABSTAIN_UNCALIBRATED` product gate. [Dedicated CI](../../.github/workflows/e002_471_reference_gap.yml) runs E002-471 together with the existing E002-456 and E002-470 adversarial suites. **Hosted verification is pending**; no new green run is claimed until its logs are inspected.

## Independent verification of the previous experiment

The previously queued [E002-470 actual-evaluator run 40398705563](https://github.com/sushxnthd/lucent/actions/runs/40398705563) **completed successfully**, passing all 12 adversarial tests and replaying the 12,000-case frozen synthetic oracle. Its sanitized [artifact 12687583012](https://github.com/sushxnthd/lucent/actions/runs/40398705563/artifacts/12687583012) was uploaded. The hosted result is recorded in [E002-470's updated report](E002_470_RESULT.md). This is independent CI execution of the **same simulator**, not a second physical instrument.

## Scientific/product decision

**No new physical acquisition; no independent anatomical human rater sheets; no authenticated shutter/encoder timing; no physiological hard velocity cap.** E002-371 remains physically **NOT_ESTABLISHED**. The E002-471 correction prevents a misleading dark-gap witness and prospective false joint-falsification label; it does not authorize hidden-closure exclusion, blink duration, PERCLOS, fatigue, or medical inference. All such outputs remain `ABSTAIN_UNCALIBRATED`.

Next decisive work is the already frozen physical optical-phase scan and moving-aperture experiment with independent timing and two blinded human anatomical raters. No further S19 clock archaeology or synthetic theorem polishing is justified without new physical evidence. Preserve draft PR #26 and keep Hush separate.
