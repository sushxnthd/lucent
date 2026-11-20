# E002-595 | Frozen native-95-fps to nominal-30-fps phase-paired human-review instrument

Date: 2026-11-02. Primary kernel E002-371. Frozen **before executing this instrument on source frames**. This is a prospective **instrument protocol**, not preregistration of a human outcome or a physical shutter experiment.

## Question and explicit nonclaim
Can a source-bound, blinded high-rate/ordinary-rate *paired annotation packet* be generated on authentic human-eye footage while preserving exactly which native frames are lost under three nominal ordinary-camera phases? This advances the missing independent-rater experiment. It does **not** turn LPW pupil labels or native container PTS into anatomical closure truth, certify continuous-time eyelid velocity, or simulate rolling-shutter exposure integration.

## Locked source, selection, and split
Use only the original LPW **development** participant 1 video `LPW/1/1.avi`, exact SHA-256 `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86`, native 2000 frames, 640x480, container stream nominal 95/1 fps. Reuse E002-573's participant-disjoint development split and E002-578's deterministic ten nonoverlapping 19-native-frame windows. Do not open a held-out participant. Acquire via the already verified E002-577 bounded-range ZIP-member path and verify CRC, SHA, geometry and frame count. Keep all video/PNGs and owner mappings in temporary private storage; never upload artifacts or source imagery to CI.

## Frozen phase mapping and falsifiable index predictions
Let a 19-frame window have local indices 0,...,18. For each nominal ordinary 30-fps point-sampling phase p in {0,1,2}, take ideal sample times `p/95+k/30` seconds relative to window start. Choose the nearest native 95-fps index by exact half-up rounding of `p+95k/30`; retain indices 0,...,18. Predictions:
- p=0: [0,3,6,10,13,16]
- p=1: [1,4,7,11,14,17]
- p=2: [2,5,8,12,15,18]
- 6 frames per phase/window; union of phases covers 18/19 native indices, with native index 9 absent from all three.
- For a synthetic *discrete index pulse* occupying 1,2,3,4 consecutive native indices, counts of start positions wholly missed are p0: [13,7,1,0], p1: [13,6,1,0], p2: [13,7,1,0]. These are exact finite-grid counts, **not** eyelid closure probabilities or physical shutter-gap certificates.

The 30-fps arm is **nearest-frame decimation**, not a physical camera, and 95-fps LPW frames are themselves temporally integrated and possibly rolling. No claim of actual phase alignment, known exposure support, continuous-time closure visibility, or calibrated 30-fps shutter is permitted.

## Paired rater instrument and privacy gate
First build and verify E002-578's two independent blank native 95-fps reviewer packets (10 clips x 19 frames x 2 raters). Then create three nominal 30-fps arms for each rater (10 clips x 6 frames x 3 phases x 2 raters). Verify byte-identical PNG SHA-256 for every copied native frame and exact geometry. No anatomical labels may be prefilled. Reviewer-facing JSON must omit participant identity, original video digest, native-frame index, and source mapping. Keep arm mapping owner-only. All temporary files must be deleted before job exit. Only aggregate frame counts, phase-index law and status are printable. If source or packet validation fails, CI must fail rather than silently downgrade.

## Independent blinded human follow-up (not performed by CI)
With authorized access, ethics/consent/privacy review and secure private packet delivery, assign two genuinely independent anatomical raters per arm, blind to each other's ratings and to the model's exclusion predictions. Require upper/lower lid margins, visibility and uncertainty intervals. Seal high-rate reference annotations before comparing to ordinary arms; use E002-585 and E002-576's one-sided adjudication and source-bound index-alias gates. Treat blur, gaze, glasses, geometry, brightness, missingness and clock uncertainty as explicit strata/abstentions. Do not treat pupil-center availability or a pixel proxy as eyelid closure. Do not promote same-participant temporal windows to independent participant holdouts.

## Prospective physical E002-371 decision
In a **separate** synchronized-camera experiment, independently calibrate shutter exposure support, rolling-row timing, camera response, anatomical aperture and clock error, plus a hard velocity/acceleration envelope. Before revealing participant-disjoint held-out high-rate closure labels, freeze each ordinary-camera gap's conservative endpoint lower bounds `l0,l1`, upper gap duration `g`, threshold `tau`, and authenticated hard velocity `V`. Only if every premise holds and `V*g < (l0-tau)+(l1-tau)` may the *model-conditional* rule exclude an instantaneous closure in an unexposed gap; otherwise ABSTAIN. For physical no-hidden-closure claims, retain ABSTAIN until independent physical validation and review. A reference-confirmed closure inside any predicted excluded gap is a falsification.

## Acceptance and release
Self-test the exact rational phase map, synthetic pulse counts, bad phase/width rejection, blinded owner selection; then execute the real source-bound packet in CI and verify all six low-rate arms, original two native arms and complete cleanup. Report source instrument PASS only on actual hosted completion. **Human ratings: 0; physical shutter calibrations: 0; hard physiological velocity ceilings: 0; held-out physical predictions: 0.** Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`, PR #26 draft/unmerged.
