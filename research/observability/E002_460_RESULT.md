# E002-460 — sharp directional exposure-centroid law; E002-458 shutter surrogate falsified in its own idealized model

**Date:** 2026-10-26. **Frozen protocol:** [E002_460_FROZEN.md](E002_460_FROZEN.md), committed first at `224b341279dae374399476bafcfbf54ddf43749e`. **Evidence tier:** conditional mathematical proof, constructive synthetic witnesses and independently implemented numerical check; **NO new human anatomical trajectories or physical camera calibration**.

## Finding and exact scope

The E002-458 conservative shutter correction is **not a sharp law** for the *dark interval between known shutter supports* if the sensor observable is itself an exact, linear, calibrated **exposure average of anatomical aperture in millimetres**. Under that unusually strong assumption, shutter width need not erode the timing boundary at all; only the shutter's temporal centroid and support location enter.

Let aperture a(t)>=0 obey directional velocity bounds `-C <= a'(t) <= O`, with C,O>0 in mm/ms. Let the two nonoverlapping shutter supports be `[l0,r0]`, `[l1,r1]`, with `r0<l1`. Known normalized nonnegative shutter kernels have temporal centroids `mu0,mu1`; their *true linear anatomical-aperture means* are `m0,m1>c`, with closure threshold c. A hidden dark-gap closure `a(tau)<=c` for some `r0<tau<l1` is possible **if and only if** there exists tau in the intersection

```
(r0,l1) intersect [mu0 + (m0-c)/C, mu1 - (m1-c)/O].
```

Here C,O must use mm/ms, and equality of the two timing bounds is allowed when the unique tau lies strictly inside the dark gap. At support boundaries, the crossing is not strictly dark-gap-hidden. For ordinary floating-point computations, numerical equality is deliberately `NOT_EXCLUDED_BOUNDARY`, never a safety certificate.

**Necessity:** if a(tau)<=c, then for all t before tau, `a(t)<=c+C(tau-t)`; after tau, `a(t)<=c+O(t-tau)`. Integrating each inequality against its normalized shutter kernel gives `m0<=c+C(tau-mu0)` and `m1<=c+O(mu1-tau)`.

**Sufficiency:** for any tau in the intersection, set `a(t)=c+alpha*C*(tau-t)` before tau and `a(t)=c+beta*O*(t-tau)` after tau, where `alpha=(m0-c)/(C*(tau-mu0))`, `beta=(m1-c)/(O*(mu1-tau))`. Both are in [0,1], so the directional derivative bounds hold. Because each exposure lies wholly on one affine side, its weighted average equals the prescribed mean for **any normalized kernel with the stipulated centroid**, including asymmetric kernels. The witness reaches exactly c at tau. This is a standard reachability/optimal-recovery argument, **not a novel general mathematical theorem**.

A dimensionless center-gap ratio `R=(mu1-mu0)/[(m0-c)/C+(m1-c)/O]` is necessary but **not sufficient** for a dark-gap witness when shutter support restricts tau; the full interval-intersection criterion is exact.

## Frozen numerical comparison (hypothetical, not physical)

Use c=2 mm, m0=m1=3 mm, C=567.103928 mm/s and O=274.616337 mm/s. These are published *sample peak maxima* borrowed solely as **hypothetical** hard caps; they are not physiological upper limits. For centered uniform shutters, the directional critical centroid gap is **5.404789 ms**.

| Center separation | Exposure width | Sharp dark-gap result | Explanation |
|---|---:|---|---|
| 4.166667 ms (240 fps) | 2.0 ms | EXCLUDED_CONDITIONALLY | Gap shorter than 5.404789 ms |
| 4.166667 ms (240 fps) | 2.3 ms | EXCLUDED_CONDITIONALLY | Same centroids; known linear aperture means |
| 6.000 ms | 2.0 ms | POSSIBLE_CONDITIONALLY | Explicit crossing witness exists |
| 6.000 ms | 5.0 ms | EXCLUDED_CONDITIONALLY | Required crossing lies inside first shutter support, not in the dark gap |

For the 240-fps, 2.3-ms exposure case, E002-458's **conservative surrogate** lowers the hypothetical critical gap to **4.096860 ms**, returning NOT_EXCLUDED. The sharp dark-gap law still excludes a crossing under the narrower linear-aperture-average assumptions. Thus **the earlier surrogate's loss of exclusion is not evidence that a dark-gap closure is feasible**. It was conservative, not incorrect as a one-sided safety bound. This result does **not** say exposure-masked closures inside shutter supports are impossible.

## Reproduction and falsification

- [Python evaluator](e002_460_exposure_centroid.py) refuses pixel contrast, uncalibrated linearity, invalid kernel/clock metadata, geometry, brightness, missingness, blur, gaze, glasses, sampling and rolling-shutter uncertainty. It always returns `physical_certification:false`.
- [Adversarial Python tests](test_e002_460_exposure_centroid.py) include the frozen four cases, support-boundary equality, nonuniform centroid, malformed data, nuisance refusal and 1,000 seeded exact piecewise-affine witnesses.
- [Independent JavaScript replay](e002_460_independent_replay.cjs) separately checks 10,000 constructive witnesses and 10,000 impossible short-gap negative controls, without importing the Python evaluator.
- A separate local Python arithmetic calculation independently checked 10,000 randomized constructive cases with **0 logical contradictions** and reproduced 240-fps critical 5.404789 ms and old-surrogate 2.3-ms critical 4.096860 ms. This is not a hosted verification of the committed Python test suite.
- [Dedicated CI workflow](../../.github/workflows/e002_460_exposure_centroid.yml) is configured to execute both implementations. **At report creation, hosted completion is pending**; no hosted pass is claimed.

## Relationship to prior work and scientific decision

**E002-421** already established the shutter-width cancellation for equal means and symmetric Lipschitz speed with uniform boxcars; **E002-422** extended to unequal boxcar means and, under a balanced-slope condition, the full observation horizon. **E002-389** provides a general joint-integral LP. E002-460 is a **directional-speed and arbitrary known-kernel-centroid dark-gap specialization**, directly correcting an overly pessimistic interpretation of E002-458. Do not present it as independent discovery of optimal recovery or as new human evidence.

The result **cannot be promoted to a real camera claim**. An ordinary RGB image or nonlinear landmark estimate is not a known linear mean of millimetre aperture; raw intensity, optical blur, occlusion, geometry, saturation, rolling shutter and exposure response violate that mapping. Nor do sample peak velocities establish hard physiological caps. The exact dark-gap law does not certify against threshold crossings *during* shutter exposures. The product gate remains `ABSTAIN_UNCALIBRATED` for physical hidden closure, blink duration, PERCLOS, fatigue and medical claims. **E002-371 physical validation remains NOT_ESTABLISHED.**

**Next decisive experiment:** independently calibrated high-rate anatomical eyelid-margin trajectories with authenticated shutter timing and two blinded anatomical raters; freeze the existing prospective E002-456 protocol, then test hidden-gap predictions on unseen participants. Stop further algebraic polishing without new anatomical evidence. S21/S22 remain sealed. Hush's separate PR #45 is untouched.
