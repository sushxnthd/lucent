# E002-398 — blinded rater instructions and adjudication plan

**This is an annotation protocol, not a completed human study.** The Eye-BCI recordings have EEG blink markers, not physically calibrated eyelid-aperture ground truth. The 152-fps effective camera timeline does not certify shutter exposure or sub-frame absence of closure.

## Materials and handling
Generate the blinded local pack using `e002_398_blinded_annotation.py` on the two verified source archives. The output **private directory contains cropped human eye frames and the event/control linkage key**. Do not upload the private directory, raw frames, key, or linkage to the public repository or public CI artifacts. The public directory contains only an unlabeled manifest, empty annotation sheet and aggregate quality summaries. Keep the two independent rater files separate until both are locked.

## Annotation instructions
- Annotate each of seven frames per clip in the provided sequence order. The crop is 190×130 pixels, with coordinates (0,0) at its upper-left corner. Use the original pixel grid; no AI super-resolution, interpolation, or automatic feature enhancement.
- Locate the upper and lower **palpebral margins** at three horizontal locations relative to the iris center (left, central, right). Record upper/lower x,y coordinates at the same x-column when visible; each point is in crop pixels. The center should track the visible iris center rather than a fixed image column; record uncertainty caused by gaze shifts. Do not annotate eyebrow, eyelashes, skin shadow, pupil boundary or corneal reflections as the eyelid margin.
- If a margin is hidden, ambiguous or outside the crop, leave its coordinates empty and set `unresolved=1`. Do not interpolate across frames, fill occluded margins or assume the eye is open because no closure was detected.
- Independently flag `occlusion`, `glare`, `glasses`, `blur`, and `gaze_issue` (0/1). Use the notes field for causes of uncertainty, not inferred EEG status. No access to event/control labels, classifier outputs, optical-flow scores or other rater annotations.
- A rater must complete all visible frames, including low-quality and non-event clips, before seeing any study summary. No cherry-picking or retrospective exclusions.

## Independent adjudication and uncertainty
Two raters independently annotate the same frames. Freeze both sheets before opening the private event/control key. Compute per-point Euclidean disagreement in original pixels, per-frame central vertical margin separation, and agreement on unresolved/quality flags. Do not substitute the average of conflicting landmarks for independent truth. A third adjudicator reviews disagreements above a **prospectively fixed** pixel tolerance, and any frame for which either rater marks a critical margin unresolved. Retain the original ratings, adjudicated coordinates and reasons.

To support E002-371, separately calibrate pixel-to-aperture geometry, camera exposure/rolling shutter and cross-device time alignment. Convert landmark and calibration uncertainty into a conservative interval for each aperture value. A physical closure threshold can be scored only when the entire calibrated uncertainty interval is on one side of the threshold; otherwise `REFERENCE_UNRESOLVED`. An observed reference frame with no visible closure is not proof that no closure occurred between frames. Independently estimate an upper speed envelope on disjoint participants and validate it out of sample; an average observed speed is **not** a hard physiological bound.

## Final analysis plan (not yet executable as physical validation)
1. Lock two rater sheets and adjudication before unblinding.
2. Publish anonymized coordinates, calibration certificates, frame-time uncertainty, exclusion counts and independent reanalysis scripts, subject to source privacy terms.
3. Freeze E002-371 ordinary-camera gap predictions on disjoint calibration participants, then evaluate untouched participant/device holdouts. Include missingness, glare, blur, gaze, geometry, brightness, glasses and clock perturbations.
4. Report false no-hidden-closure certificates, unresolved reference labels, abstention rate and uncertainty bounds separately. AUC of EEG association is not the target metric.
5. Continue `ABSTAIN_UNCALIBRATED` for blink duration, PERCLOS, physical hidden-closure exclusion and fatigue claims until all physical calibration and independent verification gates pass.

**Operational caveat:** This pack is intended for trained human annotators; generating it does not supply the two raters or validate their agreement. Full image publication is intentionally disabled.
