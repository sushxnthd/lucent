# E002-700 — Clock-gap uncertainty defeats nominal closure-exclusion certificates

**Evidence tier:** exact-rational synthetic falsification; no human or physical measurements. Local execution: 2026-11-07 UTC, Python 3 standard library.

## Falsifiable question
Can an endpoint-based E002-371 certificate computed with nominal blind-gap duration h falsely exclude an actual threshold closure when the true duration is h+delta, even with exact aperture endpoints and a valid velocity ceiling?

For L-Lipschitz aperture a(t) and exact endpoints a,b over a gap of duration d, the sharp attainable minimum is (a+b-Ld)/2, provided |a-b|<=Ld. A piecewise-linear trajectory descending at slope -L to this minimum and ascending at +L attains it. Thus a nominal exclusion when (a+b-Lh)/2>theta is unsafe if (a+b-L(h+delta))/2<=theta.

## Frozen deterministic sweep
Threshold theta=1/2, velocity L=1, nominal gap h=1/2, endpoints a,b in {0,0.1,...,1}, jitter delta in {0,1/20,1/10,1/5,2/5}. Count only trajectories feasible under the actual gap. A nominal exclusion requires nominal endpoint feasibility; the robust certificate uses the actual upper-bound gap. All arithmetic is exact Fraction arithmetic.

| delta | feasible pairs | nominal exclusions | false exclusions | robust exclusions |
|---|---:|---:|---:|---:|
| 0 | 91 | 15 | 0 | 15 |
| 1/20 | 91 | 15 | 0 | 15 |
| 1/10 | 101 | 15 | 5 | 10 |
| 1/5 | 109 | 15 | 9 | 6 |
| 2/5 | 119 | 15 | 14 | 1 |

Local script stdout ended: PASS: exact rational adversarial clock-gap falsification. Reproduce with `python3 research/observability/e002_700_clock.py`. The grid is deliberately adversarial, not a probability distribution or human false-exclusion rate. Independent replay of the committed script is pending.

## Dimensionless boundary and product consequence
Define the nominal certificate margin M=(a+b-Lh-2theta)/(Lh) and relative clock-gap overrun J=delta/h. A nominally positive certificate can fail whenever 0<M<=J; equality permits touching the closure threshold. This predicts which margins are vulnerable to independently measured timing error. A safe endpoint-based certificate substitutes the **largest physically admissible blind interval**, not a nominal frame period. Unknown dropped frames, timestamp drift, exposure-edge uncertainty, or unbounded jitter force abstention. The same logic requires independently justified anatomical aperture and velocity envelopes; ordinary phone landmarks do not establish them.

## Limitations / next test
This is a conditional mathematical falsification, not an independently calibrated shutter measurement or human validation. Do not claim a physiologic velocity maximum or camera-specific clock uncertainty. Execute E002-690 synchronized physical acquisition, verify timing bounds with an independent clock, freeze E002-695 predictions before high-rate labels, and then test participant-disjoint human sequences. Lucent remains `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
