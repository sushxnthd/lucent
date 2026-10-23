# E002-400 — a known static optical transfer can invalidate a shutter-gap certificate

**2026-10-23. Preregistered at `37b2da4` before evaluating the new witness. Evidence tier: exact synthetic optical instrument plus independent numerical quadrature. No human eyelid-aperture ground truth.**

## Falsification of an invalid measurement substitution

E002-399 is a *correct conditional physical-aperture theorem*. Its input must bound the physical aperture's **exposure mean**. The tempting pipeline

`aperture_estimate = inverse_static_optics(mean_shutter(optical_signal))`

does **not** generally equal `mean_shutter(physical_aperture)`. A known, monotone static transfer curve does not make inversion commute with integration.

Frozen witness: x(t)=0.199+|t-0.1|, threshold 0.2, V=1/s, frame centers 0 and 0.2 s, exposure 0.1 s, no clock error, f(x)=exp(120(x-0.299)). The true aperture crosses the threshold at t=0.1.

| Measurement interpretation | Inferred mean at both frames | E002-399 interval minimum lower bound | Decision |
| --- | ---: | ---: | --- |
| Static inverse of shutter-averaged optical response, **incorrectly assumed** physical mean | 0.3282923934 | 0.2032923934 | **False CONFIRMED_NO_CROSSING** |
| Exact physical exposure mean | 0.2990000000 | 0.1740000000 | UNRESOLVED |
| Optical inverse with calibrated conservative bias interval ±0.05 | 0.3282923934 | 0.1532923934 | UNRESOLVED |

The false certificate is a **counterexample to the invalid optical measurement model**, not to E002-371 or E002-399 under their actual assumptions. The exponential optical response is intentionally severe and not calibrated to any physical eye or camera.

## Quantitative correction and proof

For V-Lipschitz aperture x(t), uniform exposure duration e, and increasing C² transfer f with f'(x)≥m>0 and |f''(x)|≤K on the independently bounded aperture domain, let y=f^{-1}(E[f(x(T))]) and μ=E[x(T)]. Then

```
|y-μ| ≤ B = min{ K V² e² / (24m), V e / 2 }.
```

Taylor's theorem bounds |E f(X)-f(E X)| by K Var(X)/2. The inverse is 1/m-Lipschitz. Moreover, Var(X)=E[(X-X')²]/2≤V² e²/12. The alternative V e/2 bound follows from y being between the exposure minimum and maximum of x and |x(t)-E x|≤V e/2. This is classical Taylor/Jensen measurement analysis, **not a claim of novel mathematics**.

The second bound prevents explosive derivative ratios from making the optical interval numerically unbounded. Here B=0.05. If a candidate no-crossing certificate has lower margin smaller than B, it must be rejected or recomputed with an independently justified tighter optical bound.

## Verification

- Exact exponential shutter integral: inverse optical mean **0.3282923933831731**, versus physical mean **0.2990000000000000**; optical bias **0.0292923933831731**.
- Independent 20,000-point midpoint quadrature per shutter: inverse mean **0.3282923932581731**, absolute difference ≈1.25e-10.
- 500 seeded random piecewise-linear, V≤1 trajectories with quadratic f(x)=x+0.5x²: maximum optical-inversion bias **0.0001171645788740**, below the predeclared B=**0.0004166666666667**. Separate 100-trajectory midpoint checker also passed.
- H1–H6 passed in local execution. H7 is enforced in the E002-399 two-rater annotation bridge: a Boolean optical gate alone now returns **ABSTAIN_UNCALIBRATED**. Explicit nonnegative finite `optical_mean_error_bound` in normalized aperture units and `optical_mean_error_provenance` are required; the bound widens every measurement interval before certification. Synthetic regression checks verify abstention without the bound and loss of certification under widened uncertainty.
- The provenance string is **not independent verification**. This script cannot audit whether the bound covers nonlinear shutter inversion, image segmentation, motion blur, glasses, rolling shutter, or optical-to-physical geometry. A real deployment requires a separately validated optical model and calibrated exposure means.

## Reproduce

```bash
python research/observability/e002_400_optical_noncommutation.py
python research/observability/e002_400_independent_check.py
python research/observability/e002_399_independent_check.py
```

No real human data or physical instrument measurements were added. E002-398's 560 frames still lack two independent blinded rater sheets and exposure/velocity calibration. **E002-371 remains unvalidated on humans.** Product decisions for hidden-closure exclusion, blink duration, PERCLOS and fatigue diagnosis remain `ABSTAIN_UNCALIBRATED`. The next decisive experiment is independent calibrated physical-aperture validation, not another surrogate AUC optimization.

## Priority and physical image-formation boundary (post-experiment literature check)

The transfer `f` in this counterexample maps *instantaneous physical aperture to instantaneous optical signal before shutter integration*. It is **not** asserted to be a consumer-camera response function (CRF) applied after photodiode exposure. A camera's post-integration CRF, ISP, segmentation and landmark extraction require a different, independently calibrated forward model. Therefore this experiment does not estimate a real camera's nonlinearity, or establish that any particular camera produces the witness.

The general danger from nonlinear radiometry and blur is established prior art. Tai et al., *Nonlinear Camera Response Functions and Image Deblurring: Theoretical Analysis and Practice*, IEEE TPAMI 35(10), 2498–2512 (2013), DOI [10.1109/TPAMI.2013.40](https://doi.org/10.1109/TPAMI.2013.40), analyze nonlinear CRF/blur interaction and edge errors. Debevec and Malik, *Recovering High Dynamic Range Radiance Maps from Photographs*, SIGGRAPH (1997), DOI [10.1145/258734.258884](https://doi.org/10.1145/258734.258884), establish radiometric response calibration. Burggraaff et al., *Standardized spectral and radiometric calibration of consumer cameras* (2019), [arXiv:1906.04155](https://arxiv.org/abs/1906.04155), document quantitative consumer-camera calibration problems. E002-400's value is a precise **Lucent-specific invalid-certificate counterexample and executable abstention requirement**, not priority over these imaging principles.

## Hosted reproduction

[GitHub Actions run 39999109488](https://github.com/sushxnthd/lucent/actions/runs/39999109488) **completed successfully** on commit `f824bdd`, running the exact witness, independent midpoint quadrature, and the full E002-399 independent regression including the new optical fail-closed tests. Later documentation/figure commits have their own runs. Figure source: `e002_400_figure.py` (generates editable vector SVG with NumPy/Matplotlib; no synthetic image is presented as human footage).
