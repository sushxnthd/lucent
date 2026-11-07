# E002-481 RESULT — width-restricted shutter sensitivity can be detected despite an empty pointwise pulse core

**Date:** 2026-10-27. **Kernel:** E002-371. **Evidence:** synthetic periodic optical model, exact rational analysis, independent endpoint-overlap enumeration and JavaScript replay. No new physical shutter or human measurements. Predictions were [frozen first](E002_481_FROZEN.md) at commit `04948b9356dcecd3a94e0ac862b5de1d04570042`.

## Claim-changing distinction

E002-480 correctly found that a 0.006-ms optical pulse with independently bounded ±0.004-ms start error has **zero pointwise guaranteed illuminated core**. Its 0.0005-ms island counterexample remains valid. But this does **not** rule out robust detection of an island known independently to have a sufficiently large **minimum width and amplitude**. This is a new class-limited instrument-design consequence, not a physiological theorem.

For a rectangular shutter-response island of width L and amplitude A, and a linear detector integrating a rectangular optical pulse of width w with independent timing error ±u, the worst overlap when the nominal pulse is centered on the island is

`q_inf = max(0, min(w, L, (w+L)/2-u))`.

For N equally spaced pulse centers on a period T, an unknown island phase and independently adversarial timing errors give the sharp worst-case overlap

`q_N = max(0, min(w, L, (w+L)/2-u-T/(2N)))`.

Positive detection at threshold theta with bounded additive contrast noise ±epsilon requires **strictly** `A*q_N/w - epsilon > theta`. The worst island phase is midway between nominal centers, with per-pulse timing errors chosen independently. This is elementary interval geometry for isolated, stationary rectangular features, **not a new physical law**.

## Frozen results

At T=1000/240 ms, w=0.006 ms, u=0.004 ms, A=0.20, epsilon=0.002 and theta=0.04:

| Island width | Infinite-grid guaranteed overlap | Interpretation |
|---|---:|---|
| 0.0005 ms | 0 | Undetectable counterexample survives |
| 0.003 ms | 0.0005 ms | Geometric overlap, but robust contrast 0.014667 is below 0.04 |
| 0.006 ms | 0.002 ms | Robust contrast 0.064667 exceeds threshold despite zero pointwise core |

The infinite-density width threshold is **L > 0.00452 ms**, with equality rejected. For L=0.006 ms:

| Probes per period | Guaranteed overlap | Worst contrast | Decision |
|---|---:|---:|---|
| 668 | 0 | -0.002 | NOT DETECTABLE |
| 2815 | 0.0012599171 ms | 0.0399972370 | NOT DETECTABLE |
| 2816 | 0.0012601799 ms | 0.0400059975 | CONDITIONALLY DETECTABLE |

The 2816 threshold means separately acquired phase probes over multiple frames, not 2816 simultaneous pulses. The tiny contrast margin is **not** a practical physical design recommendation.

## Reproduction

[Exact-rational Python model](e002_481_width_class.py), [14 adversarial regression tests](test_e002_481_width_class.py), [independent JavaScript replay](e002_481_independent_replay.cjs) and [deterministic aggregate](E002_481_AGGREGATE.json) are committed. **All 14 Python tests and independent JS arithmetic passed locally** before commit. The independent endpoint-overlap adversary enumerated timing-error extremes at N=17, 71, 668, 2815 and 2816 and matched the analytic expression exactly. Hosted CI is **not yet verified**. The E002-480 hosted run was still queued at last check.

## Physical limitation and product decision

A real camera has not been shown to satisfy the assumed shutter shape, response amplitude floor, minimum feature width, optical linearity, independently measured timing, noise bounds or stationarity. Sensor tails, geometry, gain/brightness, missingness, blur, gaze, glasses, rolling rows and clock correlation can invalidate the model. Without an independently authenticated positive minimum feature amplitude and width, finite nondetection cannot establish exact-zero shutter sensitivity. An optical sensitivity-class result cannot certify anatomical nonclosure.

**Permitted research direction:** a calibrated *minimum detectable optical sensitivity class* with explicit excluded/unsupported classes and abstention, subject to held-out physical verification. **Not permitted:** promoting synthetic detection to shutter-gap guarantees, hidden-closure absence, blink duration, PERCLOS, fatigue or medical claims. Physical shutter acquisitions **0**; new anatomical human sequences **0**; E002-371 physical validation `NOT_ESTABLISHED`; all physical product claims `ABSTAIN_UNCALIBRATED`.

Next experiment: independently timed photodiode/logic-analyzer phase scans, held-out phase/brightness/row challenges, moving-aperture ground truth and blinded participant-disjoint human reference. Further synthetic refinement must not displace acquisition.
