# E002-479 RESULT — finite-grid optical shutter response can conceal a narrow sensitivity island

Date: 2026-10-27. Kernel E002-371. **Evidence tier: constructed stationary-periodic optical instrument model, not physical acquisition or anatomical human validation.** This result is a falsification of an overly strong inference from finite phase-grid coverage, not a new physiological law.

## Frozen protocol and transparent correction

[E002-479 freeze](E002_479_FROZEN.md) preceded code. A separate [pre-implementation amendment](E002_479_AMENDMENT_A.md) preserves a falsified original robust-geometry prediction: the initial island [2.020,2.030] ms could overlap a second-period grid pulse under the allowed phase uncertainty. The amended island [2.015,2.025] ms was independently checked across **both periods** before code. This is **not** an untouched preregistration.

## Exact optical observation model

Let T = 1000/240 ms and let S(t) be a nonnegative, stationary, T-periodic optical sensitivity. The pulse-averaged camera response at phase t for rectangular pulse width w is

C(t) = (1/w) integral from t to t+w of S(s) ds.

Model A has S=1 on phase [0.4,1.4] ms and S=0 elsewhere. Model B adds an optical sensitivity island of amplitude 0.20 on [2.015,2.025] ms modulo T, leaving the main exposure unchanged. This is a deliberately adversarial *synthetic* response, not a claim about a commercial camera.

At nominal pulse starts t_i=iΔ, Δ=0.05 ms, w=0.006 ms, and i=0,...,167, the added island does not intersect **any** pulse support. Even allowing an independent bounded start-phase error u=0.004 ms, the entire possible pulse support [t_i-u,t_i+w+u] misses the island in both periods. Therefore C_A(t_i)=C_B(t_i) for every sampled phase. Both models yield exactly the same camera CSV, clock CSV, raw placeholder and manifest hash, despite different shutter support in a putative dark interval.

The generic single-cell unprobed interval is Δ-w-2u = **0.036 ms** when positive. This is a geometric sampling limit, not a universal minimum physically detectable island: multi-period grids must be intersected jointly, as the preserved failed freeze illustrates. With bounded noise, arbitrarily small positive sensitivity cannot be certified to be exactly zero from a finite optical scan.

## Prespecified held-out discrimination

A separately timed probe at phase T*k+2.017 ms for k=0,1, with 20 repeats per period, two row strata, bounded ±0.002-ms phase jitter and ±0.002 normalized-contrast error, is fully contained inside the amended island. Under the frozen model it predicts contrast near 0.20 for Model B and near 0 for Model A. The prespecified 0.04 threshold detects the high-amplitude island but **does not detect** a 0.004-amplitude island. Nondetection is not physical absence.

## Verification and honest evidence tiers

Independent JavaScript interval arithmetic on the frozen geometry reproduced: 168 grid phases; 6,720 camera/clock row pairs; zero nominal island intersections; zero intersections over the full ±0.004-ms phase uncertainty; and a 0.000666667-ms intersection in the **rejected original frozen geometry**. The new [standard-library executable](e002_479_phase_island.py) constructs both fixtures and calls the **actual** [E002-477 intake](e002_477_optical_intake.py), comparing its outputs and product-release fields. The [ten regression tests](test_e002_479_phase_island.py) and [hosted CI](../../.github/workflows/e002_479_phase_island.yml) independently exercise the intake. **Hosted CI status must be checked before claiming that those tests passed.**

This result does not authenticate a photodiode, frame counter, camera pulse integration, optical transfer function, phase jitter, sensor noise, actual shutter tails, or physiological velocities. The model has no human gaze, glasses, anatomical geometry or blink dynamics; those nuisances remain untested at this stage. The CSV's distinct device IDs are synthetic declarations, not independently verified instruments.

## Decisive physical acquisition consequence

Before any physical shutter-support claim:

1. Explicitly record CORRESPONDING_FRAME or TARGET_FRAME attribution, independently authenticated pulse-to-frame mapping, raw photodiode/logic-analyzer traces and two sensor-row strata.
2. Acquire calibration grid phases, **then freeze and independently acquire offset/held-out phase probes** in dark regions. Vary phase offsets, pulse width and illumination. Validate linear response, detector tails, gain, rolling rows, clipping, brightness drift, jitter and missed frames.
3. Report an independently calibrated **upper response envelope at a specified detection threshold**, not exact zero exposure inferred from a finite grid. Reject/abstain if phase coverage or nuisance bounds leave possible unseen sensitivity.
4. Only after physical optics and moving-aperture encoder tests pass, perform blinded participant-disjoint human high-rate reference measurements. Estimate physical velocity and clock uncertainties without converting an observed sample maximum into a universal hard bound. Evaluate ordinary-camera predictions against held-out anatomical trajectories and report false exclusions.

## Product decision

The E002-477 result PASS_INTAKE_ONLY is **not** a shutter-support certificate. Finite phase scans cannot authorize a guaranteed dark gap without stronger calibrated regularity, sampling or physical constraints. Do not promote E002-371 hidden-closure exclusion to a physical product claim. Blink duration, PERCLOS, fatigue and medical inferences remain **ABSTAIN_UNCALIBRATED**. Physical acquisitions: **0**; new anatomical reference sequences: **0**. Hush PR #45 untouched.