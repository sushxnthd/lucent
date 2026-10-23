# E002-405 — finite-sample velocity ceiling invalidates a deterministic no-hidden-closure claim

Date: 2026-10-24. Frozen protocol commit: `689bbf88f482f476eb8ceb0682f1ed85ec4bc1b5`.
Evidence tier: **exact classical rank law + synthetic physical-aperture false-certificate witness + source-level fail-closed bridge regression**. NOT human velocity validation.

## Scientific result: what the calibration maximum actually guarantees

For n calibration and m future *jointly exchangeable, distinct* speed magnitudes, the maximum of the n calibration observations is exceeded by at least one of the m future speeds with probability exactly

```text
P(any future speed > calibration maximum) = m / (n + m).
```

This is a classical order-statistic identity, not a new theorem. The probability concerns **speed-bound exceedance**, not the probability of an incorrect eyelid-closure certificate. No distribution-free hard maximum can be inferred from finite samples without extra assumptions. Exchangeability itself can fail across participants, devices, physiology or acquisition conditions.

The prespecified 5,000-replicate Monte Carlo tests (seed 405) yielded:

| Distribution | n calibration | m future | Exact exceedance probability | Observed |
| --- | ---: | ---: | ---: | ---: |
| Uniform | 20 | 10 | 0.333333 | 0.3326 |
| Uniform | 100 | 100 | 0.500000 | 0.4914 |
| Uniform | 1000 | 100 | 0.090909 | 0.0972 |
| Exponential | 20 | 10 | 0.333333 | 0.3218 |
| Exponential | 100 | 100 | 0.500000 | 0.5072 |
| Exponential | 1000 | 100 | 0.090909 | 0.0924 |

All six frozen absolute-discrepancy criteria (<0.03) passed. The independent checker exhaustively enumerated distinct ranks for (n,m)=(4,2),(5,3),(7,1), without calling the Monte Carlo sampler.

## Physical witness: a wrong certificate under an empirical ceiling

Two 1-microsecond uniform exposures centered at 0 and 40 ms both observe normalized physical aperture 0.30. The actual eyelid trajectory is the triangular function `a(t)=0.18+6|t-0.020|`, so at 20 ms the aperture reaches **0.18**, crossing the threshold **0.20**. The actual maximum speed is **6/s**.

The previously accepted independent-velocity Boolean can be asserted alongside a finite-sample ceiling of **4/s**. E002-399 then reports `CONFIRMED_NO_CROSSING` with lower envelope approximately **0.219999**: a **false certificate**. Using the actual hard speed 6/s produces `UNRESOLVED` with lower envelope approximately **0.179999**. An independent analytic two-cone oracle checked the lower-envelope values and exposure means.

This falsifies the **measurement-input contract**, not E002-371's conditional mathematical bound. The witness is synthetic and does not establish how frequently human speed bounds fail.

## Enforced product restriction

The human-annotation bridge `e002_399_annotation_bridge.py` now requires `velocity_bound_calibration` in addition to the previous Boolean. It accepts the structured claim `bound_kind: deterministic_physical_upper` only when a numeric `upper_per_s` exactly matches the speed supplied to the theorem and the record includes an auditable provenance and validity domain. Missing records, sample maxima, empirical quantiles, marginal conformal bounds, unknown evidence types, mismatched numbers or missing domain **abstain**. All previous synthetic positive controls were updated to explicitly declare their **known simulator hard bounds**.

**The schema does not authenticate provenance or prove a bound is physically correct.** A deployer could lie. Independent physical calibration and external review remain necessary before any real-world certificate. Do not silently convert a population-level probabilistic tolerance statement into a deterministic per-gap guarantee.

## Independent verification

- E002-405 source: `research/observability/e002_405_velocity_rank.py`
- Independent enumeration, analytical witness and bridge regression: `e002_405_independent_check.py`
- Workflow: `.github/workflows/e002_405_velocity_rank.yml`
- [GitHub Actions 40033725774](https://github.com/sushxnthd/lucent/actions/runs/40033725774): **completed successfully**. Independent rank/witness/bridge verification, earlier E002-399–403 independent regressions and E002-404 rater-pack tests all passed. An anonymized JSON artifact was uploaded; no human frames were published.

## Priority and limitations

The result follows classical nonparametric order statistics and one-sided tolerance bounds, and is conceptually related to conformal rank calibration. Prior art includes the standard exchangeable-rank argument (e.g., Vovk, Gammerman and Shafer 2005; Lei et al. 2018) and nonparametric tolerance intervals. **No novelty is claimed for the rank identity.** The new evidence is a specific, executable wrong-certificate counterexample in Lucent and a source-level enforcement change.

**No new human annotations or independently measured human speed ceiling were obtained.** E002-371's physical shutter-gap boundary remains unvalidated on humans. Keep `ABSTAIN_UNCALIBRATED` for hidden-closure exclusion, blink duration, PERCLOS and fatigue diagnosis. The next decisive experiment remains independent two-rater annotation of the E002-404 human clips, physical-camera shutter/clock calibration and genuinely untouched-participant testing; do not replace it with further proxy AUC or synthetic theorem polishing.
