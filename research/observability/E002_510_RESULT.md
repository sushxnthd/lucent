# E002-510 | Authentic S01 source-timebase experiment

Date: 2026-10-28. E002-371 human-validation kernel, existing branch and draft PR #26.

## What was actually done

Frozen [E002_510_FROZEN.md](E002_510_FROZEN.md) at commit `c9f6542` **before** reading the Phantom XML or sync CSV. Implemented [e002_510_source_timebase.py](e002_510_source_timebase.py) and [12 adversarial synthetic controls](test_e002_510_source_timebase.py). Launched [hosted S01 acquisition and metadata-only verification](../../.github/workflows/e002_510_source_timebase.yml) at commit `4ed0881`, using the previously checksum-pinned authentic S01 archive. The script reads only source metadata, never exports frames, event timestamps, private source indices, raw CSV or XML.

This is a bounded attempt to determine whether the 150-fps acquisition period reported in the primary paper has **source-level timing support** independent of the unreliable AVI nominal header and the rehost's contradictory ~500-fps description. It does **not** authenticate an external clock. The preregistered mapping parser deliberately requires explicit Phantom frame indices and timestamps with units. If the sync CSV lacks these, the experiment must abstain, rather than reinterpret other device clocks.

## Evidence at commit time

- Protocol and code persisted on the established branch.
- Hosted authentic S01 outcome: **pending**, not yet a measured cadence or scientific confirmation.
- Synthetic test outcome: **pending hosted execution**. No test pass is asserted here.
- Existing E002-509 participant-level power [hosted CI 40722329284](https://github.com/sushxnthd/lucent/actions/runs/40722329284): **completed successfully**. This verifies its arithmetic/software only, not population risk.
- No human anatomical ratings, independent physical optical clock measurement, exposure calibration, certified continuous-time eyelid-speed upper bound or held-out physical prediction was acquired.

## Hard scientific stop

This is the **final S01 metadata-only experiment**. Even a perfect source timestamp consistency result cannot establish the physical shutter gap or hard human eyelid-speed bound required by E002-371. A failed or ambiguous source mapping is a legitimate negative result; do not tune a parser to make it pass. Subsequent substantive Lucent work must prioritize two real independent blinded S01 reviewers, calibrated optical clock/shutter measurement and participant-disjoint physical predictions. No more nominal-FPS inference or optical image-motion proxy development.

Product: `ABSTAIN_UNCALIBRATED`. Release: `BLOCKED`. Hush PR #45 unchanged; no merge or deployment.
