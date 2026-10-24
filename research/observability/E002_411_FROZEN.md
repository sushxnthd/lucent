# E002-411 — frozen sparse-pulse shutter-kernel identifiability experiment (2026-10-24)

**Status: frozen before implementing/running E002-411 code.** Persistent branch `research/observability-human-boundary`; Lucent draft PR #25. Evidence target: synthetic optical-instrument identifiability and direct release restriction, **not** a human eyelid measurement or an actual camera calibration.

## Scientific question
Does a phase sweep of a known narrow LED pulse, combined with a normalized constant-illumination response, uniquely establish the temporal first absolute moment `M = integral |s - e/2| w(s) ds` of an unknown nonnegative normalized shutter response `w(s)`? A wrong answer can make E002-403/E002-371 falsely exclude a hidden closure.

## Frozen acquisition model and witnesses
- Exposure support [0,10] ms; independently timed, perfectly rectangular LED pulses of width 0.2 ms; phase starts 0,1,...,9 ms. Shutter response nonnegative and normalized to unit integral.
- Kernel A: uniform density on [5.5,5.7] ms. Kernel B: uniform density on [9.5,9.7] ms. Both must give identical pulse-sweep responses (all zero) and identical constant-light response (one), but `M_A=0.6` ms and `M_B=4.6` ms.
- Robustness control: each phase pulse expanded by 0.05 ms on each side to conservatively cover unknown timing jitter; neither witness may intersect the expanded pulses.
- Resolution control: a 0.1-ms phase grid with 0.2-ms pulses must distinguish the witnesses (different nonzero response locations). This does **not** establish uniqueness for arbitrary continuous kernels.
- Randomized witness family: 1,000 seeded pairs (seed 4112026), one 0.10-ms-wide rectangular kernel uniformly positioned within [5.45,5.75] ms and one within [9.45,9.75] ms; both must remain outside all sparse pulses, agree on all observed sparse responses, and have first-moment separation >=3.5 ms. The generator must use independently sampled offsets and reject overlaps.
- Independent numerical oracle: sample shutter response on a fine deterministic grid and compare numerical pulse response and first moments with analytic overlap integrals; absolute error tolerance 0.005 ms for moment and 0.01 for normalized response.

## Frozen predictions
P1: identical sparse-pulse and DC observations for A and B; their first moments differ by 4.0 ms (ratio 7.6667).
P2: both remain observationally indistinguishable after +/-0.05-ms timing-jitter expansion.
P3: the 0.1-ms phase scan distinguishes A and B.
P4: all 1,000 seeded randomized pairs satisfy the collision and >=3.5-ms moment separation.
P5: independent numerical integration agrees with analytic witnesses to frozen tolerances.
P6: the release gate rejects uncovered shutter support, missing photodiode/timing calibration, missing row calibration, and any claim that sparse pulse samples uniquely establish the first moment. A passing coverage check alone must never authorize a physical certificate.

## Interpretation and scope
Nonnegative shutter responses supported in unsampled phase gaps are observationally equivalent under this instrument, despite different `M`. This is an elementary inverse-problem non-identifiability construction, not a novel general theorem. Dense phase coverage is necessary for this specific unrestricted nonnegative-kernel measurement scheme but **not sufficient** to authenticate timing, resolve all inverse-problem ambiguities, or prove a physical first-moment bound. A conservative `M<=e/2` remains available **only if independent physical exposure support and timebase are established**.

**Product consequence:** never accept a claimed calibrated shutter first moment from coarse phase sweep or nominal FPS alone; preserve `ABSTAIN_UNCALIBRATED` until independent physical shutter, aperture geometry, and velocity calibration plus blinded human validation. No blink duration, PERCLOS, or fatigue claims.