# E002-504 | Frozen fail-closed static-aperture claim test

Date: 2026-10-28. Primary E002-371 branch and draft PR #26. Frozen before implementing the claim evaluator. **Engineering consequence of E002-503's verified synthetic falsification, not a new theorem, human observation or physical validation.**

## Question and predeclared predictions

E002-503 demonstrated that two perfectly agreeing raters can share an iris-diameter scale error and put a nominal normalized aperture interval entirely on the wrong side of c=0.10. Can a downstream *static anatomical research* evaluator refuse uncalibrated claims while preserving valid interval arithmetic and abstention? This must not alter the frozen E002-492/497 annotation packet or make E002-371 hidden-closure claims.

For two independent rater frames at the same prespecified image column, with valid upper/lower landmarks and per-landmark errors, an **externally measured** reference iris diameter D in [D_lo,D_hi] (strictly positive) yields each rater's conservative static aperture interval [max(0,g-2e)/D_hi,(g+2e)/D_lo]. Union the two rater intervals (do not intersect away disagreement). If they do not overlap, abstain on disagreement. Otherwise, a threshold side is conditionally inferable only if **both full intervals** lie strictly on the same side of c, with equality unresolved. No velocity, blink, shutter, timing or fatigue conclusion follows.

Predictions frozen before implementation:
1. Without a separate reference, return `ABSTAIN_MISSING_INDEPENDENT_SCALE` even if both reviewers agree 260/260; do not fall back to either rater's self-reported iris diameter.
2. With a stipulated independent reference interval [39,41] px, the E002-503 constructed cases g=4.2 and g=3.8 px, e=0.05 px must both return `ABSTAIN_THRESHOLD_CROSSED` at c=0.10.
3. With [39,41] px and gap 8 px, e=0.05, return `RESEARCH_STATIC_ABOVE`; with gap 1 px return `RESEARCH_STATIC_BELOW`. These are conditional geometry fixtures, **not physiological results**.
4. Reject missing/nonfinite/boolean/negative calibration bounds, reversed or zero intervals, invalid geometry, differing rater frame index, nuisance flags, missing independent-reference provenance and disagreement. Treat an external provenance assertion as an *input condition*, not independent verification.
5. Never output a physical hidden-closure, blink-duration, PERCLOS, fatigue or medical claim. Every output retains `product=ABSTAIN_UNCALIBRATED` and `release=BLOCKED` until physical E002-371 validation and external review.

## Evidence tiers and stopping

This executable is a conservative downstream *research-only* interpretation of **hypothetical** externally calibrated geometry. It does not repair the actual rater's inability to collect independently authenticated iris scale, and a caller-supplied provenance string cannot prove independence. Keep original blinded reviewer templates untouched to avoid corrupting the pending S01 study. Test on synthetic fixtures only; no human frames or ratings in CI. Stop additional synthetic gate iterations after the frozen controls pass or fail, and prioritize two real blinded S01 reviewers and physical camera/shutter calibration.

E002-371 physically unvalidated; zero independent anatomical ratings; product ABSTAIN_UNCALIBRATED, release BLOCKED.
