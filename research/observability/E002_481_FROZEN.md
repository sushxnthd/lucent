# E002-481 FROZEN — class-limited detectability despite empty pointwise optical core

Date: 2026-10-27. Kernel E002-371. **Preimplementation prediction.** Evidence tier: constructed stationary periodic shutter and independently bounded pulse-timing model only. No new camera or human measurements. This tests a *different question* from E002-480: whether an optical response island known a priori to have minimum **width** and **amplitude** can be robustly detected even when the intersection of all possible pulse supports is empty.

## Frozen model

Period T=1000/240 ms. Optical pulse width w=0.006 ms, each independently measured pulse start has uncertainty |e|<=u=0.004 ms. A shutter-response island has width L and minimum sensitivity amplitude A=0.20; an observed pulse contrast is A times pulse/island overlap divided by w, plus bounded additive error |eta|<=0.002. Positive detection requires contrast **strictly greater** than theta=0.04. Assume stationary periodic rectangular nonnegative island, linear response, no unmodeled shutter tails, no saturation, and calibrated contrast; these are not established for a real sensor.

For a single pulse nominally centered on an island, the minimum overlap across allowed timing errors is predicted to be q_inf=max(0,min(w,L,(w+L)/2-u)). The E002-480 pointwise core width max(0,w-2u) is zero, but this does not automatically preclude detection of a sufficiently wide island. For N equally spaced pulse centers across one period, the predicted **worst-case over unknown island phase and independent allowed timing errors** maximum guaranteed overlap is q_N=max(0,min(w,L,(w+L)/2-u-T/(2N))) under this isolated-island model. The noise-robust class-detection condition is A*q_N/w - 0.002 > 0.04. Equality is NOT a pass.

## Predictions before implementation

1. L=0.0005 ms: no guaranteed geometric intersection even with arbitrarily dense phase scans; this agrees with E002-480.
2. L=0.003 ms: centered pulse has positive guaranteed overlap 0.0005 ms, but its worst-case contrast after negative noise is only ~0.01467 <0.04. **Geometry without detection**.
3. L=0.006 ms: centered pulse has guaranteed overlap 0.002 ms, robust contrast 0.064667 >0.04 despite zero pointwise core. Thus blanket inference from zero pointwise core to impossibility of all width-restricted detection is false.
4. With L=0.006 ms, equally spaced phase scans require **N>=2816 nominal pulse centers per period** for strict worst-case detection at the frozen threshold. N=2815 fails. At N=668 (roughly E002-480 eightfold grid per period) it fails.
5. In the infinite-density limit, width L must be strictly greater than 0.00452 ms to guarantee detection at the stipulated A, u, w, noise and threshold; equality fails.
6. If A has no independently authenticated positive lower bound, or linearity, timing, clock correlation, gain, phase attribution, or noise conditions fail, **no physical shutter-support or hidden-closure product claim is authorized**. Only a restricted sensitivity-class certificate could eventually be tested, and only after external physical calibration.

## Falsification and verification

Implement an exact-rational Python calculator and independently enumerated interval-overlap adversary (including offset endpoints and worst island phase) for small-scale and frozen threshold checks. Test strict equality, monotonicity in u/N/L/A/noise, period wrap, nonfinite values, no island, and claim abstention. Record failed predictions without silently changing these constants. Do not confuse conditional synthetic design limits with authenticated physical acquisition.

No new human dataset archaeology; E002-459 participant rows remain sealed. No physical acquisition is available. The immediate research value is to sharpen the **instrument acquisition decision**: a physically tested minimum detectable shutter-response class may be meaningful even when exact-zero response cannot be certified.