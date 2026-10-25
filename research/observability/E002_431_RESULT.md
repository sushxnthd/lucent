# E002-431 — photometric-gain alias defeats an uncalibrated physical-aperture claim

**Date:** 2026-10-25. **Evidence tier:** synthetic scalar-optical falsification, independent numerical oracle, frozen randomized stress set. **Not** human measurement, authenticated camera calibration, a novel universal theorem, or production authorization. [Protocol](E002_431_FROZEN.md) was committed before implementation.

## Decisive synthetic counterexample

Assume the deliberately simplified observable **y(t)=g(t)a(t)**, with physical central eyelid aperture a(t) in mm and unknown positive optical gain g(t). At 30 Hz (center spacing d=33.333 ms), closure threshold 2.00 mm and **hypothetical hard** speed cap V=1.2 mm/s:

- **World A:** a(t)=2.04 mm, g(t)=1; no closure.
- **World B:** a(t)=2.01 mm at both frame centers, triangular dip to **1.99 mm** halfway between them, and g(t)=2.04/a(t). Its peak physical aperture speed is **1.2 mm/s**, and gain ranges from **1.014925 to 1.025126**.
- Both worlds give exactly **y(t)=2.04 at every instant**. Consequently every shutter-integrated observation is identical at 24/30/60/120/500 Hz and 0.5/2/4-ms exposure widths.

An uncalibrated fixed-gain inversion gives an apparent sharp conditional lower aperture **2.020 mm**, falsely ruling out World B's actual closure. This does **not** invalidate the E002-371/E002-421 temporal theorem: the theorem's *physical-aperture input assumption* is violated.

## Conditional nuisance-bound rescue

For a(t)>=0, pointwise 0<g(t)<=G, a **true hard** physical Lipschitz cap V, and two equal nonoverlapping uniform shutter windows of duration E<=d with centers d apart, each observed mean y_i implies mean a_i>=y_i/G. The elementary Lipschitz inequality gives the conservative center-to-center bound

**L = max(0, min(y0,y1)/G - Vd/2).**

For every t between the exposure centers, at least one shutter window has mean |s-t|<=d/2. Thus a(t)>=mean a_i-V mean|s-t|>=min(y0,y1)/G-Vd/2. This is conservative, not claimed sharp; it does not apply to arbitrary shutter kernels, additive offsets, nonlinear imaging or unbounded geometry.

| Assumption | Lower aperture | Consequence |
|---|---:|---|
| Unauthenticated fixed gain 1 | **2.020 mm** | **False certificate** in World B |
| Independently authenticated gain in [0.97,1.03] | **1.96058 mm** | **Abstain** |
| Independently authenticated gain in [0.995,1.005] | **2.00985 mm** | Conditional synthetic candidate **only** for worlds satisfying the narrow gain bound |

World B **violates** the narrow bound; it cannot be used to falsify a genuinely authenticated narrow calibration. A photodiode or background patch is not automatically an authenticated bound on eye-region effective gain.

## Independent tests and adversarial stress

A frozen seed-431 experiment generated **2,000** piecewise-linear physical aperture traces obeying |a'|<=1.2 mm/s and time-varying gains within [0.97,1.03]. The simulator exactly integrates the product of two piecewise-linear functions over each exposure. An independently coded 100,000-point midpoint oracle verifies the integrator.

- **898** conditional synthetic candidates; **786** witnessed synthetic threshold crossings; **zero** false conditional certificates in the sampled set.
- Minimum true-aperture-minus-bound margin **0.02556 mm**. This is **not** physical uncertainty or a universal guarantee.
- **Six** local adversarial test groups passed: continuous-time velocity, shutter-rate equivalence, naive false certificate, broad/narrow gain guards, independent quadrature and malformed-input rejection.

Reproduce with standard-library Python:

```bash
cd research/observability
python -m unittest -v test_e002_431_photometric_alias.py
python e002_431_photometric_alias.py
```

[Executable experiment](e002_431_photometric_alias.py) · [Independent tests](test_e002_431_photometric_alias.py) · [Machine-readable aggregate](E002_431_SYNTHETIC_AGGREGATE.json) · [Technical figure](E002_431_PHOTOMETRIC_ALIAS.svg). Hosted CI success must be verified separately.

## Human-evidence boundary and next physical experiment

Kwon et al., *J. R. Soc. Interface* (2013), DOI [10.1098/rsif.2013.0227](https://doi.org/10.1098/rsif.2013.0227), acquired 600-fps video but annotated anatomical aperture every 5 ms; the reported group mean peak speed is not a hard cap. Navascues-Cornago et al., *The Ocular Surface* (2026), DOI [10.1016/j.jtos.2026.01.003](https://doi.org/10.1016/j.jtos.2026.01.003), reported lower-frame-rate underestimation of eyelid peak velocity. A new open 1,000-Hz EyeLink dataset (Mathema et al., *Scientific Data*, DOI [10.1038/s41597-026-06754-x](https://doi.org/10.1038/s41597-026-06754-x)) contains pupil/gaze/blink events, **not independently calibrated central physical eyelid aperture**. It is not a valid E002-371 physical reference. FaceBase's 400-fps 3D eyelid marker traces remain controlled access. No individual human traces were obtained.

**Prospective intervention:** synchronize an independently calibrated photodiode/LED reference, camera linearity/response, real shutter and clock timing, calibrated physical anatomical aperture, and two blinded eyelid-margin annotators. Test illumination steps, spectra, gaze, glasses, blur, occlusion, missingness and geometry on unseen participants/devices. Crucially, test whether an external reference *actually bounds the eye-region gain*; if not, reject physical inversion. Freeze predictions before inspecting independent high-rate references, preserving all unresolved negatives per E002-426/E002-430.

**Novelty and release:** Multiplicative gain confounding and Lipschitz optimal recovery are established phenomena. This is a Lucent-specific falsification and abstention consequence, not a new general law. E002-371 **remains physically unvalidated**. Product stays `ABSTAIN_UNCALIBRATED`; no physical no-closure, blink duration, PERCLOS, fatigue or deployment claim. Keep draft PR open and unmerged.
