# E002-447 — preregistered finite-exposure identifiability falsification (2026-10-25)

**Frozen before implementing or running E002-447 numerical tests.** This is a new synthetic camera/instrument test of a missing measurement-model assumption in E002-371, not another S19 metadata audit. Existing S19 pilot evidence is unchanged; S21/S22 remain unopened.

## Scientific question and assumptions

E002-371 reasons about *instantaneous anatomical aperture samples*. Real camera frames integrate photons over finite, potentially rolling-shutter exposures, and image brightness is not itself anatomical aperture. Test whether an **idealized linear aperture sensor** returning a known exposure-weighted mean y could be safely substituted for an instantaneous aperture value. Assume a(t)>=0 and |a(t)-a(s)|<=V|t-s| in physical mm and seconds. Neither this sensor model nor V has been calibrated on human eyelids. A successful result cannot validate Lucent physically.

For a known normalized nonnegative shutter kernel K and target instant t, define M_K(t)=E_K |U-t|. Predict the **sharp single-measurement** lower bound a(t)>=max(0,y-V M_K(t)); show a witness attaining equality when y>=V M and a nonnegative scaled witness when y<V M. For a centered rectangular shutter of width w, predict M=w/4; for an unknown shutter kernel supported in the same interval, the worst-case M=w/2. With bounded timestamp error delta, predict worst-case M=max(M_K(t-delta),M_K(t+delta)), with the boxcar integral evaluated exactly. These are statements about the stipulated mathematical model only.

## Predeclared adversarial numerical experiment

Use y=3.0 mm, V=240 mm/s, width w=0.010 s, closure threshold 2.8 mm, center t=0. The point-substitution procedure would report open (3.0>2.8). The boxcar prediction is a(0)>=2.4 mm, so closure **cannot be ruled out**. Construct two physically Lipschitz-compliant trajectories with the **same exposure average**: constant 3.0 mm (always open) and 2.4+240|t| mm (crosses 2.8). An independent linear-programming oracle on 81 uniform time knots, trapezoidal shutter integration and neighboring Lipschitz constraints must recover the 2.4-mm minimum within 1e-6 mm. The unknown-kernel support-only minimum is predicted to be 1.8 mm, not 2.4 mm.

Additional tests: noncentered shutter formula, 1-ms bounded clock uncertainty, strict threshold equality, missing/invalid samples, unbounded speed, negative/NaN parameters, kernel normalization, unknown geometry or nonlinear image-to-aperture transfer, and per-row rolling-shutter offsets. An optional independent dense-grid oracle may check the constructed witness. No fabricated human error rates or statistical significance.

## Decision rule and evidence tier

A valid witness with equal shutter averages but different closure status **falsifies** using a frame-averaged aperture as an instantaneous anatomical observation without exposure modeling. The weighted-kernel bound may be used only when physical aperture units, calibrated K, clock support, and a defensible V are independently established. If any prerequisite is unknown, product behavior remains **ABSTAIN_UNCALIBRATED**. In particular, ordinary pixel intensity or image-edge span must never be passed to this aperture-only bound. This is synthetic instrument validation and a necessary model correction, **not human physical validation, not a novel general Lipschitz theorem, and not permission to deploy**.

Retain the existing single research branch, draft PR #26, and Hush isolation. No holdout participant access.