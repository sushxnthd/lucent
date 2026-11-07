# E002-591 | Sharp sustained-closure integration boundary and one-sided anatomical dwell instrument

**Date:** 2026-11-01 UTC. **Kernel:** E002-371. **Frozen before implementation:** [E002_591_FROZEN.md](E002_591_FROZEN.md), commit 9a37b0491fcced1914060a7b5bc55a14ce8fe989. **Evidence:** idealized mathematical result, synthetic exact-rational independent replay, finite-grid LP sanity checks. **NOT** human or physical-camera validation.

## New scientific question and sharp result

E002-590 concerned an instantaneous exact-zero event. A positive-duration threshold closure is a distinct event with a different exact alias threshold. Let a(u) be absolutely continuous on [0,1], 0<=a<=1, with exact endpoints a(0)=a(1)=c, hard speed |a'|<=L=VT, and an interval of fraction d of the exposure with a<=tau<c. The ideal sensor returns the exact linearly integrated aperture mean Y=integral a(u)du; the constant-open control is a=c and has mean c.

Set S=1-d and C=tau+(1-tau)*S. A sustained-closure trajectory is reachable only if L*S>=2*(c-tau). Its sharp maximum mean is:

- M_d(L)=tau+L*S^2/4 when L*S<=2*(1-tau);
- M_d(L)=tau+(1-tau)*S-(1-tau)^2/L when L*S>=2*(1-tau).

The sharp **existence** threshold for an identical integrated mean c is:

- Lcrit=4*(c-tau)/S^2 if c-tau<=(1-tau)*S/2;
- Lcrit=(1-tau)^2/(C-c) if (1-tau)*S/2<c-tau<(1-tau)*S;
- Lcrit=INFINITY if c>=C.

For finite Lcrit, an equal-mean sustained-closure witness exists **if and only if** L>=Lcrit. If c>=C, no finite speed can create that alias under the stated ideal operator. This is not a general result for real camera pixels, unknown photometric response or rolling-shutter observations.

| Baseline c | Closure tau | Dwell fraction d | Critical L=VT |
|---:|---:|---:|---:|
| 0.50 | 0.00 | 0 | 2 (E002-590) |
| 0.50 | 0.00 | 0.10 | **2.5** |
| 0.50 | 0.00 | 0.25 | **4** |
| 0.50 | 0.00 | 0.50 | **No finite speed** |
| 0.50 | 0.10 | 0.30 | **81/23 = 3.521739...** |
| 0.20 | 0.00 | 0.10 | **80/81 = 0.987654...** |
| 0.50 | 0.10 | 0.60 | **No finite speed** |

At 30 fps, d=0.60 corresponds to 20 ms. If c=0.5 and tau=0.1, any sustained 20-ms threshold closure forces the ideal aperture mean strictly below 0.46 regardless of finite eyelid speed. This **does not** imply that real 30-fps camera images reliably detect a 20-ms blink: aperture is not pixel brightness, shutter support is not authenticated, and radiometry, gaze, geometry, blur and noise are uncontrolled.

## Proof

Replace a by max(a,tau), preserving endpoints and the Lipschitz bound without decreasing the mean. The specified dwell interval becomes exactly tau. Delete the flat dwell interval, leaving outside time S and a continuous trajectory reaching tau. Rescale its aperture to b=(a-tau)/(1-tau) and its outside time to [0,1]. The normalized speed ceiling becomes K=L*S/(1-tau), endpoints become (c-tau)/(1-tau), and the path reaches zero. E002-590's sharp maximum mean for this normalized zero-reaching path is K/4 for K<=2 and 1-1/K for K>=2 (subject to reachability). Undoing the transformations gives M_d(L). Inserting the dwell into E002-590's exact piecewise-linear extremizer attains that upper bound. At Lcrit, the mean equals c; at larger ceilings the same witness remains admissible. Below threshold the mean is strictly less than c or the path is unreachable. At c>=C, finite-speed transitions prevent attaining the cap C. This establishes necessity and sufficiency in the exact model.

## Reproduction and independent checks

