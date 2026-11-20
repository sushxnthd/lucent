# E002-585 | Executable human-validation handoff and release gate

**Status:** protocol + software instrument only; **zero** independent human rater pairs or physically calibrated camera trials collected by this experiment. The frozen protocol is [E002_585_FROZEN.md](E002_585_FROZEN.md). Execute `python research/observability/e002_585_human_rater_gate.py --self-test` before using local private inputs.

## Private local inputs (never commit them)

The script accepts `--manifest PRIVATE/manifest.json --rater-a PRIVATE/rater_a.json --rater-b PRIVATE/rater_b.json [--velocity-cert PRIVATE/velocity.json]`. A minimal schema follows. Replace the example hashes with actual SHA-256 digests of independently retained evidence, not fabricated strings. Two participants and two disjoint splits are shown solely to illustrate shape.

```json
{
  "protocol_id": "E002-585",
  "tau": 0.2,
  "clips": [
    {
      "clip_id": "opaque-clip-A",
      "participant_id": "opaque-participant-A",
      "split": "calibration",
      "frames": 2,
      "frame_time_bounds_ms": [[0, 0.2], [9.8, 10.2]],
      "clock_sha256": "ACTUAL_64_HEX_SHA256",
      "shutter_sha256": "ACTUAL_64_HEX_SHA256",
      "geometry_sha256": "ACTUAL_64_HEX_SHA256",
      "nuisance_flags": []
    },
    {
      "clip_id": "opaque-clip-B",
      "participant_id": "opaque-participant-B",
      "split": "holdout",
      "frames": 2,
      "frame_time_bounds_ms": [[0, 0.2], [9.8, 10.2]],
      "clock_sha256": "ACTUAL_64_HEX_SHA256",
      "shutter_sha256": "ACTUAL_64_HEX_SHA256",
      "geometry_sha256": "ACTUAL_64_HEX_SHA256",
      "nuisance_flags": ["glasses_reflection"]
    }
  ]
}
```

Each separate rater file has `{"rater_id":"R1","ratings":{"opaque-clip-A":[[0.08,0.12],null],"opaque-clip-B":[[0.3,0.4],[0.7,0.8]]}}` (with different `rater_id` and independently recorded intervals for the second rater). `null` means anatomically unobservable, **not open**. The optional velocity metadata must have `independently_justified:true`, `hard_upper_bound_per_s` positive, and `evidence_sha256` with a real digest; the program never authenticates this claim and never upgrades it into a physical certificate.

## Capture and blinded adjudication

1. Obtain consent, ethics/privacy review and approved storage before recording. No raw faces, IDs, landmarks, timestamps tied to identities or rater records go into public GitHub.
2. Collect simultaneously recorded high-speed anatomical reference (target >=240 fps, preferably >=400 fps) and ordinary-rate camera, viewing the same eyelids. Measure **imaging-path** exposure support, rolling-row readout and clock uncertainty using independently validated optical phase scans or equivalent; a shared LED trigger alone is insufficient. Retain independent eye-plane scale, photometric calibration and provenance.
3. Freeze participant-disjoint calibration/holdout allocation, nuisance strata and threshold before revealing high-speed held-out labels. Present clips to two blinded anatomical raters, preserving within-clip temporal order but concealing ordinary-camera predictions and the other rater's marks. Record upper and lower lid margins and visibility, not pupil-center movement or pixel brightness as anatomical substitutes.
4. Run the local gate. Any rater disagreement >0.15 normalized aperture, threshold-straddling interval, missing frame or disqualifying nuisance is `UNCERTAIN`. This is a **conservative one-sided witness** of a high-rate closure, not proof of continuous-time openness. Review the independent disagreement rate and adjudicate without leaking model predictions.
5. On the sealed holdout, freeze the E002-371 gap decisions **before** revealing reference closure witnesses. One adjudicated closure inside a gap classified `CERTIFIED_NO_HIDDEN_CLOSURE` falsifies that certificate or a premise. If velocity, shutter, clock, geometry or sensor-transfer assumptions are unauthenticated, emit `ABSTAIN_UNCALIBRATED`.
6. Report false exclusions, certified coverage, all abstentions, participant/session-cluster intervals, nuisance strata, calibration uncertainty, full negative results and preregistration timestamps. Seek independent physical metrology and external review before release.

## Quantitative study-size warning

Even with **zero** false certifications among `n` *independent* held-out units, a one-sided exact 95% upper confidence bound on the failure probability is `1 - 0.05**(1/n)` under an iid Bernoulli model. Thus `n=20` permits about **13.9%**, `n=59` about **4.95%**, and `n=299` about **1.00%**. Repeated frames, phases and windows from the same participant do not supply 299 independent units. These calculations are statistical planning bounds, **not** evidence of physical correctness, and a finite statistical guarantee is not a deterministic velocity ceiling.

## Current release decision

The script validates the internal structure of two rater records and reports only aggregate reference counts and provenance hashes. It **cannot** authenticate real camera shutter measurements, human anatomical raters or physiological speed bounds. Its output is always `ABSTAIN_UNCALIBRATED` for physical no-hidden-closure claims and `BLOCKED` for release. This is intentional fail-closed behavior. The next research run should prioritize actual independent rater acquisition and imaging-path shutter metrology, not more investigator-label reanalysis.
