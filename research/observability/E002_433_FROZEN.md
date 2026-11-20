# E002-433 — frozen joint-nuisance certification experiment

Date: 2026-10-25. Parent: E002-371. Evidence tier: synthetic instrument falsification, not human/camera validation.

## Question
Can separate, apparently conservative photometric and projection-geometry checks each issue a conditional no-hidden-closure candidate, while their *joint* uncertainty admits a hidden closure? This tests compositional validity of the measurement-to-aperture calibration, not a new universal observability theorem.

## Precommitted two-world construction
- Two equal 2-ms uniform exposure windows at centers 0 and 1/30 s; y = exposure mean of g(t) cos(phi(t)) a(t), in synthetic arbitrary intensity units.
- Closure threshold theta = 2.000 mm; hypothetical physical speed cap V = 1.5 mm/s, not a human limit.
- Gain independently bounded [0.97,1.03], angle independently bounded [15,20] degrees, both physically *unauthenticated* in this experiment.
- World A: constant a = 2/cos(20 deg) mm, g=1, phi=20 deg, so both measured means y=2.
- World B: a=2.012 mm throughout the shutter windows, piecewise linear descent after first shutter to 1.991 mm at midpoint and recovery before second shutter; phi=15 deg, g=2/(2.012 cos(15 deg)) constant. Thus identical y=2 at both shutters; the dip crosses theta, with speed <= V and gain in frozen range.
- Compare naive fixed nuisance inversion, geometry-only uncertainty (gain fixed 1), gain-only uncertainty (phi fixed 20 deg), and joint uncertainty. Use L = y/(gmax cos(phi_min)) - V*d/2 as a conservative study-only bound. For geometry-only set gmax=1; gain-only set phi_min=20 deg; naive set both fixed.
- Precommitted expected outcome: naive, geometry-only and gain-only L > theta, joint L <= theta, with hidden World B satisfying both simultaneous nuisance bounds. Physical certificate must always be false.

## Tests and falsification
1. Independent 20,000-sample midpoint quadrature reproduces both exposure means and their equality.
2. Dense 20,000-step independent finite-difference check verifies World B's physical speed and threshold crossing, with exact slope cross-check.
3. Gain and angle stay within the frozen simultaneous bounds; both worlds have identical observed exposures, and World A does not close.
4. All three incomplete nuisance checks return conditional candidates, while the joint check abstains; reject a system that composes individually passing checks by conjunction.
5. Reject malformed gain/angle/clock/exposure/observation values and prohibit physical certification even with asserted provenance.
6. A seeded 2,000-trial synthetic holdout samples physically feasible piecewise-linear aperture histories, piecewise-linear gain and projection-angle perturbations within bounds, integrates both exposures and checks zero false certificates for the joint lower bound. Negative results preserved.

## Scientific limitations
This is a two-nuisance constructed counterexample using an ideal scalar optical model and a hypothetical velocity cap, not real human validation. It tests whether a proposed safety gate survives joint nuisance bounds. It does not prove complete nuisance identifiability or support real-world blink/PERCLOS/fatigue claims. Continue physical study requiring two blinded human raters, authenticated shutter/clock/illumination/geometry and independent velocity bounds, and prospective unseen participants.
