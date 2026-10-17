# E002-252: frozen holdout

Question: Does E002-234 radial-edge endpoint saturation replicate on P_01, P_02, P_07?

Frozen rule (E002-247): at least two participants each have >=5 accepted eye-frames and >=50% of accepted radii equal 0.20 or 0.78. Same detector; no threshold tuning.

SCIENCE: This tests a detector-specific failure, not pupil accuracy or physiological waveform agreement. Strongest confound: iris texture, illumination and gaze projection.

PRODUCT: Keep quantitative pupil measurement uncertified; a positive replication reinforces retirement. A negative replication does not prove accuracy.

Main signal/reference: normalized RGB pupil radius vs synchronized same-eye Tobii diameter. Main scalar: held-out participant-bootstrap Pearson lower bound, with lag, amplitude, NRMSE, nuisance and coverage gates. Human waveform remains untested.

Decisive falsification: fewer than two participants satisfy frozen replication. Publishable main threshold: >=8 untouched synchronized participants with independent checker and holdouts. Product threshold: >=75% accurate admitted windows. Kill: three nondiscriminating runs. No fatigue claim.
