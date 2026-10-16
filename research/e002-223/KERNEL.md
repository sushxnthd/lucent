# E002-223: Clock-offset identifiability

Active question: Can a five-second RGB pupil waveform be compared to same-eye Tobii diameter with certified absolute lag when the camera exposure offset is unknown?

Signal/reference: dimensionless pupil-to-iris ratio and native tracker diameter. Frontier: original paired EOTT sources exist, but independent exposure-clock calibration is absent.

Metric: held-out lower Pearson confidence bound with separately frozen lag, amplitude, NRMSE and nuisance controls.

Confound: unknown camera time offset versus actual physiological response delay.

Falsification: independent camera-exposure anchor would remove the clock gauge. Without one, the two delays are nonidentifiable.

Publishable threshold: eight untouched participants, independent checker, holdouts and prior-art audit. Product threshold: at least 75% accepted windows. Kill: switch after two access failures; reformulate after three nondiscriminating runs.

SCIENCE: Unknown clock offset and physical lag are confounded in the observation model.
PRODUCT: Abstain from absolute physiological lag; retain within-camera intervals subject to relative-timing quality.
