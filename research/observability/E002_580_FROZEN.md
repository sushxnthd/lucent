# E002-580 | Frozen independent-annotation temporal alias control (2026-11-01)

**Primary kernel:** E002-371. This is a new *real-human-source, independent pupil-center annotation* control, **not** eyelid closure validation. The E002-579 unlabelled motion proxy was falsified and must not be reused or retuned. The E002-573 participant split and blinded human-anatomy protocol remain unchanged.

## Source and prospective question
Use only the existing DEVELOPMENT recording `LPW/1/1.avi`, original investigator ZIP member from `https://datasets.d2.mpi-inf.mpg.de/tonsen/LPW.zip`, video SHA-256 `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86`, 2,000 frames, reported 95 fps, 640x480. Retrieve its same-stem source annotation `LPW/1/1.txt` by bounded ZIP range, CRC and SHA-256. If the annotation is absent, mismatched, ambiguous, nonnumeric, or not exactly two pixel-coordinate columns per native frame, **abstain**. Do not silently coerce or repair it.

**Question:** Can a 3:1 index decimation conceal excursions in independently supplied *pupil-center coordinates*, despite nearly stationary retained endpoints? A positive answer only demonstrates pupil-coordinate temporal aliasing, **not** blinking, eyelid aperture, physical shutter exposure, or certified speed.

## Locked statistic and criterion
For each consecutive 4-frame window `(i,i+1,i+2,i+3)` with valid, finite, in-image pupil centers `p`, let `W=640`. Define
- `D_i=||p_(i+3)-p_i||_2/W`, normalized endpoint displacement.
- `E_i=max_(j=1,2) ||p_(i+j) - [(3-j)p_i+j p_(i+3)]/3||_2/W`, maximal native interior deviation from endpoint-linear interpolation.
- **Exploratory label-control witness** if `E_i>=0.020` (12.8 source pixels) and `D_i<=0.010` (6.4 pixels). These thresholds are engineering stress thresholds, not anatomical or biological cutoffs.
- **Robust witness** if it remains positive under all independent per-frame annotation perturbations of Euclidean norm at most **1 pixel**. A sufficient conservative certificate is `E_i-2/W>=0.020` and `D_i+2/W<=0.010`. This bound is independent of actual annotation accuracy and **does not** assert a 1-pixel error guarantee.

Report eligible and abstained 4-frame windows, witness and robust-witness counts for each start phase `i mod 3 in {0,1,2}`, and E/D median, p90, p99 among eligible. Count all phases, do not cherry-pick. All measurements remain DEVELOPMENT-only.

## Falsifiers, nuisance limits and safety
Self-test exact interpolation, positive 4-frame loop, threshold equality, translation invariance, uniform spatial-scale invariance, missing/nonfinite/out-of-frame rejection, wrong annotation row count, wrong source path, CRC corruption, and adversarial 1-pixel coordinate uncertainty. If source labels include an undocumented sentinel, **abstain**, do not guess its meaning. If no witness occurs, preserve zero and do not tune thresholds. Investigator pupil centers may include interpolation/estimation, reflections, gaze shifts, glasses, blur and label errors; none are independent eyelid landmarks. Pixel-coordinate statistics are unaffected by pixel brightness *by construction*, not by proof of label stability under illumination.

Never publish source imagery, pupil tracks, per-frame indices, or personally identifying metadata. Emit aggregates only, with source annotation SHA-256 and the video SHA-256 for reproducibility. No HELD_OUT access, no change to the anatomical rater selection. No physical camera shutter claim.

## Product decision
Even a positive witness cannot certify E002-371's eyelid-speed or shutter-gap boundary. Product `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. If label source is absent or ambiguous, report a source-limited null result, then return directly to real blinded anatomical raters and synchronized camera/photodiode experiments. Do not expand dataset archaeology.