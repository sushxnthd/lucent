# E002-431 — preregistered photometric-nuisance observability falsification

**Frozen:** 2026-10-25. **Primary kernel:** E002-371. **Evidence tier:** synthetic scalar-optical instrument model, not human images or a physical camera. Do not call this a new theorem or human validation.

## Question and intervention

Can a small, time-varying illumination gain produce identical image-derived aperture signals for a physically open trajectory and a hidden closure, even with exact timestamps, shutter and geometry? Does an independently authenticated gain interval recover a **conditional** no-closure certificate?

Assume the deliberately simplified optical observable `y(t)=g(t)a(t)`, where `a(t)` is physical central eyelid aperture in millimeters and `g(t)>0` is an unobserved multiplicative gain. This is a *counterexample to unverified photometric inversion*, not a physically established camera forward model. Real images also contain offsets, nonlinearities, gaze, occlusion, blur and reflectance changes, which remain unvalidated.

## Frozen experiment and expected falsifications

- Ordinary camera center spacing `d=1/30 s`, uniform exposure `E=0.002 s`, threshold `theta=2.000 mm`, **hypothetical hard** velocity `V=1.2 mm/s`.
- World A: `a_A(t)=2.04 mm`, `g_A(t)=1`.
- World B: outside `[0,d]`, `a_B=2.01 mm`; inside, triangular dip reaching `1.99 mm` at `d/2`. Set `g_B(t)=2.04/a_B(t)` for all t, including exposure tails. Both worlds have `y(t)=2.04` at every instant, including all shutter averages, but World B crosses the threshold and obeys `V`. World B's gain stays in `[1.014925,1.025126]`, a roughly 2.5% nuisance scale.
- A naive fixed-gain calculation gives `L_naive=2.04-Vd/2=2.02>theta` and falsely certifies World B.
- A **pointwise, independently authenticated** gain range `[0.97,1.03]` yields a conservative `L_broad=2.04/1.03-Vd/2 <theta`: abstain.
- A **separately authenticated** narrow range `[0.995,1.005]` yields `L_narrow=2.04/1.005-Vd/2>theta` on the constant World A; the constructed World B violates this narrow gain assumption and must be rejected, not certified.
- Verify equivalence numerically for 24, 30, 60, 120, 500 fps and exposures 0.5, 2, 4 ms. Dense independent oracle checks actual aperture minimum and velocity.
- Freeze a deterministic random adversarial stress set (seed 431; >=1000 piecewise-linear aperture/gain traces with slopes <=V and pointwise gain in [0.97,1.03]) and require **zero** false conditional certificates using `L=min(y_0,y_1)/g_max-Vd/2`. Also include a gain-out-of-range negative control that is *not* allowed through the release gate. Random coverage does not establish universal safety.

## Product release and human study consequences

Physical certificates remain **blocked** unless camera photometric inversion is independently calibrated with bounded per-pixel illumination/reflectance response and error; an exposure-shared brightness control alone is insufficient unless proven to track the eye's effective gain. Any unbounded additive offset, nonlinearity, exposure response, blur, gaze, glasses, missingness, clock error or geometry requires abstention. This test may only establish an *illustrative conditional* bound within the stipulated scalar model; all outputs must retain `physical_certificate_authorized=false` and `ABSTAIN_UNCALIBRATED`.

A real human study must measure synchronized illumination reference, camera response, physical aperture and nuisance strata with two independent blinded anatomical annotators, then freeze participant-disjoint predictions before viewing references. Prior literature on illumination-invariant photometry, inverse problems and Lipschitz recovery has priority; no general novelty claim.
