# E002-523 | Frozen physical shutter-calibration identifiability test

Date: 2026-10-29. Continue E002-371 on `research/observability-human-boundary`, draft PR #26. Freeze this before constructing the executable, tests or results. Evidence tier: exact instrument-model falsification only; no physical camera or human evidence.

## Research question
E002-522's physical closure-duration inference requires an independently certified *pointwise* temporal shutter-response cap `q(t) <= R/T`. Does a finite sequence of accurately sampled photodiode/LED shutter-response values, even with a known total response integral, certify such a cap? Test the strongest adversary: identical **noise-free** sample values and identical normalization but arbitrarily different between-sample peaks.

## Frozen two-world construction
Use physical exposure duration T=10 ms, exact point samples at integer milliseconds 0,...,10, and q0(t)=1/T everywhere. Construct q1=q0+bump_A-dip_B with nonoverlapping triangular tents strictly inside two unsampled gaps. The added tent has width w in (1,2) ms, area alpha=1/50, and peak 2 alpha/w. The subtracted tent has width d=4/5 ms in (5,6) ms, area alpha and peak 2 alpha/d <=1/T. Thus q1>=0, integral q1=1 and q1(t_i)=q0(t_i) at every sampled time, while the true cap R1=1+2 alpha T/w diverges as w tends to zero.

Fix theta=1/5 and open aperture a_open=201/1000. World 1 aperture is zero exactly on the added-tent support of width w, and a_open elsewhere. Its weighted mean is M=a_open*(1-alpha-w/T), which is below theta for w=1/100 ms and w=1/10000 ms. World 0 aperture is constant M, giving exactly the same weighted mean with uniform q0. These two worlds agree on all sampled shutter values, normalization and measured aperture mean but have very different physical closure durations (w vs T).

## Frozen falsification and safety checks
1. Verify exact sample equality, q nonnegativity, exact integral and measured-mean equality using rational arithmetic.
2. Check the naive sampled-peak cap R_hat=T*max_i q(t_i)=1 produces a positive closure-duration lower bound **larger than the actual duration** in world 1.
3. Check the true cap R1 produces a valid lower bound; repeat for w=1/100 and 1/10000 ms without stochastic search.
4. Verify the lower-bound evaluator **abstains** if the response cap is inferred only from point samples.
5. Give an actionable physical calibration criterion: a pointwise cap can be inferred from samples only with an independently justified between-sample regularity envelope. Under a certified Lipschitz constant L, absolute sample error delta, and maximum distance h to a sample, q(t)<=max_i(y_i+delta)+L*h, hence R<=T*(max_i(y_i+delta)+L*h). L must come from separate instrument physics/measurements, not be fitted to the same finite samples. Alternative validated analog anti-alias/integrating acquisition models require their own proof.
6. No claim of a new general theorem, physical response measurement, human validation or production calibration. Do not perform another random shutter sweep. Release remains BLOCKED.

## Decision
If the counterexample holds, finite photodiode point sampling alone cannot satisfy E002-522's independent R-attestation gate. Require a certified response bandwidth/regularity or independently bounded analog acquisition chain; otherwise ABSTAIN_UNCALIBRATED. Preserve all failures and never auto-merge.
