# E002-422 — unequal boxcar means yield a sharp full-horizon law

**Date:** 2026-10-24. **Preregistration:** `E002_422_FROZEN.md` committed at `fafa135c12cacb9b7eb62fbc9662f60d48cef555` **before** implementation or LP outcome calculation. **Evidence tier:** conditional mathematical proof, adversarial synthetic witness, independently implemented finite-dimensional LP, and hosted software verification. **Not a physical human or camera measurement.**

## New result and exact scope

E002-421 treated **equal** physical-aperture boxcar means and the unexposed gap. E002-422 handles **unequal** means `a,b` and the **entire horizon**, including both shutter windows. Assume a continuous `V`-Lipschitz aperture `x:[-E/2,d+E/2]->[0,1]`, equal-duration uniform shutters centered at `0,d`, `0<E<d`, exact calibrated scalar physical-aperture averages `a,b`, and closure `x<=theta`. Require

```
0 < theta < min(a,b) < 1
|a-b| <= V*(d-E)                 # balanced-slope regime
L = (a+b-V*d)/2 >= 0
max(a,b)+V*E/2 <= 1             # physical interior feasibility
```

Then the **sharp minimum over the full observation horizon** is

```
inf_{feasible x} min_{t in [-E/2,d+E/2]} x(t) = L = (a+b-V*d)/2.
t_star = d/2+(a-b)/(2*V)
Gamma_asym = V*d/(a+b-2*theta)
```

A conditional no-closure claim is sound **iff `L>theta`**, equivalently `Gamma_asym<1`. At equality, a threshold crossing is possible and must not be certified. When `L<=theta`, both a closure trajectory and a distinct always-open trajectory explain the same observations.

### Continuum proof

For any `t` in the unexposed gap `[E/2,d-E/2]`, the Lipschitz condition and exact exposure averages imply `x(t)>=a-V*t` and `x(t)>=b-V*(d-t)`. Their maximum is minimized at `t_star=d/2+(a-b)/(2V)`, with value `L`. The balanced-slope condition places `t_star` in the gap. For `t` inside shutter 1, averaging `x(s)<=x(t)+V*|s-t|` yields `x(t)>=a-VE/2>=L`; the last inequality follows from `a-b+V(d-E)>=0`. Likewise shutter 2 gives `x(t)>=b-VE/2>=L`. Thus the bound covers the **whole** two-shutter horizon, not merely the unexposed gap.

Sharpness is witnessed by `x_star(t)=L+V*|t-t_star|`. Because the cusp lies between shutters, both shutter integrals are exactly `a,b`. The frozen interior conditions keep the trajectory in `[0,1]`. An observationally identical no-closure world is `x_open=a` throughout shutter 1, `x_open=b` throughout shutter 2, joined linearly in the gap; its slope is at most `V` by the balanced-slope condition, and it remains strictly above `theta`. These two constructions prove the iff and indistinguishability claims. This is a restricted Lipschitz optimal-recovery result, **not a novel universal sampling theorem**.

## Frozen counterexample: a high shutter mean cannot certify the gap

| Quantity | Frozen value |
|---|---:|
| First/second exact exposure means | 0.400 / 0.300 |
| Hypothetical hard velocity bound | 50 normalized aperture units/s |
| Center separation / shutter duration | 6 ms / 2 ms |
| Closure threshold | 0.200 |
| Valley time `t_star` | 4 ms |
| **Sharp minimum `L`** | **0.200** |
| Unsafe shortcut `max(a,b)-Vd/2` | **0.250** |
| Independent numerical LP minimum | **0.200** |
| Authorized product certificates | **0** |

The unsafe max-mean shortcut would claim `0.250>theta` and certify, yet a V-valley touches `theta` at 4 ms while producing both exact shutter averages. A distinct always-open piecewise-constant-shutter trajectory produces the **same** averages. The shortcut is therefore falsified **within this acquisition model**; it was not an existing deployed Lucent product classifier. Figure: `E002_422_UNEQUAL_ALIAS.svg`.

## Independent verification

The separate test file `test_e002_422_unequal_boxcar.py` builds a SciPy HiGHS linear program **without calling the candidate bound**. It imposes exact trapezoidal exposure integrals, independent Lipschitz inequalities and physical `[0,1]` constraints, optimizing the minimum at every mesh node. The mesh includes the potential cusp; it is a finite-dimensional check, not a replacement for the continuum proof.

- **40 seeded admissible unequal-mean configurations** reproduced `L` within `1e-7`, including safe and ambiguous cases.
- The preregistered unsafe shortcut was falsified; independent trapezoidal quadrature verified both shutter means for both worlds.
- Nonfinite/missing parameters, invalid geometry and thresholds were rejected; out-of-regime or physically infeasible inputs returned `UNRESOLVED_MODEL` and product abstention.
- **All three test groups passed** in [hosted GitHub Actions run 40116568277](https://github.com/sushxnthd/lucent/actions/runs/40116568277) on implementation/workflow commit `472575b693ac9d85579846e91a25ce6af6a47e10`. A subsequent documentation/figure rerun may be pending. The workflow also uploaded a small conditional JSON witness; no human data were uploaded.

Reproduce:

```bash
cd research/observability
python -m pip install 'numpy>=1.24,<3' 'scipy>=1.11,<2'
python -m unittest -v test_e002_422_unequal_boxcar
python e002_422_unequal_boxcar.py
```

The implementation intentionally abstains near numerical/regime boundaries even where the exact mathematical theorem permits equality; it never promotes conditional research output to physical product authorization.

## Scientific priority, nuisance scope and product consequence

This extension matters because real shutter measurements will almost never yield **exactly equal** aperture means. It replaces the unsafe use of the larger mean with a sharp rule based on the **sum of both means** and extends the certified time interval from the gap to the full two-exposure horizon **only under its assumptions**. Outside `|a-b|<=V(d-E)`, use the existing general joint-integral LP (E002-389); this formula must not be extrapolated.

The physical prerequisites remain absent: authenticated scalar optical-to-anatomical aperture transfer, known uniform shutter weighting, camera/row clock calibration, a defensible hard physiological V, two genuinely independent blinded human landmark sheets, and prospective unseen-person/device testing. Gain, glare, blur, gaze, glasses, geometry, missing frames, HDR and rolling-shutter effects can violate the acquisition model. The finite-sample human-video results in E002-417 **rejected** the two attempted optical geometry proxies and do not calibrate `a,b`. A high-speed reference frame is not automatically closure-negative (E002-416), and unresolved labels cannot be discarded (E002-419).

**Product policy stays `ABSTAIN_UNCALIBRATED` for physical hidden-closure exclusion, blink duration, PERCLOS and fatigue.** The next decisive experiment is still E002-418 qualification of two independent real human raters, E002-407/408 blinded anatomical annotation, independently calibrated exposure/clock/velocity, and held-out E002-371 predictions. Do not spend additional runs polishing the unequal-mean theorem in lieu of acquiring those observations.

**Prior art:** Micchelli, Rivlin & Winograd (1976), *The optimal recovery of smooth functions*; Kwon et al. (2013), high-speed eyelid kinematics; Godfrey et al. (2019), 240-fps eyelid dynamics. The contribution here is a sharp acquisition-model-specific decision boundary and a reproducible negative control, not priority over classical optimal recovery.
