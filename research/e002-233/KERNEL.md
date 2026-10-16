# E002-233 | Original-human contrast-margin audit (development only)

Active signal/reference: calibrated ordinary-RGB pupil-to-iris temporal waveform versus native-time same-eye Tobii pupil diameter. Primary scalar: held-out participant-bootstrap lower Pearson r with separate lag, amplitude, NRMSE and nuisance gates. Strongest confound: iris texture/gaze/lighting and uncalibrated camera exposure time. Decisive falsification: untouched synchronized waveform failing frozen gates. Publication: >=8 untouched participants plus device, lighting, glasses holdouts, independent checker and mechanism prediction. Product: >=75% prospective windows accepted with calibrated rejection. Kill: two blocked dataset attempts switch path; three nondiscriminating primary runs reformulate.

This run reuses development-only 120 RGB eye-frame measurements from E002-225/232. It does not estimate pupil diameter, certify exposure clocks, or claim physiological waveform agreement.

SCIENCE: In all four 30-frame eye/participant strata, zero center-minus-ring contrast measurements exceed twice the iris-ring MAD. Only 8/120 exceed one MAD. Ring MAD is a texture proxy, NOT measurement error or physiological signal-to-noise ratio. Opposite-eye contrast correlation differs sharply across the two development participants (P_33 r=-0.291839; P_54 r=+0.820319). This does not establish whether physiology, geometry, or photometry caused the difference.

PRODUCT: Do not promote center-minus-ring contrast or an opposite-eye common-mode correction as a calibrated pupil-diameter observable. Direct pupil boundary extraction and independently calibrated time mapping remain required.

Repository status: analysis and checker executed locally; workflow write was blocked by tool safety checks. Evidence package retained outside repository. No human-waveform gate was executed.