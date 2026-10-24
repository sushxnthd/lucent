# E002-427 — Human-speed-scale transfer gate and high-rate reference adapter

**Date:** 2026-10-25. **Frozen before implementation:** `E002_427_FROZEN.md` committed at `17f89a26c0e73cec64b9742443c3f1304580e1fa`. **Evidence:** primary-literature human measurement values and a new **synthetic** 400-Hz virtual-camera falsification. **No individual-level FaceBase traces, physical shutter calibration, or independent human landmark sheets were obtained.** This is **not** physical validation of E002-371.

## Substantive new human-evidence finding

The 2013 Kwon et al. study recorded **25 actual people at 600 frames/s**, manually measured central palpebral aperture every 5 ms, and reported a mean peak closing speed of **243 ± 9 mm/s** (and initial aperture 9.83 ± 0.17 mm). Its literature comparison includes a prior **427 ± 30 mm/s** group-mean peak from search-coil measurements. These values show that Lucent's earlier synthetic **50–60 mm/s** velocity parameters are illustrative, **not physiologically justified conservative limits**. Neither published mean, group comparison, nor observed finite-sample maximum is a hard speed bound. Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/ ; DOI 10.1098/rsif.2013.0227.

**Illustrative observability penalty:** For the restricted E002-421 equal-exposure-average law, the aperture margin consumed by the speed hypothesis is `V/(2f)` millimeters at virtual frame rate `f`. This is a dimensional conversion, not an empirical prediction of camera reliability.

| Hypothetical speed V (mm/s) | 24 Hz margin | 30 Hz margin | 60 Hz margin | 120 Hz margin |
|---|---:|---:|---:|---:|
| 243 (2013 reported mean peak closing speed) | 5.063 mm | 4.050 mm | 2.025 mm | 1.013 mm |
| 427 (older study's reported group-mean peak) | 8.896 mm | 7.117 mm | 3.558 mm | 1.779 mm |

For example, at a hypothetical closure threshold of 1 mm, 30-Hz equal-average conditional exclusion would require both an authenticated **hard** 243-mm/s bound and measured mean aperture strictly above **5.05 mm**, before adding geometry, shutter, clock, optical or measurement uncertainty. At 427 mm/s, the nominal threshold rises to **8.12 mm**. These are **not real-camera product thresholds**, because the speed values are not hard bounds and exposure-average physical aperture is not independently available.

## High-rate data identified

**FaceBase: Eyelid Kinematics and Orbicularis Oculi Electromyography – Persons Without Facial Pathology**, released **2026-09-01**, DOI **10.25550/88-28BJ**. Eight adults performed five eyelid behaviors with **400-fps synchronized 3D eyelid-margin marker capture** and EMG. This is a better kinematic validation target than unlabeled webcam blink clips. However, individual-level data require controlled-access authorization, signed data-use documentation, and approved research use; **not downloaded or accessed**. The raw marker distance is not necessarily central anatomical aperture. Sources: https://trackhub.facebase.org/2026/09/01/recent-release-clites-eyelid-kinematics-emg/ ; https://docs.facebase.org/docs/human-data/ ; associated PNAS paper DOI 10.1073/pnas.2508058122.

## Executed synthetic falsification

The new stdlib-only adapter `e002_427_human_kinematics.py` accepts privately held deidentified, independently registered physical-aperture traces with explicit nuisance flags. It creates **virtual** boxcar camera averages from high-rate piecewise-linear interpolation, applies a conservative restricted balanced-slope conditional candidate, and scores high-rate reference labels without calling missing/ambiguous frames negative.

Nine local adversarial tests passed:

- **Wide-open synthetic trace:** 14 study-only conditional candidates, 0 witnessed failures, 0 unresolved; never authorizes a physical certificate.
- **Wrong-speed synthetic falsification:** one synthetic 400-mm/s closure at 30-Hz virtual sampling, with a deliberately incorrect **180-mm/s** camera-speed hypothesis, produced **1 witnessed false conditional candidate among 14** (7.14% of overlapping synthetic candidate intervals). The holdout secant-speed violation was explicitly flagged. This is **not a human false-certificate rate**.
- **Near-threshold synthetic trace:** 0 candidates, 14 abstentions; all-abstain selective error undefined.
- **Reference aliasing:** a 400-Hz sequence that appears open at every sample can still conceal a subframe threshold crossing when the reference-speed hypothesis permits it; the reference remains **UNRESOLVED**.
- **Nuisance/missingness and endpoint coverage:** missing samples and glasses flag prevent interpolation-based decisions; a definite clean witnessed crossing remains a falsification even when other samples are missing.
- **Integrity:** overlapping train/holdout participant IDs, invalid exposure widths, nonfinite numeric inputs and malformed CSVs are rejected.

Reproduce locally with `python -m unittest -v research/observability/test_e002_427_human_kinematics.py`. For authorized human traces, run `python research/observability/e002_427_human_kinematics.py --csv /private/registered_aperture.csv --config /private/frozen_config.json --output /private/aggregate.json`. **Do not upload source data, participant linkage, or individual-derived outputs to public GitHub/CI.**

The CLI is a **study-only adapter**, not a replacement for E002-426's prospective sealed prediction registry. Overlapping virtual-camera intervals are correlated. The code's `NEGATIVE_CONDITIONAL` label depends on a *hypothesized*, not authenticated, reference speed cap; its zero-error synthetic output is not a physical safety result.

## Direct product consequence and next action

**Reject any conversion of earlier 50–60-mm/s toy bounds into physiological camera claims.** Continue `ABSTAIN_UNCALIBRATED` for hidden-closure exclusion, blink duration, PERCLOS, and fatigue. Human data cannot be replaced by more synthetic theorem polishing.

Next decisive action: obtain controlled FaceBase access or independently consented 400–600-fps marker/video traces, register upper/lower margin motion to central physical aperture with bounded geometric error, and complete two independent blinded rater sheets. Then freeze participant-disjoint 24/30/60/120-Hz virtual-camera predictions with E002-426 before revealing reference labels, separately calibrate real shutter/clock behavior, and seek external replication. If anatomical registration or hard velocity justification fails, retain an explicitly **kinematic-marker-only** result and do not claim physical closure certification.

**Status:** local nine-test pass; hosted CI result to be checked independently. Hush branch/PR #45 unchanged.
