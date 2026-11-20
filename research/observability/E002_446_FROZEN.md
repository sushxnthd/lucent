# E002-446 — frozen anatomical-edge identifiability triage (2026-10-25)

**Frozen before any E002-446 human-frame execution.** S19 is an already-used pilot participant. S21/S22 remain sealed. The goal is to determine whether a fixed, explainable image-edge-span candidate can support *annotation triage*, not to mistake it for anatomical aperture.

## Predeclared image instrument

Use the previously published-MD5-verified S19 Phantom AVI and only its **first 3,000 decoded 320×288 grayscale frames**. Require the accompanying sync table to contain 56,911 candidate event rows, but do **not** interpret these as physical exposure times. Do not retune any thresholds using S19.

In each frame, restrict to x=[80,240); divide into 16 fixed 10-pixel strips. Compute median intensity per row and strip; smooth each profile by a 5-row uniform kernel. For each strip, choose the most negative row-gradient in y=[55,145) and the most positive in y=[146,235). Retain strips only if both magnitudes are ≥12 gray levels. Accept a candidate only if ≥12 strips survive, their upper/lower edge row IQRs are each ≤12 pixels, median separation is 12–150 pixels, and median interior is ≥15 gray levels darker than the outside bands. Otherwise return **null**. This is an **image-edge-span candidate in pixels**, not a verified eyelid boundary.

Before human execution, require synthetic tests for a constructed eye-shaped aperture, additive brightness offset, a dark pupil-only disk, blank frames, invalid dimensions and dtype, missing frames, and a deliberately *non-eyelid dark horizontal stripe* that must pass the same geometric screen as the eye-shaped construction. This last counterexample shows anatomy is not identified by pixels alone.

## Frozen human aggregate outputs

Report candidate coverage among exactly 3,000 frames; candidate span p05/median/p95 in pixels; count of adjacent pairs with two candidates; p95 of the maximum upper/lower edge-row jump; and fraction of such pairs with ≥20-pixel jump. Report null rather than zero for empty candidate statistics. **No per-frame series, participant imagery, inferred blink labels, or identifiable timestamps** are to be persisted.

A candidate fraction <0.5 or ≥20-pixel jump fraction >0.1 rejects this simple candidate as a stable *triage* observable for this pilot. Passing both criteria would permit **only** exploratory annotation triage, never physiological interpretation, because a non-eyelid stripe is observationally indistinguishable. The known synthetic stripe counterexample is a standing veto on anatomical certification regardless of human aggregate outcomes.

## Independent human validation and product consequences

The frozen test does not authenticate camera shutter times, anatomical scale, upper/lower eyelid labels, blink type, gaze, glasses, rolling shutter, blur, illumination gradients, or a physiological speed bound. It cannot validate E002-371. S21/S22 must not be opened by this experiment. A future study needs two blinded raters marking upper/lower eyelid anatomy, mm scale, independently authenticated exposure support, explicit nuisance strata, participant-disjoint predictions and unresolved-reference abstention.

Physical hidden-closure guarantees, blink duration, PERCLOS, fatigue, and medical claims remain **ABSTAIN_UNCALIBRATED**. A successful diagnostic screen is not product authorization. Preserve all negative outcomes and CI failures. Hush unchanged.
