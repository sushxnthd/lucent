# E002-736: exchangeable marginal calibration does not protect rare fast subgroups

Evidence tier: exact synthetic population counterexample; no human measurements. This is a new conditional-risk limitation of E002-735, not a human velocity bound.

Consider independent trajectory-level maxima V in {0,1}, with P(V=1)=p. Both calibration trajectories and a future trajectory are iid from the *same* mixture, so exchangeability holds exactly. Calibrate L=max(V_1,...,V_n). For a future trajectory known to belong to the fast subgroup V*=1, the probability that V*>L is (1-p)^n. The unconditional exceedance probability is p(1-p)^n <=1/(n+1). Thus a correct marginal rank bound can coexist with very poor fast-subgroup coverage.

For n=20 and p=0.01: P(V*>L | V*=1) = 0.99^20 = 0.8179069375972309, while marginal P(V*>L)=0.00817906937597231, below 1/21=0.047619047619047616. All are *synthetic* probabilities, not blink prevalence or observed risk.

Reproduce with Python standard library: `python research/observability/e002_736_subgroup_coverage.py`. Exact rational enumeration checks 90 (n,p) combinations, n=1..30, p in {1/100,1/10,1/2}. Local execution: PASS (90 cases). These checks verify the finite discrete construction, not external validity.

Product consequence: never present a trajectory-exchangeable, calibration-maximum rank bound as a participant-conditional or nuisance-stratum-conditional guarantee. For groups not supported by separately justified coverage, `ABSTAIN_UNCALIBRATED`; continue to block categorical closure exclusion for RGB exposure averages and unvalidated velocity ceilings. Predeclare subgroup/nuisance strata and independently evaluate each on participant-disjoint sequences before considering calibrated probabilistic claims. Groupwise calibration requires its own assumptions and adequate samples, and cannot repair unknown groups automatically.

No change to production authorization. Human/physical validation remains missing.
