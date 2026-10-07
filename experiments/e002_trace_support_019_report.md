# E002-TRACE-SUPPORT-019: dense-mask false separation (synthetic)

**Date:** 2026-10-08  
**Status:** Executed in ChatGPT cloud container, no human data.  
**Type:** DISCRIMINATION / CAPABILITY-BUILDING.  
**Parent:** E002-TRACE-SUPPORT-018 (synthetic long-gap adversary).

## Hypothesis
The provisional E002-018 temporal-support veto (maximum 0.20 s gap and >=80% nearby-grid support) is not sufficient to guarantee that legacy O4 between/within waveform separation reflects observed condition-specific physiology.

## Frozen construction
Six synthetic traces (three repeats each in conditions A/B) share exactly the same underlying pupil waveform and replicate drift. Sampling on the 20-Hz, five-second grid is condition-dependent: A drops indices modulo 4 == 1, B drops indices modulo 4 == 2. Each has 76/101 actual samples (75.25%), maximum gap 0.10 s, quality 0.9, and E002-018's **100% nearby-grid support**.

## Executed result
- All six pass legacy read_trace and all six pass the provisional E002-018 veto.
- Legacy O4 between/within RMSE ratio = **3.69346**, exceeding its 1.25 threshold despite zero condition effect.
- Dense same-signal control = **1.00000**.
- Co-observed timestamps only = **1.00000**.
- Condition-balanced mask control = **0.54150** (does not pass O4).
- Across mask-drop periods 3, 4, 5, 6, 8, 10, centered O4 ranges **2.458–5.643**; even with **90.1% actual observations**, false separation remains.
- First-difference O4 rises to **27.55–50.38** across those periods: derivative-based features can amplify interpolation artifacts.
- Median between-condition RMSE is only 0.00014687, ~0.077% of the simulated signal range, illustrating denominator-driven inflation.
- **10/10 automated tests passed** across the 018/019 package.

## Discovery V2
**KNOWN:** Dense, condition-correlated sampling masks can pass both legacy O4 and the 018 temporal-support veto without a physiological condition effect.
**BELIEVED:** Common-time analysis and mask-balanced controls are stronger safeguards than thresholding nearby-grid support alone.
**CONFLICTING:** A max-gap/coverage rule still catches extreme missingness; it is useful but insufficient.
**FALSIFIED:** Passing the provisional E002-018 support veto plus O4 > 1.25 is sufficient evidence of observed stimulus-specific waveforms.
**ANOMALOUS:** False separation survives 90% actual sample retention; derivative-based comparison magnifies it.
**UNTESTED:** Real-phone prevalence, sensor quality correlations, reference waveform agreement, held-out participants, and suitable real-world thresholds.

## Residual and next experiment
The mask effect is small in absolute terms but large relative to near-zero within-condition variation. This is a deterministic adversarial possibility proof, **not** a prevalence estimate. Before interpreting O4 on human captures, preregister a common-observation-time or missingness-balanced negative control, an effect-size check and a temporal-support sensitivity report. Next cheapest experiment: run those controls on existing .trace.csv exports, retaining the original frozen gates unchanged.

## Claim boundary
No webcam RGB/reference measurement, five-second fatigue state validity, or physiological breakthrough is established. RGB-SCALE-OBSERVABILITY-001 stays negative. No novel normalization or waveform-processing method is claimed.
