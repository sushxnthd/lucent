# E002-103 — Frozen five-second offset-harmonic leakage protocol
Date 2026-10-11. This analysis is conditional on E002-099/102 already-observed anomalies, NOT an independent preregistered discovery.

**Hypothesis:** smooth nonperiodic stimulus-offset transients leak into five-second 1-Hz harmonic estimates even after linear detrending. Quadratic detrending will suppress the immediate post-1-Hz baseline anomaly more strongly than the active 1-Hz signal.

**Original data:** Zenodo 18429496 data.zip members data/pft/sub1.csv, sub2.csv, sub3.csv. Verify each member CRC. Split each contiguous 400-frame 1-Hz run into four nonoverlapping 100-frame windows; use all nine 100-frame no-stimulus runs. Retain finite timestamp and pupilSize>0, at least 80 observations/window. Use real timestamps, no resampling. Normalize amplitudes by window median pupilSize.

**Linear model L:** OLS on [1,t,sin(2πt),cos(2πt)].
**Quadratic model Q:** OLS on [1,t,t²,sin(2πt),cos(2πt)].
Amplitude A=sqrt(beta_sin²+beta_cos²)/median(pupilSize). Score A_Q/A_L for every window.

**Frozen PASS gate (both required):**
1. For each eligible immediate post-1-Hz baseline in Sub1 and Sub2, A_Q/A_L <=0.50.
2. For each of Sub1, Sub2, Sub3, median A_Q/A_L over its four active 1-Hz windows >=0.80.
Do not retune after outcome. Sub3 is known to have no post-1-Hz baseline.

**Adversarial checks:** all nine baseline windows per person, off-frequency 0.7 and 1.3-Hz fits, RSS ratios (never infer signal quality from RSS alone), sampling span, matrix condition numbers, and synthetic 1-Hz sine vs quadratic-transient negative controls. Anomaly-mine any failure, preserve E002-099/102 results.

**Scope:** Original human IR wearable pupil-area data only. No ordinary phone RGB, independent tracker reference, five-second fatigue/sleepiness state validity, novel physiology, or population generalization.
