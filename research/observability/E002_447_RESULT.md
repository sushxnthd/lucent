# E002-447 — shutter-integrated observability is not point-sample observability

**2026-10-25.** Frozen before testing: [protocol](E002_447_FROZEN.md) (commit `beac4d3`). [Executable instrument](e002_447_exposure.py), [independent numerical/adversarial tests](test_e002_447_exposure.py), [technical figure](E002_447_EXPOSURE.svg), [machine-readable result](E002_447_SYNTHETIC.json), [hosted CI](../../.github/workflows/e002_447_exposure.yml). **Evidence tier: SYNTHETIC IDEALIZED APERTURE SENSOR, NOT HUMAN PHYSICAL VALIDATION.**

## Decisive falsification

The E002-371 point-sample theorem cannot be directly applied to a camera frame *as though the frame represented instantaneous anatomical aperture*. Even under the unrealistically favorable assumption that a frame reports a perfect **linear shutter-weighted average of aperture in millimeters**, different trajectories can produce the same measurement while disagreeing about closure.

Frozen synthetic conditions: shutter width 10 ms, measured mean aperture 3.0 mm, stipulated Lipschitz speed limit 240 mm/s, closure threshold 2.8 mm. Two worlds:

- **World A**: a(t)=3.0 mm throughout the shutter; no threshold crossing.
- **World B**: a(t)=2.4+240|t| mm for t in seconds, centered at zero; mean is also 3.0 mm, but a(0)=2.4 mm, below the 2.8-mm threshold.

Both are nonnegative, 240-mm/s Lipschitz, and produce exactly the same rectangular-shutter mean. An estimator replacing the mean with a point sample reports an apparently open aperture (3.0>2.8) but cannot distinguish these worlds. This is a **constructive falsification of the observation-model substitution**, not of the original E002-371 theorem under its stated point-sample assumptions.

## Sharp single-measurement boundary

Let a(t)>=0 be V-Lipschitz, let K be a normalized nonnegative exposure-time distribution, and let y=E_K a(U) be an **anatomical aperture mean**. Since a(U)<=a(t)+V|U-t|, necessarily

> a(t) >= max(0, y - V E_K|U-t|).

The bound is **sharp for one observation**. When y>=V E|U-t|, the witness a(u)=y-V E|U-t|+V|u-t| attains equality. When y<V E|U-t|, a scaled absolute-value witness has a(t)=0 and mean y while respecting the Lipschitz limit. For a centered boxcar of width w, E|U-t|=w/4 at its center, giving the exact penalty Vw/4. At offset d within the shutter, the penalty uses E|U-t|=w/4+d²/w; outside, E|U-t|=|d|. If the shutter kernel is **unknown but its support is known**, the worst-case center penalty is Vw/2 (a limiting endpoint-concentrated kernel), twice the boxcar penalty. A bounded center/clock offset delta uses the maximum distance expectation at the two uncertainty endpoints. No finite physical bound follows from an unbounded or uncalibrated V.

This is a standard consequence of Lipschitz continuity and integral exposure models, **not a claim of a novel general mathematical theorem**. The multiple-observation, real-image, and physically calibrated E002-371 boundaries are not proved by this single-observation law.

## Numerical verification and nuisance consequences

**16 local tests passed** on the frozen implementation, including an **independent 81-knot linear-programming oracle** using SciPy HiGHS that minimized center aperture under an exact trapezoid exposure mean and neighbor Lipschitz constraints. It returned 2.4 mm, matching the analytic bound within 1e-6 mm. A separate 100,001-point numerical quadrature independently confirmed the V-shaped witness mean 3.0 mm and its speed cap. The preregistered synthetic outcomes were:

| Synthetic assumption | Minimum center aperture |
| --- | ---: |
| Naive mean-as-point substitution | 3.000 mm (unsupported) |
| Known 10-ms uniform boxcar, no clock error | **2.400 mm (sharp)** |
| Same boxcar, 1-ms center uncertainty | **2.376 mm (sharp worst-case)** |
| Unknown nonnegative shutter kernel, known 10-ms support | **1.800 mm (sharp worst-case)** |

The instrument also tests row-dependent rolling-shutter centers, noncentered target instants, strict threshold equality, malformed/negative/NaN inputs, invalid kernels, low-aperture clamping, and fail-closed behavior. These are **model checks**, not human accuracy estimates. Geometric scale, image intensity-to-aperture transfer, brightness, blur, gaze, glasses, missingness, rolling-shutter row timing, and physiological V remain unvalidated on human video.

## Relationship to established Lucent work — novelty limitation

**Internal priority audit after execution:** E002-403 already derived the general shutter first-absolute-moment correction and falsified uniform-kernel substitution in a two-frame reference. E002-421/422 already proved sharp two-boxcar full-horizon laws and used independent LP verification. Consequently **E002-447 is not a new overarching shutter theorem or breakthrough**. Its incremental, reproducible contribution is the explicit **single-frame, within-exposure** closure-status alias under an idealized aperture mean, the sharp support-only and bounded-clock comparisons in the same units, and a 16-test independent numerical regression. It should be treated as a model-safety regression and product claim restriction, not a priority claim. Further iterations must seek actual human anatomical measurements and physical shutter calibration rather than extending these synthetic special cases.

## Priority and model realism

Exposure integration and rolling-shutter sampling are established computational photography phenomena, including Gu et al., *Coded Rolling Shutter Photography: Flexible Space-Time Sampling*, IEEE ICCP 2010, DOI 10.1109/ICCPHOT.2010.5585094, and Sellent et al., *Motion Field Estimation from Alternate Exposure Images*, IEEE TPAMI 2011, DOI 10.1109/TPAMI.2010.218. Lipschitz envelope arguments have a much older mathematical history (McShane/Whitney extension methods). E002-447 claims **only a concrete, reproducible falsification of a tempting Lucent measurement substitution** and an exact correction under explicit idealized assumptions. A camera pixel is a radiometric measurement, not an aperture sensor. The physical transfer from pixels to anatomical millimeters must be separately established before the mathematical law can be used for an eyelid claim.

## Product consequence and next experiment

**Kill mean-as-point aperture certification.** Do not infer a physical closure exclusion from a frame average or from an uncalibrated edge/brightness proxy. Any future product path must separately authenticate (1) anatomical aperture in mm, (2) per-row shutter support and integration kernel, (3) exposure and clock uncertainty, (4) independently supported physiological velocity/acceleration bounds, and (5) nuisance-stratified participant-disjoint human outcomes. An unresolved item is an abstention, not a negative observation.

The E002-446 fixed-edge detector was already rejected on S19 (0/3,000 candidate frames). This run **did not reanalyze S19, retune its detector, or open S21/S22**. Human anatomical labels and independent physical timing remain the priority. The E002-447 model result should guide the **physical exposure-calibration apparatus** rather than becoming another substitute for human validation.

**E002-371 physical validation: NOT ESTABLISHED.** Product: `ABSTAIN_UNCALIBRATED` for hidden-closure guarantees, blink duration, PERCLOS, fatigue and medical use. No merge, release, or Hush modification.