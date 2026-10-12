# E002-132 — Bilateral Tobii reference reliability audit (frozen pre-outcome)
Date: 2026-10-12. Classification: DISCRIMINATION / CAPABILITY-BUILDING.

## Question
Are within-recording left-pupil dynamics in the public EyeDentify reference reproducible in the simultaneously measured right pupil? The answer determines whether strict first-difference RGB-versus-left-Tobii waveform gates are interpretable on short windows.

## Dataset and fixed selection
EyeDentify CC BY-NC 4.0. Participants 44, 45, 46; sessions 1, 11, 21, 31, 41, 50 (18 participant-sessions). Select the CSV at `eyedentify/eyedentify/left_eyes/{participant}/{session}/session_data.csv` through the public Kaggle per-file endpoint. These participants were not in E002-130/131. Do not replace missing/incomplete sessions or change the six IDs. Use the complete row sequence, columns `left_pupil` and `right_pupil`, drop only rows where either is nonnumeric or nonpositive. This is tracker-to-tracker agreement, not a test of RGB measurements or APST-5 state.

## Predefined outcomes
For sessions with >=24 paired finite samples, compute Pearson r(L,R), r(detrend(L),detrend(R)) with linear detrending against sequential row index, and r(diff(L),diff(R)) using only consecutive surviving original row indices. Record n, within-session SDs, and fraction of nonconsecutive gaps. Summarize each metric by participant median, then the median of the three participant medians (equal participant weighting). No lag search, filtering, parameter fitting, outcome-based exclusion, or cross-session waveform stitching.

For secondary reliability diagnostics, compute per-session SD of common mode (L+R)/2 and differential mode (L-R)/2 after linear detrending. These are descriptive proxies only, not calibrated noise or physiological SNR. Compare across-session variation of medians to within-session SD without making causal claims.

## Frozen gates
G0: >=12 of 18 sessions have >=24 valid bilateral samples AND every participant contributes >=3 valid sessions.
G1: median of participant-median raw bilateral correlations >=0.60.
G2: median of participant-median detrended bilateral correlations >=0.50.
G3: median of participant-median consecutive first-difference bilateral correlations >=0.30.
G4: five-second active RGB measurement or sleepiness validity NOT EVALUABLE.
If G0 fails, G1-G3 are descriptive only. The 0.30 first-difference threshold is a diagnostic target, not a medical validity criterion.

## Interpretation and anomaly mining
High raw correlation with poor first-difference agreement would indicate that rapid reference changes are less reproducible across eyes than slower variation in these recordings; it would weaken use of single-eye first-difference RGB/reference agreement as a standalone hard gate, without establishing why (eye-specific physiology, gaze, missingness, sensor noise, stimulus or filtering). Conversely, high bilateral first-difference agreement would strengthen the tracker reference and point back toward RGB observability failures. Inspect sign reversals, participant/session effects, missingness, common/differential variance, and apparent sampling gaps. Preserve the original negative RGB results regardless.

## Boundaries
Original human reference signals only, 3-second fixed-color sessions; not a new 5-second active-stimulus dataset, not participant/device transfer, not independent physiological validation, not a novel pupillometry method, and not a fatigue detector. No threshold retuning after inspection.
