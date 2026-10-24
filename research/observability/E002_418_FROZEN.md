# E002-418 — frozen synthetic landmark-rater qualification experiment

**Frozen 2026-10-24, before implementation, generation, or scoring.** E002-371 remains the sole Lucent scientific kernel. This is an **instrument/observer qualification experiment** addressing the missing E002-407 independent human rater sheets. It is NOT physical eyelid calibration, human annotation evidence, or an extension of the rejected E002-417 image estimators.

## Prospective design

Generate an entirely synthetic, local-only 190×130-pixel eyelid-geometry challenge using the unchanged E002-407 offline annotator and CSV contract. Four cryptographically pseudonymized clips, 36 frames each, contain exactly 16 instances of each of nine prespecified conditions: clean, brightness 0.70, brightness 1.30, 3×3 blur, rigid vertical shift, displaced pupil/gaze, central glare, opaque occlusion, and a glasses-like obstruction. The first six have known visible upper/lower lid boundaries; the last three intentionally obscure required margins and must be marked unresolved. Every condition is distributed across clips, with concealed condition order and concealed ground-truth landmarks. Preserve the truth in a separate private directory. Do not place private truth in the blinded rater pack.

Two genuinely independent human raters must complete the **same** immutable challenge without seeing truth or each other's sheets. Each must complete all 144 rows. For resolvable cases, success means all six annotated landmarks are within 5 px horizontally of the designated left/center/right reference columns and within 3 px vertically of the synthetic ground-truth boundary at the clicked x coordinate. Any unresolved/missing frame is counted as failure for these 96 cases. For the 48 deliberately obscured cases, success requires explicit unresolved; a confident coordinate output is a failure regardless of its appearance. No post hoc removal of failures.

## Prespecified acceptance criteria

1. Generator integrity: 144 valid PNGs, SHA-256 manifest verification, 4×36 frames, 16/condition, and exact E002-407 manifest/CSV compatibility.
2. Each rater: at least 87/96 fully correct resolvable frames (>=90%), and at least 12/16 correct for **each** resolvable nuisance condition (>=75%).
3. Each rater: at least 46/48 abstentions on obscured frames (>=95%). Report false-confident counts by condition.
4. Two distinct rater IDs and complete independently exported CSVs. Report both rater results and agreement on all eligible frames; **do not** turn agreement into anatomical accuracy.
5. Positive oracle sheets must pass, while a systematically shifted landmark oracle and a confidently guessed obscured oracle must fail. The independent test must verify no truth/condition mapping is present in the public manifest.

## Decision and limitations

A pass establishes only that a rater can follow the offline tool and detect gross synthetic visibility failures. It does not qualify physical human eyelid annotation, camera timing, hard velocity bounds, anatomical landmarks, or E002-371. A failure blocks use of that rater's E002-407 sheets until the training/qualification protocol is repeated on a fresh pack. The experiment must not be called successful until two actual independent human rater sheets exist. Keep private human frames, ratings, synthetic challenge answers, and event/control linkage off public GitHub. Product state is always `ABSTAIN_UNCALIBRATED`.

This adds a prospective falsifiable observer-quality control, not a novelty claim. No change to E002-407's previously frozen real-human sample selection or to draft PR #25's branch.
