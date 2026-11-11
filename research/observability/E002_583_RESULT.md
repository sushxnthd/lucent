# E002-583 | Authentic human binocular full-closure index alias, independent cross-language replay

**Executed:** 2026-11-01. **Kernel:** E002-371. **Frozen protocol before source analysis:** [E002_583_FROZEN.md](E002_583_FROZEN.md), commit `bb90f229`. **Verified hosted source run:** [Actions #41282668183](https://github.com/sushxnthd/lucent/actions/runs/41282668183), job `124777591726`, completed **success** at 06:55 UTC. **Source:** investigator Silesian5 (Basler5) annotations, nominal 100 fps, SHA-256 `a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223`, five sequences, 58,884 annotated native frames. No original video or raw annotation rows committed.

## New question: do per-eye omission counts overstate distinct blink events?

E002-582 found 76/567 per-eye investigator full-closure runs omitted under at least one nominal 100-to-30-fps index-sampling phase. But left/right eye runs are correlated within a person. E002-583 froze **simultaneous binocular full-closure** (`LE_FC=C AND RE_FC=C` on a native frame) as the primary endpoint, with a distinct **either-eye full-closure union** (`OR`) endpoint. A maximal contiguous run of either type was independently analyzed for all ten frozen phase schedules. The published C flag means an investigator annotated an eye as 90–100% closed; it is not a calibrated aperture threshold.

| Frozen event definition | Eligible runs | Omitted in at least one of ten phases | Event-phase omissions | Native run lengths 1 / 2 / 3 / 4+ |
|---|---:|---:|---:|---|
| Both eyes simultaneously C | **279** | **39 (13.98%)** | **105** | 4 / 14 / 21 / 240 |
| Either eye C | **288** | **37 (12.85%)** | **97** | 3 / 14 / 20 / 251 |
| E002-582 per-eye runs (prior result) | 567 | 76 (13.40%) | 202 | 7 / 28 / 41 / 491 |

All 279 simultaneous-binocular and 288 either-eye eligible runs passed the **predeclared exact 7/4/1/0 omitted-phase law** for run lengths 1/2/3/4+. Zero candidates required source-flag nuisance, missing-index, or boundary abstention under the frozen criteria. The two definitions **must not be combined into 567 independent blink events**; 279 and 288 are different derived event counts, and neither is identical to the investigators' 300 blink-interval count.

For the simultaneous-binocular endpoint, omitted counts by phase 0–9 were **[16,9,10,10,12,8,12,12,7,9]** (sum 105). For the either-eye endpoint they were **[13,9,11,7,8,10,13,8,7,11]** (sum 97). No event was omitted in all ten phases. These are within-source deterministic phase comparisons, not estimated population or physical-camera miss probabilities.

## Reproducibility and adversarial controls

The [Python executable](e002_583_binocular_alias.py) passed nine local synthetic fixtures and hosted checks, including overlapping but asynchronous left/right FC runs, disjoint monocular events, long events, one-frame events, nonfrontal nuisance, missing source indices, boundary exclusion, sequence-order invariance and duplicate rejection. The [independent Node.js replay](e002_583_independent_replay.cjs) used a separate ZIP/TAG parser and modular residue test, **not** Python's retained-index enumeration. Both independently reported exactly 279/39/105 simultaneous-binocular and 288/37/97 either-eye events/omissions, matching all 10 phase counts and both run-length histograms. [Machine-readable aggregates](E002_583_AGGREGATE.json) contain anonymized sequence-level counts, no human frames or source rows.

## Scientific consequence and exact limitation

This is a **positive human-investigator-label temporal-alias result for simultaneous binocular closure**, not merely duplicated monocular labels. It sharpens the meaning of E002-582's positive endpoint: even when both eyes are marked 90–100% closed on the same source frame, some positive runs can disappear entirely under nominal ordinary-rate **index-only** subsampling. It does **not** show that a physical 30-fps camera with nonzero shutter integration would miss them. It does not certify reference sensitivity, human eyelid-velocity bounds, shutter or rolling-row timing, clock error, or the E002-371 physical observability boundary. Five participants are insufficient for a general population-rate estimate, and the ten phases are not independent trials.

Source NF and NV flags were checked but cannot independently bound brightness, glasses, gaze, blur, geometry, frame timestamp errors or human label disagreement. No second blinded anatomical rater pair exists. **No exposure-integrating camera experiment or prospective held-out physical closure prediction has been performed.**

**Product consequence:** Lucent may describe *investigator-label index-sampling aliasing* as a research result. It must not report physiological blink/PERCLOS/fatigue measurements, physical camera miss rates or shutter-gap exclusion claims from these annotations. Continue `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.

**Next decisive test:** E002-567 synchronized high-speed/reference and ordinary-camera acquisition, externally measured exposure/row/clock timing, independent blinded anatomical raters, independently justified eyelid-speed ceilings, and prospectively frozen unseen-condition physical predictions. Do not spend the next run polishing annotation-derived laws instead of obtaining physical/human evidence. Hush branch and PR #45 unchanged.
