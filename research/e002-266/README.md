# E002-266: temporal optical-drift certificate
2026-10-18. Conditional exact measurement theorem and synthetic test only. No human data.

## Active kernel
Question: can a temporal RGB full-conic pupil/iris ratio certify anatomical pupil change when pupil-only optics and boundary extraction drift?
Signal/reference: RGB apparent radius q(t) versus independently synchronized same-eye eye-tracker pupil diameter D(t).
Frontier: full-conic geometry removes shared homography, not corneal/pose magnification; EVE Basler/Tobii access pending.
Metric: pairwise log-change margin log(Q)-log(kappa)-2log(epsilon); eventual held-out within-session waveform correlation.
Confound: optical pupil-specific magnification and brightness-dependent segmentation bias.
Falsification: identical RGB changes with anatomical-only versus optical-only causes (exact counterexample), or a human holdout violating calibrated nuisance bounds (not tested).
Publishable threshold: independent theorem check, >=8 untouched human participants, participant/device/lighting/glasses holdouts, brightness/geometry controls, predicted failure boundary.
Product threshold: >=75% accurate admitted human windows with meaningful coverage and low-friction calibration.
Kill: no empirically justified nuisance bound, unusable admission, repeated prospective failures, or three nondiscriminating runs.

## Sharp conditional law
Assume q(t)=r(t)m(t)e(t), where r is anatomical pupil/iris radius, m optical magnification, e extraction bias.
If 1/kappa <= m2/m1 <= kappa and 1/epsilon <= e(t) <= epsilon, then for Q=q2/q1, B=kappa*epsilon^2:

    r2/r1 in [Q/B,Q*B].

Both endpoints are attainable. Rise iff Q>B; fall iff Q<1/B; otherwise abstain. Without calibrated bounds, no anatomical direction certificate follows from apparent change alone. Standard interval arithmetic, not a novel general theorem or universal RGB impossibility.

Exact counterexample Q=26/25: anatomical-only r2/r1=26/25,m2/m1=1; optical-only r2/r1=1,m2/m1=26/25. Identical observations. Illustrative kappa=53/50, epsilon=101/100 gives abstention; hypothetical kappa=203/200, epsilon=201/200 permits a rise. Neither nuisance bound has been validated on human RGB.

## SCIENCE ledger
2400/2400 seeded synthetic trials satisfied the exact interval. Decisions: 856 increases, 659 decreases, 885 abstentions. Exact indistinguishable worlds and endpoint witnesses verified. No human waveforms or physiological calibration; synthetic counts are not product performance.

## PRODUCT ledger
Candidate conservative increase/decrease/abstain gate, enabled only after independent nuisance calibration. No uncalibrated five-second pupil or fatigue inference. Next: EVE Basler/Tobii synchronized human data or an authorized alternative; freeze nuisance calibration and evaluate untouched holdouts. If useful admission fails, change the observable.

Frozen human waveform gates unchanged: correlation >=0.75, lag <=67ms, amplitude ratio 0.75..1.25, NRMSE <=0.70, >=75% accurate accepted windows. All untested.

Wildcard: ideal 30 fps point sampling aliases 1.2Hz and 31.2Hz. Standard sampling fact; no human claim.

Prior art: Aguirre 2019 https://pmc.ncbi.nlm.nih.gov/articles/PMC6597540/ ; Mathur et al. 2013 https://pmc.ncbi.nlm.nih.gov/articles/PMC3408927/ ; Hayes and Petrov 2016 https://pmc.ncbi.nlm.nih.gov/articles/PMC4637269/ . Consulted 2026-10-17.

Reproduce with Python stdlib: python3 research/e002-266/experiment.py. See RESULTS.json, provenance and failed gates.