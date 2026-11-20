# E002-483 RESULT — complementary temporal gates can resolve one exposure alias, conditionally

**Date:** 2026-10-27. **Kernel:** E002-371. **Evidence:** exact synthetic instrument model + local Node tests + independent Python rational replay. **Not** a physical camera, human result, medical measurement, or a new general theorem. [Frozen protocol](E002_483_FROZEN.md) was committed before code at `8affbe4853a3e49ddebe842446dc7b4ecc1c8ad0`.

## Scientific question and falsifiable answer
E002-482's two aperture trajectories have the same **20-ms full-exposure scalar average = 1 mm**, despite the moving world reaching zero aperture at 15 ms and the stationary world remaining at 1 mm. This follow-up tests a genuinely different measurement design: **two independent 10-ms temporal gates**. It does not pretend a normal single RGB exposure yields both channels.

At zero common phase error, the stationary gates measure (1,1) mm and the moving gates (1.5,0.5) mm. Define `C=(y1-y2)/(y1+y2)`, with each channel subject to independently bounded gain `g in [1-d,1+d]` and additive error `e in [-q,q]`. For positive signals the exact adversarial interval endpoints are obtained by opposite extreme gain/error choices in the two gates. At the frozen `d=0.10, q=0.03 mm-equivalent`:

| World/condition | Adversarial contrast interval or margin |
|---|---:|
| Stationary | [-0.130000, +0.130000] |
| Moving, phase 0 ms | [+0.389474, +0.600000] |
| Contrast separation margin, phase 0 | +0.259474 |
| Moving vs stationary, phase -2 ms | +0.185574 margin |
| Moving vs stationary, phase +2 ms | +0.203333 margin |
| Worst 4,001-point grid margin over phase [-2,+2] ms | +0.185574 |
| Conservative continuum margin lower bound | **+0.185374** |
| Phase -5 ms / +5 ms | **NOT CERTIFIED** (margins -0.145730 / -0.121304) |
| Independent gain drift 30% at phase 0 | **NOT CERTIFIED** (margin -0.130000) |
| Independent additive error 0.25 at phase 0 | **NOT CERTIFIED** (margin -0.192105) |

A *positive* margin means the two specified synthetic worlds have disjoint allowed contrast intervals. A nonpositive margin means this particular contrast test cannot certify separation, **not** that their full physical images are identical.

## Why the continuous-phase claim is conservative
For either 10-ms gate mean, `dm/ds = (a(s+10)-a(s))/10`. Since the frozen synthetic aperture lies in [0,2] mm, `|dm/ds|<=0.2 mm/ms`. At `s=0`, moving means are (1.5,0.5), so over `|s|<=2` they are bounded below by (1.1,0.1). In the lower adversarial contrast, the channel bounds are `x=0.9*m1-0.03` and `y=1.1*m2+0.03`; hence `x+y>=1.10`, `|x'|<=0.18`, `|y'|<=0.22`, and `|C_lower'|<=2*0.22/1.10=0.4 per ms`. The 0.001-ms grid's nearest point is at most 0.0005 ms away, so subtracting 0.0002 from the minimum sampled margin gives a valid continuum lower bound **within this frozen model**. The stationary contrast upper bound is constant 0.13.

The result is not a general identifiability theorem for arbitrary eyelid trajectories. Other waveforms, nonuniform shutter weights, spatial image formation, unmodeled brightness, or independent gate jitter may defeat it.

## Reproducibility and falsification
The standalone Node model uses exact piecewise-linear integration, 4,001 phase samples and worst-case channel nuisance bounds. **12/12 local Node adversarial tests passed**, including an independent 100,000-step numerical quadrature check. A separately implemented Python `fractions.Fraction` replay recovered exact rational margins at -5,-2,0,+2,+5 ms, including `493/1900` at phase zero and the two failed +/-5-ms controls. Hosted GitHub Actions success must be checked separately.

[Simulator](e002_483_temporal_gates.cjs) · [Tests](test_e002_483_temporal_gates.cjs) · [Independent replay](e002_483_independent_replay.py) · [Human protocol](E002_483_HUMAN_STUDY.md).

## Product decision and physical gate
**A temporal contrast instrument may distinguish this constructed hidden-closure alias when independently measured timing and nuisance budgets hold. A normal single-exposure phone camera does not provide this information.** Therefore this is a laboratory acquisition design and falsification aid, not a new supported Lucent phone measurement.

A physically credible claim requires independently timed optical shutter/row measurements, measured gain/offset/blur uncertainty, a moving-aperture reference, and blinded anatomical high-frame-rate human sequences. The [2026 FaceBase eyelid data](https://doi.org/10.25550/88-28BJ) are restricted-access and not acquired. E002-483 obtained **zero** new physical shutter acquisitions and **zero** new human anatomical reference sequences. E002-371 remains physically unvalidated. Hidden closure, blink duration, PERCLOS, fatigue and medical outputs remain `ABSTAIN_UNCALIBRATED`. No deployment or merge is justified.
