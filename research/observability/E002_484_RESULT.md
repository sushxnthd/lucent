# E002-484 RESULT — two temporal gates do not identify eyelid closure

**Date:** 2026-10-27. **Kernel:** E002-371. **Evidence tier:** exact synthetic counterexample, independent exact-rational replay and numerical quadrature. **Not:** human validation, physical camera calibration, or a physiological speed limit.

## What was falsified
E002-483 correctly showed that two 10-ms temporal gates can distinguish **one stationary 1-mm trajectory** from **one chosen trajectory that closes** under stipulated timing/gain/noise budgets. That result does not imply the two gates establish the presence of a physical closure among *all* admissible trajectories. E002-484 constructs a different, nonclosing trajectory with an identical allowed two-gate observation. Thus the stronger closure-identification interpretation is false.

## Same endpoints, same velocity class, different closure truth
Let d(t) be piecewise linear through (0,0), (5,+1), (15,-1), (20,0) in mm over ms, and define
- Closing world C: a_C(t)=1+d(t), with a_C(15)=0 mm.
- Nonclosing world N: a_N(t)=1+(1-epsilon)d(t), with a_N(15)=epsilon>0 mm.

Both worlds have **a(0)=a(10)=a(20)=1 mm**, and speed no greater than the illustrative 0.2 mm/ms. Their ideal 10-ms gate means are

C = (1.5, 0.5) mm; N = (1.5-epsilon/2, 0.5+epsilon/2) mm.

For epsilon=0.35 mm, N=(1.325,0.675) mm and never closes. Under the E002-483 independent gain budget delta=0.10 and additive error q=0.03 mm-equivalent, the raw-gate allowed intervals are:

| Gate | Closing world | Nonclosing world | Intersection |
|---|---|---|---|
| First | [1.3200, 1.6800] | [1.1625, 1.4875] | [1.3200, 1.4875] |
| Second | [0.4200, 0.5800] | [0.5775, 0.7725] | [0.5775, 0.5800] |

The **same observed pair (1.400, 0.578) mm** is admissible under both worlds. Consequently any statistic computed only from those two raw gate measurements, including normalized contrast, is identical. This counterexample already holds at phase offset zero, which is within E002-483's stipulated +/-2-ms timing interval. It does not require blur, glasses, gaze drift or a pathological clock.

## Sharp two-world overlap condition
For independent per-gate gains g in [1-delta,1+delta] and additive errors e in [-q,q], the two raw-gate intervals intersect iff the difference in ideal means does not exceed delta times their sum plus 2q. Applying this to both gates gives the exact two-world condition

epsilon <= min[(6 delta + 4q)/(1+delta), (2 delta + 4q)/(1-delta)]

for 0<epsilon<=1, 0<=delta<1, q>=0 and valid positive sensor ranges.

At delta=0.10, q=0.03, the active bound is **16/45 = 0.355555... mm**. Thus epsilon=0.35 admits an exact common observation, while epsilon=0.36 does not for this pair of worlds. At delta=0, q=0.03, the bound is epsilon<=0.12 mm. With zero gain and additive error, the endpoint-matched scaled worlds are distinguishable for any epsilon>0, but the margin can be arbitrarily small.

The original frozen protocol incorrectly stated the second-gate bound as universally sufficient. [Amendment A](E002_484_AMENDMENT_A.md) records the corrected minimum-of-two expression **before** implementation; the original is preserved.

## Stronger exact-data counterexample without independently authenticated endpoints
Even at zero gain and additive error, the smooth nonclosing trajectory a_S(t)=1+(pi/4)cos(pi*t/20) mm produces **exactly the same (1.5,0.5) mm gate means** as C. Its minimum is 1-pi/4 = 0.214602 mm, and its peak speed is pi^2/80 = 0.123370 mm/ms, below 0.2 mm/ms. Its instantaneous values at t=0,10,20 differ from C. Therefore this exact-data counterexample applies **only when endpoint apertures are not independently authenticated**. The endpoint-matched epsilon=0.35 counterexample does not need that relaxation, but does use the frozen nuisance allowances.

## Verification and limitations
The exact-rational independent Python replay reproduced the 16/45 threshold and the common observation, and a 200,000-step midpoint quadrature reproduced both cosine gate averages to ~1.3e-12. The Node implementation and 16 adversarial tests are committed. Hosted GitHub Actions is required to verify the actual committed Node source; do not claim hosted pass until it completes. [Frozen protocol](E002_484_FROZEN.md), [amendment](E002_484_AMENDMENT_A.md), [simulator](e002_484_closure_alias.cjs), [tests](test_e002_484_closure_alias.cjs), [independent replay](e002_484_independent_replay.py).

The counterexample uses scalar gate measurements and an illustrative kinematic bound, not spatial images or measured physiology. Additional independently calibrated image features or verified endpoint constraints may resolve particular pairs. It does not show every closing trajectory is indistinguishable or invalidate E002-483's narrower pairwise separation.

## Immediate scientific and product consequence
**KILL:** 'Two temporal-gate measurements establish that a full eyelid closure occurred' as a general claim. Pairwise discrimination is not event identification. To authorize any anatomical closure inference, require independently calibrated spatial/temporal measurements and a lower-bound separation from the entire admissible **nonclosing** trajectory class, including gain, brightness, blur, missingness, gaze, glasses, clock and velocity uncertainty. If such separation is absent, abstain.

No physical shutter acquisitions or new anatomical human reference sequences were obtained. Physical closure, blink duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. Next decisive work: independently timed optical acquisition, moving-aperture witnesses that include matched-gate nonclosure controls, then blinded high-frame-rate human trajectories. Do not replace these with more synthetic model polishing.
