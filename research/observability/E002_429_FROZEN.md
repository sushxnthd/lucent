# E002-429 — frozen geometry-nuisance falsification protocol

Date: 2026-10-25. **Evidence tier: synthetic orthographic counterexample only.** This is an E002-371 nuisance-control experiment on the existing Lucent research branch, not a separate kernel or a human trial.

## Predeclared question
Can two different physical eyelid-aperture trajectories produce the **same entire projected-aperture time series**, including all shutter averages, while one crosses the physical threshold and the other does not, when effective projection geometry is not authenticated?

## Frozen synthetic worlds
Use the deliberately restricted forward model `y(t)=H(t) cos(phi(t))` where H is true physical aperture in mm and phi is an effective projection angle. This is **not** a physiological gaze calibration or a full RGB-image renderer. Both worlds have a hard physical aperture speed cap V=1.2 mm/s, a physical threshold theta=2.00 mm, ordinary camera separation d=1/30 s, and 4 ms uniform exposure.

World A: H=2.04 mm, phi=20 degrees throughout. World B: H=2.01 mm at t=0,d, with a symmetric piecewise-linear V-shaped trajectory reaching 1.99 mm at t=d/2, and phi(t)=acos(2.04*cos(20 deg)/H(t)). Outside [0,d], H=2.01 mm. This makes both continuous projected signals equal by construction. All angles must be real and between 0 and 90 degrees.

## Predictions frozen before implementation
1. World A never crosses theta; world B does, while both satisfy V<=1.2 mm/s.
2. Continuous projected-signal discrepancy <1e-12, including shutter averages and virtual 24/30/60/120/500-Hz observations.
3. Incorrectly fixing phi=20 degrees converts both shutter averages into m=2.04 mm; the restricted equal-average law m-Vd/2 yields 2.02 mm > theta and a **false conditional no-closure decision** for world B. This is an *assumption violation*, not a counterexample to E002-421.
4. With an independently justified effective-angle interval 15..20 degrees, the instantaneous physical lower bound y/cos(15 deg) falls below theta, forcing abstention. This is not a time-continuous certificate for arbitrary sampled y.
5. Invalid projected measurements and angle intervals must be rejected. The product must retain ABSTAIN_UNCALIBRATED.

## Independent verification and scope
Implement an independent finite-difference velocity oracle, dense time-sampling comparison, midpoint shutter quadrature at five virtual rates, and an angle-interval guard. Report numerical results, assumptions, prior literature, and an actionable **physical geometry calibration** protocol. Do not claim human feasibility of the stipulated angle trajectory, physical shutter calibration, independent human validation, or a novel theorem. The experiment is valuable only if it changes which product claims are rejected or calibrated.

Primary empirical anchor to audit: Read et al., *Optometry and Vision Science* 83 (2006), 715–722, DOI 10.1097/01.opx.0000236811.78177.97; 76 human subjects with significant gaze-dependent palpebral-fissure changes. Its measured gaze effects do not validate this synthetic cosine model.
