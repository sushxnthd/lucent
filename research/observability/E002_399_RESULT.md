# E002-399 — calibrated reference adequacy with two-rater interval propagation

**2026-10-23. Evidence tier: preregistered synthetic-instrument experiment, local independent oracle, and executable human-annotation handoff.** No human eyelid landmark labels, independent physiological speed calibration, physical shutter calibration, or human E002-371 certificate. Protocol `E002_399_FROZEN.md` was committed first at `2d93edf`.

## Frozen synthetic results

Fixed seed 399; 200 independently randomized phase/jitter trials per cohort (1,000 total). All seven preregistered criteria passed in local execution.

| Cohort | Confirmed crossing | Confirmed no crossing | Unresolved | Wrong certificates |
| --- | ---: | ---: | ---: | ---: |
| Always open, 240 Hz, 1-ms exposure | 0 | **200** | 0 | 0 |
| Triangular crossing, 960 Hz, 0.5-ms exposure | **200** | 0 | 0 | 0 |
| Same crossing, 30 Hz, 10-ms exposure | 0 | 0 | **200** | 0 |
| Marginal open, 240 Hz, 0.5-ms exposure | 0 | **200** | 0 | 0 |
| Marginal open, alternate frames missing | 0 | 0 | **200** | 0 |

The independent checker verified 150 randomized Lipschitz-envelope problems against a separate dense-grid oracle with a rigorous grid-error bound; it also exercised two-rater disagreement, calibration denial, glare-driven missingness, and duplicate-rater rejection. **Zero errors in synthetic cases is not a population risk estimate.** GitHub CI must be checked independently before claiming hosted reproduction.

## Exact conditional reference rule

Assume a *calibrated physical* normalized eyelid aperture x(t), an **independently** established Lipschitz speed bound V, a uniform exposure of duration e_i, mean-aperture interval [a_i,b_i], nominal frame center t_i and independently bounded time/row uncertainty d_i. The shutter mean implies

```text
L_i = a_i - V*(e_i/4 + d_i) <= x(t_i)
U_i = b_i + V*(e_i/4 + d_i) >= x(t_i)
```

A confirmed physical crossing requires some U_i < theta. A confirmed absence **within [first,last] nominal frame centers only** requires

```text
min_{t in [t_first,t_last]} max_i [ L_i - V*abs(t-t_i) ] > theta.
```

The O(n) prefix/suffix cone algorithm evaluates this lower-envelope minimum exactly without discretizing time. It is sound under the stated assumptions, but **not** globally optimal inference from joint shutter integrals (cf. E002-389). Equality or uncertain calibration abstains.

For identical evenly spaced aperture means, a useful *sufficient* dimensionless exclusion margin is

```text
Gamma = (a - theta) / (V*(Delta/2 + e/4 + d)).
```

Gamma>1 excludes a crossing under the cone rule. The marginal-open cohort has nominal Gamma≈1.155 with all 240-Hz frames, falling to ≈0.607 after alternate frames are missing. The resulting transition from 200/200 certified negatives to 200/200 unresolved demonstrates how **missingness alone can destroy reference adequacy**. This is a conditional measurement consequence, not a novel physiological law.

## Human-annotation bridge

`e002_399_annotation_bridge.py` consumes the blinded E002-398 manifest, **two independent completed rater sheets**, private frame timing, and independent physical calibration. It conservatively hulls the two central upper/lower landmark distances, propagates pixel uncertainty and independently calibrated iris-scale bounds, and removes flagged glare, blur, glasses, gaze, occlusion and unresolved frames rather than imputing them. Missing frames enlarge uncertainty gaps. The bridge rejects duplicated rater IDs, duplicate/missing frame keys and out-of-crop/nonfinite coordinates. Output is aggregate, label-free triage; it does not use EEG marker/control linkage.

Private timing CSV fields: `clip_id,frame_in_clip,nominal_time_s,exposure_s,clock_error_s`. Calibration JSON needs `speed_upper`, `threshold`, `iris_scale_lower_px`, `iris_scale_upper_px`, `landmark_error_px`, plus seven `gates`: `independent_velocity`, `aperture_geometry`, `optical_response`, `exposure_timing`, `clock_synchronization`, `nuisance_resolved`, `uniform_shutter_verified`. All gates default false. **Boolean flags are assertions, not independently audited calibration evidence.** Image-space landmark separation is not automatically a calibrated exposure-mean physical aperture. Do not upload private timing/linkage, human eye crops, or rater-identifiable material to public CI.

## Reproduce

```bash
python research/observability/e002_399_reference_adequacy.py --output /tmp/e002_399.json
python research/observability/e002_399_independent_check.py
python research/observability/e002_399_annotation_bridge.py --help
```

**Product decision:** `ABSTAIN_UNCALIBRATED` remains mandatory for hidden-closure guarantees, blink duration, PERCLOS, and fatigue diagnosis. No real Eye-BCI rater sheets or independently calibrated exposure/velocity/optical envelopes are available yet. Next decisive experiment: two blinded raters on the existing 560 human crops, then physical calibration and prospectively frozen predictions on untouched participants and devices. Further EEG-marker AUC optimization is not a substitute.
