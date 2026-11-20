# E002-615 | Frozen human-source acquisition-time stress test

Frozen 2026-11-03 before examining timestamp values. Parent E002-371; branch `research/observability-human-boundary`; draft PR #26.

## Distinct question

E002-582 established a real human full-closure **frame-index** omission law using published Silesian5 Basler 100-fps annotations. E002-584 tested *hypothetical* ±1/±2 frame timing uncertainty. Here we ask whether the source's separately published **acquisition timestamp** files support the premise of uniform frame spacing, and whether timestamp-aware nominal 30-Hz *point sampling* changes the source-derived positive omission counts. This is source-derived empirical timing stress, not physical 30-fps camera shutter validation. Do not re-optimize an image feature, revisit source discovery, or reinterpret source FC labels as continuous aperture.

## Fixed source and source-shape rules

Retrieve only the already established Silesian5 annotation ZIP from https://www.blinkingmatters.com/research, SHA-256 `a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223`. The five .tag files have 58,884 annotated frames, as established by E002-582. Timestamp files are auxiliary .txt files; accept a sequence only when a unique matching timestamp member can be established **without guessing identity**, every relevant row has two numeric fields (frame ID, acquisition time), all mapped frame IDs are unique and strictly increasing, timestamps are finite and strictly increasing, and there are no unpaired annotation frames in the analyzed interval. If mapping or units are ambiguous, output `ABSTAIN_SOURCE_TIMING` with only aggregate reasons, not fabricated measurements. Never print, upload, or commit raw timestamp rows, source filenames, human images or participant identities.

## Frozen analysis

For each independently eligible source sequence, compute positive consecutive-frame timestamp differences. Report aggregate, privacy-safe dimensionless `dt/median(dt)` quantiles (0, .01, .5, .99, 1), counts exceeding ±10% and ±25% of the within-sequence median, and counts of nonpositive or unmatched pairs. Ratios do not require a time unit. A nominal 100-fps claim is not a measured calibrated 100-fps clock.

For each source FC-positive per-eye run satisfying E002-582's flanking, nuisance and continuity rules, compare the original E002-582 ten-phase index-only point selection with a **timestamp-nearest** nominal 30-fps point schedule: define `d` as median positive source interval; for phase `p=0,...,9`, nominal target times are `t_first + (p + 10*k/3)*d` for nonnegative integer `k` until `t_last`; select the source frame minimizing absolute timestamp distance to each target, breaking ties toward the earlier frame. A run is omitted only if none of its positive frame IDs is selected. Report per-phase omissions and paired counts of event-phase changes (index-only omission vs timestamp-nearest omission). This schedule is a **virtual point selector**, not a physical 30-fps exposure, and its phase grid is an artificial schedule. If exact source time units or acquisition meaning cannot be defended, report only the dimensionless cadence stress and abstain from timestamp-phase omission inference.

## Preregistered falsifiers and controls

- Synthetic uniform timestamps with exactly aligned frame indices should reproduce the original phase law only when both selectors use equivalent point rounding; do not silently assert equivalence between floor-index and nearest-time sampling.
- A single delayed frame and a dropped-frame gap must alter the cadence diagnostic; no smoothing or deletion to conceal this.
- Nonmonotonic timestamps, duplicate frame IDs, mismatched annotation/timestamp mapping, ambiguous sequence association, unknown numeric fields, and missing timestamps cause abstention.
- Uniform affine transformation of timestamps with positive slope leaves all dimensionless diagnostics and timestamp-nearest omission counts unchanged.
- Independent cross-language arithmetic or a separate brute-force implementation should verify at least the selection/tie-break fixtures before claiming independent verification.
- Any source evidence that contradicts the frozen model must be retained as a negative result; no retrospective thresholds.

## Evidence and product boundary

Source timestamps are not independently authenticated photodiode measurements and do not specify shutter exposure, rolling-row timing, anatomical aperture, or continuous-time eyelid speed. Even a clean cadence cannot validate E002-371. A cadence failure or material disagreement with index-only omissions invalidates any claim that the E002-582 index omission counts are camera-time-calibrated. In all cases Lucent remains `ABSTAIN_UNCALIBRATED`, release `BLOCKED`; only independent physical camera timing and blinded human anatomical measurement can change that. Preserve Hush branch and PR #45.
