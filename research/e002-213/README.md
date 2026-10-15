# E002-213 | Nuisance-profile ocular information certificate

**Active signal/reference:** ordinary RGB pupil/iris temporal ratio against synchronized native-time same-eye eye-tracker pupil diameter. **Human waveform data this run: zero.**

## SCIENCE
For a differentiable image mean μ(r,η) and Gaussian noise covariance Σ, define j=Σ^(-1/2)∂μ/∂r and J=Σ^(-1/2)∂μ/∂η. The exact *local* efficient radius Fisher information is ||(I−P_J)j||² (Schur complement). A zero value means first-order local nonidentifiability, not global impossibility. For locally unbiased estimators, variance is at least 1/I_eff.

In 90 synthetic camera configurations (radii 3/5/8 px, blur 1/2/3/4/5/7 px, five nuisance sets), independent SVD checks passed. With read noise SD=0.02: r=3 px and blur=4 px has ideal known-nuisance CRLB SD 0.0328 px versus **9.799 px** after nuisance projection (contrast, brightness, gradient, focus, center and ellipticity). Only 0.00112% of radius Fisher information remains. At r=8 px and blur=3 px, nuisance-adjusted CRLB SD is 0.0514 px and 11.03% information remains. **Synthetic only.** The identity is standard estimation theory, not a new theorem.

## PRODUCT
Do not certify a pupil waveform from segmentation confidence alone. A calibrated focus/contrast/gaze/noise preflight can *reject* low-information frames; this is not itself a positive waveform certificate. Illustrative synthetic 0.25-px 95% CI half-width requires I_eff >= 61.47 px^-2; not a frozen human threshold.

## Active-kernel gates
- Scalar: held-out participant-bootstrap lower Pearson waveform correlation bound, plus frozen lag/amplitude/NRMSE, nuisance-superiority, and >=75% prospective participant coverage.
- Strongest confounds: defocus, local contrast, lighting gradients, gaze/ellipse, eyelid occlusion and camera clock.
- Decisive falsification: predeclared boundary fails on untouched synchronized humans, or waveform gates fail against nuisance controls.
- Publishable: >=8 untouched paired participants, device/lighting/glasses holdout, independent checker, mechanism-predicted unseen boundary and prior-art audit.
- Product: >=75% prospective acceptance without relaxing waveform gates.
- Kill: prospective failure or three nondiscriminating runs; two blocked dataset accesses force path switch.
- Human waveform, device holdout and fatigue-state inference: **NOT RUN**.

## Source provenance
Zenodo 19442493 is **restricted** (public metadata only); its description identifies Tobii/WebGazer gaze and UI logs but does not establish native RGB pupil-diameter video. EVE remains request-only with webcam clock uncertainties. EyeDentify's processed timefold cannot certify native rapid-waveform lag. No human dataset was accessed in this run.

## Local reproducibility
The 90-row synthetic CSV, exact executable camera model, independent SVD checker, mutation test, source audit and SHA256 manifest are in the E002-213 reproducibility package. Raw CSV SHA256: `3215d936599a70eedf6004c3339af83958d69d7dda59e160f3b5f08f4eba4db0`. Code SHA256: `0fc6cc24b6ae395d32c67e09aaad7412fc1e8d27301699ff6615de217f8cc642`. No human data hashes exist because no human data was downloaded.

**Smallest claim:** Under a specified Gaussian pupil-camera model, unknown optical and geometry nuisances can destroy nearly all *local* radius information in a low-resolution blurred regime. Human ordinary-RGB observability remains unresolved.
