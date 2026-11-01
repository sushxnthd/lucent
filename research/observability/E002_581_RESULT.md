# E002-581 | Moving-linear label-order information audit: execution pending

**Date:** 2026-11-01. **Kernel:** E002-371. **Evidence tier:** authentic original-investigator LPW pupil-center annotations, not eyelid anatomy. **Frozen protocol:** [E002_581_FROZEN.md](E002_581_FROZEN.md), committed at `e52dbe0` before executable. **Code:** [e002_581_lpw_label_information.py](e002_581_lpw_label_information.py). **Hosted run:** [GitHub Actions #41269895334](https://github.com/sushxnthd/lucent/actions/runs/41269895334), queued at last inspection.

## Purpose and falsifier

E002-580 found zero pupil-coordinate hidden-excursion witnesses, but its median interpolation residual rounded to zero. E002-581 independently distinguishes stationary zero residual from *moving* constant-velocity annotation segments. It counts moving exact-linear junctions, longest runs, and tests against 499 seeded within-50-increment randomizations. The null is descriptive and cannot identify the labeling process.

## Evidence observed so far

- Frozen protocol and executable committed to the established research branch.
- Independent local synthetic reproduction of the numerical kernel **passed**: stationary tracks give 18 exact but 0 moving junctions over 20 points; a 20-point one-pixel-per-frame straight track gives 18 moving junctions and a longest run of 18; a four-pixel kink splits that run into two runs of length 8; 0.01-pixel/frame motion is excluded. The independent test also checked rotation, translation, seeded reproducibility, and within-block preservation of the full 2D increment-vector multiset. These are **synthetic controls, not human evidence**.
- The hosted authentic-label run is **not yet verified**. Do not report a real LPW count, p-value, null outcome or CI success before inspecting actual logs. The prior E002-580 authentic LPW result remains separately verified.

## Interpretation limits and decision

Even an extreme difference from the shuffled-increment null would show only nonrandom local ordering in investigator annotations. Quantization, smooth gaze tracking, repeated increments, model-assisted labeling or interpolation could produce it. It would **not** establish an interpolation mechanism, blink occurrence, eyelid aperture, physical shutter timing or a continuous-time eyelid-velocity ceiling.

**Independent human anatomical rater pairs: 0. Physical shutter captures: 0. Certified continuous-time eyelid-speed ceilings: 0. Held-out physical closure predictions: 0.**

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. The next decisive study is two independent blinded raters on authentic native-frame LPW packets, followed by synchronized photodiode/camera shutter measurements. Do not retune E002-580 thresholds or substitute this annotation control for anatomical ground truth.
