# Exact conditional two-tier shutter boundary

For rectangular global-shutter exposures [nF,nF+w], w<=F, and a threshold-defined binary closure bout of duration D, the minimum over all event phases of the maximum exposure overlap is M(D)=min(w,max(0,(D-(F-w))/2)).

In a calibrated full-RGB linear nuisance model Y_n=b+A*xi_n+c*z_n+e_n, z_n=overlap/w, ||e_n||_2<=epsilon, the nuisance-projected contrast rho=||(I-AA^+)c||_2. An event is distinguishable from no event for every shutter phase exactly when rho*M(D)/w>2epsilon. For 2epsilon<rho, equivalently D>F-w+4epsilon*w/rho. Equality admits a common observation under bounded noise.

Two closure bouts separated by an open gap G differ from the corresponding single merged bout by a gap pulse, so the same condition with G instead of D is sharp for that binary comparison. If G<=F-w, a gap can lie wholly in shutter dead time, giving identical complete RGB frames for distinct bout counts. Separately, a fully open shutter is guaranteed within every gap exactly when G>=F+w. This stronger support certificate is sufficient, not necessary, for robust event segmentation.

For 30fps, w=10ms, epsilon/rho=.09: D and G must be strictly >26.9333ms for phase-uniform two-hypothesis discrimination, and G>=43.3333ms for a guaranteed fully open shutter. An exact collision exists between two 120ms closed bouts separated by 20ms and one merged 260ms bout.

This theorem is conditional on calibrated exposure, fixed closure template, nuisance subspace and bounded per-frame noise. No human reference validation or scientific novelty is claimed. Full proofs, simulators, exact-rational checker and frozen human protocol are in the E002-363 reproducibility package.
