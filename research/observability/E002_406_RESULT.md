# E002-406 RESULT — real-human temporal coverage, 2026-10-24

## Preregistered experiment and provenance

The prospective protocol was frozen at commit `4a44eda` before evaluation. The experiment used checksum-verified Eye-BCI S01 and S19 archives and their source EEG-clock frame synchronization; it did **not** use AVI's invalid nominal 1-fps time base. The evaluation was executed at commit `91b8e4e` in [GitHub Actions run 40042006563](https://github.com/sushxnthd/lucent/actions/runs/40042006563). Both independently hosted participant jobs completed successfully, with aggregate JSON artifacts (S01 artifact 12540050896, SHA-256 d38e2ca525bd2d580bd676a1d0e3af70b2e89ef653666da5c36231d90abd30ab; S19 artifact 12539911807, SHA-256 f79895e2fdb0600c231ca26751a1ceaab2942793a4f0b3eac41f93f55b94a49e). The separate 500-case synthetic timestamp oracle passed in both jobs. Data access and verification occurred after the freeze.

## Frozen hypotheses and measured results

| Measurement | S01 | S19 |
| --- | ---: | ---: |
| Source video frames | 53,680 | 56,911 |
| Deterministically selected event/control centers | 40 | 40 |
| Seven-frame spans under 100 ms | 40/40 | 40/40 |
| Seven-frame span p10 / median / p90 | 38 / 39 / 39 ms | 39 / 39 / 41.1 ms |
| Eligible contiguous ±250-ms windows | **36/40** | **26/40** |
| Rejected for >20-ms internal gap | 4/40 | 14/40 |
| Rejected for missing boundaries / noncontiguous frame IDs | 0 / 0 | 0 / 0 |
| Eligible full-window frame-count p10 / median / p90 | 79 / 79 / 79.5 | 75 / 79 / 79 |
| Eligible full-window span p10 / median / p90 | 500 / 503.5 / 507 ms | 502.5 / 506 / 508 ms |
| Eligible max internal gap p10 / median / p90 | 7 / 7 / 8 ms | 7 / 7 / 8 ms |

**H1 PASSED**: 80/80 seven-frame packets cover less than 100 ms (all medians ~39 ms). The seven-frame packs are **inadequate for whole-event duration or velocity-ceiling validation**. **H2 PASSED**: at least one contiguous ±250-ms candidate window exists for each participant (36 S01 and 26 S19). **H3 PASSED computationally**: the evaluator rejected the 18 candidates with >20-ms gaps; no gap imputation was performed. **H4 PASSED in released artifacts**: aggregate results contain no clip IDs, EEG event times, event/control labels, individual imagery or private mappings.

The 62 eligible windows are **candidate acquisition windows, not 62 annotated blinks**. Their EEG-clock alignment is not an independently calibrated optical exposure clock. The participants have already been studied and cannot be claimed as untouched holdouts.

## Interpretation and next decisive action

The observed acquisition adequacy enables full-event private rater packets of approximately 75–80 high-speed frames per selected center, but it does not establish physical aperture, blink onset/offset, physiological maximum eyelid velocity, or E002-371 closure guarantees. **Do not estimate a deterministic velocity ceiling by taking a sample maximum** (E002-405). The next experiment must freeze a leakage-safe selection and human landmark annotation protocol for the 62 eligible full windows, obtain two blinded raters, adjudicate disagreements, and separately calibrate camera shutter response, per-row timing, geometry and physical velocity evidence. A true untouched-participant/device validation is still required.

No new positive product claim is justified. Continue `ABSTAIN_UNCALIBRATED` for closure exclusion, blink duration, PERCLOS and fatigue diagnosis. This is **real-human temporal acquisition evidence**, not physical-aperture validation.
