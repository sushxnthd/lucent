# E002-544 FROZEN | Session-wise multiplicity falsification of the optical-edge gate

Date: 2026-10-30. Primary E002-371 observability kernel. Freeze before implementation and synthetic outcomes. Same branch `research/observability-human-boundary` and draft PR #26. Evidence tier: synthetic and mathematical instrument-design validation; **zero physical or human measurements**.

## New measurement question

E002-543 flags each independently timed, strictly outside-shutter flash whose paired ROI difference exceeds a per-trial noise upper. Even if each such test has a nominal 5% null false-alarm rate, scanning many flash positions/rows/frames without multiplicity control can make the probability of at least one false *session-level* candidate approach one. The previous E002-543 rule is a **candidate generator**, not a session-level error-controlled decision. This experiment quantifies the failure and implements a separate conservative session-level gate.

## Frozen synthetic experiment

- Use an exactly reproducible Python stdlib PRNG with seed 5442026, 200 independent eligible flash positions per session, 39 independently sampled null calibration sessions, and one independent held-out test session per replication.
- Under an iid Gaussian null, use absolute unit-Gaussian paired residuals. An uncorrected per-trial two-sided 5% threshold is 1.959963984540054; compare the probability of any crossing among 200 positions with the session-max rank test.
- The session-max test statistic is `max(abs(residual))`. With m null session maxima, use the conservative finite-sample rank p-value `(1 + count(null_max >= test_max))/(m+1)`, with ties counted against rejection. Declare a session-level `FALSIFICATION_CANDIDATE_FWER` only if p <= 0.05. The rank test has marginal false-positive probability at most 0.05 under exchangeability of the *entire session maximum*, even with within-session dependence, when the test session and m calibration sessions are exchangeable. It does **not** guarantee conditional validity for a specific participant, camera, or shifted stratum.
- Run 2,000 replications for the iid null and a nuisance-shift attack where only held-out residuals are multiplied by 1.25. Record counts and empirical rates without retuning. Also test tied/discrete maxima, varying window counts, missing frames, nonfinite values, stratum mismatch, and calibration/test identity reuse. Do not silently remove any trial from a session.
- Include an exact analytic independent-null calculation `1-(1-0.05)^200` for the naive any-hit probability. No synthetic effect detection is a physical discovery.

## Owner-private session intake contract

The optional CLI accepts one local JSON object with exact keys `schema`, `prelabel_commitment`, `alpha`, `nuisance_stratum`, `calibration_sessions`, `test_session`. Schema `E002-544-v1`, digest lowercase SHA256 format, `alpha` fixed exactly 0.05. Every session has exactly `session_id`, `partition`, `nuisance_stratum`, `paired_differences`, `eligible_outside_verified`, `quality_verified`. Calibration partition `calibration_null`, test partition `heldout_outside`; flags must be literal true, signed finite paired differences in [-1,1], identical nonzero trial counts, unique IDs and matching nonempty stratum. Require at least 19 independently collected null calibration sessions. Any violation produces `ABSTAIN_INVALID_EVIDENCE`, not a filtered denominator. The CLI cannot independently authenticate the flags, the prelabel publication, source independence, or the E002-543 timing gate; these must be externally verified against private raw records.

Output is aggregate-only: calibration session count, windows per session, conservative p-value, decision, evidence tier, product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Never emit raw differences, private IDs, or physical certification. A candidate is conditional on null-session exchangeability and independent optical timing/quality audit, and remains an *unverified candidate*, not proof of shutter error. If physical evidence is absent, retain zero physical captures and no physiological claims.

## Falsification/stop criteria

If the naive any-hit rule is not strongly inflated under the frozen iid null, inspect the simulation and reject the proposed motivation. If the rank test exceeds its 5% target under exchangeable synthetic sessions beyond plausible Monte Carlo error, inspect and reject the implementation. Under shifted held-out sessions, **expect** elevated false positives; retain the failure and prohibit unconditional calibration claims. Do not use the synthetic calibration to change the existing E002-543 threshold or declare physical readiness.

Next real step: authenticated photodiode-timed acquisition with *whole-session* null controls and randomized held-out outside-edge challenges, plus E002-502 independent anatomical review. This protocol does not replace the physical/human completion gates.
