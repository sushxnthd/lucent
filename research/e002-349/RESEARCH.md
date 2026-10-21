# E002-349

Exact conditional shutter-exposure overlap bound for blink-event observation.

With frame period F, exposure width w<=F, and additive error |e|<=eps, the worst-phase maximum exposure overlap for an event of duration D is M(D)=min(w,max(0,(D-(F-w))/2)). Under this reduced scalar model, event and no-event observations are distinguishable for every phase iff eps<1/2 and D>F-w+4*eps*w. At equality, a collision exists.

Human RGB/reference validation: not performed. Mathematical novelty: not established. Do not deploy a blink or fatigue certificate without independently calibrated nuisance bounds and a prospective human holdout.

Proposed held-out experiment: freeze RGB exposure start/end, high-speed aperture reference, nuisance error budget, participant/device/light/glasses splits, geometry-only, brightness-only, missingness-only and interpolation controls; predeclare one predicted boundary crossing.
