# Frozen prospective human test — no outcomes accessed

Before outcomes: select RGB + independently captured high-rate pupil diameter and/or eyelid aperture; verify synchronization and timestamp jitter; freeze participant grouping, leave-device-out final holdout, lighting/gaze/glasses strata and feature normalization from training participants only.

Predeclare: predicted boundary crossing for an unseen participant/device/lighting regime; report calibration of N and eta, residual coverage, false-certification rate, abstention rate, physiological error and accepted-window fraction. Missing/occluded frames must remain missing; do not interpolate them into physiological observations.

Strong controls: geometry-only, brightness-only, missingness-only, temporal-smoothness-only, iris-normalized pupil ratio, and nuisance-quotient certificate. A learned model is secondary. Do not tune on the final holdout.

Failure: any nuisance-only positive certificate; true above-margin event observationally ambiguous; unbounded held-out nuisance residual; wrong prospective boundary crossing. Preserve failures and re-freeze before new testing.

Data-path attempts this run: (1) mEBAL2 requires signed access; (2) AFFEC access failed and raw RGB not established. Pivoted to exact theory after two blocked paths. No human performance numbers.