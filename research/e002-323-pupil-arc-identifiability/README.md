# Lucent E002-323: pupil-arc observability boundary

Conditional three-point geometric result, NOT an ordinary-RGB validation. Given known exact chord half-width a and measured sagitta shat with |shat-s|<=epsilon, the circle radius is R=(a²+s²)/(2s). A finite upper bound exists iff shat>epsilon (for a feasible minor arc).

For centered measurement with true radius R, visible arc span phi, and error epsilon, the sharp finite-radius boundary is phi=2 acos(1-epsilon/R). At R=20 pixels and epsilon=0.2 pixels: 16.219228911988367 degrees. For <=10% upper radius error the exact boundary is 51.80323311930823 degrees. Independent checker: 400 randomized feasible intervals and four nuisance controls passed. Frozen holdouts 15,20,49,55 degrees passed.

NO human RGB/reference evidence, no calibrated pixel-level arc extractor, no novelty claim. NIST Hopp 1994 already studied three-point circle fitting arc-angle sensitivity. See THEOREM, PROTOCOL, PRIOR_ART, FAILED_GATES and PRODUCT_RULES.

Run: python independent_checker.py (standard library only).