# E002-117 frozen evaluation specification
Local SHA-256 of complete frozen JSON protocol before scoring: 3e87f4c202933523d7e1f8f5b6df08bf988da31dc464bcecf1cbf53c798d7289.
Local SHA-256 of executable before scoring: 77d8caf187abaa444c9b4b917efa9b82c47bb31e0fed7fafdf03b22a6fc726e3.
These hashes were saved locally before execution; GitHub publication occurs AFTER scoring, so this is NOT an external preregistration.

Synthetic design: seeds 117 (primary), 118/119 (replications); 800 paired positive/negative trials per cell; 3 s at 10 Hz and 5 s at 30 Hz; signal frequencies 0.2, 0.5, 1 Hz; proxy-noise SD / within-window signal SD 0.5 or 1.0; reference-noise ratio 0.15; common linear drift slope SD 0.8/s. Positive: shared sinusoid phase; negative: independent sinusoid phase, same frequency and common drift. Metrics raw Pearson, linearly detrended Pearson, first-difference Pearson. ROC AUC via exact Mann-Whitney comparisons.

Frozen primary gate: for 3 s/10 Hz/0.5 Hz/proxy noise ratio 1.0, detrended AUC >= 0.70 AND >=0.05 above raw AND >=0.05 above first difference.
Frozen secondary gate: for 3 s/10 Hz/0.2 Hz/noise ratio 1.0, positive-class median first-difference r < 0.20 AND raw r > 0.35.
Do not modify gates post-hoc. Synthetic-only; no human validation.
