# E002-327 — Joint nuisance-budget interval gate (2026-10-20)
Status: exact conditional polyhedral identification; synthetic only; human validation 0; novelty not established.
Question: can an exposure-integrated pupil/iris log-ratio temporal amplitude be certified after jointly bounding gaze, aperture, photometric, clock, and optical nuisance?
Model: y = alpha*h + N*beta + e, l<=beta<=u, |e_i|<=eta_i. Missing frames remove rows. All bounds must be independently calibrated.
The exact identified set of alpha is the projection of the feasible polyhedron and is computed by two LPs. Positive certification iff alpha_min>0, negative iff alpha_max<0; otherwise abstain.
Synthetic frozen case: y=(.06,.06), h=(1,1), N=[(1,1),(1,-1)], eta=.01 each, gaze beta in [-B,B], brightness beta in [-.02,.02]. Alpha interval=[.05-B,.07+B], sharp critical B=.05. B=.04 certifies positive; B=.055 abstains. Unbounded gaze nuisance makes alpha unidentifiable at any frame rate.
Results: 4 exact-rational endpoint witnesses; 400 randomized feasible trials; 200 independent vertex-enumeration checks; geometry, brightness, missingness and smoothness controls passed.
Product: reject uncalibrated rapid pupil and five-second fatigue inference; conditional interval-valued ocular measurements only after human holdout calibration. Prefer independent RGB blink validation.
Full package: lucent_e002_327_interval_instrument.zip in conversation artifact.
