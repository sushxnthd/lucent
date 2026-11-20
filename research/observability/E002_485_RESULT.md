# E002-485 RESULT — actionable 150-fps human-data validation handoff

**Date:** 2026-10-27. **Kernel:** E002-371. **Evidence tier:** published human-dataset source verified at literature/host level; actual human video **not downloaded**; executable held-out evaluator and synthetic adversarial fixture tested locally. **Not:** an empirical human result, a measured shutter kernel, or a universal physiological velocity bound.

## New acquisition route

Guttmann-Flury, Sheng and Zhu, *Scientific Data* 12:587, published 2025-04-08, DOI https://doi.org/10.1038/s41597-025-04861-9, report 31 participants/63 sessions with Phantom Miro M310 eye video, Tobii tracking and synchronized electrophysiology. The primary paper specifies the video **was set to 150 fps** with approximately 6.6-ms trigger intervals, even though the March 2026 [Zenodo re-host](https://zenodo.org/records/18970793) describes `*_phantom.avi` as "~500 fps." Treat the latter as **unverified metadata**, not the actual acquisition rate. The 150-fps source is adequate for a narrower 150-to-30-fps *frame-sample* falsification study; it is not a 500-fps anatomical reference.

The re-host supplies 31 per-subject ZIPs, video `*_phantom.avi`, Phantom XML and synchronization CSVs, including S24.zip (345.6 MB; published MD5 3e8eb615d4a3415115f61dad5265ef12). This provides a reproducible route to actual held-out human data **without relying on the restricted FaceBase dataset**. The original paper reports synchronization failures for P3004L101 and ME181, plus missing initial trial footage in several tasks; reject those portions rather than silently interpolate.

**Acquisition outcome this run:** The web retrieval attempt of S24.zip was refused because the file was 345,600,876 bytes; the execution container could not resolve the Zenodo host. Thus zero human video frames or annotated trajectories were obtained, and no raw human dataset was processed. The script does not pretend otherwise.

## What is now executable

[Pre-human-data frozen protocol](E002_485_HUMAN_PROTOCOL.md) specifies S01–S20 calibration and S21–S31 held-out subjects, an operational 0.10-open-aperture threshold, high-rate annotation uncertainty, nuisance exclusions, frame-timestamp checks and an explicit falsification criterion. [Evaluator](e002_485_heldout_gap.py) accepts an independently annotated CSV, refuses incomplete real 20/11 subject coverage, and produces a machine-readable report. It does not claim the frame samples simulate an actual camera exposure.

The dimensionless conditional test is

`Z = ((l0-c)+(l1-c)) / (V_proxy*(Delta+2*clock_error))`,

for lower endpoint aperture bounds l0,l1>c. A hard-Lipschitz assumption would exclude a threshold crossing when Z>1. But V_proxy is only the **maximum observed calibrated 150-fps secant**, not a hard bound on instantaneous human motion. An independently observed high-rate threshold crossing inside a Z>1 window therefore **falsifies the joint assumptions**. Absence of a high-rate closure sample is not proof of nonclosure.

## Local synthetic adversarial run (not human evidence)

The deterministic fixture deliberately includes a held-out faster closing trajectory, a nonclosing control, a blur failure and a missing-frame failure. Eleven Python adversarial tests passed locally. Exact fixture output:

| Measure | Synthetic result |
|---|---:|
| Calibration / held-out fixture participants | 1 / 4 |
| Eligible five-interval windows | 2 |
| Conditional exclusions under proxy cap | 2 |
| Observed high-rate closures | 1 |
| **Contradictions of proxy-cap exclusion** | **1** |
| Held-out adjacent secant proxy exceedances | 5 / 14 |
| Nuisance or missing-frame abstentions | 2 |
| Physically validated shutter acquisitions | 0 |
| New real human reference sequences | 0 |

The planted contradiction has Z=3.8236246, illustrating that the evaluator reports a failed assumption instead of silently certifying nonclosure. The synthetic fixture does **not** estimate any real-world error rate.

[Deterministic aggregate](E002_485_AGGREGATE.json) · [Ten adversarial tests](test_e002_485_heldout_gap.py) · [Dedicated CI workflow](../../.github/workflows/e002_485_heldout_gap.yml). Hosted CI success is **not yet established**.

## Decision and next acquisition

This is a meaningful **human-data acquisition breakthrough in accessibility**, not yet a measurement-science validation. The most consequential new correction is that the original acquisition is **150 fps, not the "~500 fps" claimed by the secondary re-host description**. The study must use measured frame timestamps, not nominal 500-fps interpolation. A 150-fps reference can falsify claimed exclusions when it actually observes a closure; it cannot certify that no sub-frame closure occurred.

**Next decisive step:** download and verify one ZIP in an environment with outbound network, inspect the actual AVI/Phantom XML timing and annotate high-rate eyelid trajectories. Then run the frozen subject-disjoint study, acquire independent exposure/clock calibration and a moving-aperture instrument witness before any physical product claims. The current result does not justify hidden-closure, blink-duration, PERCLOS, fatigue or medical measurements.

**Product release:** `ABSTAIN_UNCALIBRATED` / `BLOCKED`. Hush PR #45 and all other branches remain untouched.
