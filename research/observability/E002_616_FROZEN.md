# E002-616 | Frozen bilateral full-closure virtual-alias test

Frozen 2026-11-03 before calculating bilateral outcomes from the Silesian5 source. Parent kernel E002-371; preserve branch `research/observability-human-boundary` and draft PR #26. No other scientific kernel.

## New question and product consequence

E002-582 and E002-615 counted *per-eye* human full-closure runs. An eye-specific omission does not establish that a **simultaneous bilateral full-closure interval** was invisible. This prospective test counts only contiguous frames in which **both** source eye FC flags equal C (published 90–100% closure categories), then determines whether nominal 30-Hz point selection omits the *entire bilateral-positive interval*. This directly tests the weaker, defensible claim that source-labelled simultaneous bilateral closure can disappear under virtual downsampling. It does not test physical shutter integration, continuous eyelid aperture or fatigue.

## Immutable source and event eligibility

Reuse the E002-615 SHA-256-pinned Silesian5 archive, parser, timestamp mapping and point selectors without modifying them. For each of the five independently matched sequences, define a bilateral-positive run as a maximal consecutive frame-index interval where both FC fields are C. Require at least one flanking frame on both sides, consecutive frame IDs across both flanks, and no nonfrontal or either-eye-not-visible N flag anywhere in that interval plus flanks. Exclude ineligible runs, report reasons. Do not conflate these with individual left/right runs or with 300 investigator-defined blink events. No raw rows, names, frames, timestamps, event IDs or identifying details in committed outputs.

## Prespecified endpoints

1. Eligible bilateral run count and histogram of lengths 1,2,3,>=4.
2. For each of 10 fixed phases p=0,...,9, omissions under E002-582 original floor-index selection and E002-615 actual source-time nearest selection. Each omission means no **bilateral-positive** frame was selected.
3. Number of distinct eligible bilateral runs omitted in >=1 phase for each selector; paired event-phase disagreement count; overlap of omitted event-phase pairs; any run length >=4 omitted under either selector.
4. Exact integer law for floor-index sampling on interior contiguous runs: omitted phases per run are 7,4,1,0 for lengths 1,2,3,>=4. Falsification is a mismatch in any interior eligible run.
5. Per-sequence privacy-safe counts, all aggregate-only. Check sums, nonnegative counts and reproducible source hash. No population-rate confidence intervals; phase trials are dependent and only five sequences exist.

## Stop/falsification and interpretation

If bilateral eligible runs are zero, report a negative result and do not infer any binocular alias phenomenon. If the timestamp pairing or source hash fails, fail closed. If the source-derived floor-index exact phase law fails, preserve counterexample count and do not repair labels or tune phases. If some eligible bilateral runs disappear under at least one phase, claim **only** human-source bilateral categorical point-sampling omission, not missed physical camera exposures or hidden continuous closures. If no such runs exist, explicitly kill the proposed positive bilateral witness in this source. Independently recheck all aggregate arithmetic with a separate minimal oracle. No source images or individual rows published.

## Release gate

Neither positive nor negative outcome validates E002-371's shutter-gap/velocity theorem in physical humans. Require independent synchronized shutter/clock calibration, independently blinded anatomical raters, justified continuous-time speed ceiling, participant-disjoint physical predictions and adversarial nuisance calibration before changing `ABSTAIN_UNCALIBRATED` / `BLOCKED`. Hush PR #45 untouched.
