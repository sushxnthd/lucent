# Lucent E002-204: original human reference semantics execution

## Active product-critical question
Can the published 15-participant MCFW-Gaze source-defined validity counts be interpreted as pupil-diameter validity? Does a prospectively fixed same-eye tracker reference admit >=75% of samples without outcome selection?

## Exact signal/reference
Primary: native-time ordinary RGB pupil/anatomical-iris waveform versus independently synchronized same-eye tracker pupil diameter. MCFW-Gaze is tracker-only for this purpose: it tests reference semantics, not RGB observability.

## Mandatory kernel
- Frontier: E002-203's exact finite-window bounds on published source-defined trial counts; source-to-pupil semantics UNVERIFIED.
- Scalar: participant-level proportion with pupil_valid AND finite positive same-eye diameter; primary observability scalar remains participant-bootstrap 95% lower Pearson correlation bound.
- Strongest confound: pupil versus gaze validity may disagree; future RGB nuisance: illumination/blur/gaze geometry and synchronization.
- Falsification: raw TSV does not match claimed validity semantics, or prospective paired human RGB fails frozen correlation/lag/amplitude/NRMSE and nuisance-control gates.
- Publishable success: >=8 untouched paired participants, participant/device/lighting/glasses holdouts, independent checker, mechanism-derived unseen prediction, prior-art audit.
- Product success: calibrated abstention at >=75% accepted coverage without post-hoc subgroup selection.
- Kill: three nondiscriminating runs or prospective waveform failure after sound reference and controls.

## SCIENCE ledger
Known: exact set-intersection bounds on source-defined metadata; the earlier 70%-of-15 binocular sampling gate is conditionally unattainable. Test now: per-eye raw pupil validity, gaze validity, positive finite pupil diameter, source counts, 30 TSV eye records. NOT known: actual pupil semantics, RGB waveform, or fatigue.

## PRODUCT ledger
Reject validity-flag-only admission; retain same-eye, finite positive diameter, raw timestamps, per-participant coverage and excluded cases. No five-second fatigue inference without untouched RGB-versus-tracker validation.

## Provenance
MCFW-Gaze v3 https://zenodo.org/records/20300972
Expected dataset MD5 5e04a7b5e50f7508775e1daea527246b; metadata MD5 369d9446b62fd00888a6d51e152697bd.
Previous 38507882731 GitHub run downloaded and MD5-verified the original archive but failed on parser aliases. E002-203 committed original raw audit and independent checker at 44ce9f4ba43b2d0f296b6f0178a7d8cfb3653a9f but never ran it.
This branch adds a push-triggered workflow, a synthetic preflight and explicit provenance. Workflow artifact must contain archive SHA256, per-TSV SHA256, results and negative gates. Source files are NOT uploaded to git.

## Wildcard (~10%)
Quantify original samples where pupil_valid is true but diameter is invalid or nonpositive; this tests reference-admission anomalies, not a new primary kernel.

## Smallest supported claim before Actions result
The original-human semantic audit is runnable via a push trigger with fail-closed synthetic controls. No raw-human semantic result is claimed until the workflow and artifact are inspected.
