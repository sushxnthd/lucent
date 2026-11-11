# E002-433 — separately passing nuisance checks can jointly produce a false closure certificate

**Date:** 2026-10-25. **Kernel:** E002-371 sharp shutter-gap/eyelid-velocity bound. **Evidence:** frozen, reproducible **synthetic** optical/instrument counterexample. **No physical human validation.** Protocol [E002_433_FROZEN.md](E002_433_FROZEN.md) was committed first at `988ee550`, before implementation and outcome files.

## Question and result

Does a measurement pipeline remain sound if it validates projection geometry with gain assumed fixed, and gain with projection angle assumed fixed, then combines the two passing conditional decisions? **No.** Both checks can individually issue a no-hidden-closure *candidate* even though a simultaneously admissible geometry/gain pair permits an unobserved physical closure. The correct joint uncertainty envelope abstains.

This is an application-specific **compositional falsification** of a measurement pipeline, not a new general inverse-problem theorem. It does not imply the individual conditional mathematical bounds are wrong: their incompatible fixed-nuisance assumptions are what make naive composition invalid.

## Precommitted acquisition model

Two ideal, nonoverlapping uniform 2-ms exposures centered at 0 and 33.333 ms measure

`y_i = (1/E) integral_{t_i-E/2}^{t_i+E/2} g(t) cos(phi(t)) a(t) dt`,

where `a` is physical eyelid aperture in mm, `g` is illumination/transfer gain and `phi` is a simplified effective projection angle. The stipulated closure threshold is 2.000 mm; the **hypothetical, nonphysiological** speed cap is 1.5 mm/s. Frozen nuisance intervals are `g in [0.97,1.03]` and `phi in [15,20] degrees`.

World A is always open at **2.128355545 mm**, with `g=1`, `phi=20 degrees`. World B has **2.012 mm** aperture throughout both exposure windows, descends to **1.991 mm** halfway between shutters, then recovers; it has `g=1.029101571`, `phi=15 degrees`. Its peak speed is **1.340425532 mm/s**, below the stipulated cap. Both worlds yield **exactly the same 2.000/2.000 optical exposure means** under the ideal model; only World B crosses the physical threshold.

For these equal observations, the conservative restricted-model joint lower bound is

`L = min(y0,y1)/(g_max cos(phi_min)) - V*d/2`.

The calculation uses the **upper** possible optical multiplier because that yields the **smallest** physical aperture compatible with an optical observation. It assumes a nonnegative physical aperture, authenticated optical multiplier bounds and a hard Lipschitz speed cap. It does not apply to arbitrary nonlinear RGB responses, unverified shutters or unbounded nuisance dynamics.

| Assumptions used by each isolated check | Conditional lower aperture | Study-only decision |
| --- | ---: | --- |
| Fixed gain 1, fixed angle 20° | **2.103356 mm** | Candidate (false for World B) |
| Gain fixed 1, angle allowed 15°–20° | **2.045552 mm** | Candidate (false for World B) |
| Gain allowed 0.97–1.03, angle fixed 20° | **2.041365 mm** | Candidate (false for World B) |
| **Both gain and angle bounded simultaneously** | **1.985245 mm** | **Abstain** |

The first three candidate calculations are conditional on assumptions **violated by World B**. The joint calculation includes World B and correctly declines to exclude closure. Thus the software anti-pattern is combining passing per-nuisance gates without propagating their uncertainty into a single joint forward model.

## Frozen unseen synthetic stress

Seed 433 generates 2,000 piecewise-linear physical aperture histories with independently sampled admissible gains and projection angles at fixed knots. The forward model numerically integrates the two optical shutter windows, and the joint conservative bound is compared with the continuous piecewise-linear physical minimum. These are **simulated** unseen trajectories, not independent human participants.

| Frozen metric | Result |
| --- | ---: |
| Simulated trials | 2,000 |
| True threshold crossings | **718** |
| Joint conditional candidates | **493** |
| False candidates under the stipulated synthetic model | **0** |
| Minimum true-aperture minus computed bound | **0.046124 mm** |

