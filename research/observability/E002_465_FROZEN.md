# E002-465 — preregistered shutter-identifiability challenge (2026-10-26)

**Status:** frozen before implementation. **Tier:** synthetic optical-instrument identifiability only; no hardware or human measurements. **Question:** Can a photodiode recording an LED command and a common trigger authenticate the *camera's actual sensor exposure support*? **Prediction: no.**

## Counterexample and falsification

Construct two uniform global-shutter worlds with identical trigger times, constant scene brightness, and identical photodiode/LED traces, but with camera exposure windows A=[0.00,0.40] ms and B=[0.20,0.60] ms for frame 0; frame 1 uses A=[2.00,2.40] and B=[2.20,2.60] ms. Both return the same constant-frame intensity. A true threshold crossing at t=0.50 ms is strictly inside A's dark gap (0.40,2.00), but *inside B's first exposure*. Thus trigger+photodiode+constant frames do not determine the sensor's shutter-dark gap. This corrects any physical-study language implying that an illumination photodiode alone measures shutter opening/closing.

**Intervention:** an independently timestamped, narrow, scanned optical test pulse must be observed through the *camera's own imaging path*. For an ideal linear uniform shutter, pulse width p=0.10 ms, phase step h=0.05 ms, noiseless measurements and known relative pulse timing, integrated frame response is the pulse/exposure overlap divided by exposure duration. The onset of nonzero response occurs at phase a-p; its disappearance occurs at phase b, for shutter [a,b]. Bracket both transitions with positive and zero responses, recovering intervals for a and b with grid-width uncertainty, without using the trigger as a shutter proxy. The A/B shutter worlds must be distinguishable by the scanned pulse response.

## Preregistered decisions

1. Metadata/trigger/photodiode-only: `SHUTTER_UNIDENTIFIED`, regardless of matching frame brightness.
2. Ideal noiseless phase scan with positive and zero transition brackets: `SHUTTER_SUPPORT_BOUNDED_SYNTHETIC`, and both true endpoints must lie inside the returned brackets.
3. Incomplete phase coverage, zero exposure duration, unknown pulse width, nonlinearity, rolling-shutter row, autoexposure, clipping, pulse-clock uncertainty without certified bounds, noise that can hide arbitrarily small overlap, or unbounded response tails: `ABSTAIN_SHUTTER_UNCALIBRATED`. No promotion to physical evidence.
4. In a physical trial, independently calibrate optical pulse timing and radiometry, per-row exposure/rolling behavior, camera gain linearity, sensor lag, pulse tails and detection sensitivity. Repeat with unseen pulse phases, gains, frame intervals and lighting. Externally escrow calibration before opening holdout traces. Retain failed and inconclusive trials.
5. **No physical-release path:** all output must keep `physical_release_authorized=false`, `ABSTAIN_UNCALIBRATED`. The E002-371 physiological cap and prospective anatomical tests remain separate, unvalidated prerequisites.

## Scientific status

This is an elementary nonidentifiability counterexample and an executable acquisition-design consequence, **not** a new general theorem, physiological observation, or validation of a physical camera. It is deliberately one decisive instrument challenge rather than another large synthetic sweep. If physical equipment is unavailable, ship a runnable acquisition protocol and refuse to invent measurements. Preserve Lucent PR #26 and Hush PR #45 independently.
