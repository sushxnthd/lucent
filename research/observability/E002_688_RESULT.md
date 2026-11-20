# E002-688 — Interval-aware physical replay product falsification

**Evidence:** conditional product enforcement and local synthetic tests; no human or physical validation.

The existing E002-685 replay used point-estimated endpoint apertures. E002-687 proved that this can produce a false exclusion when endpoint calibration is uncertain. This run adds a separate replay executable taking `left_low,left_high,right_low,right_high` rather than silently assuming exact endpoints. It computes the feasible endpoint minima a*=max(left_low,right_low-vh), b*=max(right_low,left_low-vh), and worst-case lower envelope max(0,(a*+b*-vh)/2). It abstains on inconsistent or invalid intervals and at equality. `math.nextafter` adds a conservative floating-point margin; this is not a formally verified rounding proof.

Local reproduction: `python research/observability/e002_688_robust_replay.py` (eight synthetic assertions passed on the closely corresponding local implementation). The exact committed version has not yet been independently executed. CSV mode accepts the original reference fields plus interval endpoints. A string `authenticated=external_verified` is **not cryptographic or independent authentication**: upstream provenance remains unverified and must be checked out-of-band. The executable must never be connected to live product certification on the strength of this string.

**Counterexample:** a=b=1, v=h=1, c=0.25 excludes closure under exact endpoints; replacing each endpoint by [0.5,1] forces abstention. The executable preserves this reversal.

**Limitations:** Physical anatomical endpoint calibration, independently justified velocity ceiling, synchronized exposure/clock measurement, held-out human reference labels, nuisance testing, and external replay are absent. This is a necessary safety correction, not a new theorem or empirical result. Product remains `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. Next: run frozen E002-671 acquisition with real instrument reference, not another theorem.
