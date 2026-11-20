# E002-702 — Independent pathwise randomized joint-uncertainty falsification

**Evidence tier:** deterministic-seed synthetic computational test, executed locally 2026-11-07 UTC. No human data or physical camera measurements.

## Construction

This test independently constructs continuous piecewise-linear anatomical aperture trajectories with two endpoints and a midpoint. Slopes of each half-gap are explicitly checked against a sampled true velocity ceiling. Apertures are in [0,1], true velocity ceilings in [0.3,1.0], gaps in [0.4,0.7], endpoint observation errors in [-0.1,0.1], and closure threshold 0.5. The midpoint is sampled separately and can represent a hidden closure. Random seed 702, 100,000 attempts. Invalid slope trajectories are rejected. The naive exclusion uses observed endpoints, v=0.5, gap=0.5; robust exclusion uses each observed endpoint minus 0.1, v=1.0, gap=0.7. No assertion of a statistically representative population is made.

## Executed result

Across 100,000 attempted constructions, the naive rule issued **21,545** certificates, including **288 false exclusions** against an explicit feasible hidden midpoint. The robust rule issued **4,133** certificates with **zero false exclusions** in this constructed sample. The sample is nonuniform in feasible trajectory space; counts are not clinical risk rates. One explicit false-exclusion witness: a=0.6026275847, b=0.6244955468, midpoint=0.4003264115, v=0.9469160326, gap=0.6685474827, measured endpoints 0.6400483349 and 0.6941200909. Both half-gap slopes satisfy the stipulated bound.

This is an **independent pathwise implementation** of the E002-701 stress claim, not independent external replication, and does not improve on its deterministic proof. It tests explicit trajectories rather than inferring an attainable minimum from endpoint geometry. The zero robust failures are conditional on the stipulated error, clock and velocity envelopes, which are not validated for phones or human eyelids.

## Consequence and next step

Retain `ABSTAIN_UNCALIBRATED` and production `BLOCKED`. Do not present synthetic zero failures as a safety guarantee. Stop repeated synthetic sweeps; the next decisive scientific evidence must be synchronized physical acquisition (E002-690) with externally measured shutter/exposure times, an independently bounded occluder speed, pre-frozen E002-695 low-rate predictions and high-rate reference labels, then participant-disjoint human validation. Run: `python3 research/observability/e002_702_pathwise_stress.py`.
