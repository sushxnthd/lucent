# Lucent E002-317 — RGB chromatic-rank aperture observability

A conditional measurement-science kernel extending E002-316. A full-support, linearized RGB aperture-band integral can identify shutter-mean normalized eyelid aperture despite one arbitrary-amplitude **calibrated-color** nuisance only if target RGB signature is linearly independent of nuisance signature and exposure gain is calibrated. The exact failure boundary depends on spectral angle and deterministic RGB error. This is not a human result or a claim of novel linear algebra.

Run `python independent_checker.py`. Preserve negative results. See THEOREM.md, FROZEN_PREDICTION.json, FAILED_GATES.md, PRIOR_ART.md.

Product: only calibrated, interval-valued shutter-mean aperture with abstention; reject generic webcam blink timing, pupil waveform and five-second fatigue diagnosis.
