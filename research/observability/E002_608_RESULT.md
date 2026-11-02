# E002-608 | Exposure-averaged endpoint falsification and conservative physical-evidence gate

Date: 2026-11-02. Parent E002-371. Evidence tier: **EXACT SYNTHETIC BOXCAR-ANATOMY MODEL, NOT PHYSICAL/HUMAN VALIDATION**. Frozen before code and execution in [E002-608 protocol](E002_608_FROZEN.md), commit `4c0b6b3`.

## New result: a naive point-endpoint certificate can be false

E002-371's sharp point-observation gap inequality cannot be applied directly to **exposure-averaged** eyelid apertures. Let the continuous normalized aperture be `a(t)=0.2+0.02|t-5|` for `t` in [-20,30] ms, with `V=0.02/ms` and closure threshold `tau=0.2`. The path is physically bounded in [0,1] over this interval and reaches the threshold at `t=5 ms`, hidden in the unexposed gap (0,10) ms. Ideal boxcar averages over [-20,0] and [10,30] ms are both **0.5**.

Misusing the point-sample rule would test `(0.5-0.2)+(0.5-0.2) > V*10 = 0.2` and **falsely exclude** the actual closure. The correct exposure-aware *sufficient* exclusion rule for uniform boxcar anatomical aperture averages is

```
mL_lower + mR_lower - 2*tau >
    V_upper * (gap_upper + (exposureL_upper + exposureR_upper)/2).
```

In the adversarial witness the left and right sides are both **0.6**; strict exclusion fails, correctly. The inequality follows by integrating the Lipschitz upper envelope around a hypothesized closure time `t*` and summing both exposures. Equality is attainable by the constructed triangular trajectory, so replacing `>` with `>=` is unsound. The condition is sufficient, **not claimed necessary** in the presence of anatomical range constraints or additional measurements.

A constant-open control with both exposure averages 0.6 yields left side 0.8 versus right side 0.6, and the model conditionally excludes hidden closure under all its stated premises. The dimensionless ratio `R=(mL_lower+mR_lower-2*tau)/[V_upper*(g_upper+(eL_upper+eR_upper)/2)]` must strictly exceed 1 when its denominator is positive. Zero-denominator cases use the exact strict-margin test without dividing.

## Executed checks

- Nine adversarial Python tests passed locally, including hidden-closure boundary, constant-open control, missing calibration/evidence, all eleven nuisance flags, invalid geometry/values, uncertainty monotonicity and zero velocity.
- A separately written Node.js BigInt rational integrator reproduced both exposure averages `1/2`, the naive false exclusion and exact shutter-aware boundary equality without importing Python.
- `python e002_608_exposure_gate.py --example` returned `ABSTAIN_HIDDEN_CLOSURE_POSSIBLE`, exact strict margin 0 and ratio 1.
- [Executable conditional gate](e002_608_exposure_gate.py), [Python regressions](test_e002_608_exposure_gate.py), [independent replay](e002_608_independent.cjs), and [dedicated hosted workflow](../../.github/workflows/e002_608_exposure_gate.yml) are committed. **Hosted E002-608 status was not yet confirmed when this report was written.**

## Direct enforcement consequence

The gate takes conservative shutter exposure bounds, a physically independent continuous-time velocity upper bound, measured **linear anatomical aperture exposure-average lower bounds**, geometry and clock uncertainty, nuisance flags, and SHA-256 evidence references. It rejects malformed intervals and abstains for missing premises, digests or nuisance uncertainty. Even `MODEL_EXCLUDE_CONDITIONAL` is **not** a verified camera or human result: supplied attestations/digests cannot authenticate their own physical provenance. This gate is research-only and cannot be used to certify actual blink absence from pixel brightness, grayscale averages, CNN scores, nominal FPS, or uncalibrated exposure metadata.

A real custodian must first establish an independently calibrated sensor-to-aperture integration model. The physical instrument in [E002-607](E002_607_RESULT.md) estimates shutter timing only *conditionally* and cannot provide anatomical aperture, a velocity ceiling, or authenticated clock origin. If boxcar linearity, rolling shutter, exposure alignment, geometry, brightness, gaze, glasses, missingness, blur, occlusion, saturation, or sampling assumptions fail, the gate must abstain. A verified hard V ceiling cannot be obtained from sampled maximum speed alone.

## Evidence and next decisive work

**Human closure measurements: 0. Physical shutter captures: 0. Independent continuous-time human eyelid velocity ceilings: 0. Held-out physical predictions: 0.** This is a mathematical product-safety falsifier, not new physiological evidence, independent human validation, or a priority claim. The next eligible substantive work must prioritize consented synchronized physical-camera/optical calibration and blinded high-speed human anatomical review under [E002-598](E002_598_HUMAN_STUDY.md), or authorized access to a suitable independent high-rate annotated dataset. Do not spend additional runs on theorem polishing or dataset-download retries.

**Lucent product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. Hush branch/PR #45 unchanged during this primary run.
