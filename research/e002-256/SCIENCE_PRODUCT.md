# E002-256 — Two ledgers

## SCIENCE — what is true?
Source: CondadosAI/pupil-diameter-webcam, pinned commit aa9bddf498a3b6e4104c2c000d2cc0c06a816aae, 51 participant summaries/eye from the released EyeDentify/PupilSense checkpoint. Unknown training overlap; not Lucent's detector.

- Left: pooled r 0.875523, participant-centered r **0.705074**; between-person mean differences account for **78.1319% of pooled covariance**.
- Right: pooled r 0.858658, participant-centered r **0.673715**; between-person mean differences account for **82.9032% of pooled covariance**.
- Between-person fractions of predictor variance: 75.8445% left, 82.5314% right; reference variance: 69.4739% left, 72.8193% right.
- Reconstructed pooled r and reference SD match upstream published summary to floating-point precision.
- This is a decomposition of covariance, NOT r or R². Between-person differences may be real physiology. Centered r pools across sessions/lighting conditions and does NOT establish within-session or five-second dynamics.
- Exact covariance decomposition is prior mathematical knowledge. No general RGB impossibility or novel theorem established.

## PRODUCT — what changes?
- **Reject** pooled pupil regression r as a rapid temporal measurement certificate. Most pooled covariance here is explained by participant-level means, not within-person co-fluctuation.
- **Require** within-session, nuisance-matched, exposure-synchronized human waveform comparison with brightness/geometry placebos, nondegeneracy, device/glasses holdouts and calibrated abstention.
- **Retain** dimensionless pupil/iris dynamics only as an unproven candidate; no 5-second fatigue inference.
- **Next high-information action:** raw synchronized RGB+tracker recordings, rather than further summary-level decomposition or unsynchronized EOTT timing heuristics.

Smallest supported claim: In this published third-party model/dataset, approximately four-fifths of pooled RGB prediction/reference covariance is between-participant, limiting the interpretation of pooled r for rapid physiological waveform measurement.
