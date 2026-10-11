# E002-106 — Onset versus time-reversed placebo (FROZEN)
Date: 2026-10-11. Classification: DISCRIMINATION. Dataset: Zenodo 18429496, original data/pft/sub1.csv, sub2.csv, sub3.csv. No participant independence beyond 3 subjects. IR wearable, not ordinary RGB.

## Primary question
Does the forward onset exponential (E002-105) outperform an equally flexible, reversed-time placebo when suppressing the spurious fitted 1-Hz component in the first approximately five seconds of off-target frequency-tagging runs?

## Extraction and analysis (fixed before any E002-106 original-data scoring)
Use the original three 4500-row CSVs, preserve original run order and 9 stimulus frequencies (1, 1.1111, 1.25, 1.4286, 1.6667, 2, 2.5, 3.3333, 5 Hz). For each 400-frame stimulus run split into four contiguous 100-frame windows. Only the first 100-frame window is the primary endpoint; no selection by outcome. Remove only non-finite and nonpositive pupil measurements; require >=80 samples. Time origin = start of each stimulus run. Fit OLS with response raw pupilSize and intercept, elapsed time, sin(2*pi*1*t), cos(2*pi*1*t). Report 1-Hz harmonic coefficient magnitude normalized by median valid pupilSize. Reference model: these 4 columns. Forward model: add exp(-t/1.5) to the four columns. Reverse-time placebo: add exp(-(T-t)/1.5), where T = time of last sample in the first window, to the same four columns. Use unregularized least squares; no tau search or post-hoc selection. All 3 models have identical sample sets. Keep all nine conditions and all subjects.

## Frozen confirmatory gate
For each subject compute median over the 8 off-target first windows of forward/reference amplitude and reverse/reference amplitude. Primary subject contrast = median(reverse/reference) - median(forward/reference). Gate passes only if >=2/3 subjects have contrast >=0.10 AND retain >=80% of 1-Hz active amplitude under forward adjustment. Otherwise FAIL. Do not relabel a failed gate. Secondary descriptive: compare active-to-max(2,5 Hz) control ratio under each model; evaluate later 100-frame windows separately. Report individual per-frequency values and any near-zero denominator issues.

## Adversarial interpretation
The reverse exponential is a mathematical placebo, not an experimentally randomized control. A positive result would support temporal asymmetry, not prove physiological versus camera/segmentation source or true waveform fidelity. A null does not kill the original frequency-tagged IR foothold. Investigate any frequency- or subject-level reversal and report condition-wise sensitivity; do not retune tau or threshold.

## Reproducibility and uncertainty
Attempt original ZIP member CRC validation, source checksum if feasible, independent numerical code and tests. Do not claim full archive validation if not done. Source is 3 subjects with correlated conditions. No population-level p-value. No RGB, no GP3 paired validation, no five-second behavioral state claims. Any results are same-data follow-up, not independent participant replication.
