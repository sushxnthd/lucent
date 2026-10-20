# Lucent product decisions

ALLOW ONLY CONDITIONALLY: interval-valued calibrated shutter-mean normalized eyelid closure and raw threshold occupancy with actual exposure metadata, independently validated error envelope and missing-time bounds. Abstain on broad intervals.

REJECT: nominal-FPS blink count/timing, unrestricted eyelid velocity, uncalibrated pupil waveforms, uncalibrated PERCLOS, five-second fatigue diagnosis, clinical or safety-critical use.

REDESIGN: record true exposure start/end times and rolling-shutter offsets, temporal duty, maximum blind gap, dropped frames and calibrated η. Certify a closure plateau only when d>G+4ηE/a and the rectangular lower-envelope assumption has been verified; otherwise abstain.

NEXT: human synchronized RGB/reference holdout crossing, not another metadata-only audit.