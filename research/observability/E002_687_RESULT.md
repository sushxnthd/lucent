# E002-687 — Sharp robust shutter-gap certificate with uncertain endpoint calibration

**Evidence tier:** analytic conditional result and executed synthetic exact-rational verification, **not** human or physical evidence.

For true anatomical endpoint apertures a in [al,au] and b in [bl,bu], a nonnegative physical velocity ceiling v and conservative effective blind gap h, require |a-b| <= vh. If the feasible rectangle/band intersection is empty, return **INCONSISTENT/ABSTAIN**, not an exclusion certificate.

Otherwise set a*=max(al,bl-vh), b*=max(bl,al-vh). These are simultaneously feasible and componentwise no greater than any feasible endpoint pair. Therefore the exact worst-case minimum aperture across all feasible endpoints and all v-Lipschitz trajectories is **max(0,(a*+b*-vh)/2)**. The Lipschitz tent achieves this bound. Strictly certify closure exclusion only when this lower bound exceeds the physical closure threshold c. Equality is **ABSTAIN**.

## Executed falsification

An independent candidate-corner oracle and the closed-form implementation agreed in **5,625** exact-rational interval configurations (grid {0,1/2,1,3/2,2} for each of six inputs, retaining ordered endpoint intervals). One explicit uncertainty reversal: exact endpoints a=b=1, v=h=1 imply minimum 1/2 and would exclude a closure threshold c=1/4. But if each true endpoint can lie anywhere in [1/2,1], the robust minimum is 0, so exclusion is forbidden. This is a constructed witness, not a camera error rate.

Reproduce: `python research/observability/e002_687_interval_endpoints.py`. The script was executed in a local Python runtime; hosted CI and independent replay are outstanding.

## Measurement/product consequence

An E002-685 replay must **not** treat noisy point-estimated endpoint apertures as exact. It needs externally calibrated anatomical endpoint intervals, a valid physical velocity ceiling, and a conservative effective shutter gap including exposure, rolling-row, missingness and clock uncertainty. Unbounded, unverified, or inconsistent inputs must abstain. This result neither establishes any physiological ceiling nor authenticates human labels. Keep `ABSTAIN_UNCALIBRATED` and production `BLOCKED`.

**Priority:** E002-671 synchronized physical acquisition and blinded participant-disjoint human validation. Do not use further synthetic agreement as a substitute.
