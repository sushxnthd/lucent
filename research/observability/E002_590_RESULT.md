# E002-590 | Sharp full-duty integrated-aperture alias threshold

**Freeze:** [E002_590_FROZEN.md](E002_590_FROZEN.md) was committed first at `7b8c8e9`. **Primary kernel:** E002-371. **Parent falsification:** E002-589. **Evidence tier:** exact mathematical/idealized synthetic observation-operator result. **NOT** a human, clinical or physical-camera measurement.

## Result: the E002-589 speed-4 witness is not sharp

Let a:[0,T]->[0,1] be absolutely continuous with a(0)=a(T)=c in (0,1), |da/dt|<=V almost everywhere, and a(t*)=0 for some t*. Let an ideal, perfectly calibrated, full-duty linear aperture-integrating sensor measure the frame mean `Y=(1/T) integral a(t)dt`. The open control is `a_open(t)=c` and has `Y=c`. Define the dimensionless speed `L=V*T`.

**Sharp existence law:** A zero-reaching trajectory with **the same** measured frame mean c exists if and only if

```
L >= Lcrit(c) = 4c                  for 0<c<=1/2
                1/(1-c)            for 1/2<=c<1.
```

The auxiliary reachability constraint `L>=2c` is automatically implied by `L>=Lcrit(c)`. In particular, at `c=1/2`, the sharp alias threshold is **L=2**, not E002-589's witness speed L=4. For the specified ideal observation model, full optical duty cycle plus a speed ceiling does not exclude a hidden complete closure once the dimensionless ceiling reaches this threshold.

## Upper bound and constructive proof

Normalize time u=t/T. For any admissible zero-reaching path and level z in (0,1), either the path never reaches z or the below-level set `{u:a(u)<z}` has length at least `min(1,2z/L)`. For z<=c this follows from the Lipschitz travel required on both sides of a zero. For z>c, if the level is reached on only one side, the required below-level travel from the opposite endpoint to zero, then zero to z, plus the endpoint's return below z, totals at least `(c+z+z-c)/L=2z/L`; reaching z on both sides cannot reduce it. Layer-cake integration therefore gives

```
Y = integral_0^1 |{u:a(u)>z}| dz
  <= integral_0^1 max(0,1-2z/L) dz
  = L/4          if L<=2,
    1-1/L        if L>=2.
```

The bound is **attained** whenever L>=2c: put the zero at `u=c/L`, travel at maximum speed up to `min(1,L/2)`, and return to endpoint c, using a plateau at 1 when L>=2. Explicit extremal knots are

- L<=2: `(0,c), (c/L,0), (c/L+1/2,L/2), (1,c)`.
- L>=2: `(0,c), (c/L,0), ((c+1)/L,1), (1-(1-c)/L,1), (1,c)`.

At the stated Lcrit the attained upper bound equals c. Below Lcrit, either reaching zero is impossible or the maximal mean is strictly below c, so aliasing to the constant-open frame mean is impossible. Above Lcrit, the critical-speed witness remains admissible because its speed is no greater than the new ceiling. This proves both necessity and sufficiency under the exact stated assumptions.

## Exact-rational experiment and independent replay

| Baseline c | Sharp Lcrit | Mean of closure witness | Illustrative Vcrit at 30 fps |
|---|---:|---:|---:|
| 1/5 | 4/5 | 1/5 | 24 normalized aperture/s |
| 1/2 | 2 | 1/2 | 60 normalized aperture/s |
| 4/5 | 5 | 4/5 | 150 normalized aperture/s |

The exact-rational Python verifier checks 19 baselines c=n/20 for n=1,...,19, including the exact critical witness and a ceiling 1% below threshold. All 19 critical constructions have exact mean c, a true zero and admissible slopes; all 19 subthreshold ceilings have maximal means strictly below c. An independently written Node BigInt rational replay reconstructs the same 19 cases and the three named witnesses without reading Python results. Both programs were executed locally and passed. The dedicated [CI workflow](../../.github/workflows/e002_590_sharp_integration.yml) is committed; hosted verification must be inspected before claiming a hosted pass.

- [Exact Python verifier](e002_590_sharp_integration.py)
- [Independent Node verifier](e002_590_independent_replay.cjs)
- [Frozen protocol](E002_590_FROZEN.md)

## Adversarial scope and product decision

This is a **single-frame ideal linear integration theorem** with **exactly known instantaneous endpoint aperture**, a hard continuous-time speed ceiling, a perfect normalized aperture range and an exact zero event. It does **not** transfer directly to video pixels, facial fatigue, clinical sleepiness, or physical blink misses. Nonlinear pre-integration response, motion blur, gaze, glasses, eyelid geometry, illumination changes, rolling shutter, missing frames, clock uncertainty and endpoint-estimation errors require separately validated observation operators. A positive-duration closed interval can require a different threshold. A speed bound inferred only from sparse frames is **not** a hard continuous-time ceiling. This result is a sharpness correction for the Lucent conditional model, not a priority claim over general Lipschitz sampling, signal integration or optimal-control literature.

**Product consequence:** A full-duty image-integrated frame cannot be treated as an instantaneous anatomical observation. In this narrow ideal model, if L>=Lcrit(c), two different anatomical histories can produce identical measurements; the no-hidden-closure certificate must be rejected. If L<Lcrit(c), this excludes only an exact zero closure against the specified constant-open baseline and exact endpoints, not all threshold closures or other measurement confounders. In actual camera operation, absent independent calibration of image formation, geometry, endpoints and continuous-time velocity, **ABSTAIN_UNCALIBRATED**. Production remains **BLOCKED**.

**Next decisive work:** Stop treating additional synthetic constructions as human validation. Acquire consented synchronized high-speed/ordinary-camera human captures, independently calibrate shutter/clock and continuous-time eyelid motion, collect two blinded anatomical rater streams, then prospectively evaluate E002-371 and E002-590 on participant-disjoint holdout trials. This experiment obtained zero new physical captures, zero independent human rater pairs, zero hard human velocity ceilings and zero held-out physical predictions.
