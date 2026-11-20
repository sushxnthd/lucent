# E002-459 FROZEN — gaze-shift transfer of human directional velocity limits

**Freeze date:** 2026-10-26. **Kernel:** E002-371/E002-457. This file must be committed **before** running E002-459 on the external human CSV. This is a *new out-of-condition falsification*, not a second search for data or a physiological hard-bound claim.

## Source and immutable split
Reuse only the author-published 2026 Culemann et al. `Blinks.csv` from `https://osf.io/download/m34qd/`, SHA256 `6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43`, already independently verified by E002-453/457. Participant IDs 3, 6, 9, 12, 15 are **held out**; all other 12 participants are calibration. Columns: `subject`, `target_pos` in `bottom,center,top`, `peak_closing_velocity` (positive mm/s), `peak_opening_velocity` (absolute magnitude mm/s). Never export rows, IDs or raw images; publish only aggregate counts.

## Primary transfer stress
Fit **center-gaze-only** calibration sample maxima separately for closing C and opening O, using calibration participants only. Evaluate these frozen maxima on **top and bottom** gaze blinks of held-out participants, with strictly greater-than comparisons. Also report center-gaze held-out as in-distribution control. Primary falsification is **at least one held-out noncenter blink** with either closing or opening peak above its center-trained maximum. Count exceeding **participants**, not only blinks; do not claim independent blink trials.

## Prespecified comparison arms
Compute the pooled-gaze C/O maxima from the same 12 calibration participants (positive control for wider coverage), and each gaze-specific C/O maximum (within-gaze transfer). Compare held-out exceedance counts in all three gaze strata and among distinct participants; report any empty calibration stratum as `NOT_EVALUABLE`. Do not retune split, threshold, stratum, sign convention, or velocity limits after seeing results.

## Hypothetical camera consequence
For **1.0-mm true instantaneous endpoint clearance** and zero nuisance uncertainty, calculate `Tcrit_ms=1000*(1/C+1/O)` for each center-only, pooled and gaze-matched pair. At nominal 240 fps, `dt=1000/240` ms, report **conditional mathematical exclusion** only; physical certification remains `ABSTAIN_UNCALIBRATED` even when no observed exceedances. If a velocity limit is exceeded, the *sample-based* center-only transfer assumption is empirically falsified for that held-out observation; the E002-371 theorem itself is not falsified.

## Analysis and kill criteria
- Any held-out noncenter exceedance kills the **center-trained sample-cap transfer assumption** on that gaze; it does not imply a population physiological upper bound for pooled or matched alternatives.
- If none exceed, report the negative result and the five-participant uncertainty explicitly; no cap validation claim.
- Even a passing transfer cannot substitute for continuous anatomical aperture trajectories, verified camera shutter/clock, geometry or independent physiological limits.
- Validate checksum, participant disjointness, finite positive speeds, complete source, known gaze, and nonempty strata. Preserve all negative outcomes.
- Use Python standard library for analysis, separate synthetic adversarial tests, and a dedicated hosted CI replay; do not access S21/S22 or modify Hush.
