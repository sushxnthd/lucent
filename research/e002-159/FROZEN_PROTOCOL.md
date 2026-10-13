# E002-159 frozen protocol — ratio-sign disagreement (2026-10-13)

## Kernel and product-critical question
Ultimate exact pair: ordinary-RGB pupil/full-anatomical-iris temporal waveform versus concurrently timestamped eye-tracker pupil waveform over approximately 5 s. Current frontier: human annotated pupil/visible-eye masks show denominator drift, but no validated RGB/tracker pairing. Intermediate question: does visible-eye area normalization change inferred direction or 5%-scale response decision relative to width-normalized pupil radius, even with the same original-human mask annotations? This is normalization-risk, not physiological ground truth.

## Source and independence
Reuse only E002-155 original-human PAIRS.csv previously released in E002-157; pinned SHA256 ec150e35dc84e120f1a0418a003989f4948595a8034ecbc68088954cfe0ce730. Original Zenodo ZIP SHA256 049df72454682c1c77c50c8236bb607919a6e333528bc2b89c567b625e459700. Source is annotated pupil/visible-eye masks, not anatomical iris, actual RGB segmenter, tracker or state labels. Filename groups are NOT verified participants/devices. Frame gaps 1/5/15/30 are NOT seconds. This is post-hoc exploratory reuse, not untouched validation.

## Frozen observables
For each pair, A = 0.5*dPn = log[(sqrt(P2)/W2)/(sqrt(P1)/W1)], width-normalized pupil-radius response. B = dq = log[(sqrt(P2/E2))/(sqrt(P1/E1))], visible-eye-normalized response. Exact identity B=A-0.5*dD. Neither A nor B is physiological ground truth. C = 0.5*dPn+0.5*(dE-dD) = 0.5*dlogP, raw pupil-radius response. Classify constriction (-1) if response <= -log(1.05), dilation (+1) if >= log(1.05), otherwise indeterminate (0).

Primary scalar D_k = fraction with class(A) != class(B) at each gap k. Secondary S_k = fraction class(A)*class(B)==-1 (strong opposite 5%-scale decisions). Also compute unthresholded sign reversal A*B<0, and class(C) versus class(B) disagreement. Group bootstrap B=3000 seed=1592026 for 95% percentile intervals on D_1 and D_30. Report per-group concentration and camera-prefixed subgroup. No gate optimization or retrospective threshold changes.

## Frozen gates
G0: source SHA matches, >=10 filename groups and >=1000 lag-1 pairs.
G1: D_1 <= 0.05 (product screening criterion only).
G2: D_30 <= 0.05.
G3: no strong opposite 5%-scale decisions across all four gaps (strict no-reversal null).
G4: max |B-(A-0.5*dD)| < 1e-10.
G5: independent checker reproduces all event counts and gate states.
G6: synchronized RGB/reference, real segmentation, participant/device holdout and fatigue UNTESTED.

## Predictions and falsification
Prediction: disagreement increases with indexed separation and clusters in high |dD| pairs. Any decision disagreement falsifies universal interchangeability of the two normalizations; G1/G2 set pragmatic screening thresholds. If low, do NOT promote visible-eye denominator to iris or physiology. If high, reject unconditional visible-eye ratio as a measurement route; preserve uncertainty and abstain.

## Confounds, novelty and product threshold
Eyelid aperture, gaze, cropping, annotation, width drift, illumination (not measured), and correlated pairs. No independently timed human physiological reference. No novelty claim for algebraic identity or normalization. Publishable Lucent success requires frozen paired RGB/tracker waveform, strong photometric/geometry controls, independent checker and unseen-condition prediction. Product threshold requires real RGB/paired-reference calibrated rejection at useful coverage, not this mask proxy. Kill this intermediate question after one reproducible audit; do not iterate mask-only thresholds.
