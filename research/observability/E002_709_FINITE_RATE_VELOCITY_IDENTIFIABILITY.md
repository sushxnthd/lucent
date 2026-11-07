# E002-709: finite-rate velocity nonidentifiability

Evidence: constructive mathematical counterexample, not human or physical measurement.

Suppose aperture x(t) is observed exactly at finitely many times t_i. Even when every sampled value equals a>0, there exist smooth trajectories matching every observation, with an unobserved full closure and arbitrarily large instantaneous speed. Choose a smooth bump b supported inside one gap (t_i,t_{i+1}), with 0<=b<=1 and max b=1. Set x(t)=a(1-b(t)) inside that gap and a outside. The path reaches zero yet matches every observed sample. Shrinking the bump width epsilon while retaining amplitude a makes peak speed proportional to a/epsilon, unbounded as epsilon approaches zero. A constant-open trajectory produces the same observations.

Thus high-frame-rate samples or finite differences alone cannot establish a deterministic continuous-time velocity ceiling. Such a ceiling must be independently justified by physiology, instrument constraints, or a validated model. Empirical finite-sample velocity quantiles are not hard ceilings. Even reference video can miss a closure between exposures.

Define R=V_ext*h_ref/A, where V_ext is an externally justified maximum speed, h_ref is the reference-camera maximum true blind interval, and A is required aperture excursion. A symmetric full close-and-reopen requires at least 2A/V_ext, hence R>=2 permits a hidden closure under a Lipschitz-only model. If V_ext is unavailable, R is undefined, not zero.

Prospective test: use independently timed narrow-pulse physical occluder controls phase-shifted through reference-camera blind gaps. Record actual exposure boundaries, rolling shutter, missingness and timestamp uncertainty. Freeze predictions before revealing pulse phase. Treat reference-negative intervals as indeterminate unless independently justified. Do not infer a deterministic physiological ceiling from maximum observed frame-to-frame differences. For probabilistic claims, preregister participant-disjoint calibration and explicit coverage assumptions.

Product consequence: deterministic CERTIFY_NO_CLOSURE remains unavailable without external velocity calibration; ABSTAIN_UNCALIBRATED and production BLOCKED. No physical or human validation was performed. This is an elementary identifiability result, not a novelty claim.
