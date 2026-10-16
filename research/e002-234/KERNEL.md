# E002-234: original-human radial boundary preflight (development only)

## Active question
Can a geometry-normalized radial pupil boundary be measured in ordinary RGB eye images with stability under controlled photometry and stronger shifted-center nuisance controls, before a native-time same-eye Tobii waveform comparison?

- **Signal/reference:** RGB pupil-radius / iris-radius radial-edge proxy versus native-time same-eye Tobii pupil diameter (reference NOT compared in this run).
- **Frontier:** E002-229 original-human geometry/contrast conflict; E002-231 synthetic radial-edge false-admission; E002-232 opposite-eye shared-scale counterexample; E002-233 contrast-to-texture-margin failure. P_54 video PTS uniqueness gate failed.
- **Primary scalar:** lower participant-bootstrap Pearson correlation bound on untouched synchronized waveform; lag, amplitude, NRMSE and nuisance gates separate. **This preflight:** original-human eye-frame admission fraction under frozen radial controls.
- **Strongest confound:** iris texture, reflections, eyelids and gaze projection mimic dark-to-light edges; uncertified camera exposure clock.
- **Decisive falsification:** failure against shifted-center, angular-split, gamma-photometry and edge-margin controls; later untouched synchronized waveform below frozen gates.
- **Publishable success:** >=8 untouched participants, independent checker, device/lighting/glasses holdouts, mechanism-derived unseen prediction, prior-art audit and synchronized reference.
- **Product success:** >=75% prospective accepted windows under calibrated pupil-boundary uncertainty and waveform gates.
- **Kill:** two blocked attempts on a data path require switching; three nondiscriminating primary runs require reformulation; never deploy an estimator with unbounded false admission.

## Frozen preflight
P_33 and P_54 only, 30 source-hashed original RGB frames each, nominal seconds 5-10 sampled at 6fps. Use MediaPipe iris landmarks for center/scale, not pupil truth. Median outer-minus-inner intensity along 48 rays at 30 normalized radii from 0.20 to 0.78. Gate: iris diameter >=12px, positive radial edge, peak/median absolute edge >=1.5, opposite angular-half fitted radii within 0.12 iris radius, gamma 0.75/1.25 radius change <=0.05 iris radius, and all four centers displaced 0.65 iris radius have peak <0.8 of original. All are exploratory engineering thresholds, not physiological certification.

## SCIENCE ledger
No claim until original-human workflow executes. Passing internal robustness cannot establish true pupil diameter without annotated contours or reference agreement. Failed gates are retained.

## PRODUCT ledger
Fail => reject this simple radial estimator. Pass => permit contour-ground-truth and synchronized waveform experiment only. No five-second fatigue inference.

## Provenance
Source EOTT: https://webgazer.cs.brown.edu/data/WebGazerETRA2018Dataset_Release20180420.zip. E002-220 ZIP CRC and SHA256 verification must run first. P_01/P_02/P_07 reserved untouched. Preserve all per-frame raw CSV, source pins, derived results, checker output and CI logs.
