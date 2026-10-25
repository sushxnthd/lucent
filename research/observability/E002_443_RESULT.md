# E002-443 — prospective human sparse frame-event timing falsification (2026-10-25)

**Experiment:** [successful hosted run 40200503432](https://github.com/sushxnthd/lucent/actions/runs/40200503432), [machine-readable aggregate](https://github.com/sushxnthd/lucent/actions/runs/40200503432/artifacts/12601458832). Seven adversarial synthetic fixture tests passed; real S19 archive MD5 was verified. The event timing criteria were frozen before inspecting row-level event positions.

## Measured result
The S19 synchronization table contains **479,560** 1-ms grid rows. Exactly **56,911** have numeric `RelTime` entries, matching the AVI's declared frame count. Using the independently observed `Time` grid at these candidate event rows:

| Preregistered statistic | Observed |
| --- | ---: |
| Candidate events | 56,911 |
| Event timestamps nonmonotone | 0 |
| Median positive inter-event gap | **7.000 ms** |
| 1st percentile gap | **6.000 ms** |
| 99th percentile gap | **8.000 ms** |
| Fraction with 1–3 ms gaps | **0%** |
| Gaps >10 ms | 170 |
| Gaps >100 ms | 40 |
| Longest contiguous <=10-ms burst | 2,922 frames |
| Event timestamp span | 409.941 s |
| Preregistered ~500-Hz event-clock test | **FAIL** |

**Interpretation:** If numeric `RelTime` rows are indeed one-to-one frame events, their 7-ms median spacing corresponds to an *approximate event cadence* of 143 Hz, not the advertised ~500 fps. The row/frame count equality supports but does **not** independently prove that mapping; synchronization-table rows may represent software processing or export rather than sensor exposures. Therefore **neither the AVI's reported 1 fps nor an assumed 500 fps nor the 143-Hz candidate can be used as authenticated shutter timing**. This is a substantive negative result, not a claim that the published dataset or its acquisition hardware is fraudulent.

## Scientific decision and product gate
Do not repurpose S19 as 500-fps physical ground truth for E002-371. Do not retune the frozen 500-Hz criterion to pass the observed 7-ms cadence. Obtain original hardware exposure logs / camera documentation or independently calibrated prospective high-rate recordings; S21/S22 remain untouched and held out.

The existing dual-rater and nuisance protocols remain necessary before any physical eyelid velocity, no-hidden-closure, blink duration, PERCLOS or fatigue claim. No human anatomical eyelid-aperture traces, verified shutter timing or physiological velocity upper bounds were established here. Keep `ABSTAIN_UNCALIBRATED` and draft/unmerged status.
