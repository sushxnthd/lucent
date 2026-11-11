# E002-610 | Frozen radiometric-nuisance falsification of cross-camera aperture witnesses

Date: 2026-11-02. Parent E002-609 / E002-608. Branch `research/observability-human-boundary`, draft PR #26. Evidence tier: **synthetic instrument model, no physical/human validation**.

## Specific falsifiable question

E002-609 needs a physically defensible upper bound on the **linear anatomical aperture exposure average**, not a dark-pixel score. Under an explicitly stipulated, independently calibrated linear radiometric model, can bounded time-varying illumination and background/gain uncertainty yield such an upper bound, and exactly when does the bound become uninformative? This is a nuisance stress test and prospective instrument requirement, **not a new theorem or a claim that real eyelid images obey the model**.

Model: normalized aperture `a(t) in [0,1]`, illumination `L(t) in [Lmin,Lmax]`, linear sensor response `y = b + g * average(L(t)*a(t))`, `g in [gmin,gmax]`, `b in [bmin,bmax]`, and measured exposure signal `y in [ymin,ymax]`. Assume `0 < Lmin <= Lmax`, `0 < gmin <= gmax`, `0 <= bmin <= bmax`, and that all intervals are *independently* certified for the entire exposure. Then the conservative anatomical mean upper bound is `m_hi = min(1,max(0,(ymax-bmin)/(gmin*Lmin)))` whenever input intervals are physically feasible. It is a **model bound**, not an observed anatomical aperture. Reject/abstain on inconsistent calibration, nonlinear/gamma-compressed signal, missing bounds, or any unresolved geometry, brightness, blur, gaze, glasses, missingness, clock, rolling shutter, occlusion, saturation or sampling nuisance.

## Precommitted tests and predictions

1. Hypothetical `y=[0.15,0.15], b=[0,0.01], g=[0.98,1.02], L=[0.9,1.1], tau=0.20`: `m_hi=25/147` (0.170068...), therefore conditional `MEAN_WITNESS`.
2. Widen only `Lmin` to 0.5: `m_hi=15/49` (0.306122...), therefore `NO_MEAN_WITNESS`, never proof of absence. With `Lmin=0`, `ABSTAIN`.
3. Same observed `y=0.20` from two physical worlds `(a,L)=(0.2,1)` and `(0.5,0.4)` at `g=1,b=0`; an uncalibrated brightness-only closure witness is nonidentifiable.
4. Widening signal, gain, background or illumination uncertainty must never create a witness where none existed; specifically decreasing `Lmin` or `gmin` and increasing `ymax` cannot decrease the conservative upper bound.
5. 10,000 seeded piecewise-constant time-varying aperture/illumination trajectories with independent gain and background values must have **zero** cases where the actual anatomical mean exceeds the computed upper bound, when all input intervals are correctly specified. Random synthetic cases are not human miss rates.
6. All required attestations and digest references must be present and nuisances explicitly cleared, else `ABSTAIN`. A flag or digest never authenticates physical calibration. Independently implemented Node.js rational-arithmetic controls must reproduce tests 1–3.
7. Output remains `ABSTAIN_UNCALIBRATED` and release `BLOCKED` even when a conditional model witness is computed. Do not automatically feed these synthetic values into E002-609 as physically verified evidence.

## Physical study decision

If independently measured illumination/transfer lower bounds and raw linear-light response cannot be established under real eye geometry, this route is **killed for human aperture witnessing**. Instead use independent blinded anatomical annotations with conservative uncertainty and retain E002-609 abstention. For an optical phantom pilot, calibrate raw linear-light intensity with an external photodiode and variable illumination, include unseen exposure/lighting conditions, and compare the conservative bound against known motor/occluder aperture; only after a separate human anatomical transfer study can a human closure witness be considered. No physical data are available in this run.

This protocol is frozen before writing the E002-610 simulator, tests, or results.