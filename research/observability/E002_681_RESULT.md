# E002-681 | Finite-rate eyelid velocity ceilings are not identifiable from samples

**Evidence tier:** analytic counterexample with executed standard-library regression; no human or physical data. This is a negative identifiability result, not a claim that actual human eyelids achieve the constructed motion.

## Proposition (sampling cannot certify a hard instantaneous speed ceiling)
Given any finite strictly increasing sampling times with at least one positive gap, an aperture trace taking values in [0,1], and any proposed finite speed ceiling M, there exist two continuously differentiable aperture trajectories that agree at every sampled instant, yet one has instantaneous speed exceeding M. Thus a ceiling inferred solely from finite samples is not a deterministic upper bound without additional regularity or physical assumptions.

**Construction.** Begin with constant baseline a(t)=1/2. Choose adjacent sample times t0<t1 and center c=(t0+t1)/2. Pick 0<w<(t1-t0)/2 and amplitude 0<A<=1/2. Define b(t)=A(1-((t-c)/w)^2)^2 for |t-c|<w, and zero otherwise. Then a+b lies in [0,1], is C1, and agrees with a at every sampled time. Its maximum absolute derivative is 8A/(3 sqrt(3) w), which exceeds any fixed M as w tends to zero. Both traces can have identical sample values and arbitrarily different peak velocities. This remains true for arbitrarily high but finite reference FPS. The argument also holds for finitely many sample-derived difference quotients.

**Scope:** This does not rule out a separately justified physical speed bound; it rules out deriving a hard bound from a finite sample maximum alone. Finite-duration exposure measurements impose different linear constraints and require their own null-space construction. The present result is explicitly for instantaneous samples, not a proof about all exposure kernels.

## Reproduction
Run `python research/observability/e002_681_speed_nonidentifiability.py`. The executed test verifies that three C1 bumps with widths 10, 1 and 0.1 ms all leave 30-Hz samples unchanged while maintaining a nonzero hidden peak; the analytic derivative establishes unbounded speed escalation. Test was executed locally; no hosted CI or independent replay.

## Operational consequence
Never promote a measured high-speed finite-difference maximum to the hard E002-371 Lipschitz constant. An independently established physical ceiling and its validity domain are prerequisites for deterministic human closure-exclusion certificates. Otherwise report conditional curves as a function of assumed V, or abstain. Existing E002-671 protocol remains frozen. No product claims unlocked; `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.

## Next empirical action
Obtain synchronized ordinary/high-speed human recordings with shutter timing and independent physical velocity assumptions; test conditional exclusion against blinded anatomical reference. If no independently defensible hard ceiling exists, pursue calibrated statistical risk statements rather than deterministic absence.