The [Python exact-rational implementation](e002_591_duration_alias.py) passed all seven frozen cases, 48 additional rational-grid finite-threshold constructions, exact endpoint/mean/slope/dwell checks and 1%-subthreshold exclusions. The [independently written Node BigInt replay](e002_591_independent_replay.cjs) reproduced all seven frozen cases and 48 rational-grid constructions without consuming Python output. Its first local draft exposed a wrong high-branch knot and failed the speed check; the bug was corrected before persistence. This is a preserved implementation failure, not a failed scientific prediction.

An independently formulated [SciPy HiGHS finite-grid LP](e002_591_lp_crosscheck.py) passed four 401-node optimizations: three grid-aligned critical witnesses attained means 0.5, 0.5 and 0.2; the partial-closure witness attained 0.499283696 versus the continuous maximum 0.5 because its critical switch time lies between grid nodes. Numerical grid agreement is a sanity check, not a proof.

The Python implementation also includes a **one-sided prospective anatomical dwell certificate**. If an independently established hard aperture-speed ceiling V and a source-bound upper aperture bound u<=tau are available at nominal time t with certified time error e, then the interval [t-r,t+r], r=(tau-u)/V-e, is guaranteed subthreshold when r>=0, clipped to the valid domain. Only overlapping/touching certified intervals may be joined; missing calibration or nuisance flags trigger abstention. Empty witness intervals **never** certify continuous openness. Nine synthetic controls passed. The booleans accepted by the software do not authenticate physical provenance; a separate evidence audit is mandatory.

The path-scoped [hosted workflow](../../.github/workflows/e002_591_duration_alias.yml) was committed. Inspect its actual Actions conclusion before claiming a hosted pass. No private video, annotation rows, human imagery or personal identifiers were committed.

## Literature and priority boundary

This is not a claim to have invented bounded-speed optimal control, temporal integration, or human eyelid kinematics. Kwon et al. (2013, *Journal of the Royal Society Interface*, DOI [10.1098/rsif.2013.0227](https://doi.org/10.1098/rsif.2013.0227)) recorded 25 volunteers' voluntary eyelid motion at 600 fps. Wambier et al. (2014, *Ophthalmic Plastic & Reconstructive Surgery*, DOI [10.1097/IOP.0000000000000031](https://doi.org/10.1097/IOP.0000000000000031)) compared high-speed video against magnetic search-coil motion in 21 subjects. Godfrey et al. (2019, *Ophthalmic Plastic & Reconstructive Surgery*, DOI [10.1097/IOP.0000000000001356](https://doi.org/10.1097/IOP.0000000000001356)) measured spontaneous blinks using 240-fps smartphone video in 10 people. Their measured typical/peak velocities are not universal hard physiological speed ceilings. The conditional sustained-duration alias boundary has not undergone a comprehensive mathematical-priority audit or independent external peer review.

## Next decisive physical study and product consequence

Freeze the closure threshold, minimum duration, normalized anatomical geometry, calibration/holdout participants and one-sided contradiction endpoint before revealing held-out reference labels. After consent and privacy review, simultaneously record eyelids with an anatomical high-speed reference (prefer 400–600 fps; 240 fps if constrained) and an ordinary camera, plus independently calibrated exposure, rolling-row and clock channels. Collect two blinded anatomical rater streams and explicit geometry, gaze, eyewear, brightness, missingness and blur flags. Obtain a defensible **independent** hard speed ceiling, not the maximum finite difference from the same sampled frames. Use the one-sided dwell instrument to lower-bound sustained closure, then prospectively test E002-371/E002-591 predictions against sealed held-out camera observations. Independently validate the transfer from anatomical aperture integration to real image pixels.

**New physical captures: 0. Independent anatomical rater pairs: 0. Authenticated shutter calibrations: 0. Hard human velocity ceilings: 0. Held-out physical predictions: 0.** E002-582–584's investigator-label index omissions and E002-578's authentic-video instrument do not supply these missing measurements. Further synthetic analysis cannot substitute for physical validation.

**Product:** reject any claim that a single positive 100-fps annotation certifies sustained dwell, or that ideal aperture-mean observability certifies actual camera-image observability. Return ABSTAIN_UNCALIBRATED for physical blink, PERCLOS, fatigue and sleepiness claims. **Release BLOCKED.** Keep draft PR #26 open/unmerged. Hush branch and PR #45 unchanged.
