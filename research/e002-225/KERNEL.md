# E002-225 | Native RGB iris-visibility preflight (frozen before execution)

## One active product-critical question
Can the original Brown Eye of the Typer ordinary-RGB frames reliably expose enough eye/iris geometry to justify attempting a pupil/iris temporal observable, before claiming physiological waveform observability?

- **Exact eventual signal/reference pair:** RGB pupil-to-iris diameter ratio as a function of independently calibrated exposure time, versus native-time same-eye Tobii pupil diameter in mm. **This run measures neither paired ratio nor waveform correlation**: it measures MediaPipe iris landmark visibility and local photometric contrast on original RGB frames.
- **Best-known frontier:** E002-220/221 verified original EOTT RGB, tracker and events for P_33/P_54; valid pupil samples approximately 40 Hz; P_54 has unreliable video presentation timestamps. E002-223/224 show clock-lag and excitation confounds. No exposure-clock calibration, human waveform agreement or independent device holdout.
- **Primary scalar preflight metric:** fraction of sampled RGB frames with a detected iris landmark diameter >=12 pixels per eye, separately by participant. This is an **exploratory engineering threshold**, not a proven optical resolution law. Eventual observability metric is participant-bootstrap lower Pearson r bound plus lag, amplitude, NRMSE, nuisance and prospective acceptance gates.
- **Strongest confounds:** gaze/head geometry, exposure/brightness, focus and eyelid occlusion; P_54 clock metadata is independently unsuitable for lag certification.
- **Decisive falsification:** verified original RGB frames show frequent missing/undersized iris landmarks, or positive geometry gate fails in an unseen participant; success of the preflight does **not** establish pupil waveform observability.
- **Publishable threshold:** >=8 untouched independently synchronized RGB/tracker participants, device/lighting/glasses holdouts, independent checker, nuisance baselines, prior-art audit and unseen mechanism prediction. This preflight alone is not publishable evidence of physiological observability.
- **Product threshold:** >=75% prospective windows accepted only after frozen waveform gates; for this cheap preflight, >=80% frames with iris landmark diameter >=12 pixels per eye is an exploratory admission diagnostic, not a product acceptance claim.
- **Kill condition:** if original RGB is not retrievable in two attempts, switch dataset; if three primary runs are nondiscriminating, reformulate; if preflight fails, do not continue this source as a primary pupil-ratio benchmark.

## SCIENCE ledger
Prior verified source hashes must match; use source RGB only. MediaPipe iris landmarks estimate iris geometry, **not pupil diameter**. An iris of >=12 px is not proof of measurable pupil changes. No camera/reference time mapping is inferred from dense reference coverage.

## PRODUCT ledger
If a large fraction of frames lacks even coarse iris geometry, Lucent should reject them before attempting physiological inference. If geometry is present, it only authorizes a separate pupil segmentation/contrast and synchronized reference experiment. No app/UI work or five-second fatigue claim.

## Controlled wildcard
Reserve <=10% of exploratory analysis for brightness-vs-contrast and eye-side asymmetry as potential abstention cues. No frozen physiological evaluation may be tuned on these samples.
