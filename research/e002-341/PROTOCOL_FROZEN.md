# E002-341 — Prospective paired-human blink observability protocol
Frozen 2026-10-21, before any paired-human outcome inspection. No human evaluation completed.

## Question
Can native ordinary-RGB eyelid aperture detect independently measured blink events across participant, device, lighting, gaze and glasses changes, with an instrument-derived abstention boundary?

## Signal and reference
RGB feature: eyelid aperture divided by eye-corner span at native exposure timestamps. Reference: EOG-confirmed blink events, independently adjudicated without RGB. EOG may indicate blink occurrence but **does not certify full eyelid closure or peak eyelid velocity**. Those quantities require a separate calibrated high-speed eyelid reference.

## Measurement model
RGB: I_k(x) = Q_k[(1/E_k) integral over W_k of (gain_k(t) * blur_k * Render(x; pupil, iris, aperture, gaze, glasses) + offset_k(t)) dt + noise_k(x)].
EOG: z(t) = h_b * blink_event(t) + h_s * eye_rotation(t) + electrode_drift(t) + noise(t).
Clocks: t_RGB = alpha*t_EOG + beta + delta(t), with calibrated bounded delta.
Do not equate the width of an EOG transient with closure duration.

## Falsification and controls
Participant-disjoint training/calibration/test, camera-model holdout when available, glasses and lighting strata, no outcome-dependent exclusions. Baselines: geometry-only, brightness-only, missingness-only and temporal smoothness-only. Evaluate event recall at fixed <=1 false alarm/minute, onset error intervals and abstention. If clock or exposure metadata are missing, do not issue sharp temporal certificates.

## Predeclared boundary
For an independently verified eyelid closure duration D (NOT an EOG event duration), exposure windows W_i, contrast a_i, bounded feature error eta_i:
M(D) = min_onset max_i (a_i * overlap(W_i, event) / E_i - 2*eta_i).
Under the restricted rectangular-closure scalar measurement model, guaranteed event/no-event distinguishability iff M(D)>0. This is inherited from E002-338, not a new discovery. Freeze one predicted holdout crossing before final evaluation.

## Publication and product gates
Publish only after synchronized independent human validation, calibrated nuisance bounds, untouched predicted boundary crossing, independent checker and primary prior-art differentiation. Allow research-only blink occurrence with abstention. Reject five-second fatigue certification, uncalibrated rapid pupil-waveform recovery and 10-Hz blink completeness.
