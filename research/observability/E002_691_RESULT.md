# E002-691 — synthetic instrument surrogate (2026-11-07 UTC)

**Evidence tier:** deterministic exact-rational synthetic falsification; NOT acquired instrument or human evidence. Reproduce: `python research/observability/e002_691_instrument_surrogate.py` (Python standard library only).

## Frozen construction and outcome
Seed 691, 20,000 generated parameter draws, 18,639 endpoint-feasible piecewise-linear aperture paths. Each path has endpoints a,b and a reachable midpoint at h/2; both linear segments obey the stipulated hard velocity ceiling v. Apertures and timestamps are exact rational values. The reference truth is the minimum of the three path vertices. The ordinary-camera model observes only endpoints and an underestimated nominal blind interval; the robust model uses endpoint lower uncertainty limits and a guaranteed upper blind-gap duration.

Executed locally before repository upload: 18,639 feasible trials; 6,195 reference closures; 1,328 robust exclusion certificates; **0 robust false exclusions**; **76 naive false exclusions**; 3,074 naive exclusions withdrawn under uncertainty. These counts are deterministic for the included seed and implementation, not statistical human performance estimates. No physical device, image sensor, acquisition rate, photodiode, or independent velocity calibration was used. The surrogate assumes the physical ceiling and its exact applicability.

## Falsification consequence
Using nominal frame intervals and exact point estimates can produce unsafe exclusions even for a perfectly speed-bounded physical path. Using a conservative timing upper bound and endpoint lower limits avoids this specific failure in the generated paths. This does not validate the velocity ceiling, timing provenance, endpoint calibration, shutter integration, rolling shutter, or the real-world closure-label pipeline.

## Release disposition
No change: `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. E002-690's synchronized independently measured instrument acquisition and participant-disjoint human protocol remain mandatory. No further theorem-only substitution for physical evidence.
