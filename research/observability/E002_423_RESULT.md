# E002-423 — pulsed-LED shutter calibration: synthetic instrument falsification

**Date:** 2026-10-25. **Frozen before code and outcomes:** `E002_423_FROZEN.md` at commit `b96e6b325fde584fadc9639f9ff1304fe958490a`. **Evidence:** seeded synthetic instrument experiment, interleaved held-out phase tests, independently expressed pulse-integral oracle, adversarial nuisance cases, hosted CI. **Not** a real LED, camera, photodiode, oscilloscope, human eyelid or shutter measurement. Do not call this physical validation of E002-371.

## Why this experiment matters

E002-421/422's exact scalar-aperture shutter-gap laws require **known exposure response and correct row-specific center times**. A camera's advertised 240 fps does not establish either. This run freezes and exercises a practical optical pulse metrology gate instead of extending the Lipschitz theorem again.

For an ideal linear boxcar shutter `[c-E/2,c+E/2]`, and an externally timed LED pulse `[s,s+p]`, the normalized response is `y(s)=|[s,s+p] intersect [c-E/2,c+E/2]|/E`. The simulation uses a separately written positive-part antiderivative to generate observations and a min/max overlap model to fit them. The fitter never receives the hidden synthetic exposure width or row centers.

**Known model limits:** This equation is not a model of raw RGB pixel transfer under unknown demosaicing, HDR, gain, tone mapping, blooming, motion, spectral mismatch, PWM, sensor nonlinearity or optical pulse rise/fall. An independent photodiode trace and linear RAW calibration are prerequisites to physical use.

## Frozen simulation and results

A 0.50-ms pulse was swept across **101 known phases** from -3.0 to 7.0 ms, spaced 0.10 ms apart, at two simulated sensor rows (0 and 800). The fitter used 51 alternating phases; **50 interleaved phases per row were held out**. Hidden synthetic exposure was 2.40 ms for both rows, with centers at 0.00 and 3.20 ms. Seeded noise amplitude was bounded by 0.003 normalized intensity units. The search grid resolution was 0.10 ms in both parameters; the frozen held-out acceptance threshold was RMSE <= 0.015.

| Condition | Row 0 fitted E / center (ms) | Row 800 fitted E / center (ms) | Held-out RMSE (row 0 / row 800) | Frozen decision |
|---|---|---|---|---|
| Clean synthetic | 2.40 / 0.00 | 2.40 / 3.20 | 0.001878 / 0.001686 | **PASS** |
| Independent pulse jitter ±0.80 ms | 2.70 / 0.10 | 2.10 / 3.10 | 0.045037 / 0.058625 | **REJECT** |
| Nonlinear response `sqrt(y)` | 2.30 / 0.00 | 2.30 / 3.20 | 0.128873 / 0.127898 | **REJECT** |
| Shuffled phase-to-observation linkage | 3.30 / 3.70 | 3.30 / -0.20 | 0.098896 / 0.116709 | **REJECT** |

All frozen H1–H6 checks passed **on these particular synthetic cases**, not as universal sensitivity guarantees. The independently formulated integral was checked against the fitting overlap expression for 1,000 seeded random intervals; invalid, missing, duplicate, nonfinite and clipped observations were rejected. Operator assertions alone never authenticate a physical instrument; all cases retain `ABSTAIN_UNCALIBRATED`.

**Reproduce from the repository root:**

```bash
python -m unittest -v research/observability/test_e002_423_pulse_metrology.py
python research/observability/e002_423_pulse_metrology.py
```

