# E002-546 FROZEN | High-rate reference can itself alias a closure

Date: 2026-10-30. Primary E002-371 human-validation kernel. Frozen **before** implementation and numerical checks. Evidence tier: public-source qualification + exact instrument/sampling falsifier; **not human validation**.

## Question and decision

Can a nominal 100 or 200 frames/s *reference camera* be treated as complete truth when evaluating a 30 frames/s shutter-gap closure-exclusion rule? **No**, absent an independent continuous-time bound or independent reference instrument. A sampled reference positive is a usable witnessed closure; a sampled reference negative does not certify no closure.

Predeclare the following hypothetical continuous-time aperture trajectory, without fitting any parameter to a human:
- normalized open aperture `b=9/10`, closure threshold `c=1/5`;
- one triangular closure of total duration `T=1/100 s`, apex at `T/2`, minimum aperture zero, with endpoint aperture `b`;
- slope magnitude `V=2b/T=180/s`, a **constructed** velocity, not a physiological upper bound;
- ideal instantaneous, noise-free frames with unknown phase uniform on one sampling period `delta=1/f`.

Freeze exact calculation: the interval at or below `c` has width `w=T*c/b=1/450 s`. The probability that a periodic sample intersects this interval under a uniform unknown phase is `min(1, w/delta)`. Worst-case adversarial phase can miss whenever `w<delta`. Check at `f={30,100,200,240,500}` Hz. For 100 Hz use phase 0; for 200 Hz use phase 1/400 s, demonstrating missed threshold contact despite frame rate above the event's reciprocal duration. Verify exact rational arithmetic; no floating-point threshold fitting.

## Two concrete human-video acquisition routes

1. **Silesian5**, [author dataset page](https://www.blinkingmatters.com/research): 100 fps Basler video, 5 subjects, approximately 300 blinks, 58,884 annotated frames after conversion. Original annotation imprecision and codec truncation are documented. The author says access to converted videos requires approval from Krystian Radlak and a signed license agreement. **No authorized video was obtained** in this run. This is a candidate for positive-witness and nuisance tests, not an unqualified negative ground truth.
2. **OpenEDS**, [original paper](https://arxiv.org/abs/1905.03702): eye-facing cameras at 200 Hz, 152 participants, short video sequences, data access upon request. The paper's eye-region segmentation annotations are not independently certified continuous-time eyelid closure measurements. **No authorized frames obtained**. Qualify rights and eyelid visibility before use.

mEBAL2 and ZJU/Eyeblink8 are ordinary-rate resources and do not provide an independent high-rate reference. Do not repeat broad dataset searches in the next run without a specific new access path.

## Prespecified empirical protocol once access is lawful

- Lock participant IDs and camera/timestamp provenance; keep one entire participant-disjoint evaluation set unseen. Never treat contiguous windows as independent people.
- Independently annotate upper/lower eyelid separation with two blinded raters, landmark uncertainty, visibility, glasses, gaze, blur, occlusion, illumination, geometry and rolling-shutter row. Resolve disagreement without access to Lucent's predicted exclusions.
- For each high-rate **positive witness**, generate ordinary-rate observations with known timestamps and actual integration kernels, not naive frame dropping. Independently estimate a conservative velocity envelope on calibration participants; finite differences alone do not certify a continuous-time ceiling. Evaluate precommitted E002-371 exclusion predictions on held-out people. Any confidently witnessed closure in an excluded gap is a falsification candidate requiring timing/geometry audit.
- For a **negative reference**, require a separately justified continuous-time coverage guarantee or label `REFERENCE_NEGATIVE_UNCERTIFIED`; never count it as proof of absence. In particular, 100/200 Hz alone cannot provide it.
- Predeclare nuisance strata and abstention. Report participant-level false exclusions, reference-unknown fraction, coverage, uncertainty intervals and no pooled window-level confidence claims. Unseen conditions include glasses, gaze change, motion blur, variable exposure, dropped frames and clock offset.
- Physical validation still requires externally authenticated shutter timing (photodiode or equivalent), observation transfer, and an independently measured motion ceiling. Synthetic sampling results do not substitute.

## Product gate

No physiological bound or ordinary-camera hidden-closure exclusion may be advertised from this exercise. Current product state `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Preserve negative findings. Do not merge PR #26 or modify Hush PR #45.
