# Lucent E002-297 — Aperture mass and rolling-shutter gauge
Evidence tier: **exact conditional 1-D laws and synthetic checks only**. Human ordinary-RGB/reference validation and field-level novelty NOT established.
Active question: does exposure-averaged **projected eyelid aperture ratio**, measured from linearized RGB against an independent high-speed eyelid-margin reference, survive PSF, illumination, geometry, gaze and glasses? Not pupil diameter, velocity, blink count or fatigue.
Metric: held-out reference interval coverage, interval width, and mechanism-predicted crossing at v*tau=q/(1+q).
Strongest confounds: rolling row-time shear, unknown contrast, reflections and nonuniform iris/sclera radiance.
Exact model, proofs and collisions: THEOREM.md.
Falsification: prospective holdout exceeds calibrated error intervals or nuisance controls explain apparent signal.
Synthetic tests: 400 PSF trials (max area error 7.11e-15 px), 150 rolling trials (max error 4.89e-6 px), exact 601-point rolling collision and 601-point contrast collision, 30 rational mass checks, 4 rejected mutations. Synthetic unseen prediction: 12.0665205621 px; independent integration: 12.0665205562 px.
Untouched human: not run. Publication requires >=90% held-out interval coverage, median relative width <=10%, >=20% MAE gain over best control with participant-bootstrap CI excluding zero, plus an unseen boundary crossing.
Product: investigate calibrated exposure-averaged aperture with abstention; reject uncalibrated pupil, velocity and fatigue claims.
Full runnable package: lucent_e002_297_aperture_mass_rolling.zip in automation artifact; no raw human data acquired.