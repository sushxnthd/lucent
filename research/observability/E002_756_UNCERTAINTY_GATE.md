# E002-756 | Nominal camera-gap certificates fail under independently bounded nuisance uncertainty

**Tier T1: synthetic exact-arithmetic falsification. No human or physical data.**

## Frozen adversarial experiment
The two observed positive endpoint apertures are nominally 3/5 each, nominal gap 1, nominal Lipschitz speed bound 1. Every nominal certificate excludes a hidden zero because 6/5 > 1. In four adversarial conditions, separately enlarge admissible aperture error, clock gap, velocity ceiling, and all three jointly. Under these stipulated uncertainty sets, a zero-reaching nonnegative piecewise-linear trajectory exists. The robust certificate must abstain in all four conditions. In the unchanged control it excludes.

## Exact condition and sharpness
Let a0_low,a1_low be *certified* lower bounds on physical aperture at the actual observation instants; let V_high be an independently justified upper bound on physical aperture speed and T_high an upper bound on separation between the actual observation instants, including timestamp/exposure uncertainty. Under a continuous nonnegative V_high-Lipschitz aperture model, a hidden zero is impossible if and only if a0_low+a1_low > V_high*T_high for the rectangular uncertainty model with independently attainable extremes. Equality permits a piecewise-linear trajectory touching zero. This is an elementary Lipschitz reachability consequence, not a novel physiological theorem. If endpoint times are exposure-integrated rather than point measurements, those quantities are not certified and this test is inapplicable without a separately validated observation inverse.

## Executed reproducible test
Run `python research/observability/e002_756_uncertainty_gate.py`. Locally executed with Python standard library and exact fractions. Output: nominal exclusions 5/5; conservative exclusions 1/5; admissible hidden-zero witnesses 4/5; all assertions PASS. These counts are constructed adversarial cases, **not an estimated camera false-exclusion rate**.

## Release and prospective validation consequence
Reject any product-level 'no closure occurred' inference that uses a point-estimate aperture, nominal FPS, or fitted velocity as if each were a certified bound. The physical protocol must independently bound endpoint aperture geometry, exposure-to-instant inference, actual inter-observation timing and speed under participant-disjoint conditions. Under unbounded or unvalidated nuisance factors return `ABSTAIN_UNCALIBRATED`. This does not justify fatigue, sleep or alarm efficacy claims.

## Decisive next evidence
Execute the E002-744 synchronized shutter/photodiode protocol, characterize the reference detector's phase and exposure response (E002-750–755), then test held-out human blink recordings with independent velocity estimation and participant-disjoint scoring. Do not count uncertain reference negatives as successful exclusions.
