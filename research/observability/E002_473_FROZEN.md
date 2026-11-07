# E002-473 FROZEN — primary-literature velocity stress test of camera design

Date: 2026-10-27. Frozen **before** new code, numeric evaluation, or results. One active Lucent kernel remains E002-371's physical shutter-gap/eyelid-velocity validation. This experiment uses *published human measurements* as externally sourced design stressors; it is not independent raw-video validation, a universal human velocity bound, or another nominal-frame-rate audit.

## Independent source values and distinctions

1. Kwon et al., *J. R. Soc. Interface* 10 (2013), DOI 10.1098/rsif.2013.0227, https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/ . Phantom high-speed imaging at 600 fps, 25 volunteers, palpebral aperture sampled for analysis every 5 ms. Reported mean of peak **voluntary closing** aperture speed 243 ± 9 mm/s (authors' SEM). This is **not** a hard upper bound, a reflex/spontaneous blink maximum, or proof of ordinary-camera calibration.
2. Sun et al., *Investigative Ophthalmology & Visual Science* 38 (1997), 92–99, as *secondarily tabulated* by Kwon et al. (2013), Table 1, 500-Hz electromagnetic search-coil measurement. 40–49 age stratum n=8 reports 427 ± 30 mm/s closing peak. This is a **different measurement modality** with lid-attached coil and cannot be equated to optical palpebral aperture velocity without calibration. Use only as a non-comparable stress scenario; do not claim independent primary-text verification of this value.
3. *Analysis of Spontaneous Eyelid Blink Dynamics Using a 240 Frames per Second Smartphone Camera*, 2019, PMID 30893187, https://pubmed.ncbi.nlm.nih.gov/30893187/ . Ten volunteers; reported mean blink closure velocity 93 mm/s and observed range 40–160 mm/s. Not directly comparable to the Kwon peak voluntary aperture speed; report context only, not a hard cap.

## Frozen predictions and quantitative gates

Use E002-472's *already frozen* symmetric uniform-shutter sufficient condition and fixed endpoint margin 1.0 mm, per-endpoint aperture uncertainty 0.1 mm, ordinary clock error 0.1 ms, reference exposure 0.2 ms, reference clock error 0.1 ms. No fitted parameters.

At each (fps, exposure ms) = (30,4), (240,1), (300,1), compare external velocity *stress scenarios* V=93, 160, 243, 427 mm/s. Compute critical speed Vcrit and minimum aperture margin mcrit for each. Independently recompute via Python fractions and via the repository's E002-456 evaluator. Predict:
- 30/4 at 243: conditional exclusion **not supported** at 1-mm margin.
- 240/1 at 243: **conditionally feasible only**, no physical release.
- 240/1 at 427: **not supported** at 1-mm margin.
- 300/1 at 427: **conditionally feasible only**, no physical release.
- A larger margin can restore conditional feasibility at a given V; report the exact strict inequality and never call a published cohort mean a physiological cap.
- If the reference dark gap fails, return design abstention regardless of numerical Vcrit.

Falsification: disagreement with E002-456 on any row, arithmetic discrepancy >1e-9 in independent rational checks, any row authorizing physical release, or any claim that a published mean/SEM/range is a universal hard bound. Report all rows, including negatives. No new raw human acquisition is claimed. Existing physical protocol remains the next experimental gate.

## Noninterference and release

Do not access holdout human videos, modify other E002 evidence, merge PR #26, alter Hush PR #45, or change hourly scheduling. Commit protocol first, then simulator/tests and result. Preserve E002-455's prior optical nuisance failure and any in-progress CI evidence.