# E002-617 | Verified human-source boundary-uncertainty falsification

**Status: hosted experiment PASSED on 2026-11-02 UTC; recorded 2026-11-03 IST.** Frozen protocol at [cb9b150](https://github.com/sushxnthd/lucent/commit/cb9b1504ed541955177e446dac3fb1718a7be087), before source-derived evaluation. [Hosted run #41548054575](https://github.com/sushxnthd/lucent/actions/runs/41548054575) completed successfully on source-analysis commit `751196abee3a54de74922e19c9c053af86537d98`. [Aggregate-only workflow artifact](https://github.com/sushxnthd/lucent/actions/runs/41548054575/artifacts/13189547455) and [committed aggregate](./E002_617_AGGREGATE.json) preserve the source-derived outputs; no human images or per-event records are committed.

## Frozen prediction and observed result

The source was the SHA-256-pinned Silesian5 five-sequence published human categorical full-closure annotations and timestamps. All 279 eligible bilateral full-closure runs and ten virtual sampling phases were retained. The perturbation is a **hypothetical** ±1 native-frame label-boundary uncertainty budget, not an estimate of actual human annotation error.

| Prespecified endpoint | Floor-index selector | Source-timestamp selector |
|---|---:|---:|
| Baseline omitted event-phase pairs | 105 | 105 |
| Still omitted after maximal one-frame outward extension on both sides | **4** | **4** |
| Distinct events with an outward-robust omitted phase | 4 | 4 |
| Baseline omitted pairs belonging to events surviving one-frame inward trim | 21 | 21 |
| Two-sided stable omission event-phase pairs (inward survival AND outward omission) | **0** | **0** |
| Two-sided stable distinct events | 0 | 0 |

**18/279 events** of length one or two native frames disappear under maximal inward trim. Of the original 105 omitted event-phase pairs, **101 (96.19%)** cease to be omitted under maximal outward extension. The frozen index prediction (4 outward-robust, 0 two-sided stable) was reproduced exactly, and the previously unmeasured source-timestamp endpoint independently returned the same aggregate counts. The outward-robust *phase positions* differ between selectors (index `[0,2,0,1,1,0,0,0,0,0]`, timestamp `[0,0,0,0,1,0,1,0,2,0]`); identical totals are not event-phase equivalence.

**Falsification decision:** Under the predeclared ±1-frame adversarial categorical-label model, reject any assertion that E002-616's positive virtual omission evidence has a two-sided annotation-stable witness. Do **not** reject the literal published-label omission result (105/2790 event-phase pairs per selector), and do not infer measured human rater error.

## Independent checks and limitations

Hosted Python six-group synthetic/nuisance fixtures passed; independent Node exact phase oracle passed 60 cases. Node aggregate audit passed, including **four deliberate corruptions rejected**. The pinned source archive SHA-256 was `a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223`. The archived aggregate is an aggregate-only reproducibility artifact; the primary data are external and access may vary.

This is **real published human-label evidence for virtual point-sampling sensitivity**, not a calibrated shutter experiment. No paired physical camera exposures, blinded anatomical rater pairs, independently certified eyelid velocity ceiling, participant-disjoint physical predictions, or physiological calibration were obtained. E002-371's physical shutter-gap/velocity observability boundary remains **empirically unvalidated**.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. Next decisive evidence: blinded independent anatomical review with verified image provenance, physical optical shutter/clock measurement and participant-disjoint predeclared predictions. Stop further synthetic label-boundary polishing absent new independent measurements. Hush's separate PR #45 was not modified.

---

## Prespecified rationale (retained from pre-result report)



The previously verified E002-616 source-derived bilateral FC run-length histogram was 4 runs of length 1, 14 of length 2, 21 of length 3, and 240 of length >=4, totaling 279 eligible runs. E002-616 established 105 floor-index virtual omission event-phase pairs under ten phases, by the exact selector law `4*7 + 14*4 + 21*1 = 105`.

If each investigator-labelled bilateral FC run can be extended by **one native frame on both sides** (a *hypothetical* label uncertainty model), an event of length L becomes length L+2. The exact floor-index omission law (7,4,1,0 for lengths 1,2,3,>=4) then predicts:

| Conditional quantity | Predicted index-selector count | Evidence tier |
|---|---:|---|
| Baseline omitted event-phase pairs | 105 | Previously measured source-label aggregate (E002-616) |
| Omitted pairs surviving maximal one-frame outward extension | **4** | New exact counterfactual deduction from E002-616 human histogram |
| Baseline omitted pairs for events surviving one-frame inward trim (L>=3) | **21** | New exact counterfactual deduction |
| Same event both survives inward trim and remains omitted after outward extension | **0** | New exact counterfactual deduction |
| Baseline events erased by inward trim (L<=2) | **18** | New exact counterfactual deduction |

Thus **101/105** baseline index-selector omission pairs are *not invariant* to this maximal outward extension. And **zero** satisfy the stronger two-sided stability criterion under this stipulated annotation model. These are exact conditional calculations, **not measured human annotation errors**, and cannot erase the literal E002-616 observation.


