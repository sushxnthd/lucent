# E002-499 | Frozen column-consistency falsification of blinded anatomical review

Frozen 2026-10-28 **before** implementing the falsifier or amending the offline rater. Primary E002-371 human-validation kernel. This is a synthetic *instrument-validity* falsification, not an observed human eyelid result.

## Hypothesis and flaw under test
E002-497 permits a reviewer to click any upper/lower lid pair at approximately the same horizontal coordinate **within a frame**, but its E002-492 output schema stores only y coordinates. Two independent reviewers may therefore choose different x columns on the **same static image**, and one reviewer may change x between frames. The E002-492 adjudicator has no means to detect the mismatch. Reopening a frame already redraws stored points at x=160 even if they were originally clicked elsewhere. This may create apparent anatomical disagreement or temporal motion from geometry alone.

## Prespecified falsifier (all values synthetic)
Let a static upper lid be y=90 pixels and lower lid be y=90 + h(x), where h(x)=12 + 0.03(x-160)^2 pixels. Use the same image, iris diameter d=40 pixels and per-landmark uncertainty e=0.5 pixels. Rater A chooses x=160, rater B x=170. Their exact normalized aperture intervals are [0.275,0.325] and [0.35,0.40], disjoint despite identical anatomy. E002-492 should report one disagreement. A static image viewed at x=160 then x=170 also produces an apparent normalized aperture change of 0.075 with **no physical motion**. At a shared x=160 both raters should agree. If any prediction fails, report it without adjusting the geometry.

## Conservative pre-label amendment
Because **zero human annotations have been collected**, amend E002-497 before field use to accept lid landmarks only at native x=160 (within half a native pixel for input, canonicalized to 160). Draw a visible reference line; a frame without reliably visible anatomy at this fixed column must be flagged POOR_GEOMETRY, MISSING_ANATOMY, GAZE or another nuisance, not moved to a different column. The original iris-center-column instruction is **superseded**; the new measurement is an explicitly fixed-image-column aperture and may have low coverage. The E002-492 JSON schema remains unchanged, but only the amended interface is eligible for future review.

## Acceptance / kill criteria
- Exact synthetic intervals, disagreement and zero-motion counterexample reproduced by an independent unit test using the actual E002-492 adjudicator.
- UI prevents off-column click acceptance, visually displays the reference column, restores saved points consistently, and retains local-only privacy and explicit abstention.
- Existing E002-497 schema/security tests plus new static tests and Node syntax check pass in hosted CI.
- If authentic S01 frames have no reliably measurable iris/lids at x=160, **kill this fixed-column pilot** rather than relaxing x post hoc. Do not claim that fixed x corrects gaze, projective geometry, occlusion, timing, or independent anatomy.
- No human images or ratings committed or uploaded; no camera fps inferred; E002-371 physical hidden-closure certification remains unavailable. Product ABSTAIN_UNCALIBRATED; release BLOCKED.

No Hush or automation changes.