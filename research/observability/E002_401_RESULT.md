# E002-401 — rolling-shutter landmark time skew invalidates scalar aperture certificates

**2026-10-23. Frozen protocol committed first at `9211b62`. Evidence: exact synthetic two-landmark shutter instrument, independent numerical row integration, adversarial bridge regression, hosted CI. No real rolling-shutter camera or human aperture annotation.**

## A physically distinct nuisance: common-mode eyelid motion

E002-399 assumes that its input interval bounds the *exposure mean of the physical aperture* x(t)=l(t)-u(t). In a rolling-shutter image, the upper and lower landmarks may be captured at distinct row times. Their apparent separation is

```
m(t) = mean_e[l(t+dl)] - mean_e[u(t+du)]
```

rather than the simultaneous physical aperture mean `mean_e[l(t)-u(t)]`. Even if the physical aperture has **zero velocity**, a common translation of both eyelids can produce a large artificial separation because the row timestamps differ. Therefore, a bound on aperture velocity alone is insufficient to justify an upper/lower landmark-derived E002-399 certificate.

For independently bounded landmark speeds |u'|<=U and |l'|<=L, equal independently verified row exposures, and calibrated absolute row-time offsets |du|, |dl| relative to the nominal center, a sound correction is

```
B_row = U*|du| + L*|dl|.
```

The triangle inequality proves `|m - mean_e[x]| <= B_row`. This is classical Lipschitz analysis, **not claimed as a novel theorem**. It does not cover unequal row exposure profiles, nonlinear segmentation of blurred images, unknown rolling-readout timing, optical distortion, camera pose or unmodeled timing errors. Those require additional independently calibrated bounds or abstention.

## Frozen witnesses

Threshold 0.2; two frames centered -1 and +1 ms; each row exposure 1 ms; upper row center -4 ms relative to frame center, lower +4 ms. Both landmarks translate at 20 normalized coordinate units/s while the **true physical aperture is constant**.

| Physical aperture | Common translation | Asynchronous apparent aperture | Naive decision | Corrected (B=0.16) |
| ---: | ---: | ---: | --- | --- |
| 0.19, genuinely closed | +20/s | 0.35 | **False CONFIRMED_NO_CROSSING** | UNRESOLVED |
| 0.30, genuinely open | -20/s | 0.14 | **False CONFIRMED_CROSSING** | UNRESOLVED |

With zero row skew, the same synthetic cases produce the correct decisions. This falsifies a **measurement substitution**, not E002-371/E002-399 under their true assumptions.

## Frozen held-out synthetic instrument

Seed 401; 1,000 trials (500 truly below threshold, 500 above); independent common-motion sign and magnitude 15–20/s, acquisition phase ±0.2 ms, and upper/lower row offset jitter ±0.25 ms. The correction uses a predeclared fixed envelope U=L=20/s and |du|,|dl|<=4.25 ms, giving B_row=0.17. The certificate never receives the individual trial's true motion speed.

| Decision class | Naive | Corrected |
| --- | ---: | ---: |
| CONFIRMED_CROSSING | 494 | 9 |
| CONFIRMED_NO_CROSSING | 506 | 248 |
| UNRESOLVED | 0 | 743 |
| **Incorrect certificates** | **510 / 1000** | **0 / 1000** |

Maximum observed absolute asynchronous-mean bias: **0.1671745255**, below the preregistered 0.17 bound. All frozen predictions W1–W8 passed. **These rates characterize an adversarial synthetic design, not a real-camera failure rate or human risk estimate.**

An independent checker computed each moving eyelid's shutter mean by 2,048-point numerical quadrature, not by calling the analytical row-mean routine. Across 100 independently sampled cases, maximum analytic/numerical discrepancy was **2.17e-15**. It independently verified the triangle-inequality bound and physical landmark coordinate range.

## Enforcement in the human annotation bridge

`e002_399_annotation_bridge.py` now requires a `row_timing_calibration` object before issuing physical-aperture certificates, even if all older Boolean gates are asserted. Required fields:

```json
{
  "row_timing_calibration": {
    "upper_offset_abs_s_upper": 0.004,
    "lower_offset_abs_s_upper": 0.004,
    "upper_landmark_speed_upper_per_s": 20.0,
    "lower_landmark_speed_upper_per_s": 20.0,
    "equal_row_exposure_verified": true,
    "provenance": "independent_device_and_landmark_calibration"
  },
  "gates": {
    "calibrated_row_shutter": true
  }
}
```

The bound is added to the existing E002-400 optical exposure-mean error interval before E002-399 certification. A **verified global shutter** must still provide an explicit zero-row-offset calibration object. Absent row calibration => `ABSTAIN_UNCALIBRATED`; invalid speed/timing, missing provenance or unequal exposure profile => reject. This schema is a research prototype; the provenance string and Boolean verification fields are **not authenticated evidence**. Real use requires external audit of shutter timing, per-landmark speed and optical image formation.

Existing E002-399 and E002-400 regressions passed after updating the synthetic global-shutter fixtures to declare explicit zero skew. Earlier intermediate CI runs failed immediately after the stricter bridge was introduced; they were repaired by updating the existing regression fixtures before the final E002-401 CI. No historical evidence was rewritten.

## Reproduction

```bash
python research/observability/e002_401_rolling_shutter.py
python research/observability/e002_401_independent_check.py
python research/observability/e002_399_independent_check.py
python research/observability/e002_400_independent_check.py
```

Hosted verification: [GitHub Actions 40003737717](https://github.com/sushxnthd/lucent/actions/runs/40003737717), **completed successfully**.

## Priority, human evidence and product

Rolling-shutter distortion and motion-dependent geometric errors are established camera-imaging phenomena. The defensible contribution here is the exact **Lucent-specific wrong-certificate witness**, independent reproducibility, and direct fail-closed calibration gate. No novel general sampling law or empirical camera performance claim is made.

The existing 560 human eye crops have no blinded physical landmark annotations, independently measured exposure/row timing, or physiological speed envelopes. E002-371 is therefore **not yet human-validated**. The next decisive milestone is a synchronized real rolling/global-shutter reference instrument and untouched-participant aperture annotations with independently measured row-time offsets and optical transfer. Preserve negative results and keep draft PR #25 unmerged. Unconditional blink, PERCLOS, and fatigue diagnosis remain unsupported. **Product: ABSTAIN_UNCALIBRATED.**
