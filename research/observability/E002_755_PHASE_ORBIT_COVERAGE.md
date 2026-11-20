# E002-755 | Phase-orbit coverage is a prerequisite for negative reference evidence

**Evidence tier:** T1 exact synthetic; no hardware or human observations.

## New falsifiable result

For a detector sampled at integer phases modulo N, a pulse-onset phase walk with increment s visits exactly N/gcd(N,s) distinct phases, independent of the number of repeated injections after one full orbit. For N=100 and 10,000 injections, increments 100, 50, 25, 20, and 37 cover respectively 1, 2, 4, 5, and 100 phases. Consequently, the number of trials is not a proxy for phase coverage. This generalizes the E002-754 locked-versus-coprime example to an exact orbit-size law. The phase-coverage limitation is elementary modular arithmetic, not a claim of novel number theory.

For an ideal point detector with closure interval [0,25) modulo 100, an increment of 37 forces exactly 2,500 detections per 10,000 injections, regardless of starting phase; increment 100 can yield zero or 10,000 detections. These counts are model predictions, not estimates of instrument sensitivity.

## Physical falsification and decision rule

Measure actual rather than commanded relative phases. Before looking at detector responses, compute occupied phase bins and the largest unvisited cyclic run, including independently characterized timestamp error. Withhold pulse-width/phase combinations and rerun after restart/relocking. A claimed phase-swept reference sensitivity must be rejected if the measured phase orbit collapses, timestamp uncertainty makes phase-bin assignment ambiguous, or held-out short pulses go undetected. No finite phase grid alone proves continuous-phase sensitivity: separately bound phase interpolation, pulse width, exposure kernel, and response threshold.

**Product consequence:** Reference-negative labels remain uncertain unless pulse sensitivity is established for the actual clock/exposure/phase regime. Preserve `ABSTAIN_UNCALIBRATED` and production `BLOCKED`. Positive verified reference closures can still falsify Lucent exclusion claims.

## Reproduction

Run `python3 research/observability/e002_755_phase_coverage.py`. It uses Python standard-library integer arithmetic, enumerates every initial phase and asserts orbit coverage and predicted detection counts. This script has been committed but has **not** been executed in the connected GitHub runtime; no hardware validation is claimed.
