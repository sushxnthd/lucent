# E002-617 | Frozen one-frame annotation-boundary adversarial test

Frozen 2026-11-03 before evaluating any E002-617 source-derived endpoints. Parent scientific kernel E002-371. Preserve existing `research/observability-human-boundary` branch and draft PR #26. This is an adversarial sensitivity test of E002-616 published-human categorical virtual point-sampling evidence, **not** a new anatomical rating, calibrated physical camera experiment, or velocity-bound validation.

## Question and exact falsifier

E002-616 found 105 omitted event-phase pairs among 279 bilateral full-closure runs, under each of two nominal 30-Hz point selectors. Does that observation remain an event-level **omission witness** if investigator FC labels may be off by one native frame at each run boundary? The 1-frame perturbation is a hypothetical adversarial uncertainty budget, **not** an empirically estimated annotation error.

Reuse the pinned Silesian5 archive SHA-256 `a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223`, the E002-616 bilateral event definition and eligibility, and the E002-615 source timestamp-nearest and E002-582 floor-index selectors without tuning. No source member names, individual frame IDs, image pixels, identities, or per-event results in committed artifacts.

For each eligible baseline bilateral run [a,b] with independently valid immediate flanks, evaluate exactly ten phases for both selectors, with three *fixed* intervals:
- baseline [a,b];
- maximal outward uncertainty [a-1,b+1] (hypothetically reclassify both flanking frames positive);
- inward uncertainty [a+1,b-1], defined only for baseline length >=3 (shorter runs are **erased**, not counted as misses).

Report, separately per selector and aggregated over five sequences: baseline omission event-phase pairs; outward-robust omission pairs (no selected frame in [a-1,b+1]); outward-robust *distinct events* (at least one phase); baseline omission pairs belonging to inward-surviving events (length>=3); and **two-sided stable omission pairs** (length>=3 AND omission after outward expansion). Report erased events of lengths 1 or 2 and paired selector disagreement on the two-sided endpoint. Also report per-sequence aggregate counts and event-length histogram, with strict invariants outward-robust subset baseline and two-sided subset outward-robust.

A positive **two-sided stable omission witness** requires both event survival under maximal one-frame inward trimming and omission under maximal outward extension for the *same baseline event and phase*. If zero, kill the claim that E002-616's positive virtual omission evidence is robust to this particular ±1-frame adversarial annotation model. If positive, report exact number, without claiming any empirical annotation uncertainty or physical shutter behavior.

## Predeclared predictions and independent checks

For an interior contiguous run under floor-index selection, outward dilation changes its effective length from L to L+2. The E002-616 exact phase law therefore predicts **4** outward-robust event-phase pairs from the four length-1 runs, and **0** two-sided stable pairs because surviving events have L>=3. Treat any mismatch as falsification of the selector implementation or its premises, preserve it, and do not repair thresholds post hoc. For source timestamp-nearest selection, no exact numerical result is assumed; record the outcome and any surprising long-run omissions.

Include synthetic fixtures for a single-frame run, a three-frame run, nonconsecutive flanks, nuisance exclusion, and timestamp jitter; a separate independent cross-language aggregate verifier must reject deliberately corrupted aggregate counts. No population confidence intervals, no independence assumption across phases.

## Product and stop conditions

A one-frame categorical label perturbation cannot establish how often human annotators err. This sensitivity result may invalidate an *annotation-robust* virtual omission claim, but cannot invalidate the literal E002-616 published-source observation. Neither result validates E002-371 continuous-time shutter/velocity exclusion, fatigue, or sleepiness. Maintain `ABSTAIN_UNCALIBRATED` and production `BLOCKED`. Next decisive step remains independently calibrated paired high-speed/ordinary camera exposure with blinded anatomical review and participant-disjoint predictions. No changes to Hush branch or PR #45.
