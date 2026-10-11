# E002-094 | Frozen P_33 direct RGB/reference pilot (development-only)

Lock date: 2026-10-11 UTC. This file is committed before evaluating any RGB-candidate/reference correlation in this experiment. Previous P_33 reference-only and whole-frame photometric correlations were already inspected; **P_33 is not an untouched participant**. P_01/P_02/P_07 remain unopened prospective waveform holdouts.

Source: Brown Eye of the Typer (ETRA 2018), publicly released original archive, GPLv3. Use HTTP byte ranges to reconstruct only the P_33 initial dot-test video, browser event JSON, and raw Tobii P_33.txt. Verify archive ZIP CRC via ZIP extraction. No participant imagery or full raw archive is committed.

Video: `1492456607850_3_-study-dot_test.webm`. Browser video-start epoch is taken from event `1492456607850_3_/study/dot_test` with `event="video started"`, NOT inferred from tracker outcome. Nominal frames at 5.25,5.75,...,19.75 s from video start (30 points). Use Wolfram VideoExtractFrames; requested presentation time is an approximation to camera exposure time.

Reference: raw Tobii `true_time`, valid pupil diameters >0, nearest valid reference to (browser-start epoch/1000 + requested video time), max 75 ms separation; average two eyes when both valid, otherwise one. No lag optimization. Report matches, actual time separation, reference amplitude, and valid-eye count.

RGB geometry candidate: for each frame compute left/right six-point eyelid landmarks using Wolfram FacialFeatures. Eye width = Euclidean horizontal corner separation; aperture = vertical landmark spread. Grayscale profile = mean over three rows around eye-landmark centroid between outer corners, smoothed by three-pixel moving average. Threshold = q15 + 0.50(q85-q15). Candidate dark-core span = longest contiguous below-threshold run with midpoint in central 70% of eye, excluding border-touching runs. Normalize span by eye width. No use of tracker labels to fit geometry or thresholds. This is an **unverified dark-core proxy, not validated anatomical pupil diameter**. No learned-mm PupilSense estimates.

Baselines: whole-frame mean luminance; central eye profile mean luminance; eyelid aperture/width. Evaluate each separately against reference, with same matched times. Primary diagnostics: Pearson r of RGB core-span ratio vs reference level and first differences, each eye separately; cross-eye correlation; normalized RMSE after train-only affine calibration not applicable in this pilot. Report candidate validity coverage and sign stability. No tuning after observing correlations.

Predeclared exploratory foothold gate: at least 20 valid matches per eye; same-sign candidate level r >= +0.50 in both eyes; candidate |r| exceeds whole-frame luminance |r| by >=0.15 in both eyes; zero-lag |r| exceeds median |r| at +/-1s. Failure is preserved. Even a gate pass cannot be described as physiological pupil-waveform fidelity until manual/independent anatomical segmentation verifies boundaries.

Anomaly mining after frozen outcome: threshold q15+{0.35,0.65}(q85-q15), segmentation failure by eye, gaze, aperture, photometric startup, and time shifts. Mark all posthoc. Next discriminating experiment: original human RGB iris/pupil mask validation on development images, then untouched participant-held-out waveform evaluation.

Classification: DISCRIMINATION / CAPABILITY-BUILDING. Negative outcomes cannot be retuned to pass. APST-5 fatigue/sleepiness/alertness inference is outside this dataset's labels.
