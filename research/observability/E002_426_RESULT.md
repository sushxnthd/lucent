# E002-426 — Prospective human-validation lock: completed study-control experiment

**Date:** 2026-10-25. **Frozen before implementation:** `E002_426_FROZEN.md` at commit `d279b12ae11bb9b2cbce7708cd705e439647a104`. **Evidence tier:** executable synthetic adversarial evaluation of study design and reporting, **not** human physical-aperture evidence. No real human reference sheets or camera hardware were accessed.

## Decisive falsification of pooled-only evaluation

A frozen 100-trial synthetic control assigns 99 valid, reference-negative conditional predictions to one held-out participant and a single witnessed false certificate to a second held-out participant. A pooled, frame-weighted false-certificate fraction is **1/100 = 1%**, while the equally participant-weighted average is **(0%+100%)/2 = 50%**. Both numbers are mathematically correct for their respective estimands; reporting only the pooled result conceals the failure of the second participant. This is a standard cluster-weighting/evaluation problem, not a novel scientific theorem or measured human failure.

A second synthetic control with one witnessed failure and two unresolved/missing references among 100 conditional predictions yields sharp descriptive finite-set bounds **[1%,3%]**. The unresolved cases remain in the denominator and are never silently treated as safe. An all-abstain system reports undefined selective error.

## Preregistration and adversarial integrity results

Six independent local Python unittest groups passed:

1. Pooled-vs-participant-macro imbalance and blur nuisance stratification.
2. Explicit unresolved/missing reference accounting and rejection of missing CSV rows.
3. SHA-256 seal detects prediction, interval, nuisance, calibration-reference, and trial-list mutation.
4. Training/holdout subject overlap, duplicate trials, missing nuisance fields and nonfinite times are rejected.
5. All-abstain selective error remains undefined, not zero.
6. Duplicate or invalid reference CSV labels are rejected.

**Important threat-model limitation:** A SHA-256 seal detects post-freeze changes only when the original seal is archived independently before labels are viewed. A dishonest coordinator who replaces both manifest and seal can evade this software check. The scorer does not authenticate physical provenance, rater independence, timestamp/exposure calibration or deterministic human speed bounds.

## Reproduce (stdlib only)

```bash
python -m unittest -v research/observability/test_e002_426_prospective_lock.py
python research/observability/e002_426_prospective_lock.py freeze --registry /private/study/predictions.json > /independent-archive/seal.json
# Archive the seal and registry immutably before reference data become available.
python research/observability/e002_426_prospective_lock.py score \
  --registry /private/study/predictions.json \
  --seal /independent-archive/seal.json \
  --reference /private/study/independent_reference.csv > /private/study/score.json
```

The public repository contains **no real subject identifiers, face images, rater sheets, source linkage or event labels**. CI executes synthetic registry controls only and deliberately uploads no sensitive study artifacts.

## Product consequence

The prospective study must predeclare participant-disjoint predictions and report both pooled and participant-macro false-certificate identification intervals, as well as nuisance-stratified coverage and abstention. A good pooled score alone is insufficient to justify generalization. Even perfect results in this tool cannot authorize a physical no-hidden-closure certificate. `product=ABSTAIN_UNCALIBRATED`; `product_claim_authorized=false`.

## Next physical experiment (not performed)

Obtain two genuinely independent blinded E002-418 qualification and E002-407/408 real-human landmark sheets; independently measured photodiode/LED shutter waveform and rolling-shutter timing; anatomical geometry/optical transfer calibration; and a separately justified velocity envelope. Freeze untouched participant/device predictions with this E002-426 registry **before** high-speed reference labels are inspected. Score witnessed crossings, conditional negatives and unresolved intervals, including reference-camera temporal ambiguity from E002-416 and finite-set bounds from E002-419. A finite observed speed maximum is not a hard bound. Human evidence remains absent, so E002-371 is physically unvalidated.

## Priority and literature context

Participant-level evaluation and leakage control are established research practice. For comparison, the public GazeBase data descriptor reports 1,000-Hz eye-tracker data but **not a calibrated physical eyelid-aperture shutter model** (Scientific Data, 2021, DOI 10.1038/s41597-021-00959-y). RT-BENE has independently annotated open/closed images but does not by itself provide an authenticated high-speed physical aperture reference (Cortacero et al., ICCV Workshops 2019; Zenodo DOI 10.5281/zenodo.3685316). These resources are not claimed to satisfy Lucent's E002-371 physical-validation gate.

**No new physical human measurement was obtained in this run.** The meaningful advance is a reproducible, falsifiable prospective study lock and a direct product-evaluation restriction, not another synthetic shutter theorem.
