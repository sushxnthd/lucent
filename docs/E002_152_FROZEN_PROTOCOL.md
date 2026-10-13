# E002-152: temporal-error gauge (frozen before local evaluation)
Date: 2026-10-13. Exact algebra/software checks only; no original-human inference.
Signal/reference: estimated ordinary-RGB pupil/full-iris diameter ratio versus true pupil/full-iris diameter ratio.
Model: observed rhat_t = r_t exp(b + u_t); b is constant within a scan, u_t is variable differential measurement error. Shared image-scale cancels only when truly common.
Gates frozen: (1) log-response identity residual <1e-12 over 10,000 seeded trials; (2) 10,000 interval checks no violations, with explicit sharp counterexamples; (3) 10,000 waveform correlation-bound checks no violations and numerical sharpness within 1e-7; (4) 10% pupil/iris static-bias example cancels temporally, 5% constriction certified for log drift <=0.02 but ambiguous for 0.06; (5) preserve all human-data gates as NOT EVALUABLE.
Direction certificate: z_t=log(rhat_t/rhat_0), if |u_t-u_0|<=delta, true x_t lies [z_t-delta,z_t+delta]. Sign certified only if interval excludes 0.
Waveform certificate: centered observed z, true x=z-e, if ||center(e)||<=E<||center(z)||, Pearson(x,z)>=sqrt(1-(E/||center(z)||)^2). Reject if E>=||center(z)||.
Product success requires independent held-out human calibration of E and delta, participant/device/lighting/glasses transfer, correlation>=0.8, waveform lag/amplitude/NRMSE gates. Otherwise abstain.
Kill if credible bounds cannot be calibrated from real paired ordinary RGB+tracker recordings.
No novelty claim for normalization, basic algebra, or geometric correlation bound.