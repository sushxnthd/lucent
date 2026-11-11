# E002-585 | Verified synthetic rater-gate instrument, no human evidence

**Executed:** 2026-11-01 UTC. **Frozen protocol:** [E002_585_FROZEN.md](E002_585_FROZEN.md), committed first at `e23924e`. **Hosted workflow:** [Actions #41296366425](https://github.com/sushxnthd/lucent/actions/runs/41296366425), job `124817949908`, completed **success** on CPython 3.11.17. **Executable:** [e002_585_human_rater_gate.py](e002_585_human_rater_gate.py). **Human handoff:** [E002_585_HUMAN_HANDOFF.md](E002_585_HUMAN_HANDOFF.md).

## Verified output

```json
{"human_data":false,"independent_rater_pairs_obtained":0,"physical_shutter_captures":0,"product":"ABSTAIN_UNCALIBRATED","release":"BLOCKED","synthetic_fixture_groups_passed":10}
```

The hosted job compiled the Python instrument and executed its synthetic fixtures. Tested: participant-disjoint calibration/holdout enforcement, two distinct rater IDs, complete frame counts, valid aperture intervals, strictly ordered non-overlapping timestamp intervals, provenance-digest syntax, conservative threshold ambiguity, missing ratings, nuisance-induced uncertainty, shutter evidence omission and explicit refusal to certify physical exclusion even when all metadata fields claim to be present.

Synthetic rater pairs classified a four-frame calibration fixture as one CLOSED, one OPEN, two UNCERTAIN, and a two-frame held-out fixture as zero CLOSED, one OPEN, one UNCERTAIN. These are **synthetic fixtures**, not actual human judgments. No faces, source annotations or private ratings were uploaded.

## Scientific contribution and limits

The result is a reproducible **measurement-instrument validation** and a fail-closed adjudication gate for the first independently rated anatomical study. It is **not** a new physiological result, empirical verification of the E002-371 velocity inequality, or authentication of real camera shutter evidence. Merely supplying a hash or a JSON claim of independent velocity certification does not establish its validity. The program deliberately never emits `CERTIFIED_NO_HIDDEN_CLOSURE`.

The gate is deliberately strict: rater intervals are combined by union hull, not averaging; threshold straddles and disagreement become UNCERTAIN; participant-disjoint splits are enforced. No absence-of-closure inference is made from a missing or uncertain high-rate frame.

## Next decisive experiment

Obtain consenting human reference footage with imaging-path shutter/clock calibration and eye-plane geometry; collect two independently blinded anatomical aperture interval ratings on participant-disjoint calibration/holdout sessions; prospectively test the E002-371 gap decisions against adjudicated high-rate closure witnesses. A single confirmed held-out closure in a physically certified no-closure gap falsifies that claim or its premises. Until real evidence exists, **zero** human rater pairs, **zero** calibrated physical captures, **zero** certified continuous-time eyelid-velocity ceilings and **zero** held-out physical predictions. Product `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. No Hush changes.
