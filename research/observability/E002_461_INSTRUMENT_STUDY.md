# E002-461 — executable physical-instrument and human validation handoff

**Status:** prospective protocol, **not executed**. This complements [E002-456](E002_456_FROZEN.md), not a substitute for independently annotated human eyelid kinematics. No purchase or human recruitment is authorized by this file.

## Stage A: falsify the measurement model with a moving aperture phantom

**Question:** Does a static image-feature-to-aperture calibration commute with exposure integration? The E002-461 quadratic model predicts that it need not. Construct a slit/eyelid phantom whose physical opening is driven through known positions; acquire reference aperture position with an independently calibrated scale and timebase. A printed ruler visible in the eye plane is not by itself a dynamic reference; require a separately checked displacement trace and timing.

1. **Static calibration (training only):** Hold the aperture at at least 12 preselected openings spanning the test range. Measure the camera feature, repeat under three illumination levels and at least two focus settings, and fit the transfer map without any moving frames. Record residuals, gain, saturation and photometric drift. Split calibration from evaluation by motion sequence and lighting condition.
2. **Dynamic acquisition:** Use a hardware LED time code shared by the test camera and a separate high-speed reference (target >=400 fps if available). Record per-frame exposure width, readout/rolling-shutter timing, dropped frames, LED transitions, gain, and clock residuals. A 240-fps phone recording alone is not an authenticated 400-fps reference; virtual decimation is labeled simulation.
3. **Predeclared motion:** Include constant-speed closure/reopening, V-shaped near-threshold events, asymmetric closing/opening, stops/reversals, and trajectories whose closure occurs strictly between exposure supports. Change speed and exposure duration independently. Never infer a hard human speed cap from phantom motion.
4. **Nuisance matrix:** factorial or blocked changes of brightness, background texture, geometry, defocus/blur, gaze-like rotation, transparent glasses/reflections, sampling drops, and clock offsets. Include rolling-shutter skew and autoexposure as explicit failure conditions. Report each stratum; do not average failures away.
5. **Three blinded pipelines:** (A) invalid static inversion of exposure-averaged feature; (B) full dynamically calibrated forward sensor model; (C) E002-461 variance-aware bound only where an authenticated quadratic model is justified. The analyst running predictions must not inspect the high-speed crossing reference first.
6. **Predeclared falsification:** Any independently verified crossing strictly inside the shutter-dark gap classified EXCLUDED_CONDITIONALLY kills that pipeline's claim for the tested conditions. Unknown timing, geometry or transfer -> ABSTAIN, never impute open. Report denominator, coverage, abstention, false-exclusion count and per-condition error; retain all negative results and scripts.

**Minimum data record (private until deidentified):** sequence_id, instrument_id, shutter support and kernel, centroid and uncertainty, sensor transfer version, reference scale and uncertainty, clock calibration and residual, nuisance flags, blinded reference crossing witness with uncertainty, frozen prediction, and exclusion/abstention reason. SHA256 raw-file checksums and an independent pre-unblinding manifest timestamp are mandatory.

## Stage B: prospective human anatomical reference

Use [E002-456 sealed holdout](E002_456_RESULT.md) with consent, locally controlled storage, two blinded anatomical raters, verified eye-plane mm geometry, synchronized >=240-fps anatomical reference (prefer >=400 fps), and simultaneous ordinary-camera recordings. Stratify neutral/up/down gaze, glasses, lighting, motion, voluntary/spontaneous blink, blur, and missingness. Raters must annotate anatomical upper/lower lid margins, not pupil contrast or RGB brightness. Keep participants disjoint between velocity calibration and reference testing.

**Hard distinction:** observed sample maximum or high quantile of blink velocity is not a physiological upper bound. The deterministic physical EXCLUDED label is forbidden without independently defensible velocity and sensor assumptions. A future statistical product may estimate restricted-condition error/coverage only after independent participant-level calibration and external review; report participant-cluster intervals, not iid-frame confidence.

## Release blocker checklist

- [ ] External review of E002-371/E002-460/E002-461 assumptions and primary-literature priority.
- [ ] Independent reference trajectory and authenticated shutter/kernel/timebase; no synthetic substitution.
- [ ] Dynamic sensor transfer validated under unseen motion and nuisance strata.
- [ ] Independently justified closing/opening velocity limits with declared population/conditions.
- [ ] Prospective, sealed participant-disjoint hidden-closure challenge completed.
- [ ] No witnessed false exclusions under any claimed deterministic condition; otherwise claim withdrawn.
- [ ] Calibration/abstention and out-of-distribution behavior evaluated at participant/session level.
- [ ] Production threat model, tests, monitoring, documentation and external review completed.

Until these checks are independently satisfied: **E002-371 NOT PHYSICALLY VALIDATED; ABSTAIN_UNCALIBRATED for hidden closure, blink duration, PERCLOS, fatigue and medical claims.** S21/S22 remain sealed; no release or merge.
