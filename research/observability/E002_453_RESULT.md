# E002-453 — first participant-disjoint human velocity-cap transfer audit

**Date:** 2026-10-26. **Preregistered before examining velocity distributions:** [E002_453_FROZEN.md](E002_453_FROZEN.md), commit `0c2a3674b9596d9cb6b249e696de0441bff79ceb`. **Evidence:** external published per-blink *human* estimated eyelid peak velocities; one study, 17 participants, voluntary blinks, 3 gaze positions. **Not** Lucent's own anatomical annotations or high-speed exposure-ground-truth validation.

## Source and integrity

Culemann et al., *Behavior Research Methods* 58, article 89 (2026), DOI [10.3758/s13428-026-02984-4](https://doi.org/10.3758/s13428-026-02984-4); author OSF project [tud8a](https://osf.io/tud8a) and public [Blinks.csv](https://osf.io/m34qd). The public OSF API reports SHA256 `6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43` and 743,520 bytes. The independently accessed browser-extracted CSV contained 743,520 characters and 2,306 data rows. **This initial aggregate is not yet a cryptographically verified raw-file replay**; the committed [stdlib analyzer](e002_453_external_human_velocity.py) requires exact SHA256 and the [dedicated hosted workflow](../../.github/workflows/e002_453_external_human_velocity.yml) is intended to independently verify source bytes, run tests and reproduce aggregates. Until hosted verification succeeds, treat this as a preliminary source-backed aggregate.

The source CSV includes `subject`, `target_pos`, `peak_closing_velocity`, `peak_opening_velocity`, `closing_amplitude` and `duration`. The velocity is an *estimated peak per blink*, not a certified upper bound on instantaneous physiological motion. No raw videos, camera exposure timing, individual anatomical trajectories, or physical maximum were obtained. Raw participant rows were not committed.

## Frozen participant-disjoint test

Hold out participants **3, 6, 9, 12 and 15** before examining values; use the other 12 participants to construct three candidate velocity caps. All 2,306 rows parsed as valid with zero exclusions; 1,657 calibration blinks and 649 holdout blinks.

| Estimated peak closing velocity, mm/s | Calibration (12 people) | Holdout (5 people) |
|---|---:|---:|
| Minimum | 61.260 | 98.116 |
| Median | 238.377 | 241.292 |
| Maximum | **567.104** | **427.053** |
| Nearest-rank 99th percentile | 509.901 | Not used for fitting |

The calibration-set maxima by gaze target were **546.552 mm/s (bottom, n=539)**, **567.104 (center, n=558)**, and **521.107 (top, n=560)**. Holdout maxima were **402.709 (bottom, n=208)**, **427.053 (center, n=222)**, and **392.030 (top, n=219)**. This is descriptive only: target labels are not calibrated gaze angles for every frame, and these measurements are method- and population-specific.

**Frozen transfer outcomes:** 0/649 holdout velocities exceeded the calibration pooled maximum; 0/649 exceeded the calibration pooled 99th percentile; and 0/649 exceeded the corresponding calibration gaze-specific maximum. All five held-out participants had zero exceedances for these three rules. This is a **negative falsification attempt**: these particular sample-derived caps were *not* contradicted by these five people, but there is no basis to promote them into hard physiological speed limits. Blink events are clustered within people; 649 is not 649 independent participants. The study was voluntary-blink-only, and the holdout people came from the same acquisition protocol.

## New product-relevant implication

The calibration sample's **observed peak estimate of 567.104 mm/s** is nearly 2.84 times the prior E002-452 illustrative 200-mm/s value. The latter was explicitly hypothetical, not a prior asserted cap. Using the *sample maximum only as a hypothetical conditional bound*, and hypothetical **instantaneous** endpoint apertures of 3 mm, threshold 2 mm, the E002-371 sharp Lipschitz condition would require an unsampled gap **strictly shorter than 3.52669 ms** to exclude an unobserved threshold crossing. Nominal 30-fps (33.33 ms), 60-fps (16.67 ms), and even 240-fps (4.17 ms) frame intervals exceed that illustrative threshold. Real shutter integration, rolling shutter, clock uncertainty, missed frames, nuisance motion and geometry can only complicate this comparison. **No actual 30/60/240-fps video was certified by this experiment.**

This is a concrete warning against making physical no-hidden-closure claims from ordinary cameras based on pooled average blink velocities or nominal frame rates. It does **not** establish that every actual camera gap hides a closure, nor that 567.104 mm/s is a universal physiological maximum. Without a valid speed bound, the conditional exclusion has no physical authorization.

## Falsification, limitations and next measurement

- Frozen cap transfer was **not falsified** on this small same-study holdout; report this negative result without recasting it as proof.
- The new external human source supplies per-blink **velocity estimates**, not time-resolved high-speed anatomical paths. It cannot directly test whether a supposedly excluded gap contained an actual hidden closure. It also cannot authenticate S19 exposure timing or repair the E002-446 edge-proxy failure.
- Reproduce on the raw hash-verified CSV in hosted CI, and compare the independently generated aggregate to [E002_453_HUMAN_AGGREGATE.json](E002_453_HUMAN_AGGREGATE.json). If checksum, row counts, or outcomes differ, invalidate the preliminary aggregate and preserve the failure.
- The next physically decisive study remains independently calibrated high-frame-rate anatomical margin trajectories, authenticated exposures, gaze/behavior strata, nuisance controls, and **prospectively frozen** hidden-crossing predictions evaluated on participant-disjoint ordinary-camera samples. The restricted FaceBase 400-fps release is a promising authorized-access target. S19 requires two independent human rater exports; S21/S22 remain untouched.
- No physical closure guarantee, blink duration, PERCLOS, fatigue or medical use is authorized. `ABSTAIN_UNCALIBRATED` remains mandatory. PR #26 stays draft/unmerged.

**Reproduce with source file held locally:** `python -m unittest -v test_e002_453_external_human_velocity.py`; `python e002_453_external_human_velocity.py --csv /authorized/Blinks.csv --out /tmp/e002453_aggregate.json`. The script fails closed on a SHA256 mismatch. No new dependencies or API costs.
