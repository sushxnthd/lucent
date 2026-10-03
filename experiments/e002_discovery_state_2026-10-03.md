# E002 Discovery Protocol V2 evidence update — 2026-10-03

## Classification
SURPRISE / DISCRIMINATION. No frozen E002 outcome inspected.

## Evidence state
- KNOWN: EyeDentify contains paired ordinary-webcam eye crops and Tobii pupil reference for 51 participants.
- KNOWN (independent public reproduction, not Lucent replication): an August 2026 reproduction reports that PupilSense absolute-mm error contains large participant-specific offsets while within-participant temporal correlation can remain similar across participants with very different absolute MAE. Example reported participants 4 and 50 have correlations 0.615 and 0.617 despite MAE 0.322 mm vs 0.043 mm.
- BELIEVED: this pattern is consistent with a temporal/waveform foothold surviving failure of absolute scale.
- CONFLICTING: the same reproduction requires tracker-derived per-person offsets to reduce absolute error, so it does not establish deployable calibration or geometry-normalized observability.
- FALSIFIED: robust raw absolute-mm geometry invariance (RGB-SCALE-OBSERVABILITY-001).
- ANOMALOUS: absolute error and temporal tracking can decouple strongly by participant.
- UNTESTED: whether explicit dimensionless RGB geometry beats raw pixels/PupilSense on the frozen E002 participant-held-out waveform gates and photometric leakage controls.

## Mechanistic prediction
If the dominant failure is a participant-specific scale/offset nuisance rather than destruction of temporal pupil information, then reference-normalized or baseline-fractional waveforms should retain correlation/timing more reliably than absolute-mm estimates, while scale perturbations should affect them less.

## Competing explanations
1. True pupil geometry is preserved but absolute calibration is person-specific.
2. PupilSense tracks stimulus-correlated periocular photometry rather than pupil geometry.
3. Shared stimulus timing inflates correlation.
4. Eye-crop geometry contains participant identity and scale cues that do not generalize.

## Cheapest discriminating experiment
Run frozen E002 on participant-held-out EyeDentify with: raw pupil pixels; direct pupil/reference ratio; PupilSense; photometry-only nuisance predictor; circular-shift/permutation controls. Preserve all gates and inspect subgroup residuals only after primary scoring.

## Claim boundary
This update is a hypothesis/evidence-state refinement, not an E002 PASS and not evidence of fatigue/sleepiness validity.
