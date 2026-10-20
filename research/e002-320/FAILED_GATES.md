# Preserved failed gates

- Human paired RGB/high-speed validation: NOT RUN.
- RGB-to-closure inversion and deterministic error bound η: NOT CALIBRATED.
- Camera exposure timestamps, rolling-shutter readout, ISP, gaze and glasses residuals: NOT CALIBRATED.
- Geometry-only control: FAIL under unbounded gaze/head nuisance.
- Brightness-only control: FAIL under unbounded photometric nuisance.
- Missingness-only control: FAIL; dropped frame creates 56.667ms blind gap hiding a 40ms plateau.
- Temporal smoothness-only control: FAIL; smooth blink-like events can be invisible in gaps.
- Generic blink-event detection: REJECTED; theorem requires a lower-envelope plateau.
- PERCLOS and five-second fatigue certification: REJECTED.
- Field-level publication novelty: NOT ESTABLISHED; classical sampling theory.
- Remote GitHub Actions CI: UNVERIFIED. Local independent checker passed.