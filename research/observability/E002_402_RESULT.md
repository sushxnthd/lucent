# E002-402 — diagonal landmark distance is not a physical eyelid aperture

**Date:** 2026-10-24. **Evidence tier:** prospectively frozen source-level counterexample, 1,000 seeded synthetic landmark trials, 300 independent contour-oracle trials, end-to-end bridge regressions and hosted CI. **Not** a human or calibrated-camera experiment. Protocol frozen first at `6ffa78e`.

## Failure discovered in the actual annotation bridge

The previous `e002_399_annotation_bridge.py` used `hypot(x_upper-x_lower,y_upper-y_lower)` as an aperture. This measures diagonal landmark separation, not the signed vertical palpebral gap at a common anatomical column. Two reported landmarks at (60,40) and (80,40) have **zero vertical separation** but a Euclidean distance of 20 pixels. At iris scale 50 pixels and closure threshold 0.2, the old bridge substitutes a fictitious 0.4 aperture and issues **CONFIRMED_NO_CROSSING** for an eye that is physically closed under the specified vertical-gap model. This is an invalid input substitution, not a counterexample to E002-371's shutter-gap theorem.

The corrected method uses an independently calibrated reference column `x0`, signed vertical separation, independent upper/lower lid slope envelopes, and per-coordinate landmark error. If `E` bounds x/y annotation error, `S_u,S_l` bound lid slopes, and `(x_u,y_u),(x_l,y_l)` are observed landmarks, then the physical gap at `x0` is enclosed by

```
d = y_l - y_u
B = S_u*abs(x0-x_u) + S_l*abs(x0-x_l) + E*(2+S_u+S_l)
gap_at_x0 in [d-B, d+B].
```

This follows by applying the triangle inequality to each lid contour. The two raters' intervals are combined by **union**, never averaging or intersection; lower and upper normalized bounds use independent iris-scale bounds. A negative signed landmark separation, nonfinite coordinate, or invalid geometry calibration rejects that frame. This is classical bounded-error photogrammetry, not a new general theorem.

Vector schematic: [E002_402_GEOMETRY.svg](E002_402_GEOMETRY.svg), showing the exact wrong-certificate witness and corrected aperture definition.\n\n## Frozen predictions and results

| Frozen criterion | Outcome |
| --- | --- |
| G1: zero vertical gap, 20px horizontal offset causes legacy false open certificate | **Passed**: old CONFIRMED_NO_CROSSING, corrected CONFIRMED_CROSSING |
| G2: sloped contours with 13px observed gap but 9px true reference-column gap are bounded | **Passed**: interval [0.18, 0.34] encloses true 0.18 |
| G3: 1,000 seeded held-out linear-contour trials cover true gap or reject inverted geometry | **Passed**: 953/953 accepted intervals cover truth, 47/1000 excluded |
| G4: missing quantitative geometry abstains; calibrated clean controls work | **Passed**: bridge regressions |
| G5: larger slope/landmark-error envelope cannot strengthen certificates | **Passed**: all accepted trials and bridge regression |
| G6: independent linear-contour oracle, without the implementation's interval routine | **Passed**: 300/300 cases |

The synthetic trial distribution was constructed adversarially, not sampled from human eyelid physiology. The 47 exclusions are **not** a population abstention rate; the 953/953 coverage is **not** a real-camera accuracy estimate. All historical E002-399/400/401 reference, optical and rolling-shutter regressions passed on the final branch head.

**Verified CI:** https://github.com/sushxnthd/lucent/actions/runs/40017665109 (success, commit `77e6411`). Two intermediate CI runs failed because the initial patch introduced a malformed Python warning string; the error was repaired before final verification. No negative scientific results were discarded.

## Enforcement and honest scope

`landmark_geometry_calibration` is now required in addition to the existing Boolean gate, with fields:

```json
{
  "landmark_geometry_calibration": {
    "reference_column_px": 70,
    "upper_lid_slope_bound": 0.2,
    "lower_lid_slope_bound": 0.2,
    "vertical_axis_verified": true,
    "provenance": "independent_geometry_calibration_required"
  }
}
```

A missing object forces `ABSTAIN_UNCALIBRATED`; a malformed object is rejected. Provenance and Boolean flags are **not independently authenticated**. The x-reference and vertical image axis must be physically justified; 2D vertical gap is not automatically 3D physical eyelid aperture under head rotation, perspective, gaze changes, glasses, occlusion or optical warping. Fixed image-column calibration may fail if gaze or head pose changes, so a calibrated anatomical reference and nuisance envelope are mandatory. The independent shutter, optical, row timing, velocity and clock gates remain active.

The strongest supported product consequence is **fail-closed measurement qualification**, not physical blink detection or fatigue diagnosis.

## Primary-literature priority context

- Read, Collins, Carney and Iskander (2006), *The Morphology of the Palpebral Fissure in Different Directions of Vertical Gaze*, *Optometry and Vision Science* 83(10), 715–722. DOI 10.1097/01.opx.0000236811.78177.97. Measured changes in vertical aperture, angle and contour with gaze in 76 subjects. https://pubmed.ncbi.nlm.nih.gov/17041316/
- Patil et al. (2011), *Anthropometry of the Eyelid and Palpebral Fissure in an Indian Population*, *Aesthetic Surgery Journal* 31(3), 290–294. Defines vertical palpebral dimension in standardized frontal photographs. https://pubmed.ncbi.nlm.nih.gov/21385738/

Neither source establishes this exact source-code counterexample. Both substantially limit any novelty claim about vertical eyelid geometry or gaze effects.

## Reproduction

```bash
python research/observability/e002_402_geometry.py
python research/observability/e002_402_independent_check.py
python research/observability/e002_399_independent_check.py
python research/observability/e002_400_independent_check.py
python research/observability/e002_401_independent_check.py
```

**World-class gate remains open.** Next decisive evidence is blinded human eyelid-margin annotation at a calibrated anatomical reference location, independently measured shutter/row/clock/optical response, independently bounded physiological velocity and untouched-participant/device predictions of E002-371. Do not claim physical no-hidden-closure guarantees, blink duration, PERCLOS or fatigue diagnosis. Keep PR #25 draft.
