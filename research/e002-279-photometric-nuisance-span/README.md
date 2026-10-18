# E002-279 — Exact photometric nuisance-span collision (2026-10-18)

**Status:** Exact conditional identifiability law; independent synthetic LP verification. NO human RGB/reference evaluation; NO camera-calibrated error bound; NO fatigue claim; NO claim of novel general mathematics.

## Active kernel — one product-critical question

Can ordinary RGB pupil/iris log-radius changes be distinguished from a camera brightness-dependent contour artifact when both are driven by the same screen stimulus?

1. Signal/reference: z=log(apparent RGB pupil/iris radius) versus synchronized same-eye eye-tracker log-diameter change (reference NOT accessed).
2. Frontier: pupil foreshortening, camera contrast and optical bias are established; bounded-noise regression and Chebyshev approximation are classical.
3. Scalar metric: d_inf(s,col(X))=min_beta max_i |s_i-(X beta)_i|; critical amplitude 2*epsilon/d.
4. Strongest confound: a delayed brightness-dependent camera artifact sharing the physiological pupil light-reflex impulse response.
5. Generative model: raw image I_k = camera_pipeline(exposure_average(render(pupil,iris,gaze,eyelid,brightness,optics)),gain,blur,noise); restricted scalar z=X beta+A s+e, |e_i|<=epsilon. X includes intercept, time drift, measured screen brightness and photometric-artifact response; s is a known sampled physiological template. This simulator uses sampled first-order transfer functions, NOT raw-image rendering.
6. Decisive falsification: artifact-only and physiology-only traces coincide exactly when s belongs to col(X); omission of this artifact from X produces a false certificate.
7. Mechanism boundary: H0 and H1(A) intersect iff |A| d_inf(s,col(X))<=2epsilon. If d=0, amplitude is unidentifiable regardless of size; if |A|d>2epsilon the two specified hypotheses are separated.
8. Untouched human test: pending; freeze nuisance channels, clock uncertainty, reference-blind admission, participants/devices/light/gaze/glasses splits BEFORE seeing references.
9. Publication: independent checker, primary prior-art audit, calibrated physical-camera nuisance bounds, unseen prediction and untouched human holdouts needed; math alone not a field-level breakthrough.
10. Product: reject light-probe PLR/fatigue certification without calibrated camera response. Allow a conditional response certificate only when d>0 and error bounds are independently established. Investigate blink/eyelid timing as a separate candidate.

## Exact theorem / constructive witness

Let H0={Xb+e: ||e||inf<=epsilon} and H1(A)={As+Xb+e: ||e||inf<=epsilon}. They intersect iff min_g ||As-Xg||inf<=2epsilon. Proof: subtraction gives necessity. For any g meeting the bound, z=(As+Xg)/2 belongs to both sets with errors +/- (As-Xg)/2. Positive homogeneity gives the threshold. The dual is d=max_{X^T w=0, ||w||1<=1} w^T s. This is classical finite-dimensional set separation, NOT a new mathematical discovery.

## SCIENCE ledger (deterministic synthetic only)

30 fps, 120 samples, physiological lag 0.24 s, first-order time constant 0.32 s, hypothetical epsilon=0.001 log units, test amplitude 0.020 log units. No human measurements.

| Screen probe | Camera-artifact lag 0 s: Acrit | Lag 0.12 s: Acrit | Lag 0.24 s |
| --- | ---: | ---: | --- |
| Single step | 0.010299 | 0.014653 | infinity |
| Double pulse | 0.007367 | 0.010802 | infinity |
| Pseudorandom blocks (seed 279) | 0.006078 | 0.008991 | infinity |

A nuisance response at 0.24 s has exactly the physiological template; EVERY tested stimulus becomes unidentifiable. Adding richer stimuli cannot fix a transfer-function collision if the nuisance class includes the physiological response for every stimulus. With the omitted delayed nuisance, the reduced model incorrectly certifies a purely artifactual waveform as physiological. This is a model-misspecification adversary, NOT a measured real-camera false-positive rate.

Independent checker: nine feasibility LP replays; exact rational two-sample anchor (Acrit=2/5); three mutation guards. Full raw synthetic vectors and dual witnesses for two cases are generated in results.json. A wildcard blink-like aperture pulse not locked to brightness gave hypothetical d~0.5, Acrit~0.004; it is NOT human blink evidence.

## PRODUCT ledger

**Reject** brightness-locked physiological or fatigue claims when delayed pupil-specific camera artifacts are unbounded. **Calibrate** pupil/iris contour contrast, gain/exposure response, aperture, gaze, optics and clock. **Conditionally allow** a response detector only when X and epsilon are independently validated, reference-blind admission holds, and |A|d>2epsilon. **Explore** blink/eyelid observables with independent human ground truth. Do not resume app-building or APST-5.

## Reproducibility / failed gates

Run: python experiment.py && python independent_check.py. Dependencies: numpy, scipy. The workflow saves raw and derived JSON as an Actions artifact. Missing gates: human paired data, physical camera calibration, independent device holdouts, clock bounds, real RGB nuisance transfer and novelty beyond established regression mathematics. Inherited workflow success is not proof that this new kernel ran.

## Primary prior-art collision

- Hayes & Petrov 2016, gaze-position artifact: https://www.alexpetrov.com/pub/brm16/
- RGB smartphone pupillometry with 630-700 nm filter and external hardware (2023): https://doi.org/10.1038/s41598-023-40796-0
- Pupillometry publication recommendations (2022): https://pmc.ncbi.nlm.nih.gov/articles/PMC9272460/
- Portable PLR latency (2024): https://pmc.ncbi.nlm.nih.gov/articles/PMC11503361/
- Beck & Eldar 2007, bounded-noise regression: https://doi.org/10.1137/060656784
