# E002-721 — Unaccounted clock gap creates false exclusion certificates

**Tier:** executed deterministic synthetic instrument-timing challenge; no physical or human observations. 2026-11-08 UTC.

## Test and falsification
For positive rational endpoint apertures a0,a1, nominal time gap d, and actual continuous-time speed ceiling V, introduce an unaccounted nonnegative time gap j (representing clock offset, exposure-time misassignment or dropped time). A hidden complete closure/reopening is constructively possible exactly when V(d+j) >= a0+a1. Compare a nominal certificate Vd < a0+a1 with the conservative certificate V(d+j) < a0+a1. This is a deliberately bounded interval experiment, **not** a statistical model of real camera jitter.

Run `python research/observability/e002_721_clock_interval.py` using only the standard library. It enumerates a0,a1,d,V in {1/4,...,2} and j in {0,1/8,1/4,1/2}, yielding 16,384 cases.

## Executed local results
- Conservative exclusions: **11,684**; constructive false exclusions: **0**.
- Conservative abstentions: **4,700**.
- Nominal-gap certificates contradicted by possible closure witnesses: **988**.
- Example: a0=a1=1/4, d=1/4, V=3/4, unaccounted j=1/2. Nominal Vd=3/16 < 1/2, falsely excluding closure; actual V(d+j)=9/16 >= 1/2, allowing a triangular closure trajectory.

Counts are synthetic grid frequencies, not estimated real-world error rates. This experiment is algebraically related to E002-715 and does not constitute independent empirical validation.

## Acquisition and enforcement consequence
The input must be an independently calibrated **upper bound on elapsed time between the actual aperture observation instants**, not nominal FPS, presentation timestamps or frame midpoint assumptions. For exposure-integrated frames without validated instantaneous-aperture recovery, no endpoint certificate is allowed. Missing or inconsistent exposure-start/end, sensor clock uncertainty, rolling-shutter row timing or dropped-frame accounting must cause `ABSTAIN_UNCALIBRATED`. Do not infer a finite timing uncertainty envelope from unverified metadata.

**Next decisive work:** acquire the E002-714 physical shutter/photodiode session with independently logged exposure intervals, clock offsets and randomized phase, then blinded replay. No more synthetic sweeps in lieu of acquisition. Production remains BLOCKED.
