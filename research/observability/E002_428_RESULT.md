# E002-428 — independent 2026 human frame-rate evidence and velocity-tail power falsification

**Date:** 2026-10-25. **Frozen protocol:** [E002_428_FROZEN.md](E002_428_FROZEN.md), committed first at `afb0506087e6fa916d13edd491a4f21816c3a0f5`. **Evidence tier:** independently published **human aggregate study** plus new reproducible **statistical/instrument-design calculations**. **No individual-level human recordings were obtained, analyzed or represented as Lucent validation.**

## External empirical result that changes the measurement strategy

Navascues-Cornago et al., *The Ocular Surface* **40** (2026), pp. 22–30, DOI **10.1016/j.jtos.2026.01.003**, published online January 19, 2026, recorded spontaneous blinks in **20** participants and reflex blinks in **10** additional participants at **500 fps**, downsampling to 250, 100, 50 and 25 fps. The peer-reviewed abstract reports **marked underestimation of maximum velocities below 250 fps** for both blink types, particularly reflex blinks. It recommends at least **250 fps for comprehensive blink-dynamics measurement**. It also finds some amplitude/duration metrics comparatively less sensitive to frame rate. [PubMed 41565104](https://pubmed.ncbi.nlm.nih.gov/41565104/) · [University of Manchester publication record](https://research.manchester.ac.uk/en/publications/video-frame-rate-influences-the-accuracy-of-blink-dynamics-measur/).

**Interpretation:** E002-371 needs an *upper* speed bound to exclude hidden closures. Low-frame-rate observed speed maxima are therefore biased in the dangerous direction if promoted to a hard V. A finding that blink *duration* has low mean bias in a particular population does **not** imply that each hidden closure is identifiable or that fatigue/PERCLOS can be certified. No raw study data or individual distributions were supplied; no quantitative velocity bias percentages are invented.

## Frozen participant-level risk calculation, executed

A frozen V from a separate training cohort is evaluated as a **participant-level** exceedance event across the declared tasks and nuisance conditions, not as frame-wise Bernoulli trials. With k witnessed exceedances among n independent held-out participants, the one-sided 95% exact Clopper-Pearson upper confidence limit p_U solves `Pr(Binomial(n,p_U) <= k)=0.05`; at k=0, `p_U = 1 - 0.05^(1/n)`.

| Independent held-out participants n | Witnessed exceedances k | One-sided 95% upper bound on participant exceedance probability |
|---:|---:|---:|
| 8 | 0 | 31.234% |
| 25 | 0 | 11.293% |
| 100 | 0 | 2.951% |
| 299 | 0 | 0.997% |

**Decisive study-power consequence:** Even a perfect zero-violation result on 25 independent people does not establish a 1% tail ceiling; under IID sampling the one-sided 95% upper bound is **11.293%**. A target strictly below 1% requires at least **299 independent held-out people with zero violations**. This remains a *probability* statement, never a hard bound on an individual trajectory.

The evaluator explicitly distinguishes **witnessed exceedances**, **unresolved participants**, and **clean nonexceedances**. It reports a best-case/worst-case sensitivity interval for the exact upper limit, with all unresolved treated as violations in the conservative end. It refuses malformed counts, nonfinite/nonpositive V, absent freeze references and invalid alpha. A reference string is not cryptographic provenance; it must be independently archived before holdout access. Statistical coverage additionally requires IID participants in the specified stratum, prespecified V, credible peak-speed measurement, and multiplicity control across strata.

## Verification and reproduction

The stdlib-only [evaluator](e002_428_velocity_tail.py) and [independent test suite](test_e002_428_velocity_tail.py) were executed locally before commit. **Five groups passed**, including separate `math.comb` binomial inversion, zero-event frozen power values, monotonicity, missingness worst cases, provenance/input rejection and invariant `ABSTAIN_UNCALIBRATED`. This is a numerical/statistical verification, **not a new human empirical trial**.

```bash
python -m unittest -v research/observability/test_e002_428_velocity_tail.py
python research/observability/e002_428_velocity_tail.py --participants 25 --witnessed 0 --unresolved 0 --frozen-velocity-mm-s 400 --frozen-reference independently-archived-training-v
```

The second command is a **hypothetical 400 mm/s** sensitivity example, not an estimate of the human tail. Hosted CI is tracked separately; do not call it successful before a completed run.

## New claim boundary and executable next study

**Reject** ordinary-camera velocity maxima as a hard E002-371 input, and **reject** finite-cohort 95% velocity-tail bounds as substitutions for the deterministic hard V. Keep physical hidden-closure guarantees, blink duration, PERCLOS and fatigue at **`ABSTAIN_UNCALIBRATED`**. A future probabilistic product would need direct prospective participant/device-disjoint evaluation of the **entire camera classifier**, not just a velocity tail.

**Human acquisition:** Obtain controlled 400-fps FaceBase marker data with authorized use and validated mapping to central anatomical aperture, or independently consented **>=500-fps** synchronized eyelid videos. Independently verify exposure, row timing and clock with photodiode; obtain **two blinded human raters**; stratify spontaneous versus reflex blinks, geometry, brightness, missingness, blur, gaze and glasses. Freeze V from training participants and participant-disjoint 24/30/60/120-Hz virtual-camera predictions under E002-426 **before** reference labels. Reserve >=299 *independent* holdout people only if pursuing a 1% population-tail claim under the stated IID assumptions; this is a demanding sample-size illustration, not an immediate recruitment promise. Evaluate each stratum's power and multiple-testing plan separately. Where human data access fails, preserve this synthetic/statistical substitute and report the unresolved physical gate.

**Novelty/priority:** Exact binomial confidence limits are classical (Clopper–Pearson, 1934); frame-rate bias in blink kinematics is independently established in 2026. No new theorem, novel human physiological discovery, physical camera calibration, or external replication is claimed. Hush's independent branch and PR remain outside this workstream.
