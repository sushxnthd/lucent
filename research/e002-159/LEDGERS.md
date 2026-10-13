# E002-159 SCIENCE / PRODUCT ledgers (2026-10-13)

## Active kernel
**Exact target pair:** ordinary front-camera RGB pupil/full-anatomical-iris ratio waveform vs independently timestamped concurrent eye-tracker pupil waveform during ~5 s active scan.
**Frontier:** no valid paired ordinary-RGB/reference human waveform yet; original-human mask geometry and oracle photometric audit are intermediate evidence.
**Scalar target:** frozen participant/device/lighting-held-out waveform correlation, lag, amplitude fidelity, NRMSE and coverage. **Current intermediate scalar:** fraction of original-human annotation frame pairs whose 5%-scale response classification differs between pupil/sqrt(visible-eye area) and pupil/eye-width.
**Confound:** eyelid aperture/visible-eye mask area, width, gaze, cropping, illumination, segmentation.
**Decisive falsification:** actual synchronized held-out RGB/reference waveform fails frozen agreement gates or brightness/geometry controls explain the same response.
**Publishable success:** untouched paired human waveform, strong baselines, independent checker, unseen-condition prediction and novelty audit.
**Product threshold:** validated response quality/abstention at useful coverage on ordinary RGB with real physiological reference.
**Kill:** repeated genuine paired-reference failure -> restrict capture or switch ocular signal; no fatigue model before clearance.

## SCIENCE
- KNOWN (E002-159, post-hoc human masks): among 4,781 lag-1 annotation pairs across 26 filename groups, 361 (7.55%) produce different 5%-scale response classes depending on visible-eye-area vs width normalization. At lag 30: 693/4,038 (17.16%). 95% group bootstrap descriptive intervals: lag 1 [4.57%, 11.03%], lag 30 [12.67%, 22.42%]. Group labels are not people.
- KNOWN: 21 lag-1 and 28 lag-30 pairs produce directly opposite >=5%-scale classifications. Strict G3 no-opposite-reversal fails.
- KNOWN: high absolute denominator drift concentrates disagreement; exploratory top-decile |dD|: 49.48% lag-1 disagreements vs 2.88% among the rest. This association is partly algebraic and is not causal physiological evidence.
- FALSIFIED: unconditional interchangeability of these two mask-derived normalization choices; frozen G1 (<=5% lag-1) and G2 (<=5% lag-30) failed. Neither proxy is ground truth.
- ANOMALOUS: camera-prefixed filename group had 56.76% lag-30 disagreement; acquisition identity and cause unverified.
- UNTESTED: anatomical iris reconstruction, RGB segmenter, eye-tracker waveform, person/device holdout, photometric confounds and fatigue.

## PRODUCT
- REMOVE: treating pupil/sqrt(visible-eye area) and pupil/eye-width as equivalent response estimators; even the response direction can disagree in original-human masks.
- CANDIDATE: compute two independent-looking geometry references and flag inconsistent classifications as a *normalization sensitivity warning*, NOT a guarantee of physiological correctness. Retained agreement is not evidence of true accuracy; both can be wrong.
- NEXT: stop further mask-only threshold tuning. Obtain verified synchronized ordinary RGB and tracker waveforms; evaluate frozen gates. E002-158 original RGB photometric contrast audit is separate and does not itself establish physiology.

## Provenance and execution
Input E002-155 PAIRS.csv SHA256 ec150e35dc84e120f1a0418a003989f4948595a8034ecbc68088954cfe0ce730, derived from original Zenodo ZIP SHA256 049df72454682c1c77c50c8236bb607919a6e333528bc2b89c567b625e459700. E002-159 protocol committed BEFORE outcome computation; prior E002-155 through E002-157 mask summaries were known, so this is post-hoc exploratory, not pristine confirmation. Local cloud/container checker passed all 17,903 row reconstructions. CI workflow creation was blocked by tool safety checks; do not claim a new GitHub Actions run. No user laptop, spend, or hardware.
