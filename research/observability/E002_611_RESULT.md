# E002-611 | Published eyelid velocities constrain the feasibility of Lucent's 30-Hz no-hidden-closure gate

Date: 2026-11-02. Parent E002-371, E002-608, E002-610. Evidence tier: PRIMARY-LITERATURE PHYSIOLOGICAL SCENARIOS + EXACT-RATIONAL GATE AUDIT; NOT HUMAN-VIDEO VALIDATION.

[Protocol frozen before implementation](E002_611_FROZEN.md), commit 39663d3f7b43c3bdc3fc2a8bb7b0b5bbd34abbc5.

## Concrete result

The existing E002-608 sufficient exclusion gate, under equal exposure-average lower bounds m, identical boxcar exposure durations e, ideal regular f-Hz sampling, normalized closure threshold tau, full-open palpebral aperture A mm and a HYPOTHETICAL hard continuous-time upper lid velocity v mm/s, requires

    m > tau + v/(2*A*f).

This is a reparameterization of the already established shutter-aware sufficient bound, NOT a new theorem. For this restricted symmetric idealization the gate's required margin depends on frame period, not exposure duration, because the dark gap plus one exposure duration equals one frame period. Actual observed m, noise, shutter shape, missingness and optical identifiability still depend on exposure.

At tau=0.2, f=30 Hz, A=9.8 mm, the minimum symmetric mean m is strictly above 0.35816 for v=93 mm/s, 0.47211 for v=160, 0.61327 for v=243, and 0.88027 for v=400. At m=0.5 the 93 and 160 scenarios pass this purely illustrative sufficient arithmetic test; 243 and 400 fail. NO scenario passes a physical exclusion certificate: no independently authenticated anatomical means or continuous-time velocity ceilings were acquired.

A stronger product-design limit occurs at 30 Hz, A=7.4 mm, v=400 mm/s: required m > 1.10090, impossible for any normalized m<=1. Thus THIS PARTICULAR sufficient gate cannot exclude closure in that scenario, even with perfectly calibrated, noiseless full-open averages. Doane reported spontaneous eyelid descent occasionally OVER 400 mm/s, making 400 a useful stress-test scenario, NOT a population maximum or a certified individual bound. This is not an impossibility theorem for all cameras or stronger algorithms.

The dimensionless ratio Q=v/[2*A*f*(1-tau)] yields a simple gate-feasibility boundary Q<1; Q>=1 means the strict sufficient gate cannot pass even at m=1. It is NOT a novel biological law.

## Reproduction and negative outcomes

- 72 frozen literature-anchored scenario rows (3 frame rates x 3 apertures x 4 velocities x 2 hypothetical means).
- 62/72 rows pass the purely illustrative sufficient arithmetic test; 10/72 fail. These are NOT empirical coverage, sensitivity, or false-negative rates.
- 2/72 rows have no possible mean that can pass: the two mean choices for the single triple (30 Hz, 7.4 mm, 400 mm/s).
- Eight local Python unit tests passed. Independently written Node.js integer arithmetic reproduced six critical controls. The executable generates a machine-readable 72-row CSV with exact-rational intermediate arithmetic.
- Equal-exposure e=2 ms and e=80% of frame period produce the same conditional threshold margin on this restricted model; this does NOT establish equivalence of actual camera measurements.
- No human video, physical shutter trace, rater annotations, or held-out physical predictions were used. Hosted CI not confirmed at report creation.

Reproduce from repo root: python -m unittest discover -s research/observability -p 'test_e002_611_velocity_feasibility.py' -v; node research/observability/e002_611_independent.cjs; python research/observability/e002_611_velocity_feasibility.py --csv. See [72-row scenario grid](E002_611_GRID.csv).

## Primary-source provenance and transportability warning

1. Godfrey et al. (2019), https://doi.org/10.1097/IOP.0000000000001356, https://pubmed.ncbi.nlm.nih.gov/30893187/: 240-fps spontaneous blinks, 10 adults; reported mean closing speed 93 mm/s, observed range 40–160 mm/s.
2. Kwon et al. (2013), https://doi.org/10.1098/rsif.2013.0227: 600-fps VOLUNTARY blinks, 25 adults; reported mean peak closing speed 243 ± 9 mm/s, full-open apertures 7.4–12.8 mm (mean 9.8).
3. Doane (1980), https://doi.org/10.1016/0002-9394(80)90058-6: spontaneous eyelid descent generally 17–20 cm/s and occasionally over 40 cm/s.

These are heterogeneous descriptive measurements. Combining one study's aperture with another study's speed is SCENARIO ANALYSIS ONLY, not a paired observation, an independent hard continuous-time V bound, or a transportable distribution. A finite-frame peak velocity cannot certify an unseen instantaneous maximum.

## Decisive product and study consequence

Do not adopt the 93 mm/s spontaneous mean, 160 mm/s observed range endpoint, or 243 mm/s voluntary group mean peak as a universal safety cap. The existing 30-Hz conditional no-hidden-closure gate can be mathematically noninformative for high-speed/small-aperture scenarios even under idealized measurements. Higher frame rate improves this particular feasibility bound but does NOT authenticate shutter timing, anatomy, continuous-time speed, or clock. Prioritize independent physiological velocity-envelope justification and actual synchronized high-speed/ordinary camera acquisition with blinded anatomical review, or abandon deterministic absence certification and limit product claims to calibrated positive witnesses and explicit abstention.

Physical validation: NOT PERFORMED. Lucent product: ABSTAIN_UNCALIBRATED; release BLOCKED. Hush branch/PR #45 not modified in this primary run.
