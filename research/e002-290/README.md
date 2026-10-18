# E002-290: Joint-nuisance observability certificate

**Status: exact conditional theorem, synthetic verification only; NO HUMAN RGB EVIDENCE.** The result is a classical matched-subspace / convex-duality application, not a novel generic theorem.

For a locally linearized RGB feature vector `z=a*s+N*theta+e`, `||e||_inf<=eta`, the no-change and fixed-change observation sets are disjoint **iff** `|a|*d_inf(s,N)>2*eta`, where `d_inf(s,N)=min_theta ||s-N*theta||_inf`. The dual certificate is `max{w^T*s:N^T*w=0,||w||_1<=1}`.

If pupil-specific optical magnification is an unrestricted nuisance with the same feature signature as physiology, `d_inf(s,[N,s])=0` exactly: these features cannot certify pupil dynamics at any amplitude. If independently calibrated to `[-b,b]` per hypothesis, the sharp condition is `max(0,|a|-2b)*d_inf>2*eta`.

Synthetic six-feature example: d=5/23 with independently measured gaze; d=0 without gaze or with unrestricted pupil-specific optical magnification. For hypothetical eta=0.01 and b=0.03, critical dimensionless amplitude is 0.152. Unseen synthetic nuisance holdout: critical amplitude 9263/67500 = 0.1372296296. These are NOT camera- or physiology-calibrated thresholds.

Run: `pip install numpy scipy sympy && python experiment.py && python independent_checker.py`.

See THEOREM.md, HUMAN_FROZEN_GATE.md, PRIOR_ART.md, FAILED_GATES.md and PRODUCT.md. The local expanded package includes 400 randomized primal/dual LP checks, exact counterexamples and SHA256 hashes; this branch stores a minimal independently runnable core. The repository's inherited CI is not claimed to run this experiment.