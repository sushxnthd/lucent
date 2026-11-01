# E002-580 | Genuine LPW investigator pupil-center temporal-alias control: negative

**Date:** 2026-11-01. **Primary scientific kernel:** E002-371. **Evidence tier:** real human-source *investigator pupil-center annotation*, not anatomical eyelid validation. **Status:** completed hosted verification, [GitHub Actions #41265906391](https://github.com/sushxnthd/lucent/actions/runs/41265906391). The [protocol](E002_580_FROZEN.md) was committed before any label extraction or inspection. The executable is [e002_580_lpw_label_alias.py](e002_580_lpw_label_alias.py).

## Actual experiment

Source-linked official LPW ZIP, exact annotation member `LPW/1/1.txt` (SHA-256 `12f60068317a341809babb7c2cbce90b8ba299ad877d75186687b0d521f6d5d2`), development participant 1 only. All **2,000** annotation rows parsed as exactly two finite, in-image pupil-center coordinates. ZIP CRC verification passed. The corresponding video `LPW/1/1.avi` had been previously independently extracted and hashed as `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86` in E002-577/578; **this run did not rehash the video**. Source acquisition rate is reported 95 fps, not a certified exposure or clock. No image or individual track was published.

The precommitted 3:1 *index* decimation test compares native intermediate pupil-center labels with the linear interpolation between retained endpoints. A positive exploratory witness required an interior deviation of at least **12.8 px** (E >=0.020 image widths) despite an endpoint displacement at most **6.4 px** (D <=0.010 image widths). A stricter witness additionally requires the criterion to hold for all independently bounded 1-px Euclidean perturbations of each annotation point; **1 px is an adversarial stress radius, not an empirically justified label error bound**.

| Start phase (mod 3) | Eligible 4-frame windows | Exploratory witnesses | Robust 1-px witnesses | Interior E median | Interior E p99 |
|---|---:|---:|---:|---:|---:|
| 0 | 666 | **0** | **0** | 0.0000000 | 0.0036125 |
| 1 | 666 | **0** | **0** | 0.0000000 | 0.0035469 |
| 2 | 665 | **0** | **0** | 0.0000000 | 0.0035945 |
| **All** | **1,997** | **0** | **0** | — | — |

The E p99 values correspond to roughly 2.27–2.31 pixels of interior deviation. Endpoint D medians were 0.0054665, 0.0054976 and 0.0056250 image widths, respectively. No eligible windows were excluded by the source-label parser. The effective 3:1 index rate is **31.67 fps**, not 30 fps or an exposure-integrated ordinary camera.

## New interpretation: high-rate video is not high-rate anatomical ground truth

The investigator-provided pupil-center annotation sequence has **zero median** interior deviation from a 3-frame endpoint interpolation in *all three phases*. This is an observed temporal regularity in the **labels**, not in independently measured eyelid motion. One possible explanation is temporal smoothing or interpolated labeling, but this experiment does **not** identify the annotation-generation mechanism. A follow-up can test the exact-linear-run distribution against an increment-permutation null, without claiming that a nonzero effect proves interpolation.

**Frozen outcome:** zero positive pupil-center witnesses under the locked threshold. Do not retune E or D to manufacture a positive. These labels cannot establish any eyelid-closure witness, negative closure certificate, physiological velocity upper bound, blink frequency, PERCLOS, fatigue, or E002-371 shutter-gap validation. Even perfectly verified pupil centers are not eyelid aperture; label interpolation, gaze, blur, glasses, geometry and brightness may confound temporal inference. The authors explicitly describe several different pupil-label construction methods, including mapped gaze-target positions and manual corrections ([original dataset](https://www.mpi-inf.mpg.de/departments/computer-vision-and-machine-learning/research/gaze-based-human-computer-interaction/labelled-pupils-in-the-wild-lpw), [ETRA 2016 DOI](https://doi.org/10.1145/2857491.2857520)).

## Verification and negative evidence

- **Initial hosted CI [#41265736741](https://github.com/sushxnthd/lucent/actions/runs/41265736741) failed before source access**: the Python ZIP library invokes `read()` without a length near the end of the archive, while the range reader initially rejected all unbounded reads. The fix allows only a <=1 MiB remainder and still refuses full-archive reads. The initial failure is preserved, not rewritten.
- **Corrected hosted CI [#41265906391](https://github.com/sushxnthd/lucent/actions/runs/41265906391) passed** all synthetic adversarial checks and the authentic original-annotation experiment. Tests included hidden-loop positive control, linear negative control, translation and spatial-scale invariance, missing/nonfinite values, malformed row counts/columns, coordinate bounds, ZIP range reading and deliberate CRC corruption.
- Machine-readable aggregates are in [E002_580_AGGREGATE.json](E002_580_AGGREGATE.json). Raw coordinates, per-frame indices, identifiable imagery and source videos were never uploaded as artifacts.

## Decision

**Reject any inference from these pupil-center labels to anatomical closure or continuous-time speed.** This experiment establishes only that the frozen pupil-coordinate alias criterion has no positive witnesses in this development recording and exposes a potential temporal-annotation regularity worth independently checking. It neither supports nor falsifies E002-371's *conditional mathematical bound*.

**Human anatomical rater pairs:** 0. **Authenticated physical shutter captures:** 0. **Certified continuous-time eyelid velocity ceilings:** 0. **Held-out physical closure predictions:** 0. Next decisive work: two genuinely independent blinded anatomical raters on source-bound LPW packets and synchronized physical shutter/photodiode validation. Avoid additional dataset archaeology or arbitrary threshold retuning.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. **Hush:** no changes.