The hosted workflow `e002_423_pulse_metrology.yml` runs both, checks all frozen outcomes, and uploads a JSON **synthetic-only** artifact. No eye images or private calibration traces are uploaded. The initial hosted workflow completed successfully on commit `43a7d7b`: [Actions run 40121895766](https://github.com/sushxnthd/lucent/actions/runs/40121895766). A subsequent regression adds the exploratory row-offset consequence below and must be verified separately before claiming that extension hosted-successful.

## Exploratory product-decision reversal (not preregistered)

A post-freeze **illustrative** calculation couples the synthetic inferred 3.20-ms row offset to the previously proven E002-422 sharp bound. This is not a human measurement or a new theorem. Suppose two normalized physical-aperture shutter means are `a=0.40` and `b=0.35`, threshold `theta=0.20`, a **hypothetical** hard `V=50/s`, and shutter duration 2.40 ms. If an implementation naively uses only nominal 240-fps frame spacing, `d_nom=4.1667 ms`, its sharp conditional minimum is `L_nom=(a+b-V*d_nom)/2=0.27083`, **above** the threshold. If the two measurements instead come from rows whose center-time offset adds 3.20 ms, `d_corrected=7.3667 ms`, the same calculation gives `L_corrected=0.19083`, **below** threshold. The balanced-slope regime holds in both cases.

Thus an unmeasured rolling-row offset can reverse an apparently safe *conditional* certificate. This is a model-specific counterexample, **not** evidence that a real phone has 3.20-ms row delay or that an actual eyelid crosses the threshold. A physically calibrated device would need to account for both frame and row timestamps. Without them, fail closed. Neither calculation authorizes a product measurement.

## Concrete physical metrology and human-study handoff

1. **Acquire an independent optical clock.** Borrow a pulse generator, LED, photodiode and oscilloscope/logic analyzer with measured timing uncertainty. The camera's own timestamps cannot authenticate the source pulse. Capture both commanded edges and measured optical rise/fall, jitter and pulse-to-pulse drift. Record serial numbers, settings, raw traces, clock provenance and hashes. If hardware is unavailable, record `NOT_MEASURED`, not a fabricated timing precision.
2. **Identify the camera acquisition kernel.** Record linear RAW/dark/flat-corrected LED response at a frozen randomized pulse-phase schedule over >=3 image rows, multiple exposure settings and illumination levels. Fit on one phase set; reserve an unseen phase set and a different session/device for prospective error. Test row-specific delay, exposure shape, frame clock, nonlinear response, saturation, gain/white-balance/HDR, brightness, blur, glare, gaze and glasses. Use measured confidence *bounds*, not a point estimate or metadata assertion, to determine whether the boxcar approximation is admissible.
3. **Independently label anatomy.** Two genuinely independent human raters complete the E002-418 blinded qualification and E002-407/408 anatomical eyelid landmarks on the fixed high-speed recordings; preserve disagreement and unresolved intervals. Do not revive E002-417's rejected pixel-gap proxies. Obtain actual physical geometry and separately measured physiological velocity evidence from calibration participants, and freeze a prospective held-out participant/device prediction.
4. **Falsify before certifying.** Compare every predeclared ordinary-camera gap prediction against high-speed reference evidence, counting unresolved reference intervals in E002-419's partial-identification bounds. A witnessed crossing contradicting a certified no-crossing is a hard failure. Keep selective coverage, nuisance-stratified abstention, false-certificate counts, calibration uncertainty and participant-level independence explicit. External replication is required. No PERCLOS, blink-duration or fatigue claim is inferred from this instrument test.

## Prior art and decision

Pulsed/LED shutter metrology is not novel: Huai et al., *Optics Letters* 48, 847–850 (2023), DOI [10.1364/OL.474375](https://doi.org/10.1364/OL.474375); Kurosawa et al., *Japanese Journal of Forensic Science and Technology* 29, 135–153 (2024), DOI [10.3408/jafst.875](https://doi.org/10.3408/jafst.875); shutter-speed measurement review, *Sensors* 22, 1871 (2022), DOI [10.3390/s22051871](https://doi.org/10.3390/s22051871). These precedents prevent claiming novelty for LED calibration or rolling-shutter detection. Lucent's contribution here is a reproducible, fail-closed gate tied to its conditional no-closure decision.

**Scientific decision:** Synthetic instrument checks support the feasibility of a *specific* externally timed LED calibration experiment and falsify several corrupt acquisition assumptions. They do **not** establish physical shutter timing, anatomical aperture, a hard physiological velocity bound or a real-human no-hidden-closure result. E002-371 remains **physically unvalidated**. Product output stays **`ABSTAIN_UNCALIBRATED`** for hidden closure, blink duration, PERCLOS and fatigue.
