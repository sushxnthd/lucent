# E002-455 frozen protocol: human high-rate optical aliasing under temporal decimation

Frozen 2026-10-26 before implementing the analyzer or running it on S19. Parent E002-371; previous result E002-454 rejects strong cap validation. This experiment asks a **different, empirical** question: can an ordinary-camera-like endpoint subsample of *real high-frame-rate human eye imagery* conceal a measurable **image-space contrast excursion**? It does **not** label anatomical eyelid closure, blink, shutter integration, or physical speed.

## Source and separation
- Only previously inspected S19 from Guttmann-Flury et al. (2025), hash-verified with existing E002-444 acquisition; S21/S22 remain sealed.
- Decode the first 12,000 320x288 grayscale frames in order. Frame index is the sole time coordinate; archive synchronization events are **not** treated as authenticated exposure timestamps. No claim of physical 30/60 Hz acquisition.
- Preassign frames 0..1999 for threshold calibration; frames 2000..11999 are the untouched temporal evaluation block **within S19** (not participant-disjoint). No image or individual time series enters public artifacts.

## Observable and nuisance control
- Center C: rows 72:216, columns 80:240 (same as E002-445); border B: its complement. Primary scalar z = (mean(C)-mean(B))/255, signed and dimensionless.
- Negative-control scalar w = (mean(B_left)-mean(B_right))/255, where B_left and B_right are pixels in border B with x<160 and x>=160 respectively. Both control patches are disjoint from C.
- z cancels spatially uniform additive illumination in unclipped images, not nonlinear brightness, spatially varying light, gaze, blur, occlusion, compression, or geometry. w is an imperfect spatial nuisance control, not a guaranteed null.
- Threshold T = max(4/255, 8*median(abs(diff(z_calibration)))) computed only on frames 0..1999; freeze this formula, do not retune to observed evaluation outcomes. Threshold must be finite and >0.

## Exact evaluation
For each decimation stride K=8 and K=17, enumerate all phases p in 0..K-1, with nonoverlapping endpoint intervals within each phase: a=2000+p+j*K; b=a+K<12000. Across phases windows overlap, so **no iid or participant-level confidence interval**. For each interval, linearly interpolate endpoint z. Call a **hidden optical excursion** when abs(z[b]-z[a])<=T/2 and max over strictly interior frames of abs(z[i]-interpolated_z[i])>=T. Repeat with w and the same T as a negative-control comparison; no threshold fitted to w. Report interval counts, excursion counts, fractions and min/max/median phase fractions, plus endpoint-near counts for each channel. No extrapolation from phase counts to independent participants.

## Frozen kill/interpretation criteria
- At least one qualifying z excursion at each K supports the narrow statement: *some actual S19 image-space contrast trajectories have nearly equal decimated endpoints but an intervening excursion under this fixed optical definition*. Otherwise label NOT_OBSERVED and preserve the negative result.
- If the w control's excursion fraction >= z's at either K, mark SPATIAL_SPECIFICITY_NOT_ESTABLISHED. If z>w at both K, mark PRIMARY_OPTICAL_ALIASING_OBSERVED_CONTROL_LOWER, still **not** eyelid anatomy.
- Any malformed frames, source checksum mismatch, incomplete decode, nonfinite metrics or bad phase accounting fail closed.
- Synthetic tests must include a triangular hidden excursion (positive), monotone trace (negative), additive uniform brightness (invariance when no clipping), spatial-gradient nuisance that can produce a false anatomical inference (explicit rejection), missing frames (reject), and phase-count integrity.
- No physical shutter/clock calibration, independent anatomical labels, validated physiological cap, or holdout participants: E002-371 physical validation remains NOT_ESTABLISHED, product stays ABSTAIN_UNCALIBRATED. Keep PR #26 draft/unmerged. No Hush writes.

## Novelty/priority boundary
E002-371 already establishes conditional mathematical nonobservability, E002-445 already measured S19 spatial optical associations, and E002-447 already studied synthetic shutter integration. E002-455 is **only** a new prospective human-video temporal-decimation test of a defined nonanatomical optical observable. It is not a new theorem or a blink detector.
