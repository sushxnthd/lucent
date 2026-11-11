# E002-713 — Exact phase-coverage falsification for correlated shutters

**Evidence tier:** exact-arithmetic synthetic instrument audit, not human or physical measurement.

## Question and frozen model
A closure of duration fraction w of a periodic reference cycle has an unknown onset phase uniformly distributed on [0,1). An ideal instantaneous shutter sample at phase p intersects that closure iff its onset lies in the circular arc (p-w,p]. For any predetermined sequence of phases p_i, the detection probability is **the Lebesgue measure of the union of those arcs**, not generally 1-(1-w)^n. This is exact under the stipulated periodicity, phase-uniformity, ideal timestamp, instantaneous sampling, and perfect signal classification assumptions. Exposure duration, uncertain phase, velocity, and photometric response are outside this model.

## Constructive negative controls
For w=1/10 and ten exposures: ten identical phases yield detection probability 1/10; ten evenly spaced phases yield probability 1; ten clustered phases at 0,1/40,...,9/40 yield probability 13/40. Merely collecting ten frames does not guarantee ten independent opportunities to see a hidden closure. In particular, the iid formula 1-(9/10)^10≈0.651 is invalid for deterministic correlated schedules. The code computes the exact circular union using rational arithmetic and includes regression checks plus an exhaustive small-grid discrete cross-check.

## Product consequence
Reject any multiplicative missed-closure probability derived solely from frame count or nominal FPS. The acquisition protocol must retain per-exposure timestamps and phase uncertainty; absent independently validated phase randomization and a closure-onset model, report **ABSTAIN_UNCALIBRATED**. This audit does not rehabilitate brightness-based blink exclusion (E002-711), nor infer a human velocity ceiling (E002-709).

## Falsification and next physical test
Drive a calibrated occluder at independently timestamped onset phases. Compare repeated, clustered, evenly spaced, and randomized camera triggers at equal frame counts; record optical detector and camera exposure timestamps, rolling shutter, clock drift, blur, illumination, and missed frames. Freeze shutter schedules before labels. An unseen-condition holdout should vary period, clock drift, and exposure phase. Any false exclusion invalidates the corresponding certificate. Human participant-disjoint testing follows only after the instrument passes. No physical or human result is claimed here.

## Reproduce
`python research/observability/e002_713_phase_coverage.py` (Python standard library only).
