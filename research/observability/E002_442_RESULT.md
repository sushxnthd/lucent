# E002-442 — preregistered real-human synchronization-table falsification (2026-10-25)

**Hosted execution:** [successful workflow 40200230005](https://github.com/sushxnthd/lucent/actions/runs/40200230005) with [machine-readable aggregate](https://github.com/sushxnthd/lucent/actions/runs/40200230005/artifacts/12601363247). Nine adversarial fixture tests passed. S19 archive's published MD5 was reverified. No raw frames or absolute participant timestamps were uploaded.

## Frozen test and result
The E002-442 protocol was committed before inspecting any S19 CSV data rows. It asked whether any one of five named time columns directly provided a **complete, one-row-per-video-frame, 500-Hz clock** with valid monotonicity, 2-ms spacing and correct overall span.

**Result: no column passed.** The sync CSV has **479,560 rows**, whereas the decoded AVI declares **56,911 frames**. Its `Time` column is a complete strictly increasing **1-ms sample grid** (479,559 positive adjacent steps, median approximately 0.001 seconds; total span 479.559 seconds). `RelTime` is numeric in **exactly 56,911 rows**, with 422,649 other rows nonnumeric/blank; `PhanTime` and `LocalTimeStamp` are nonnumeric in all rows; `RecordingTimestamp` has 40 numeric entries. No simple row-to-frame mapping or physically authenticated shutter clock follows from these facts.

**Important newly observed structure:** the number of numeric `RelTime` entries equals the AVI frame count *exactly*. This is a strong reason to test whether those entries mark per-frame acquisition events, rather than discarding the source or assigning its AVI's 1-fps container clock. The equality alone is not proof of alignment or frame-time provenance.

## Next decisive test
E002-443 should preregister a **sparse-event mapping**: extract only `Time` values on rows with populated `RelTime`, calculate frame-event gap distributions, 500-fps within-burst compatibility, monotonicity, event span and recording gaps. Preserve S21/S22 as unseen participants. If the event rows fail timing checks, reject the inferred frame clock; if they pass, it remains a conditional *synchronization-table* proxy requiring independent camera shutter calibration.

**Evidence tier:** published real human video and real sync-table statistics; **not** physical eyelid-velocity calibration or E002-371 human closure validation. Product stays `ABSTAIN_UNCALIBRATED`; no deployment authorized.
