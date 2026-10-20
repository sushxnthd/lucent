# E002-313 failed gates and negative controls

HUMAN_REFERENCE: NOT_RUN.
GAIN_RATIO: NOT_CALIBRATED on any real RGB camera. r=.5 is illustrative.
FULL_IMAGE_INVERSION: NOT_CALIBRATED on real blur/compression/glasses.
GAZE_GEOMETRY: NOT_CALIBRATED; unknown time-varying gaze mimics eyelid edge.
MISSINGNESS: FAIL_CLOSED; removing half the spatial support invalidates naive full-image certification.
SMOOTHNESS: FAIL_AS_POINT_IDENTIFIER; two smooth trajectories have identical complete images and mean values 4/9 vs 5/9.
FIELD_NOVELTY: NOT_CLEARED; expectiles and motion blur have substantial precedent.
HUMAN_HOLDOUT_PREDICTION: NOT_FROZEN; only synthetic prediction exists.
CI: remote check pending.
PRODUCT: reject point subframe blink timing, uncalibrated pupil waveform and five-second fatigue diagnosis.
