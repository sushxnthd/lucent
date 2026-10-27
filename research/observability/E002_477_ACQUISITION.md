# E002-477 — physical optical intake contract and operator procedure

This is an acquisition interface, **not** a calibration certificate. No participant data or raw eye images belong in the repository. Use the [E002-472 physical handoff](E002_472_PHYSICAL_HANDOFF.md) for external metrological requirements and the [E002-466 detector dead-zone finding](E002_466_RESULT.md) before interpreting phase-scan signals.

## Files kept locally (never commit physical raw videos by default)

1. `manifest.json`: JSON object with `schema: lucent-e002-477-optical-intake-v1`, `frame_period_ms`, `phase_step_ms` (<=0.05), `scan_periods` (>=2), `repeats_per_phase` (>=20), `row_strata` (at least two named rows), `pulse_width_ms`, `pulse_width_tolerance_ms` (<=0.01), `clock_error_bound_ms` (<phase step), `expected_gain`, `camera_gain_locked: true`, `clock_source_type: independent_photodiode_logic_analyzer`, distinct `camera_device_id` and `clock_device_id`, and SHA256 hex digests for the three source files below.
2. `camera.csv`: exactly `row_stratum,phase_index,repeat_index,response,dark_reference,gain,saturated,dropped`. The response is an unsaturated raw linear-signal ROI aggregate for the specified row, with an independently acquired dark reference in the **same units**. Preserve RAW frames and ROI code separately. `saturated` and `dropped` are `0` or `1`.
3. `clock.csv`: exactly `row_stratum,phase_index,repeat_index,pulse_start_ms,pulse_end_ms`. These are independently logged optical pulse-edge times **relative to the externally authenticated frame-period phase origin**, not camera PTS, a software timer, or a commanded LED delay. Preserve the logic-analyzer/photodiode trace and clock mapping outside this compact CSV for review.
4. `raw_video_bundle`: original binary frames or archive; must be nonempty and match `raw_video_sha256`. Hashes detect accidental substitution, not fabrication or true timing independence.

All rows require one paired camera and clock record for every phase/repeat/row key. A 240-fps, 0.05-ms, two-period, 20-repeat, two-row pilot requires **6,720 paired observations**. The 0.05-ms grid and >=20 repeats are protocol targets, not proven sufficient to resolve physical shutter tails.

Run from the repository root:

```bash
python research/observability/e002_477_optical_intake.py manifest.json camera.csv clock.csv raw_video_bundle
```

Exit code 0 means **intake QA only**; exit code 2 means rejected. Neither exit code authorizes physical claims. The JSON output deliberately never contains raw data or participant identifiers. The source filenames are not embedded in the output.

## Independent reviewer gate after a passed intake

- Authenticate that the photodiode and logic analyzer really recorded emitted optical pulses, that the camera and clock devices are distinct, and that frame-phase origin, jitter, drift and pulse response are bounded by independent measurement. Declared device IDs and SHA hashes alone are insufficient.
- Examine RAW imaging-path response across phase, illumination intensity, dark/flat noise, gain linearity, clipping, optical memory/tails, rolling-row differences and any missed/duplicated frames. A thresholded nondetection is **not zero exposure**.
- Freeze a second held-out optical session with unseen phase offsets, brightness and row conditions before opening it. Predict the response and shutter-support uncertainty from calibration only. Publish all failures and abstentions, not only accepted windows.
- Obtain a separately calibrated encoder/moving-aperture positive witness. Then, with consent/approval and privacy controls, obtain blinded human reference trajectories, split by participant. Do not derive a universal hard velocity limit from the largest observed sample speed.

If any of these independent physical gates is unavailable, label the result `INTAKE_ONLY_NOT_PHYSICALLY_VALIDATED` and keep every product output `ABSTAIN_UNCALIBRATED`.


## E002-480 mandatory phase-coverage and detector-sensitivity amendment (2026-10-27)

The [frozen adversarial phase-dither experiment](E002_480_RESULT.md) shows that merely adding nominal phase offsets is insufficient for deterministic optical coverage when each pulse has an independently uncertain start. **This is a synthetic worst-case design result, not measured jitter.**

Before a reviewer may assert a physical shutter-support envelope, require the independent clock to provide per-pulse measured start/end times and a defensible error model. For reported pulse start `m`, pulse width `w`, and independent start uncertainty `±u`, the guaranteed illuminated core is `[m+u,m+w-u]` only if `w>2u`. Otherwise it is empty. Compute the union of these cores *from authenticated measured pulse times*, separately for each sensor row, exposure mode, and frame attribution. Record uncovered phases and **abstain** if any phase needed for the intended exclusion is not guaranteed sampled. If errors are common-mode or correlated, document and independently verify that model instead of silently applying the independent-jitter counterexample.

**Coverage is not detection.** Independently calibrate the camera/detector response, dark noise, gain, linearity, pulse width, optical tails, brightness drift, blur, missing frames and threshold sensitivity. A geometric hit can produce an undetectably small response. Report a threshold-dependent upper response envelope and a minimum detectable signal class, not exact zero. Do not infer a physiological hard speed cap from human sample maxima. `PASS_INTAKE_ONLY` and `GEOMETRY_COVERAGE_ONLY` never authorize hidden-closure, blink duration, PERCLOS, fatigue, or medical outputs; preserve `ABSTAIN_UNCALIBRATED` until independent physical and anatomical validation passes.
