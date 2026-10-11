# E002-107 — Frozen stationary phase-lock adversarial falsification
Date: 2026-10-11. Classification: DISCRIMINATION / SURPRISE.
Parent: E002-106 frozen human-data forward-vs-reverse nuisance test. This experiment is synthetic, not an independent human replication.

## Mechanistic rival
An onset-shaped coefficient advantage may arise *without any onset transient* if off-target periodic signals begin at stimulus-locked phases, finite windows are ~4.95 s, and target 1-Hz nuisance regressors are nonorthogonal. The earlier synthetic E002-106 no-transient test randomized phases at 2 Hz only, and could have averaged away a phase-locked effect.

## Frozen design
Use t = 0,0.05,...,4.95 s (100 samples), y = 1500 + 25 sin(2π f t + φ), with no onset, camera artifact, or measurement noise. Frequencies f = [1.1111,1.25,1.4286,1.6667,2,2.5,3.3333,5] Hz. Phases φ = [0,π/2,π,3π/2]. Fit exactly E002-106 OLS columns [1,t,sin(2πt),cos(2πt)] plus either exp(-t/1.5) or exp(-(4.95-t)/1.5). Divide fitted 1-Hz amplitude by median(y). For each f and phase, record forward/reference, reverse/reference and difference. If reference amplitude < 1e-12 dimensionless, flag numerical-zero and do not use ratios; retain raw amplitudes. Also test phase grid of 721 equally spaced phases [-π,π] as exploratory boundary mapping. Add 1000 seeded Gaussian-noise replicates per condition (σ=5) for stability, exploratory only.

## Frozen primary test
At phase 0, does a *stationary* no-transient signal generate E002-106's 24/24 directional signature (forward/reference<1 and reverse/reference>1) for >=6 of 8 off-target frequencies? If yes, pure phase-lock/leakage is a sufficient synthetic counterexample to attributing the directionality to a physical onset transient. If not, that simple rival fails its frozen criterion, but phase-lock may still explain subsets. Secondary diagnostic: across 4 cardinal phases count frequencies with E002-106 directional signature, identify zero-amplitude instability and dependence on stimulus phase.

## Uncertainty and interpretation
This is a deterministic linear-algebra counterexample search; it cannot estimate human frequency content, stimulus phase, camera artifact or physiology. Strong negative or positive results must not alter E002-106 frozen human-data PASS. No tuning of tau, frequency set, or gate after scoring. Record anomalous near-misses and the cheapest discriminating original-data test: estimate off-target phase relative to stimulus and repeat correction on GP3 reference and camera traces.

## Reproducibility
Python NumPy implementation, independent direct normal-equations check on well-conditioned cases, code/test SHA256, original JSON results, state update. Keep untouched human-data results untouched.
