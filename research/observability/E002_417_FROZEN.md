# E002-417 — frozen real-human eyelid-geometry candidate falsification

**Frozen 2026-10-24 before implementation or evaluation.** E002-371 is the sole scientific kernel. This experiment tests whether an automatically extracted **pixel-space candidate** is even sufficiently stable to justify *subsequent* independent human annotation. It cannot establish physical eyelid aperture or shutter/velocity calibration. The previously rejected E002-397 optical-flow and E002-412 fixed darkness scores are not rehabilitated.

## Source and design
- Reuse the exact MD5-verified S01 and S19 Eye-BCI archives, E002-412's deterministic first two complete event/control pairs per participant, eight half-second clips, approximately 632 frames, and the fixed 190×130 eye crop. No new subject/clip selection based on appearance.
- Use two independently specified, fixed image-to-pixel-gap estimators without fitting or post-result tuning: **A** pairs an upper negative and lower positive vertical intensity-gradient ridge in central columns; **B** estimates the central dark interval using adaptive skin-band intensity. Both must return an explicit unresolved state if geometry/contrast/saturation checks fail.
- This is *not* two human raters, and algorithmic agreement is *not* accuracy. The methods have shared image nuisance and can agree while both are wrong.
- Apply deterministic transforms to each source frame: 0.70× and 1.30× brightness, Gaussian blur sigma 2 px, translation (+8,+6) with reflected border, and a central white-glare rectangle. For translation, compare **vertical gaps**, which should be invariant to a rigid shift, not absolute pixel coordinates. No frame interpolation. Synthetic image controls with known rectangular apertures test whether both methods can recover a gap at all.

## Prespecified decisions (report all denominators)
H1: Exactly eight clips and at least 600 source frames.
H2: At least 60% of *all* clean frames produce valid A and B estimates agreeing within 5 px, not merely 60% of jointly valid frames.
H3: For **each** of gain070, gain130, blur2 and translation(+8,+6), at least 95% of the clean joint-valid frames must retain both valid estimates and each method's gap must change by <=3 px; separately report all-frame valid retention.
H4: At least 95% of white-glare frames must abstain in both methods (fail closed).
H5: Both methods recover a fixed 24-pixel gap on synthetic idealized open-eye controls within 3 px, and neither emits a product certificate.
The **joint transfer gate** passes only if H1–H5 pass. Failure kills the geometry candidate *as a transferable measurement* without post-hoc threshold adjustment. A pass only advances it to independent blinded human landmark validation, never to physical product authorization.

## Independent checking, data protection and limitations
- Independent tests construct their own known-gap images, independently verify exact transform parameters, assert count conservation and missingness denominators, and reject malformed/blank/saturated inputs. Do not silently drop invalid frames.
- Report aggregate metrics only, not raw frames, per-frame gaps, participant-linked events, source timestamps or EEG mapping. Source frames remain ephemeral in CI. Never upload raw eye images or rater sheets.
- Camera exposure/rolling shutter/clock, anatomical scale, gaze, glasses, physiological hard velocity and true lid-margin locations are **uncontrolled**. A computer-vision gap cannot be equated with physical aperture. Even if every H passes, product remains `ABSTAIN_UNCALIBRATED`.
- Human-validation next gate is still E002-407 two **actual independent blinded human rater sheets** plus E002-408 adjudication and separately calibrated physical reference. No synthetic annotation is represented as human annotation.

Prior art: eyelid landmark and image-intensity extraction are established; this is a preregistered, dataset-specific necessary-condition falsification, not a novelty claim.
