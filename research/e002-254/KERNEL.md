# E002-254 — Native reference coverage does not certify camera synchronization

Post-hoc original-human provenance audit, 2026-10-17. No new physiological waveform experiment.

Active question: Can the frozen RGB normalized pupil-radius signal be independently time-aligned to same-eye native-time Tobii diameter and survive participant/device/lighting/glasses holdout?
Signal/reference: E002-234 webcam radius ratio versus Tobii Pro X3-120 diameter, P_33/P_54 development only.
Frontier: E002-244 original-human detector failure; E002-221 native reference is available, but exposure-clock offset unverified.
Scalar: future held-out participant-bootstrap Pearson lower bound plus frozen lag/amplitude/NRMSE; current provenance scalar is diameter of offsets passing 75ms nearest-valid-reference coverage.
Strongest confound: camera exposure timing versus browser start-event/packet PTS, plus iris texture, gaze, autoexposure.
Decisive falsification: independently calibrated clock plus untouched human waveform fails frozen gates; or offset-proximity gate accepts knowingly shifted offsets.
Publishable: >=8 untouched humans, participant/device/lighting/glasses holdout, independent replay, mechanism-derived unseen prediction and prior-art audit.
Product: >=75% prospectively accurate admitted quantitative windows under calibrated timing and image uncertainty.
Kill: two access blocks force source switch; three nondiscriminating runs reformulate; failure of prospective waveform kills quantitative pupil claim.
Wildcard: packet PTS collision audit; no fatigue inference.

Elementary conditional law: For uniform reference-valid spacing h, all mapped video timestamps inside the reference grid have nearest reference within h/2. If tolerance tau>=h/2, reference-availability coverage cannot distinguish any such clock offset. This sampling geometry is not a novel general theorem. E002-221 real data are irregular; only the five evaluated offsets are empirically certified.

This is post-hoc; no untouched evaluation was inspected or modified.