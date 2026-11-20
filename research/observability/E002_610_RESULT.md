# E002-610 | Radiometric nonidentifiability and uncertainty-induced loss of closure witnesses

Date: 2026-11-02. Parent E002-609 / E002-608. **Evidence: deterministic synthetic nuisance simulation only; zero new human/physical data.**

[Protocol frozen before implementation](E002_610_FROZEN.md), commit `8c15ed5b53dcaf44e5bcb86ee5cf64f5f0dc8849`.

## Result: brightness cannot serve as anatomical aperture without independent transfer and illumination bounds

A stipulated **linear** sensor model is `y=b+g*average[L(t)*a(t)]`, with anatomical aperture `a(t) in [0,1]`, unknown time-varying illumination `L(t) in [Lmin,Lmax]`, and independent interval bounds on background `b`, gain `g`, and measured linear-light signal `y`. The exact conservative upper bound is `m_hi=min(1,max(0,(ymax-bmin)/(gmin*Lmin)))` when all model assumptions and feasibility constraints hold. This is an elementary inequality, **not a new mathematical discovery**. It is not valid for arbitrary eye pixels, nonlinear/gamma-encoded frames, unregistered geometry, or unknown scene illumination.

- Hypothetical `y=0.15, g in [0.98,1.02], b in [0,0.01], L in [0.9,1.1]`: upper mean aperture `25/147 ~= 0.170068`, below the stipulated `tau=0.2`, yielding **conditional model witness**.
- Widen only the illumination lower bound to `Lmin=0.5`: upper mean aperture `15/49 ~= 0.306122`, above threshold; **no witness**. Zero or unknown positive flux lower bound: **ABSTAIN**.
- The same observed `y=0.2` arises from `(a,L)=(0.2,1)` or `(0.5,0.4)` with gain 1 and background 0. Thus a dark pixel does not identify a closure even in a linear radiometric model unless illumination is independently constrained.

**Additional precommitted nonlinearity kill test:** a hypothetical gamma-2 sensor maps a truly open constant aperture `a=0.4` to `y=a^2=0.16`. If the image is falsely treated as linear intensity at unit illumination, the model emits a closure witness for `tau=0.2` even though `a=0.4` throughout. Explicitly withholding the `raw_linear_light` attestation changes the output to `ABSTAIN_ATTESTATION`. This is a **synthetic counterexample under violated calibration premises**, not an observed false positive on a human video. It makes raw linear sensor response or independently validated inverse response a non-negotiable physical release blocker.

## Seeded adversarial synthetic sweep

A fixed-seed 10,000-trajectory test varied 16 within-exposure aperture bins (sinusoidal motion) and illumination bins, then compared tight `L in [0.95,1.05]` against the *same exact synthetic observations* evaluated under loose `L in [0.4,1.6]`. Synthetic true aperture mean `<=0.2` occurred in **4,971/10,000** trajectories. The interval model emitted **4,473** conditional witnesses under tight flux bounds versus **1,718** under loose bounds, a **61.6% decrease** in witnesses. Across both arms: **0** computed-upper-bound violations and **0** false witnesses on this seeded finite test. These are simulator-specific counts, **not** real human sensitivity, false-negative rates, clinical validity, or proof of model soundness outside its assumptions.

Twelve local Python adversarial tests passed. A separately implemented Node.js BigInt rational verifier passed exact `25/147`, `15/49`, and two-world controls. No actual camera or photodiode was connected. [Python executable](e002_610_photometric_bound.py), [tests](test_e002_610_photometric_bound.py), [independent verifier](e002_610_independent.cjs), [CI](../../.github/workflows/e002_610_photometric_bound.yml). **Hosted CI not yet confirmed at report creation.**

## Product and empirical consequence

The operationally important result is the **fragility of a closure witness to illumination uncertainty**. E002-609 must not receive a brightness-derived `linear_aperture_upper` unless the physical anatomical-to-linear-light transfer, sensor response, flux minimum throughout the exposure, background, gain, geometry and shutter/clock are *independently calibrated*. A synthetic flag or SHA-256 string is not authentication. Every E002-610 output is `ABSTAIN_UNCALIBRATED` and release `BLOCKED`.

**Stop criterion:** if an eye-plane phantom experiment cannot independently bound illumination and anatomical transfer across unseen brightness, gaze, glasses, blur, occlusion and geometry conditions, kill this photometric bridge for human closure claims. Prefer two blinded human anatomical raters and conservative interval annotation under E002-598/609; retain abstention when physical premises are missing. A real human closure claim still needs synchronized shutter/clock, independent anatomical review, and an independently defensible continuous-time eyelid velocity bound for E002-371 exclusion.

**Outstanding empirical evidence:** 0 physical camera/shutter captures, 0 independent human eyelid ratings, 0 independently certified human velocity ceilings, 0 held-out physical predictions. No new dataset-access attempt. Hush branch and PR #45 untouched.
