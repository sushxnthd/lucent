# E002-554 RESULT | Finite LED flash calibration can leave a false closure exclusion

**2026-10-31. Primary E002-371 shutter-gap/eyelid-observability workstream.** Frozen at commit `a782b4a` before executable and tests. **Evidence tier: exact synthetic calibration-identifiability falsification only.** No measured shutter, human eyelid recording, photodiode trace, or physiological speed/acceleration ceiling.

## Falsified calibration shortcut

E002-553 established that shutter-kernel temporal variance affects the sharp conditional closure-exclusion envelope. E002-554 asks whether a finite LED flash calibration restricted to central exposure offsets can identify that variance. The answer is **no, even with noiseless measurements, exact clock, full-support positive shutter kernels, equal gain, equal support and equal center**.

On normalized shutter coordinate x in [0,1], construct `K_high=1+q(x)/2` and `K_low=1-q(x)/2`, where q=+1 on the first/last tenth, q=-1 on the adjacent tenths, and q=0 elsewhere. Both kernels are strictly positive, have unit integral and temporal mean 1/2. All pulse exposures entirely within [1/5,4/5] produce **identical integrals** for both kernels. Yet their variances are `137/1500` and `113/1500`; difference `2/125`. A pulse in [1/20,1/10] distinguishes them.

With true K_high on exposures [-1/2,0] and [1,3/2], actual aperture `f(t)=(t-1/2)^2`, gap [0,1], hard acceleration A=2, and threshold `theta=3/1000`, both exposure-averaged aperture measurements are exactly `439/750`. The true gap minimum is **zero**. If the lower-variance K_low is wrongly accepted from center-only calibration, the E002-553 midpoint lower envelope is `1/250=0.004 > theta`: **false exclusion of an actual hidden closure**. With the true K_high variance, the lower envelope is zero and correctly abstains.

| Exact synthetic quantity | Result |
|---|---:|
| Equal integrated gain and shutter center | 1 and 1/2 |
| True kernel normalized variance | 137/1500 |
| Wrong candidate normalized variance | 113/1500 |
| True measured mean in each exposure | 439/750 |
| Wrong-kernel lower bound | 1/250 |
| Correct-kernel lower bound | 0 |
| Closure threshold | 3/1000 |
| Actual gap minimum | 0 |

This is a finite-probe **identifiability** counterexample, not a claim that every finite pulse schedule fails. A sufficiently broad scan, a calibrated bandwidth/smoothness bound, or a validated parametric response model could distinguish or bound the kernels. The example specifically shows why matching a few pulse offsets, mean and gain cannot certify a shutter second moment.

## Verification

- [Exact Fraction executable](e002_554_calibration_identifiability.py) returns the above fractions without floating-point approximation.
- [13 adversarial Python test methods](test_e002_554_calibration_identifiability.py) passed locally, including 59 central-offset probes, a distinguishing edge pulse, positivity, equal moments and the wrong/correct decision reversal.
- [Independent Node BigInt oracle](e002_554_independent.cjs) separately integrates the piecewise kernels and quadratic trajectory. It passed locally and reproduced `m=439/750, bad=1/250, good=0`.
- [Frozen protocol](E002_554_FROZEN.md) preceded implementation. Hosted CI requires independent confirmation; local success is not hosted success.

## Physical acquisition handoff and kill rules

1. Use independently clocked LED plus photodiode, log raw/linear camera response, sensor row, exposure start/stop and pulse current. Randomize narrow pulse offsets **across the entire shutter**, not just central offsets; replicate each offset with matched dark and brightness controls. Recover a conservative *interval* for the kernel second moment, not just a best-fit point.
2. Hold out interleaved pulse offsets and shutter settings. An independently calibrated moving-aperture target tests the predicted change in exclusion decisions. The primary falsifier is an independently witnessed closure within an interval that the **conservative calibrated** envelope excludes.
3. Fail closed if the unprobed response is unbounded, clock synchronization is absent, saturation/ISP nonlinearities occur, or rolling-shutter row transfer is not established. Random offsets do not by themselves certify the unsampled kernel; a justified response regularity bound or worst-case moment interval is required.
4. Separately validate geometry, brightness, blur, missingness, gaze, glasses, and anatomical transfer. Then use the existing blinded participant-disjoint human protocol E002-548/549 and independently calibrated kinematic limits E002-550. Reference-negative frames never prove continuous-time absence.

**Product consequence:** Do not infer shutter-kernel variance from finite center-only flashes or nominal shutter support. Even after physical flash calibration, a closure exclusion is permitted only if its lower bound survives the **entire calibrated moment uncertainty set** and all anatomy/clock/nuisance gates. Otherwise return `ABSTAIN_UNCALIBRATED`.

## Evidence and novelty boundary

This is a classical inverse-problem non-identifiability construction applied to the E002-553 observability law. It is **not** a new general theorem, observed camera failure, or human blink result. Previous E002-545 randomized flash calibration and E002-553 kernel-aware curvature bounds remain relevant; E002-554 exposes a specific finite-offset coverage failure not resolved by those calculations.

Authenticated physical shutter captures **0**; independent anatomical human rater pairs **0**; certified continuous-time human motion ceilings **0**; participant-disjoint physical predictions **0**. **Production BLOCKED.** Stop additional synthetic kernel tuning; next substantive primary work must acquire real optical or independently rated human evidence.
