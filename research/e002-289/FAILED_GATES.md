# Failed gates, including preserved checker failure
- Initial exact checker assertion failed because SymPy Rational was compared with fractions.Fraction dictionary keys. Corrected to SymPy Rational; original observed eigenvalues were {4/25:1,1:2}. This was a type-comparison bug, not a theorem counterexample.
- Human RGB/reference gate: FAIL, no human data processed.
- Primary mathematical novelty gate: FAIL, Wang et al. 2019 established the ideal conic invariant.
- Real-camera nuisance bounds: FAIL, epsilon/u/kappa hypothetical.
- Universal full-RGB impossibility: NOT CLAIMED; contour-only restricted model.
- Untouched human holdout, participant/device variation: NOT RUN.
- Dedicated remote scientific CI: UNVERIFIED.
