# E002-751 | Ideal reference-detector phase-coverage experiment (2026-11-11 UTC)

## Scope and predeclared idealization
A zero-aperture pulse occupies [p,p+d] within a unit sampling interval, with samples at integer times. The detector is noiseless, point-sampled, and detects endpoints. Sweep 10,000 exact rational phases p=i/10000 for d/h = 1/4, 1/2, 3/4, 1, 5/4. This is a **synthetic instrument model**, not human or photodiode data. Code: `e002_751_phase_sweep.py`.

## Executed results
| d/h | detected / 10000 | missed / 10000 |
|---|---:|---:|
| 1/4 | 2501 | 7499 |
| 1/2 | 5001 | 4999 |
| 3/4 | 7501 | 2499 |
| 1 | 10000 | 0 |
| 5/4 | 10000 | 0 |

The extra one detection for subperiod pulses is the endpoint-aligned phase p=0, and is a **grid artifact**, not a continuous-random-phase probability. Under uniform continuous phase the detection probability is min(1,d/h); adversarially, any d<h can be missed. Exact enumeration assertions and adversarial-phase checks passed locally using Python standard library.

## Scientific interpretation and release consequence
Sampling frequency alone does not establish negative-label sensitivity. Even an ideal point sampler misses 49.99% of half-period pulses on this finite grid. Analog bandwidth, thresholding, shutter transit, clock uncertainty, and exposure integration can further degrade detection; this model cannot quantify those degradations. E002-744's reference-negative labels remain UNKNOWN unless minimum closure dwell or independently bounded detector sensitivity makes negative labels defensible. Do not use this synthetic result as evidence of a physiological eyelid-velocity ceiling, a real detector's miss rate, or product readiness.

Evidence T1 synthetic; no human or physical capture. Product ABSTAIN_UNCALIBRATED; release BLOCKED.
