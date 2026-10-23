# E002-391 supplementary unseen-condition and adaptive-adversary freeze

Frozen before running supplemental code, 2026-10-23. This does **not** alter the original E002-391 frozen protocol, results, or success thresholds. The two tests are separate confirmatory instrument predictions.

**Unseen acquisition condition:** Keep the same triangular aperture `a(t)=min(1,40|t|)`, threshold 0.2, 5-ms exposures and 12 identical repeated events, but change frame rate from 30 to **60 Hz**. Use 12,000 fresh trial sets, seed 39113. Predict single-event phase capture probability `p=2 theta/(V F)=0.6`, fixed-phase 12-event any-detection within 0.02 of 0.6, and independently randomized-phase any-detection >0.99 and within 0.02 of `1-(1-p)^12=0.999983222784`.

**Adversarial phase coupling:** At 30 Hz with each camera phase randomized, allow an event scheduler to observe each phase and choose its triangular event trough at a phase offset `F/2` relative to the camera exposure start. Predict that the camera reports **zero positive mean-threshold detections** across 12,000 12-event trial sets despite a real physical crossing in each event. This is a deliberately adversarial event-time dependency, not an ordinary physiological model. It shows why randomization without event-phase independence is not a deterministic no-hidden-closure guarantee.

Independent checker must calculate phase-capture width from geometry, not reuse the primary exposure integration. Do not modify these thresholds after running. Report failures. Product consequence: phase-sweep detection statistics are allowed only for controlled, independently timed repeatable calibration events; adaptive event timing or unknown phase coupling forces abstention.
