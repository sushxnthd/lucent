# Product decision

**REJECT:** Uncalibrated rapid pupil-waveform reconstruction and five-second fatigue-state certification.

**INVESTIGATE, NOT RELEASE:** An independently calibrated nuisance-quotient pupil/iris feature with a positive worst-case separation margin, valid local linearization and held-out coverage.

**CALIBRATE:** gaze, aperture, iris scale, global/local illumination, pupil-specific optical magnification, exposure/clock, glasses and missingness. Training calibration cannot reuse final holdout.

**ABSTAIN:** zero invariant distance, unbounded pupil-specific optics, failed nuisance residual, unknown timebase or insufficient reference.

**REDESIGN:** If no pupil-specific optical bound can be established, prioritize reference-validated geometric blink events and avoid inferring five-second fatigue from blink count.