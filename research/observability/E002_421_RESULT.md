# E002-421 — sharp two-boxcar gap law and a falsified ratio-based shortcut

**Date:** 2026-10-24. **Preregistration:** `E002_421_FROZEN.md` was committed first at `bae8a9569194d8af104e571e1cf16357d2d4027d`, before E002-421 code or outcome calculation. **Evidence tier:** analytical proof plus independently computed synthetic numerical verification. **No real human annotation, real-camera shutter calibration or external replication.**

## Scientific result: exact conditional boundary

Let `x:[-E/2,d+E/2] -> [0,1]` be `V`-Lipschitz, with `0<E<=d`. Suppose *calibrated scalar physical-aperture* **uniform boxcar averages** over `[-E/2,E/2]` and `[d-E/2,d+E/2]` are both exactly `m`. Assume `0<theta<m<1`, `m-Vd/2>=0` and `m+VE/2<=1`. For the unexposed gap `G=[E/2,d-E/2]`,

```
inf_{all feasible x} min_{t in G} x(t) = m - V*d/2.
Gamma = V*d / (2*(m-theta)).
```

The **conditional** no-closure statement over G is therefore sound **if and only if `Gamma<1`**, with threshold crossing defined by `x<=theta`. When `Gamma>=1`, the observations permit both a closure and an always-open world. The exposure duration E does not appear in this *particular sharp gap law* provided the windows are nonoverlapping and the interior physical feasibility conditions hold. This does **not** mean shutter duration is irrelevant for other target intervals, nonuniform kernels, unequal means, RGB images or shutter uncertainty.

### Proof (continuum, not a grid approximation)

Fix `t in G`. For any `s` in the first exposure, `s<=t`; Lipschitz continuity implies `x(s)<=x(t)+V(t-s)`. Averaging and using the exact mean `m` gives `m<=x(t)+V*t` because the first exposure is centered at zero. For the second exposure, `s>=t`, hence `m<=x(t)+V*(d-t)`. Thus

```
x(t) >= max(m-V*t, m-V*(d-t))
     = m - V*min(t,d-t)
     >= m - V*d/2.
```

The bound is attained by `x_valley(t)=m-Vd/2+V*abs(t-d/2)` over the full observation horizon. Its two shutter means are exactly m by symmetry and linearity on each exposure. The frozen interior conditions ensure it stays in [0,1]. It crosses the threshold precisely when `m-Vd/2<=theta`. The alternative `x_open(t)=m` is always above theta and yields the same two shutter means. This proves necessity, sufficiency and sharpness **within the stated model**.

## Preregistered falsification of the earlier witness-family ratio

E002-420 correctly warned that its construction-specific ratio `R=V*(4*d-E)/(8*(m-theta))` is **not** a universal certificate. E002-421 gives an explicit counterexample to the tempting shortcut `R<1 => safe`:

| Frozen quantity | Value |
|---|---:|
| Both exposure means | **0.315** |
| Closure threshold | 0.200 |
| Hypothetical V | 60 normalized units/s |
| Frame-center separation d | 4.166667 ms (240 Hz) |
| Boxcar duration E | 2.000 ms |
| E002-420 witness-family R | **0.956521739 < 1** |
| Sharp law Gamma | **1.086956522 > 1** |
| V-shaped minimum | **0.190 < 0.200** |
| Open-world minimum | 0.315 |
| Independent numerical means in both worlds | **0.315, 0.315** |
| Physically validated human V or shutter | **None** |

**P1–P4 held** under the frozen assumptions. The old R ratio was never a deployed general classifier; this is a negative control against *misusing* it, not a demonstrated regression in production.

## Independent verification and falsification controls

A separately written `scipy.optimize.linprog` oracle uses piecewise-linear aperture nodes, exact trapezoidal integration of both shutter windows, bounds `0<=x<=1`, and adjacent Lipschitz constraints. It does not import the candidate sharp formula to construct its LP. On **24 seeded admissible parameter cases**, LP minima at the gap midpoint agreed with `m-Vd/2` to within `1e-7`. Both conditional classes occurred. Independent midpoint quadrature checked the frozen 240-Hz witness and all randomized V-valleys. Another 1,000 synthetic convex-combination trajectories respected the lower bound; these are **not** independent humans or cameras. Invalid exposure geometry, nonfinite speed, impossible [0,1] bounds and missing usable parameters were rejected. The candidate always emits `ABSTAIN_UNCALIBRATED` as its product decision, even when the conditional research decision is `CERTIFY_NO_CROSSING`.

Local reproduction (Python 3.11, NumPy, SciPy):

```bash
cd research/observability
python -m pip install 'numpy>=1.24,<3' 'scipy>=1.11,<2'
python -m unittest -v test_e002_421_sharp_boxcar_gap
python e002_421_sharp_boxcar_gap.py --bins 20000
```

**Local result:** four test groups passed on 2026-10-24. Dedicated GitHub Actions verification is tracked separately; no hosted success is claimed before that workflow concludes. Technical figure: `E002_421_SHARP_GAP.svg`.

## Robust nuisance qualification and scope restrictions

If the **true** means are independently known only to exceed `l` and the center separation is independently known only to satisfy `d<=d_max`, then `x(t)>=max(0,l-V*d_max/2)` is a *sufficient* conservative bound for the actual gap. It is not a general sharp interval-observation result. The velocity V must be an independently justified **hard** upper bound, not a sample mean or empirical maximum. Clock jitter, rolling shutter, HDR, nonuniform temporal response, uncalibrated geometry, gaze, blur, gain, glare, glasses, dropped frames and nonlinear RGB-to-aperture transfer can invalidate the model. E002-403's temporal-kernel warnings and E002-389's general joint-integral LP remain necessary. The theorem covers **only the unexposed gap**, not possible crossings inside either shutter interval or outside the observation horizon.

Any unsupported physical nuisance or provenance returns `ABSTAIN_UNCALIBRATED`; conditional synthetic success is never a real-world measurement authorization.

## Priority and completion boundary

This is a closed-form **special case** of classical Lipschitz optimal recovery, not a claim to have invented optimal recovery, interval integration or a new universal sampling theorem. Primary-literature anchors:

- Micchelli, Rivlin & Winograd (1976), *The optimal recovery of smooth functions*, Numerische Mathematik (https://research.ibm.com/publications/the-optimal-recovery-of-smooth-functions).
- Bojanov (1994), *Optimal Recovery of Functions and Integrals* (https://doi.org/10.1007/978-3-0348-9110-3_11).
- Kwon et al. (2013), *High-speed camera characterization of voluntary eye blinking kinematics* (https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/).
- Godfrey et al. (2019), 240-fps smartphone eyelid dynamics (https://pubmed.ncbi.nlm.nih.gov/30893187/).

The contribution is an exact and falsifiable **measurement-qualification boundary** for this specific acquisition model. It has not passed a comprehensive publication-priority audit. E002-417's automatic geometry surrogates remain rejected. Next: two independent actual blinded human landmark sheets; independent shutter, clock, geometry and physiological velocity calibration; and frozen unseen-participant/device tests with unresolved-reference outcomes retained under E002-419. **E002-371 remains physically unvalidated.** Do not authorize blink duration, PERCLOS, fatigue or hidden-closure exclusion in a real product. Hush's branch/PR are untouched.
