# E002-421 frozen protocol — exact two-boxcar gap observability and E002-420 ratio falsification

Date: 2026-10-24. **Frozen before E002-421 code or result computation.** Active kernel: E002-371 human shutter-gap validation. Evidence tier: conditional analytic measurement science plus synthetic independent LP, not physical human validation or mathematical-priority claim.

## Scientific question

E002-420 constructed one pair of exposure-average aliases and explicitly warned that its witness-family ratio R<1 was **not** a general safety certificate. Determine the **sharp** no-hidden-closure boundary in the strictly narrower model of two *equal* calibrated scalar boxcar exposure averages, separated exposure windows and a known hard Lipschitz velocity cap. Falsify the tempting use of E002-420's R as a universal classifier.

Model: a continuous normalized physical aperture x(t) in [0,1], |x(s)-x(t)|<=V|s-t|, V>0. Two uniform shutter intervals centered at 0 and d>0, each of duration E with 0<E<=d, report identical exact means m. A closure is x(t)<=theta at any t in the **unobserved gap** [E/2,d-E/2]. Assume 0<theta<m<1 and the interior feasibility conditions m-V*d/2>=0 and m+V*E/2<=1. No RGB-to-aperture conversion is assumed.

## Preregistered predictions

P1. For every feasible trajectory and every t in the unobserved gap, x(t)>=m-V*d/2. The lower bound is **sharp**, attained at t=d/2 by x_star(t)=m-V*d/2+V*abs(t-d/2), restricted to the observation horizon [-E/2,d+E/2]. The constant x_open(t)=m has the same two exposure averages.

P2. Consequently, the exact conditional gap decision is CERTIFY_NO_CROSSING only when m-V*d/2>theta; otherwise AMBIGUOUS, including equality. This is a deterministic **conditional** claim, not a calibrated human or product certificate.

P3. E002-420's construction-specific ratio R=V*(4*d-E)/(8*(m-theta)) can be <1 while a hidden closure remains possible. Frozen falsification witness: m=0.315, theta=0.20, V=60/s, d=1/240 s, E=0.002 s. Predict R<1 and min x_star=0.190<=theta, with both exposure means 0.315. No post hoc retuning.

P4. For a separately authenticated lower bound l on both true exposure means and independently bounded center separation d<=d_max, the sufficient robust certificate is l-V*d_max/2>theta. This is a **sufficient** uncertain-acquisition bound, not an exact boundary if the two mean intervals differ. Unknown shutter shape, clocks, optical transfer or physiological V must abstain.

P5. Independent numerical quadrature of both windows and a separately coded finite-dimensional linear program on piecewise-linear aperture nodes will reproduce the sharp gap minimum on at least 24 seeded admissible parameter sets within 1e-6. Randomly generated admissible Lipschitz paths must never violate the bound. Invalid exposures, missing provenance and uncertified inputs must fail closed. Product output must always remain ABSTAIN_UNCALIBRATED.

## Verification and limitations

Freeze before computing: compare analytic predictions to independent scipy.optimize.linprog constraints built without calling the candidate function; use exactly integrated piecewise-linear exposure means and the speed bound. Include a deliberately unsafe R<1 classifier as a negative control, not as product code. A finite-grid LP validates a piecewise-linear subset, while the analytic Lipschitz proof covers the continuum. Any numerical mismatch, infeasibility or failed prediction must be reported, not suppressed.

This model is *narrower* than E002-389's general joint-integral LP and E002-403's arbitrary temporal-kernel calibration. The point is a **closed-form sharp boundary and a falsified prior-family diagnostic**, not rediscovery of LP optimal recovery. Priority anchors: Micchelli, Rivlin and Winograd (1976) optimal recovery of smooth functions; Bojanov (1994) optimal recovery of functions and integrals; Kwon et al. (2013) high-speed human eyelid kinematics. No novelty or physiological velocity claim is inferred from those papers.

Product remains ABSTAIN_UNCALIBRATED until independent shutter/clock/geometry/velocity calibration, two real blinded human rater sheets and prospective unseen-device human evidence. Rejected E002-417 optical surrogates stay rejected. Preserve Hush branch and PR separately.
