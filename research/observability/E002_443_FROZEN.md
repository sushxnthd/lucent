# E002-443 — frozen S19 sparse-event frame-clock test (2026-10-25)

Parent E002-371 / E002-441 / E002-442. Frozen **before reading any S19 row-level event positions or values**. Known aggregates: 479,560 1-ms synchronization rows, 56,911 numeric `RelTime` entries, 56,911 declared AVI frames, and unusable AVI 1-fps stream clock.

## Primary prospective test
Treat rows with numeric `RelTime` as *candidate* frame events, without asserting that they are camera-exposure triggers. Extract their corresponding `Time` values, using the independently observed seconds unit (1-ms grid). Report event count, strictly increasing fraction, quantiles of inter-event spacing, proportion with 1–3 ms gaps, 500-fps within-burst compatibility, gaps over 10 ms and 100 ms, total event span, and maximal contiguous <=10-ms burst length.

**Pass for a *candidate table-based frame-event clock*** only if: event count equals 56,911; every event time is finite and strictly increasing; at least 90% of event-to-event intervals are between 1 and 3 ms; median inter-event gap between 1.5 and 2.5 ms; at least one >=100-frame contiguous burst with every gap <=10 ms. Do not require total event span to equal 113.82 s, since recording may be intermittent. A passing result is NOT authenticated exposure time or anatomical closure evidence.

## Adversarial controls and stop rule
Synthetic fixtures must reject reordered events, missing event times, 1-fps surrogate intervals, count mismatches and nonmonotone clock. Record negative results without refitting thresholds. Do not inspect or tune S21/S22. No frame images, absolute timestamps, or participant identifiers beyond S19 leave the runner. No assumption that `Blinks` implies physical eyelid closure.

## Product consequence
If event-clock candidate passes, the next stage may test **algorithmic human blink-event observability** after explicitly documented row/frame alignment and blinded anatomical labels; it cannot certify hidden physical closures. If it fails, reject timing-dependent physical claims and seek source hardware acquisition logs or prospective instrumented video. In all cases retain `ABSTAIN_UNCALIBRATED` for hidden closure, blink duration, PERCLOS and fatigue.
