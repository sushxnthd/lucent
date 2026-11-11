# E002-480 RESULT — nominal phase dithering cannot overcome independently bounded pulse timing

**Date:** 2026-10-27. **Kernel:** E002-371. **Evidence tier:** constructed stationary-periodic optical instrument model, with independent JavaScript arithmetic and local Python regression. **Not** measured hardware or human anatomy. [Frozen predictions](E002_480_FROZEN.md) were committed at `d1cd1d9c09466dc49b11fe3a381d00e08978c942` before implementation. The shared-offset control below was added *after* inspecting the independent-jitter result and is explicitly exploratory.

## What was tested

E002-479 established that a finite optical phase grid can miss a narrow shutter-response island. The new falsifiable question is whether collecting more nominal staggered phases fixes that problem when actual pulse timing is only bounded rather than known exactly.

The synthetic camera has frame period T=4.1666667 ms (240 fps), optical pulse width w=0.006 ms, per-pulse independent timing error |e_i|<=u=0.004 ms, and a periodic shutter sensitivity with base response on [0.4,1.4] ms. The adversarial world adds an amplitude-0.20 sensitivity island of width 0.0005 ms centered at 2.01525 ms. Each camera response integrates sensitivity over the *actual* pulse interval. The control world omits the island. This sub-microsecond island is deliberately constructed and **not asserted to exist in a physical camera**.

The independent-jitter adversary selects one allowed timing error, -u or +u, separately for each nominal probe. This is a worst-case uncertainty model; it is not a stochastic or experimentally estimated jitter distribution. Four grids cover two periods, with 1x/2x/4x/8x nominal phase density relative to the E002-477 0.05-ms step.

## Frozen predictions versus executed synthetic results

| Nominal phase density | Nominal probes across two periods | Probes with unavoidable island intersection | Difference between worlds under allowed adversarial timing |
|---|---:|---:|---:|
| 1x | 168 | 0 | 0 |
| 2x | 335 | 0 | 0 |
| 4x | 668 | 0 | 0 |
| 8x | 1,335 | 0 | 0 |

All four frozen predictions survived the local simulator. The adversarial actual timing schedule yields identical response vectors for the two worlds despite a positive sensitivity island. This is an **existence counterexample**, not a measured false-negative rate. It does not assert that all possible timing realizations hide the island.

[Vector timing-core figure](E002_480_TIMING_CORE.svg) illustrates the distinction between possible pulse supports and their guaranteed intersection.

## Sharp geometric law and dimensionless design condition

If the independent measurement reports a pulse start m with true start anywhere in [m-u,m+u], the set illuminated for **every** allowed timing realization is

`[m+u, m+w-u]` when `w>2u`, and empty otherwise.

Define the robust-core fraction `q=max(0,1-2u/w)` and the phase-coverage number `Gamma=N*max(0,w-2u)/T`, for N phase probes per period. Complete worst-case phase coverage requires `Gamma>=1`. For equal-width pulses and freely placed phase starts, this condition is also sufficient when the starts are equally spaced around the period. This is an elementary interval-covering consequence, not a novel physical law. It certifies **geometric intersection with some probe**, not detection at finite signal-to-noise ratio.

At the frozen w=0.006 ms and u=0.004 ms, `2u/w=1.3333` and every robust core is empty. Nominal staggering alone cannot produce a deterministic per-phase hit guarantee against *independent* bounded errors. If a separately calibrated clock could instead achieve u=0.001 ms, the robust core would be 0.004 ms and the minimum complete equal-spacing design would require **1,042 reported starts per period**. A 1,041-phase control leaves a 0.000002562-ms gap. The required uncertainty and pulse timing are **hypothetical**.

## Independent detector-sensitivity blocker

With island amplitude 0.20 and width 0.0005 ms, even perfectly aligned 0.006-ms optical pulses can yield at most `0.20*0.0005/0.006 = 0.016667` normalized response from the island. Adding the allowed +0.002 noise cannot reach the stipulated 0.04 detection threshold. Even *complete* geometric coverage would therefore not guarantee detection. At this amplitude and threshold, at least **0.00126 ms** of overlap is necessary to exceed threshold under the worst -0.002 measurement error; this is not a guarantee that any such overlap occurs.

**Exploratory nuisance-correlation control, not part of the freeze:** at eightfold nominal density, using the *same* clock offset for all probes gives two island-intersecting probes for each tested offset -0.004, 0, and +0.004 ms. The independent-error counterexample must **not** be generalized to a shared systematic offset. Physical clock-error correlation and the independently logged actual pulse times matter to the correct coverage certificate. These three checked offsets do not establish a continuum or physical guarantee.

## Verification and reproduction

- [Standard-library simulator](e002_480_phase_dither.py) emits [deterministic aggregate](E002_480_AGGREGATE.json). Local execution reproduced all four grids, the robust-core design and the detection ceiling.
- [Adversarial Python tests](test_e002_480_phase_dither.py): 14 frozen/core tests passed locally on the original independently developed implementation; one additional post-freeze shared-offset control was committed. The committed implementation is semantically equivalent, but its hosted run must pass before claiming verification on the repository branch.
- [Independent JavaScript replay](e002_480_independent_replay.cjs) reproduced all four grid counts, zero unavoidable intersections, 1,042-phase threshold and optical detection ceiling. It additionally records the exploratory shared-offset control.
- [Dedicated CI](../../.github/workflows/e002_480_phase_dither.yml) reruns Python tests, independent JS and exact committed aggregate comparison. **Do not claim hosted success before checking its run.**

## Acquisition and product consequence

A physical optical shutter-support certificate must (a) authenticate pulse-to-frame attribution and actual independently measured optical pulse times; (b) calculate the union of *guaranteed* pulse cores from measured timing uncertainties, not from nominal commanded phase steps; (c) bound the detector transfer function, pulse integration, brightness/gain changes, noise floor, missingness, rolling rows and optical tails; and (d) declare a **detectable-response envelope at a stated threshold**, never exact zero from finite nondetections. Require independently acquired held-out phases and moving-aperture ground truth before a human anatomical test. Distinguish independent per-pulse error, common offset, and correlated drift with separate calibration evidence.

The existing E002-477 `PASS_INTAKE_ONLY` remains **not** a physical shutter-support certificate. This experiment adds no new camera measurements, anatomical reference trajectories or physiological velocity hard limits. E002-371 physical validation is `NOT_ESTABLISHED`; hidden-closure, blink-duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. No change to Hush, no deployment, no merge.

**Next decisive action:** physical optical-phase acquisition with an independently authenticated timing trace. Stop expanding synthetic examples unless a new result changes the acquisition design or product claim boundary.