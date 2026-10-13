# E002-168 — Frozen conditional schema/timebase kernel

Source files were inspected before this protocol, so the experiment is a retrospective source audit, not an untouched human test.

**Active question:** Can ordinary RGB pupil/full-anatomical-iris temporal log-ratio recover valid synchronized GP3 HD LPMM/RPMM (mm) waveforms in five-second windows with participant/device/lighting/glasses holdout?

- **Exact pair:** RGB log(pupil/iris) waveform vs GP3 HD valid pupil-mm waveform with original TIME and FLIR frame timestamps.
- **Frontier:** E002-167 identified TCP fragmentation vulnerability; no qualifying human waveform. RGBE-Gaze uses industrial FLIR RGB, not a phone.
- **Scalar metric:** held-out Pearson r, with frozen lag/amplitude/NRMSE/coverage gates.
- **Confounds:** gaze, photometry, occlusion, clock alignment, and positional schema shifts.
- **Decisive falsification:** untouched human reference agreement fails vs geometry/brightness controls.
- **Publishable threshold:** >=8 unseen participants x >=3 windows; participant-bootstrap lower 95% CI r>0.30, >0.10 above nuisance-only; median |lag|<=100ms, amplitude ratio 0.5–1.5, NRMSE<=0.75, accepted coverage>=75%, independent checker and unseen-condition prediction.
- **Product threshold:** >=75% useful accepted windows with calibrated rejection, no fatigue inference before waveform validity.
- **Kill:** switch dataset after two access blocks; reformulate after repeated held-out failures; three non-discriminating runs kill/reformulate.

**Predeclared synthetic tests:** source converter + positional MATLAB mapping with counter enabled (49 fields, TIME seconds, LPMM column42, 251 unique matches), without counter (48 fields, TIME_TICK column2, LPMMV column42, illustrative 10MHz tick mismatch), necessary 49-field schema gate, independent checker.

**Post-hoc wildcard:** delete one optional middle attribute and append a spare to preserve 49 fields; test whether field count and plausible clock wrongly accept shifted pupil semantics.

No participant data, no phone claim, no five-second fatigue score.