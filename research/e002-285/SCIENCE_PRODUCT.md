# E002-285 | SCIENCE and PRODUCT ledgers

## SCIENCE: what is true?
The two-frame conditional observability law is exact under orthographic pose projection, known pitch, bounded depth Z, bounded depth change D, bounded localization error eps, and free initial anatomical aperture. Closure delta is distinguishable from no change iff delta>2(S+E). A 0.5mm *hypothetical* closure passes at fixed 30deg with D=.08mm (critical .323316mm) but fails at 30-to-40deg (critical .704836mm) and with D=.4mm (critical .692820mm). Eight frozen synthetic cases, five explicit observational collisions, 250 randomized LP checks, three mutation rejections. No real camera/human validation, no field-level novelty.

## PRODUCT: what capability changes?
**Conditionally allow:** pose-stable blink-change acceptance only if independently calibrated Z,D,eps and timing/photometry gates all pass. **Reject:** unconditional monocular pose-corrected anatomical aperture, reliance on estimated 3D network landmarks as ground truth, and five-second fatigue claims. **Calibrate next:** independent high-speed or stereo eyelid depth coherence during real blinks, pose estimation, gaze effects, landmark errors and device/lighting/glasses holdouts. If D cannot be bounded, abstain and pivot to coarse event detection. The rule is a candidate design gate, not a deployed detector.
