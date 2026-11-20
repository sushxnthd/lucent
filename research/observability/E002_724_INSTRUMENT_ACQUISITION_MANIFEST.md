# E002-724 — Executable randomized acquisition manifest (instrument only)

This artifact operationalizes the frozen E002-714 physical occluder protocol. It does **not** contain physical measurements, human observations, a validated velocity ceiling, or a release authorization.

## Prospective acquisition design

Use `e002_724_acquisition_manifest.py --seed 724 --replicates 2 --output manifest.csv` before collecting data. It creates 896 randomized trials crossing nominal camera sampling rates (15, 24, 30, 60 FPS), seven predeclared nuisance conditions (baseline, dim, bright, blur, gaze, glasses, occlusion), two independent repeats and sixteen evenly spaced target occluder phases. The seed, exact schedule and file SHA-256 must be archived before acquisition. Trial order is randomized, but **physical** stimulus phase, clock timing, sensor exposure and aperture must be measured, not inferred from this schedule.

## Required independent instrumentation

Each trial must log sensor-native exposure start/end timestamps, independent occluder state/position ground truth, timestamp alignment uncertainty, reference sensor calibration, aperture-to-geometry uncertainty, image capture, dropped frames and nuisance condition. The ground truth sensor must not be the ordinary camera under test. Use a programmable physical shutter/occluder and an independently timed photodiode or encoder; nominal FPS is never a timing certificate. Before acquisition, define acceptance tolerances for reference timing and occluder-position uncertainty, and reject trials outside tolerance. Randomization does not replace independent calibration.

## Blinded analysis and falsification

Freeze predictions using lower aperture bounds, upper observation-gap bounds and independently justified upper occluder velocity bounds, before opening reference closure labels. For each trial record CERTIFIED_EXCLUSION or ABSTAIN; do not substitute an observed sampled slope for the continuous-time bound. A ground-truth closure in a certified exclusion interval is a falsification of the combined model/calibration. Report all exclusions, false exclusions, abstentions, reference-invalid cases and nuisance-stratified coverage. The physical occluder validates an instrument/model pipeline only; it does not establish human physiological velocity ceilings or authorize human blink product claims.

## Executed manifest smoke test

Local invocation with seed 724 and 2 replicates produced 896 unique trials, SHA-256 `955a5588972a8d7c2f61aa35b560193c62559aeb8bcff43448fd11e17574feb1`. This hash is specific to the local Python CSV serialization and should be verified on the actual acquisition machine. No real measurements were acquired. Product: ABSTAIN_UNCALIBRATED; release BLOCKED.
