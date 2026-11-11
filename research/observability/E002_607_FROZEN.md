# E002-607 | Prospective optical shutter-identifiability instrument protocol (frozen before synthetic execution)

Date: 2026-11-02. Parent E002-371, same branch and draft PR #26. This is a **hardware handoff**, not human or physical calibration evidence.

## Question
Can an independently timed, coded LED target identify the shutter start offset, exposure duration and rolling-row delay of an ordinary camera from *measured linear-light intensities*, and when must the calibration abstain? A nominal codec FPS is never a substitute for optical calibration.

## Predeclared synthetic design
- Time unit: 1 ms, with an externally authenticated 0/1 LED waveform at integer-ms bins, length >= 120 ms.
- Hypothetical global timing: frame starts at 0, 20, 40, 60, 80 ms; sensor rows indexed 0,1,2; true offset 3 ms, exposure 4 ms, row delay 2 ms per selected row step.
- Candidate offsets 0..8 ms, exposures 2..8 ms, row delays 0..4 ms (315 candidates). The measured pixel response is the *linear-light time average* of the LED waveform over each row exposure. No image-based eyelid proxy is involved.
- Freeze a deterministic pseudo-random LED code using Python random.Random(607) bits for 120 ms; hold out the last two frame starts (60,80 ms) from candidate fitting and require their independent predictions to agree.
- Fit first three frames, all three rows, by exact rational boxcar averages; a candidate survives only if every fitted sample lies within +/-0.01 of the observed value. Report the *full identified set*, never a fitted point if multiple candidates remain.
- Negative controls: constant LED must be non-identifying; an absent/unknown radiometric linearization certificate must abstain; a wrong clock origin or shifted row timing must not be silently accepted. A larger +/-0.10 intensity error budget must never yield fewer feasible candidates than +/-0.01. Missing observations must not create false identifiability.
- A candidate identified from fitting but inconsistent with the held-out frames must be rejected, not retuned.
- If the synthetic coded fixture is nonidentifying, preserve the negative result; do not change the frozen code or thresholds to manufacture uniqueness.

## Physical deployment boundary
A real run requires an independently timed LED/photodiode reference, time-stamped frame/row intensities, independently measured sensor response/black level and saturation bounds, a declared optical geometry, and a clock-offset uncertainty interval. External hardware clock uncertainty must be *added* to the identified set, never fitted away. Photodiode and image sampling must be aligned by an independently witnessed sync event. Report measured uncertainties and fail closed for auto-exposure, rolling-row ambiguity, nonlinear gamma, flicker, clipped pixels, missing frames, or invalid provenance. Never upload raw eye video to GitHub.

No claim about human closure, velocity ceilings, or camera calibration follows from the synthetic fixture. Product remains ABSTAIN_UNCALIBRATED; release BLOCKED.