Zero synthetic false candidates is expected from the conservative model and does **not** establish any population error rate, physiological hard speed bound or physical-camera reliability. The seeded stress is not a proof of universal sufficiency. The two-world construction, not the Monte Carlo count, is the decisive falsification of incomplete calibration composition.

## Reproducibility and independent tests

Files: [implementation](e002_433_joint_nuisance.py), [independent adversarial tests](test_e002_433_joint_nuisance.py), [aggregate](E002_433_SYNTHETIC_AGGREGATE.json), [technical figure](E002_433_JOINT_NUISANCE.svg), and [CI workflow](../../.github/workflows/e002_433_joint_nuisance.yml). From repository root:

```sh
PYTHONPATH=research/observability python -m unittest -v research/observability/test_e002_433_joint_nuisance.py
PYTHONPATH=research/observability python research/observability/e002_433_joint_nuisance.py
```

Six independent test groups cover separate 20,000-step trapezoid integration, dense physical velocity verification, admissibility of both nuisance bounds, the incomplete-gate counterexample, a 2,000-trial frozen holdout with a separate Lipschitz oracle, malformed-input rejection and explicit product abstention. Hosted CI status must be checked separately; **do not infer a pass from committing a workflow**.

## Prior art and priority boundary

- Kwon et al. (2013), *High-speed camera characterization of voluntary eye blinking kinematics*, J R Soc Interface, DOI [10.1098/rsif.2013.0227](https://doi.org/10.1098/rsif.2013.0227), recorded 25 humans at 600 fps but annotated aperture every 5 ms; its mean peak closing speed is not a hard bound.
- Navascues-Cornago et al. (2026), *Video frame rate influences the accuracy of blink dynamics measurement*, Ocul Surf, DOI [10.1016/j.jtos.2026.01.003](https://doi.org/10.1016/j.jtos.2026.01.003), found low-frame-rate underestimation of peak blink velocities, especially below 250 fps.
- Confounding in inverse imaging and propagation of measurement uncertainty are established. E002-429 and E002-431 already showed separate synthetic geometry and gain aliases. **E002-433 adds a distinct *joint-calibration integration test*, not a priority claim over those principles.**

## Product consequence and concrete human study

**Reject a design that ANDs independently passing geometry-only and photometry-only certificates.** A single measurement-to-physical-aperture model must carry joint nuisance sets through shutter integration, geometry, gain, missingness, blur, gaze, glasses and clock error. If joint calibration is unavailable, return `ABSTAIN_UNCALIBRATED`. Do not substitute model confidence for physical calibration.

Prospective human protocol: (1) acquire consented 400–600-fps or equivalent synchronized 3D eyelid-margin traces with hardware timestamps and a separately characterized photodiode/LED shutter/clock trace; (2) independently measure physical aperture in millimeters and collect two blinded rater sheets, preserving unresolved reference intervals; (3) calibrate geometry and gain on training participants only, including **crossed** head/gaze angles (15°/20° illustrative, not universal) and randomized brightness/exposure/blur/glasses interventions; (4) independently establish a conservative physical speed envelope with a prespecified uncertainty and population-tail interpretation, not an ordinary-camera secant maximum; (5) preregister joint versus separate-gate predictions with E002-426's sealed participant-disjoint registry before reading unseen participant labels; (6) report per-participant false conditional certificates, abstention, unresolved intervals, and nuisance-stratified coverage with exact uncertainty bounds. **Any witnessed false no-closure certificate under authenticated assumptions is a failure; unresolved references are not successes.**

No authorized individual high-speed physical-aperture traces, independent instrument timing, blinded rater sheets, hard velocity bound or unseen participant results were obtained in this run. The restricted FaceBase 400-fps 3D dataset remains a potential authorized path, not evidence accessed. This experiment does not authorize physical hidden-closure guarantees, blink duration, PERCLOS or fatigue. **Product: `ABSTAIN_UNCALIBRATED`. PR stays draft and unmerged.**
