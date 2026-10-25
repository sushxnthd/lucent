# E002-430 — a 600-fps recording is not a continuous-time negative reference

**Date:** 2026-10-25. **Evidence tier:** original **synthetic finite-reference-sampling falsification**, independent numerical oracle and published human *aggregate* kinematics. **Not** a human-trial validation, real-camera calibration or new theorem.

## Decisive experiment

A high-rate camera can observe every acquired frame with eyelid aperture **2.15 mm**, while a continuous physical aperture dips below a **2.00-mm** threshold *between frames*. Construct World A with constant aperture 2.15 mm and World B with a single triangular dip to **1.95 mm** exactly halfway between two reference samples. Both worlds give the same physical aperture at **all** reference sample times, not merely at two selected endpoints.

| Reference grid | Interval (ms) | Hidden-world required peak speed (mm/s) | Lower envelope using V=243 mm/s (mm) |
|---|---:|---:|---:|
| 200 Hz (5-ms annotations) | 5.0000 | 80 | **1.5425** |
| 400 Hz | 2.5000 | 160 | **1.84625** |
| 500 Hz | 2.0000 | 200 | **1.9070** |
| 600 Hz | 1.6667 | 240 | **1.9475** |

Every synthetic witness has speed <= 243 mm/s and crosses the threshold, despite all sampled reference apertures being above it. **243 mm/s is a reported sample/group mean peak closing speed, not a verified individual or population upper bound.** It is used solely for illustrative sensitivity. This is an adversarial construction, not evidence that real humans make such precise subframe triangular dips.

[Technical vector figure](E002_430_REFERENCE_ALIAS.svg) compares the indistinguishable sampled worlds and the hidden physical crossing.

## Why this changes Lucent's validation protocol

A held-out reference video is not automatically a continuous-time ground truth. Calling an interval NEGATIVE_CONDITIONAL because every 400–600-fps annotation is above threshold can **understate Lucent's false-certification rate** if an unobserved crossing occurs between reference frames. The product may remain blocked even after a high-speed dataset arrives unless reference uncertainty is controlled.

For independently authenticated *physical* aperture samples y0,y1 with errors <= epsilon, sample spacing dt, endpoint clock errors <= j, and a **hard** physical velocity cap V, let a=y0-epsilon, b=y1-epsilon, D=dt+2j. The interval lower envelope is

```
L = max(0, (a+b-V*D)/2, a-V*D, b-V*D)
```

This follows classical Lipschitz cone intersection and is **not new mathematics**. If L>theta for *every* valid reference interval, a no-crossing reference label is conditionally supported; otherwise, absent a witnessed crossing, the reference label is **UNRESOLVED**. A speed cap inferred from observed frame-to-frame differences or from published group means is **not** a hard physical cap. Geometry, exposure, blur, occlusion, brightness, glasses, gaze and missingness must also be independently bounded; if any is unresolved, abstain.

This bound is a reference-sampling control, **not** a replacement for E002-371's calibrated exposure-integrated camera theorem.

## Verification

The standard-library-only [experiment](e002_430_reference_sampling.py) and [independent tests](test_e002_430_reference_sampling.py) ran locally with **six passing test groups**. The tests independently construct the triangular witness on 10,001 time points per rate, check peak slopes, compare the envelope against 200,001-point two-cone numerical minimization in four regimes, test 0.05-mm measurement error and 0.1-ms clock uncertainty, require a positive safe control, and reject invalid input. A separate [machine-readable aggregate](E002_430_SYNTHETIC_AGGREGATE.json) records the four frozen rates.

Reproduce:

```bash
cd research/observability
python -m unittest -v test_e002_430_reference_sampling.py
python e002_430_reference_sampling.py
```

The numerical oracle is independent code but not an external laboratory replication. No hosted verification is claimed until GitHub Actions actually completes.

## Primary-literature boundary and access

Kwon et al., *J. R. Soc. Interface* (2013), DOI **10.1098/rsif.2013.0227**, acquired **600-fps** video from 25 volunteers but **measured central palpebral aperture every 5 ms**. Thus, the published aperture annotation cadence was 200 Hz, not 600 Hz. They report mean peak closing speed **243 ± 9 mm/s**. [Full article](https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/).

Navascues-Cornago et al., *The Ocular Surface* (2026), DOI **10.1016/j.jtos.2026.01.003**, acquired human blink video at **500 fps** and reported underestimation of peak velocity at lower sampling rates. [PubMed](https://pubmed.ncbi.nlm.nih.gov/41565104/).

Two targeted public high-rate human-data searches did not yield downloadable, independently registered, individual-level **physical-aperture traces with authenticated shutter and clock**. FaceBase's 400-fps human eyelid data require controlled access. No public imagery was repurposed as calibrated physical ground truth.

## Next physical experiment and release consequence

Obtain consented/authorized 400–600-fps traces and two blinded human anatomical-margin annotations, physical geometry/scale and camera/photodiode timing. Preseal ordinary-camera predictions on unseen participants and devices. For each high-rate reference interval, independently bound anatomical error, timing and a physiologically justified speed hypothesis; classify witnessed crossing / conditionally excluded crossing / unresolved. Preserve every unresolved interval in the E002-426 participant-weighted error identification interval, including nuisance and missingness strata. Never infer a population deterministic speed cap from finite participant maxima.

**E002-371 remains physically unvalidated.** This result tightens the reference-label release blocker, not the product's allowed measurement set. Lucent retains `ABSTAIN_UNCALIBRATED` for physical no-closure guarantees, blink duration, PERCLOS and fatigue. Do not merge or claim world-class completion without real human and independent instrument evidence.
