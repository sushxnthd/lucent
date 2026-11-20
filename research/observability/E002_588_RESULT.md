# E002-588 | An exact nonlinear-camera counterexample to optical shutter identifiability

**Frozen first:** [E002_588_FROZEN.md](E002_588_FROZEN.md), commit `b4dacf9`, before executable implementation. **Evidence tier:** exact synthetic measurement-model falsification; no physical sensor or human validation. Parent E002-587, primary E002-371.

## Result

Two different camera exposure models produce **identical brightness observations at all 75 frozen phase/row samples**, even with exact timestamps, zero intensity noise, three rolling-shutter rows and a single, shared, continuous **strictly increasing** intensity-transfer function in the second world. A camera's optical-step brightness is not a uniquely invertible exposure-support measurement if the imaging response is merely assumed monotone rather than independently calibrated linear.

For row `r`, phase `p`, exposure start `s=s0+0.1r` ms, exposure duration `E`, and tone response `h`, the synthetic observation is

`y(r,p)=h(clip((s+E-p)/E,0,1))`.

The 75 frozen samples use rows 0,20,40 and 25 phases 0,0.5,...,12 ms. World A uses `s0=2.1`, `E=4`, `h(x)=x`. World B uses `s0=2`, `E=4.5`, and the same monotone LUT at every row and phase:

| Raw fraction x | 0 | 1/9 | 8/9 | 1 |
|---|---:|---:|---:|---:|
| World B transfer h(x) | 0 | 1/40 | 9/10 | 1 |

Linear interpolation between these knots has strictly positive slopes `9/40, 9/8, 9/10`; it is continuous and maps black to black and white to white. This is **not** a per-sample adjustment or a nonmonotone adversarial mapping. The worlds have exactly equal observed brightness for **75/75** samples, including **51 saturated** observations, as checked with rational arithmetic.

| Row | A exposure support (ms) | B exposure support (ms) |
|---|---|---|
| 0 | [2.1,6.1] | [2,6.5] |
| 20 | [4.1,8.1] | [4,8.5] |
| 40 | [6.1,10.1] | [6,10.5] |

Under the illustrative assumption that these three rows span the relevant imager support, with an exact periodic 30-Hz frame interval, the interframe uncovered gap is `T-(40d+E)`. Thus A yields **76/3 ms (25.333...)** and B yields **149/6 ms (24.833...)**, differing by **exactly 1/2 ms**. This is a model-conditional exposure-gap consequence, not a measured 30-fps sensor.

## Prospective unseen-phase discriminator

The frozen row-0 probe at **p=6.25 ms** is not among the 0.5-ms phase-grid observations. World A predicts **0** brightness and World B predicts **1/80**. This is a concrete prediction for an additional optical measurement that separates the *two constructed worlds*. It does not imply that a single additional phase identifies an arbitrary unknown camera response.

## Independent verification

The Python [exact-rational generator and adversarial controls](e002_588_nonlinear_shutter.py) and a separately implemented [Node BigInt replay](e002_588_independent_replay.cjs) both passed locally. The independent implementation recomputes all 75 observations and the held-out probe from first principles rather than trusting the generator's outputs. Controls reject a nonmonotone LUT and show that identity-only B, a changed rolling delay, and a swapped phase no longer reproduce the same observations. [Dedicated hosted workflow](../../.github/workflows/e002_588_nonlinear_shutter.yml) was committed; do not infer hosted success without checking its actual run.

**Scope and limitations:** The construction is synthetic and uses a selected finite phase grid and a monotone piecewise-linear tone response. It is a counterexample to **unverified monotone-response identifiability**, not to the E002-587 linear-model LP (which remains mathematically conditional on its stated assumptions). A camera with an authenticated linear raw sensor response, independent dark/white linearization, photodiode timing and sufficiently informative phases may exclude this particular alternative. No claim is made that a deployed camera actually has this LUT, that all unknown response functions are ambiguous by 0.5 ms, or that this is novel relative to camera response calibration literature.

## Direct enforcement consequence

**Reject** a physical shutter-gap certificate derived from step-brightness inversion unless linear radiometric response (or a defensible bounded nonlinear response family) is independently authenticated for the actual image path and settings. Include that response uncertainty in the feasible exposure-support set; an LP certificate conditional on an unauthenticated linearity flag cannot be promoted to physical evidence. Preregister a held-out randomized phase scan, optical clock/photodiode reference, dark/white response controls, auto-exposure/HDR/rolling-mode controls and adversarial brightness/gain changes. Any held-out observation outside the predicted response interval invalidates the camera certificate. Do not equate optical gap estimates with physiological blink or fatigue inference.

**Unresolved:** independently blinded anatomical rater pairs 0; calibrated physical shutter captures 0; independently justified hard continuous-time eyelid-velocity ceilings 0; held-out physical closure predictions 0. **Lucent product:** `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush branch and PR remain separate.


## Primary-literature priority check

The general requirement to estimate nonlinear camera radiometric response is established, not novel: Debevec and Malik, *Recovering High Dynamic Range Radiance Maps from Photographs*, SIGGRAPH 1997, DOI [10.1145/258734.258884](https://doi.org/10.1145/258734.258884), explicitly reconstruct imaging response from differently exposed images. Mitsunaga and Nayar, *Radiometric Self Calibration*, CVPR 1999, DOI [10.1109/CVPR.1999.786966](https://doi.org/10.1109/CVPR.1999.786966), explain that camera/video output is frequently nonlinear and present response-function calibration. E002-588 claims **only an exact counterexample for the specific Lucent optical shutter-support certificate under an unverified response assumption**; it does not claim first discovery of radiometric ambiguity, nonlinear sensor behavior or response calibration. This is a targeted, not exhaustive, priority check.
