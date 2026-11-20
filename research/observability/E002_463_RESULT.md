# E002-463 — independent encoder witness integration and physical bench handoff

> **E002-465 shutter-metrology correction (2026-10-26):** An LED photodiode and shared trigger authenticate the *illumination pulse and trigger*, **not** the camera sensor's exposure window. Actual imaging-path shutter support requires independently timed optical phase scanning or an equivalently validated sensor-exposure measurement, with clock, radiometry, response tails and rolling-row uncertainty bounded. See [E002-465](E002_465_RESULT.md). Until then any inferred dark-gap crossing is shutter-unidentified and product claims abstain. Historical protocol below is retained for traceability.


**Date: 2026-10-26. Evidence tier: synthetic end-to-end instrument integration; independent arithmetic check; no physical hardware or new human labels.** [Protocol](E002_463_FROZEN.md) was committed before implementation at `c28660fdc8bfad0b749a0fe7781507c4987b4a3f`. This work is a direct enforcement consequence of E002-462, **not a new observability theorem or physiological discovery**.

## Falsifiable result and what it establishes

E002-462's nondegenerate 400-fps aperture witness (baseline 2.30 mm, minimum 1.95 mm, threshold 2.0 mm, 0.30-ms exposure) remains fully inside the ideal reference-camera dark gap. The shutter means for that trajectory and for an always-open aperture are exactly identical. An **independently timed encoder sample** at t=1.0 ms with a stipulated 0.01-mm position error and 0.02-ms clock error positively distinguishes the synthetic worlds, because 1.95+0.01 < 2.0 mm and its entire timing support is inside the dark gap.

The preregistered synthetic ordinary-camera rule uses **an intentionally false illustrative velocity cap of 100 mm/s** and 2.30-mm endpoint means separated by 2.50 ms. Its conservative E002-456 lower envelope is **2.1675 mm**, above the 2.0-mm threshold, so it declares `EXCLUDED_CONDITIONALLY`. The encoder's independent positive witness therefore yields `FALSIFIED_JOINT_ASSUMPTIONS`. The correct interpretation is **the stipulated joint speed/measurement assumptions are false for this constructed trajectory**. The mathematics is not falsified. The always-open control must yield `REFERENCE_UNRESOLVED`, never a certified negative reference.

The independent Node.js arithmetic replay was executed locally and reproduced: excursion [0.282829, 2.274505] ms within dark gap (0.15,2.35) ms, subthreshold duration **0.370239 ms**, and lower envelope **2.1675 mm**. It separately checked timing-boundary equality, encoder sample support and the no-negative-label rule. This is an independent *synthetic arithmetic check*, not a hosted Python pass or physical experiment.

## Executable enforcement

- [Encoder-positive adapter](e002_463_encoder_reference.py) accepts a private E002-456 case and a separately declared encoder record with source SHA256, position/time/bandwidth calibration identifiers, units, bounded timing support and monotone quality-passed samples.
- It admits only robustly interior **positive** anatomical crossing witnesses, feeds them to the existing E002-456 evaluator, and returns no raw positions, timestamps, source identifiers or participant IDs. Above-threshold samples and missing observations never become OPEN ground truth.
- [18 adversarial tests](test_e002_463_encoder_reference.py) cover the frozen positive/negative worlds, exposure overlap, exact timing boundary, encoder integration support, clock error, missing calibration/source hash, duplicate times, nonfinite data, quality failures, participant privacy and nuisance abstention.
- [Independent JavaScript replay](e002_463_independent_replay.cjs) shares no Python implementation. [CI workflow](../../.github/workflows/e002_463_encoder_reference.yml) checks the Python suite, independent replay and frozen output. **Hosted CI result was queued at report writing; do not claim the 18 Python tests passed until its completion is checked.**
- Calibration IDs and SHA256 values are **declarations**. This code does not verify hardware, clock trace, physical independence, consent or external timestamp escrow. It always returns `physical_release_authorized=false` and `ABSTAIN_UNCALIBRATED`.

## Physical bench protocol — concrete next acquisition, not yet executed

1. **Independent reference:** Borrow a linear motion stage/slit phantom with a separately logged analog position encoder or displacement sensor. Independently calibrate physical position in mm across 1.8–2.5 mm, dynamic bandwidth/lag, uncertainty, and clock using a second timing instrument. Do not call stage commands or camera pixels the ground truth. Record continuous analog trace or sufficiently sampled trace with a separately justified acceleration/bandwidth envelope; sample maxima alone are not a hard motion bound.
2. **Clock and shutter:** Use a photodiode and shared hardware trigger to record actual optical pulse edges and per-camera exposure supports. Acquire at 400 and 1000 fps with measured 0.30-ms nominal shutter targets and at ordinary-camera rates 30, 60 and 240 fps when available. Record exposure-kernel uncertainty, rolling rows, dropped frames and sync residual. Camera metadata and encoded PTS are not authenticated exposure timing.
3. **Blinded motion challenge:** Freeze speed-cap hypotheses, threshold, encoder uncertainty, aperture calibration and ordinary-camera predictions on a development motion set. Hold out unseen motion waveforms, phases, lighting and camera settings. Include a constant-open control, finite-duration crossings strictly inside reference-camera dark gaps, near-threshold noncrossings and false-speed-cap intervention. Externally timestamp the frozen manifest before opening encoder traces.
4. **Nuisance strata:** Vary geometry/rotation, brightness/autoexposure, missing frames, blur/focus, gaze-like orientation, glasses/reflections, shutter phase and clock offset independently. Any unbounded nuisance must abstain. Publish every condition's coverage, witnessed falsifications and unresolved intervals; do not aggregate away failures.
5. **Human follow-up:** Only after the phantom study, obtain consented high-speed anatomical eyelid-margin recordings with independently measured eye-plane geometry, two blinded raters and participant-disjoint calibration/holdout. The high-speed camera can positively witness crossings, but cannot certify negative intervals without independent completeness bounds. No claim of universal physiological maximum may be based on observed sample maxima.

**Stop rule:** One authenticated interior crossing in an interval classified as excluded kills that restricted joint measurement/cap claim. Zero crossings or no encoder witness does not certify absence. External metrology review and genuinely independent human evidence are mandatory before product promotion.

## Priority, safety and persistence

E002-430/447/462 already establish reference-camera incompleteness. E002-456 already provides the sealed prediction mechanism. **E002-463 adds only the executable independent-encoder positive-witness adapter and an end-to-end synthetic falsification of a deliberately false cap.** It is a concrete hardware handoff, not a scientific breakthrough.

E002-371 **remains physically unvalidated**. No hidden-closure guarantee, blink duration, PERCLOS, fatigue or medical claim is authorized. Product: `ABSTAIN_UNCALIBRATED`. S21/S22 sealed. Hush branch/PR #45 untouched. Lucent PR #26 stays draft/unmerged.
