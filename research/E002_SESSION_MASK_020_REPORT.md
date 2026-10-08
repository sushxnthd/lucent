# E002-020 — Session-shared missingness under nonperiodic dropout (2026-10-08)

**Classification:** DISCRIMINATION / CAPABILITY-BUILDING. **Data:** synthetic waveforms only. No human, phone, tracker, pupil-reference or state measurements. Source: `experiments/e002_session_mask_020.py`; NumPy only, seed 20261008, 500 draws/cell.

## Hypothesis and prediction
Identical latent A/B pupil waveforms can produce O4 between/within RMSE >1.25 after interpolation if missingness patterns are shared within a condition/session and differ across conditions. Independent replicate masks at the same dropout rate should reduce this artifact. The provisional E002-018 temporal-support veto (maximum gap <=0.2 s, supported grid >=80%) may still pass.

## Results (conditional on all six traces passing support veto)

| Dropout | Session-shared false passes | Independent-mask false passes | Session median O4 | Independent median O4 |
|---|---:|---:|---:|---:|
| 5% | 483/499 (96.8%) | 5/500 (1.0%) | 1.864 | 0.919 |
| 10% | 490/490 (100%) | 8/477 (1.7%) | 2.879 | 0.958 |
| 20% | 387/387 (100%) | 12/259 (4.6%) | 5.102 | 1.002 |

Synthetic frequencies only; **not** estimates of real-world false-positive rates. Approximate 95% Wilson intervals for the 5% shared case: 94.9–98.0%; 10% shared: 99.2–100%; 10% independent: 0.9–3.3%. These intervals exclude model misspecification.

**Exact small-sample diagnostic:** E002-019 periodic O4=3.693 gives unpaired exact permutation p=0.10 (2/20 assignments) and paired exact p=0.25 (2/8 flips). With 3+3 observations, a two-sided symmetric exact unpaired test cannot attain p<0.10; with three matched pairs the corresponding bound is p>=0.25. Condition-dependent masks violate exchangeability, so these p-values are diagnostics, not valid physiological inference. The constructed periodic missingness alone predicts condition 6/6 times.

**Independent implementation and boundary:** A separately implemented pairwise-distance O4 with independent random seed 81731 reproduced 491/491 false passes for 10% shared dropout at original replicate variation (median O4=2.914). Increasing replicate variation 10x or 100x reduced this to 0/494 and 0/491 (median O4 1.012 and 0.998). This is a conditional failure mode, not an inevitable outcome.

## Discovery Protocol V2

- **KNOWN:** Session-shared nonperiodic missingness can create a false O4 pass with identical physiology, even after the provisional support veto.
- **BELIEVED:** Acquisition-process correlations at the session/condition level are more informative than missing fraction alone.
- **CONFLICTING:** Greater within-condition variation eliminates the false pass in this constructed regime.
- **FALSIFIED:** The E002-019 artifact requires periodic missingness; the E002-018 support check alone is sufficient.
- **ANOMALOUS:** 5% shared dropout caused 483/499 false passes, versus 5/500 with independently sampled masks.
- **UNTESTED:** Real capture prevalence, person-wise RGB/reference correspondence, active-response and behavioral-state validity.

**Residual/surprise:** Same dropout percentage but dramatically different O4 outcomes. **Competing explanations:** near-zero within-condition denominator, interpolation, session-level lighting/pose/quality; only missingness was manipulated. **Uncertainty:** fixed synthetic waveform, small 3x3 replication, conditional Monte Carlo rates. **Cheapest next experiment:** Real traces with frozen participant/session IDs; preserve original O4, add mask-only label predictability, observed fraction, max gap, common-time waveform comparison, absolute effect size, session-blocked randomization and reference fidelity. No retuning of historical gates.

**Roles:** Explorer (nonperiodic masks), Skeptic (identical latent waveforms), Experimentalist (six conditions), blinded Analyst (O4 only), Anomaly Hunter (5% boundary and noise sensitivity), Prior-Art Auditor (no novelty claim for missing-data controls), Replicator (independent distance code), Theorist (denominator and exchangeability). Cluster E002-018/019/020 as **observation-process confounding**, with the acquisition mechanism as the missing variable.

**Claim boundary:** This is a methodological negative result, not human replication, ordinary-RGB pupil-waveform observability, five-second fatigue inference or a physiological breakthrough. RGB-SCALE-OBSERVABILITY-001 remains a negative result. Raw PupilSense millimetres remain rejected.
