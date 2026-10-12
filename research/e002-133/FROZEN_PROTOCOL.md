# E002-133 prospective protocol, 2026-10-12

Participants 47,48,49; EyeDentify CC BY-NC 4.0; sessions 1,11,21,31. Use all positive numeric bilateral Tobii pupil rows from session_data.csv. No replacement, lag search or filtering. Evaluate signed Pearson r of adjacent first differences for left vs right pupil; report raw and detrended correlations, counts and variance. Sessions valid if >=24 paired samples.

G0: >=2 participants have all 4 sessions valid. G1: r11>r21 for >=2/3 participants. G2: median(r11-r21)>=0.25. G3: r11>r1 and r11>r31 for >=2/3. G4: median r11>=0.50. If G0 fails, other gates descriptive only. These thresholds are frozen before examining participants 47-49. Motivation: E002-132 exploratory session 11 anomaly in participants 44-46. No five-second RGB or fatigue validity claim. Competing causes: amplitude, trial-specific stimulus, timebase, tracker noise, missingness and physiology.
