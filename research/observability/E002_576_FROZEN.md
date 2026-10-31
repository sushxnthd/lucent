# E002-576 | Precommitted LPW two-rater native-frame alias adjudication

Frozen 2026-11-01 before implementation and before any authentic LPW ratings were obtained. Primary kernel E002-371. Extends E002-573/574/575 without changing the participant split, selected windows, or all three 3:1 decimation phases. This is **not** physical shutter validation.

## Testable prediction

For a complete, independently reviewed 19-frame held-out window, classify a frame CLOSED only if both independent anatomical interval estimates have a nonempty intersection **entirely at or below** a prespecified normalized aperture threshold c=0.20. Classify OPEN only if their nonempty intersection lies **strictly above** c. Anything else, including zero uncertainty, unreviewed frames, nuisance flags, disagreements or unverified iris-diameter error budgets, is UNCERTAIN.

For every phase p in {0,1,2}, retain native indices i with i mod 3=p. A positive alias witness requires two adjacent retained OPEN frames with at least one CLOSED native frame strictly between them. Count all phases; do not select a favorable phase after seeing ratings. Report participant-level counts and all abstentions. A positive witness is **native-frame index aliasing only**, never an actual 30-fps exposure or continuous-time closure proof. A zero witness count cannot exclude closures.

## Independent iris scale

The existing E002-574 rating schema contains iris_diameter but **no denominator uncertainty**. A separate owner-private, pre-established and independently justified positive per-video diameter uncertainty budget is mandatory. Apply interval arithmetic to each rater's pixel-gap bounds and iris-diameter bounds before adjudication. If the budget is missing, nonpositive, nonfinite or lacks independent provenance, refuse all OPEN/CLOSED labels. An asserted JSON provenance string is not independently authenticated; output evidence is conditional until verified by a human custodian.

## Adversarial controls

Test positive alias, negative/no-alias, phase differences, rater disagreement, near-threshold denominator uncertainty, nuisance/blur/gaze/missingness, zero/absent calibration, duplicate or missing native frames, wrong participant/clip mapping, malformed frame geometry and partial review. Require deterministic output under shuffled dictionary insertion order and never export private per-frame labels or identifiable images. No physiologic product claim is allowed.

## Stop/go

Only run on private genuine human rater exports after separately authenticated source custody and independent rater identity. Local synthetic fixtures test the implementation, not human performance. If no actual rater pair exists, preserve the tool and stop; do not generate pseudo-human ratings or new synthetic physiology theorems. E002-567's independently synchronized physical shutter/photodiode study remains mandatory.

Release remains BLOCKED; all physiological claims ABSTAIN_UNCALIBRATED.