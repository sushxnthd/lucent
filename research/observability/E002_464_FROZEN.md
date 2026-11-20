# E002-464 — frozen dynamic-reference transfer falsification (2026-10-26)

**Frozen before implementation or synthetic sweep.** Primary Lucent E002-371 physical validation remains blocked. This experiment probes a concrete unsoundness in the *reference-witness adapter*, not the shutter-gap theorem. No hardware, new human data, or novel filtering theorem is claimed.

## Question and hypotheses

E002-463 requires a bandwidth-calibration identifier but does not require a numerical upper bound on the encoder's temporal impulse-response memory, nor nonnegative normalized response weights. Can it incorrectly label a shutter-dark-gap closure when the physical aperture never crosses the threshold in that gap?

H1 (delayed encoder counterexample): ordinary camera exposures have centers 0 and 2.5 ms and width 0.3 ms, so the dark gap is (0.15, 2.35) ms. The physical aperture is 2.30 mm throughout this dark gap; a short crossing to 1.95 mm occurs at -0.40 ms, entirely before the first exposure. An independent encoder with a *pure 1.40-ms delay* reports 1.95 mm at timestamp 1.00 ms (position error 0.01 mm, clock error 0.02 ms). E002-463 will treat this as an interior positive crossing despite the true dark gap being open. This is an intentionally adversarial, nonphysiological transfer fixture.

H2 (signed-response counterexample): a sensor whose output is 2*x1 - x2 can read 1.95 mm from two strictly open physical apertures 2.20 and 2.45 mm. The output is not a valid existential crossing witness without a verified nonnegative unit-mass impulse-response assumption.

H3 (repair): a new *research-only* adapter must require a declared, numerically bounded input-support envelope: maximum causal past memory L, maximum future lead F, centered acquisition support E, and sample time uncertainty delta. The entire effective physical influence interval [t-delta-E/2-L, t+delta+E/2+F] must be strictly within the ordinary-camera dark gap; equality is unresolved. It must also require an explicitly declared nonnegative, normalized temporal response and bounded position error. The declarations are **not independently verified**.

H4 (preserved positive): with a declared nonnegative unit-mass response, L=0.10 ms, F=0, E=0, delta=0.02 ms, and 1.95±0.01 mm, the physical influence interval is [0.88,1.02] ms, strictly inside the gap, so the positive *existence* witness survives. Missing declarations, signed weights, nonfinite bounds, outside-gap support, and bad quality must fail closed.

H5 (deterministic sweep): on a grid L,F in {0.00,0.01,...,2.00} ms, with the fixed fixture, E=0, delta=0.02 ms, exactly 83*133 = **11,039** of 40,401 pairs have effective support strictly interior (with a 1e-12 ms strict-boundary guard). This is a synthetic instrument-coverage count, **not** a real-world rate.

## Logical justification and kill criteria

For a physically calibrated reference output y = integral k(s)*a(t-s) ds + e, with k(s)>=0, integral k(s) ds=1 and |e|<=epsilon, y+epsilon<=c implies that at least one anatomical aperture value a within the *entire influence support* is <=c. If that support is inside the shutter-dark gap, a positive existential crossing witness is valid. Without nonnegative normalization or bounded support, the implication fails. No finite collection of above-threshold samples establishes absence of a crossing.

A failed H1/H2 counterexample, an accepted positive witness whose declared support crosses the dark-gap boundary, or a promoted OPEN negative label kills the repaired gate. If the repaired gate refuses even the calibrated H4 positive, it fails utility. The exact grid count is frozen before running code.

Keep E002-463 files as historical evidence; add a separate E002-464 gate and tests. No physical release; all outputs `ABSTAIN_UNCALIBRATED`. No access to S21/S22. No change to Hush, no merge or force-push.
