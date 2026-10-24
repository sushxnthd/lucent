# E002-416 — reference-camera false-negative label falsification

**Date:** 2026-10-24. **Frozen first:** `E002_416_FROZEN.md` committed at `099069a459f5e75cf50efc21a7264a7c2717c072` before implementation. **Evidence tier:** deterministic synthetic reference-camera counterexample, exact conditional Lipschitz lower envelope, independent 1,000-case numerical oracle, nuisance/provenance regression. **Not measured human physical aperture or instrument timing.**

## Result and decision

A high-speed recording is not an automatically valid *negative* ground-truth oracle. In particular, two reference frames both showing open eyelids cannot rule out a closure between frames unless independently bounded physical aperture velocity, measurement uncertainty, shutter timing and geometry jointly exclude it. This problem applies to the high-speed reference itself, not only to the ordinary camera being evaluated.

For equal instantaneous normalized-aperture endpoints `a(0)=a(d)=0.30`, closure threshold `theta=0.20`, and **hypothetical** hard Lipschitz velocity `V=60/s`, the exact possible minimum is `max(0,0.30-V*d/2)`. The dimensionless risk ratio `V*d/[2*(0.30-theta)]` gives:

| Reference rate | Inter-frame gap | Dimensionless ratio | Sharp possible minimum | Conditional reference-negative label |
|---|---:|---:|---:|---|
| 160 fps | 6.25 ms | 1.875 | 0.1125 | **UNRESOLVED** |
| 240 fps | 4.1667 ms | 1.25 | 0.175 | **UNRESOLVED** |
| 1000 fps | 1 ms | 0.30 | 0.270 | NEGATIVE_CONDITIONAL |

The 160-fps witness `a(t)=0.30-60*min(t,d-t)` is physically continuous and exactly respects the *assumed* speed limit, yet falls to **0.1125** between two observed open/open frames. This is a **synthetic mathematical witness, not an observed human blink**. A 1000-fps conditional negative label becomes unresolved when the independent per-endpoint clock uncertainty is 1.5 ms (effective worst-case gap 4 ms).

For asymmetric uncertain endpoint apertures, the exact conservative lower envelope is the minimum on `[0,d]` of `max(L0-V*t, L1-V*(d-t), 0)`, with the meeting point clipped to the interval. A negative reference label requires that bound **strictly exceed** the closure threshold. A witnessed positive requires an independently measured instantaneous aperture upper bound at or below the threshold. Inconsistent endpoint constraints and all critical nuisance flags fail closed.

## Executed verification

The dependency-free Python implementation and a **separately coded brute-grid oracle** passed seven local tests: H1 sampling-rate transition; H2 explicit hidden-closure witness; H3 clock-error reversal; H4 empirical velocity maxima rejected as hard limits; H5 missingness, blur, glare, occlusion, gaze, glasses, geometry, brightness, saturation, clock and rolling-shutter fail-closed controls; H6 product-output isolation; plus **1,000 seeded independently gridded cone-envelope checks** (2,001 grid points each). No real human annotation or camera acquisition was executed in this experiment.

Files: `e002_416_reference_truth.py`, `test_e002_416_reference_truth.py`, `.github/workflows/e002_416_reference_truth.yml`.

Local reproduction from repo root:

```bash
python research/observability/test_e002_416_reference_truth.py
```

The tool's inputs are self-asserted and **never authenticated by the tool**. Even a conditional negative result remains `REFERENCE_NEGATIVE_CONDITIONAL`, never `CONFIRMED_NO_CROSSING`; every output retains `product: ABSTAIN_UNCALIBRATED`, `product_claim_authorized: false`, `physical_provenance_authenticated_by_tool: false`. GitHub-hosted CI must be checked separately; local success is not described as hosted success.

## Priority and independent literature context

The result is a classical Lipschitz inter-sample extremum bound, **not a new theorem**. Espinosa et al., *PLoS ONE* 13:e0196125 (2018), DOI 10.1371/journal.pone.0196125, already investigated **26 human participants recorded at 240 fps**, and explicitly discussed why 60-fps imagery inadequately resolves eyelid kinematics. Their paper describes reflected-intensity eyelid-position proxies and a public data link (University of Alicante repository handle 10045/74398). The repository landing page returned HTTP 403 during this run; access to the actual videos and calibration metadata was **not** verified. This prior work prevents novelty claims for high-speed blink capture, intensity tracking, or the general need for higher frame rates. The 2025 *Scientific Data* EEG/eye-tracking/high-speed-video dataset remains Lucent's existing real-human source; it does not independently calibrate physical aperture and shutter response.

## Direct human-validation consequence

The 632 unannotated frames in E002-407 are not 632 negative reference labels. Even after two raters annotate them, a frame-to-frame open/open interval must be recorded as `REFERENCE_UNRESOLVED` unless a separately verified deterministic velocity and timing/geometry envelope rules out a crossing. A negative label cannot be inferred merely from absence of a closed reference frame. Exclude unresolved intervals from the *resolved-reference* denominator, but retain them explicitly in eligible-gap and abstention denominators to prevent optimistic censoring (E002-413/414). This rule prevents falsely favorable false-certificate estimates.

## World-class gate still unmet

No real-human hard velocity cap, two independent blinded physical eyelid annotations, independently measured camera shutter/exposure response, instrument-clock uncertainty, unseen-device prediction, or independent external replication exists. This run therefore does **not** validate E002-371 or justify blink duration, PERCLOS, fatigue, or hidden-closure exclusion. Next experimental priority remains two blinded E002-407 rater sheets, E002-408 adjudication, and independently timed physical reference measurements; avoid further synthetic theorem polishing unless it exposes a concrete invalid study or product decision.
