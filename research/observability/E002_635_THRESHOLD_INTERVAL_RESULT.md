# E002-635 | Closure-threshold uncertainty defeats a point-threshold exclusion

**Evidence tier:** exact-rational synthetic counterexample, NOT human physiology or physical shutter calibration.

## Target and frozen assumptions
The E002-632 prospective scorer computes `(aperture0_lo_mm - closure_mm)/v_close_mm_s + (aperture1_lo_mm - closure_mm)/v_open_mm_s > gap_hi_s` and emits EXCLUDE, but takes `closure_mm` as an unqualified point estimate. A physical/anatomical closure threshold can depend on geometry, rater definition and calibration. If it is an interval, the conservative exclusion must use its **upper** endpoint, not its point estimate.

## Exact witness
Take a 20 ms exposure-free gap, both endpoint apertures 2 mm, and speed ceilings 100 mm/s in each direction. A reported threshold of 0 mm yields a 40 ms minimum round-trip and the existing scorer would exclude closure. If the true operational closure threshold is 1.5 mm, a valid Lipschitz trajectory goes 2 mm at 0 ms, 1.5 mm at 5 ms, 1 mm at 10 ms, 1.5 mm at 15 ms, and 2 mm at 20 ms. It satisfies both speed ceilings and is below the actual threshold. The correct minimum round-trip is 10 ms; closure is feasible. Thus the nominal EXCLUDE can be a false exclusion without any velocity or shutter timing error.

## Enforcement consequence
Require an independently authenticated, predeclared upper confidence/certification bound `closure_hi_mm` (not a nominal point estimate). Replace both reachability distances by `aperture_i_lo_mm - closure_hi_mm`; if either is nonpositive, abstain. If the interval cannot be independently certified, `ABSTAIN_UNCALIBRATED`. An unverified CSV YES flag must never unlock EXCLUDE. This is a model-input soundness correction, not proof of a population-level risk guarantee.

## Reproduction and limitations
Run `python research/observability/e002_635_threshold_interval_counterexample.py`; the script asserts the exact counterexample and conservative guard. A separate exact-rational arithmetic check confirmed the trajectory and the 40 ms versus 10 ms calculation. No human recordings, measured shutter gaps, or independently certified physiological thresholds were acquired. Existing E002-631 prospective study remains frozen; this finding is a predeployment protocol amendment to be tracked separately, not a retrospective alteration of trial outcomes.

**Product:** ABSTAIN_UNCALIBRATED; production BLOCKED. No merge authorization.
