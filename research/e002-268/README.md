# Lucent E002-268 — prospective-admission oracle audit

## Active question
Can ordinary visible-RGB pupil/iris dynamics be admitted for physiological waveform measurement **using only information available at deployment**, then meet frozen E002-261/E002-267 reference gates on independently synchronized same-eye pupil diameter?

- **Signal/reference:** visible-RGB dimensionless pupil/iris waveform vs synchronized same-eye native-time eye-tracker diameter (mm).
- **Frontier:** E002-267 frozen synthetic-only evaluator admits windows using `valid_ref` and `sd(reference_mm)`, neither available to camera-only deployment; human waveform outcome remains unmeasured.
- **Scalar:** reference-blind admitted coverage and certified-window accuracy; held-out participant-bootstrap correlation lower bound and frozen lag/amplitude/NRMSE/nuisance gates retained.
- **Strongest confound:** illumination/gaze-dependent optical scale plus reference-dependent selection.
- **Decisive falsification:** identical RGB/nuisance observables, differing reference amplitude; any RGB-only selector must treat paired sessions identically, but oracle admission selects only the easy session.
- **Publishable threshold:** >=8 untouched human participants, independently checked provenance, holdouts, nuisance controls, independent checker, mechanism-derived unseen prediction, prior-art audit.
- **Product threshold:** >=75% accurate *prospectively admitted* human windows at >=50% RGB-only coverage; no reference-derived admission.
- **Kill:** repeated non-discriminating runs or no deployable calibration/admission at useful coverage; two blocked dataset attempts force path switch.

## Executed synthetic counterexample
8 held-out synthetic participants with two 5-second sessions each. RGB, brightness, geometry, iris, device, lighting, glasses and timestamps are identical between paired sessions. One reference amplitude is 0.24 mm and the other 0.02 mm; assignment alternates across participants. Training uses 0.24 mm. E002-267 oracle admission excludes 8 low-reference-SD sessions and reports 8/8 correct accepted windows at 50% coverage. A camera-only quality selector cannot distinguish these paired sessions and admits 16/16, with only 8/16 satisfying the frozen waveform/amplitude gates. The low-amplitude sessions violate amplitude ratio by factor 12. This is **synthetic only** and not a real-world error estimate.

## SCIENCE ledger
Confirmed reference-dependent admission vulnerability and self-attested source-hash vulnerability. `admit_provenance` accepts a purported human `source_dataset_sha256='0'*64` without reading source bytes. This is an intentionally false metadata test, NOT human evidence. Original E002-267 evaluator blob: `c97fcdc77ca27235e5dc8186529cdbd3e87f6bd4`. The general indistinguishability observation is elementary, not a novel field theorem.

## PRODUCT ledger
**Do not issue Lucent product certificates from E002-267.** Admission must depend exclusively on deployment-visible RGB/quality features, frozen before reference outcomes. Missing/low-variance references may be labeled unscorable but cannot silently vanish from the deployed-coverage denominator. Verify source hashes against bytes and synchronization independently. Keep original waveform gates; do not infer fatigue.

## Reproduce
Run from repository root: `python3 research/e002-268/audit.py` and `python3 research/e002-268/independent_check.py`. Requires Python 3 standard library only, imports unmodified E002-267 code. `RESULTS.json` is local deterministic replay, not remote CI. No GPU, hardware, spending, or human data.

## Failed gates
Human paired data: NOT_ACCESSED. Human waveform: NOT_EVALUATED. Reference-blind admission in prior evaluator: FAIL. Source hash validation in prior evaluator: FAIL. Human participant/device/lighting/glasses holdouts: NOT_EVALUATED. Optical calibration: NOT_EVALUATED. Breakthrough: NOT_ESTABLISHED.

## Wildcard (~10%)
Checked a second provenance channel: an arbitrary 64-character zero source hash is accepted by the existing validator. No allegation about any real dataset; this is a software guardrail defect.
