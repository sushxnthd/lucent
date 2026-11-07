# E002-585 | Frozen independent anatomical-rating and physical-calibration gate

**Freeze:** 2026-11-01 UTC, before implementation or use on human data. Kernel E002-371, existing branch `research/observability-human-boundary`, draft PR #26. No human acquisition or rating is claimed.

## Decisive measurement question

Can independently rated, time-calibrated high-speed human eyelid aperture provide a **held-out** reference against which E002-371's conditional shutter-gap predictions can be falsified? Earlier Silesian5 index-omission results do not answer this because there is no independent physical shutter, continuous-time velocity ceiling, or second anatomical rater.

## Prospective input and abstention rules

Input is a **local-only**, privacy-controlled session manifest, two separate blinded rater files, and an external velocity certificate. Every session has a pseudonymous clip ID, pseudonymous participant ID, a participant-disjoint split (calibration or holdout), native frame count, calibrated per-frame timestamp bounds, calibrated imaging-path exposure/rolling-row support, a verified eye-plane geometry scale, and explicit nuisance flags (illumination, blur, gaze, glasses, occlusion, dropped frames, clock drift). A trigger LED alone does **not** authenticate the sensor's exposure window. No identities, frames or anatomical measurements are committed to GitHub.

Each rater independently supplies framewise *intervals* for normalized anatomical eyelid aperture [0,1], or `null` when invisible. Raters must be blind to each other, ordinary-camera predictions and the held-out outcomes. The reference uses the **union hull** of two valid independent aperture intervals, never an average. With preregistered closure threshold `tau=0.2`: classify `CLOSED` only when the hull upper bound <=tau; `OPEN` only when the hull lower bound >tau; otherwise `UNCERTAIN`. Rater disagreement exceeding 0.15 normalized aperture, missing/invalid interval, or any active nuisance that invalidates geometry yields `UNCERTAIN`, never an inferred open eye. Uncertain frames cannot prove absence of a hidden closure.

A participant may occur in **exactly one** of calibration and holdout. Two different declared rater IDs are mandatory. All timebases and imaging-path shutter supports must be independently certified. A measured maximum or upper sample quantile of velocity **cannot** serve as a deterministic human velocity ceiling. If any certificate is missing or any condition is out of scope, the physical no-hidden-closure decision is `ABSTAIN_UNCALIBRATED`.

## Fixed synthetic verification and kill tests

Build a zero-dependency executable that (1) rejects participant split leakage; (2) rejects duplicate raters; (3) handles missing/invalid intervals; (4) distinguishes unanimous closure, unanimous open, and threshold ambiguity; (5) refuses nuisance-corrupted frames; (6) never turns a missing velocity/shutter/clock/geometry certificate into a physical exclusion; (7) emits only aggregate counts and provenance hashes, not private rows. Execute synthetic fixtures independently of real data.

**Human study primary endpoint (future):** on sealed participant-disjoint holdout, compare frozen per-gap `CERTIFIED_NO_HIDDEN_CLOSURE` predictions with independently adjudicated high-rate closure witnesses. One confirmed hidden closure under certified premises falsifies that physical certificate or its premises. Report false exclusions, abstention/coverage, disagreement, per-participant and nuisance-stratified counts. Do not treat multiple frames or decimation phases as independent participants.

**Evidence ceiling for this run:** a validated protocol compiler/annotation adjudication instrument is **not** human validation. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED` until physical shutter metrology, independent raters, defensible continuous-time velocity ceilings, held-out prospective predictions, and external review exist.
